import logging

from app.config import settings
from app.exception import exceptions
from app.interfaces.dataset_deletion_repository_interface import DatasetDeletionRepositoryInterface
from app.interfaces.dataset_storage_repository_interface import DatasetStorageRepositoryInterface
from app.models.collection_exericise_end_data import CollectionExerciseEndData
from app.models.dataset_models import DatasetMetadata, UnitDataset
from app.models.deletion_models import DeleteMetadata
from app.services.shared.datetime_service import DatetimeService

logger = logging.getLogger(__name__)


class DatasetService:

    def __init__(
            self,
            dataset_deletion_repository: DatasetDeletionRepositoryInterface,
            dataset_storage_repository: DatasetStorageRepositoryInterface
    ):
        self.dataset_storage_repository = dataset_storage_repository
        self.dataset_deletion_repository = dataset_deletion_repository

    def get_dataset_metadata_collection(
            self,
            survey_id: str,
            period_id: str
    ) -> list[DatasetMetadata]:
        """
        Gets the collection of dataset metadata associated for
        a specific survey and period id.

        :param survey_id: survey id of the collection.
        :param period_id: period id of the collection.
        """
        return self.dataset_storage_repository.get_metadata(
            survey_id, period_id
        )

    def get_all_dataset_metadata_collection(
            self
    ) -> list[DatasetMetadata]:
        """
        Gets the collection of dataset metadata
        for ALL surveys held in SDS.
        """
        return self.dataset_storage_repository.get_all_metadata()

    def get_unit_supplementary_data(
            self,
            dataset_id: str,
            identifier: str
    ) -> UnitDataset | None:
        """
        Retrieve supplementary data for a particular unit given the dataset id and identifier.

        :param dataset_id: The dataset id.
        :param identifier: The unit identifier.
        """
        return self.dataset_storage_repository.get_unit_supplementary_data(
            dataset_id, identifier
        )

    # ------------------------
    # END COLLECTION
    # ------------------------

    def end_collection_exercise(
            self,
            collection_exercise_end_data: CollectionExerciseEndData
    ):
        """
        When a collection exercise ends, the message is received
        and the dataset is marked for deletion

        :param collection_exercise_end_data: The collection exercise end data.

        returns: list of dataset ids marked for deletion or None if no dataset_guid is present in the message.
        """

        collection_has_dataset_guid = (
            self._check_if_collection_has_dataset_guid(
                collection_exercise_end_data
            )
        )

        # Ignore message if there is no dataset guid
        if not collection_has_dataset_guid:
            logger.info("No Dataset GUID found in collection exercise end message")
            return None


        logger.info("Collecting all dataset versions for period and survey")
        logger.debug(
            f"Collecting all dataset versions for survey_id: {collection_exercise_end_data.survey_id} and period_id: {collection_exercise_end_data.period_id}"
        )

        list_dataset_metadata: list[DatasetMetadata] = self.get_dataset_metadata_collection(
            collection_exercise_end_data.survey_id,
            collection_exercise_end_data.period_id
        )

        # Ignore message if no metadata is found using the survey_id and period_id
        if not list_dataset_metadata:
            logger.info("No supplementary data found")
            return None

        # Ignore message if the supplied dataset guid is not found in the metadata collection
        if collection_exercise_end_data.dataset_guid not in [metadata.dataset_id for metadata in list_dataset_metadata]:
            logger.info("Dataset GUID not found in dataset metadata collection")
            return None

        # Mark all dataset versions for deletion
        self._mark_collections_for_deletion(
            list_dataset_metadata, collection_exercise_end_data.end_date
        )

        return None


    def _check_if_collection_has_dataset_guid(
            self, collection_exercise_end_data: CollectionExerciseEndData
    ) -> bool:
        if (
                collection_exercise_end_data.dataset_guid is None
                or collection_exercise_end_data.dataset_guid == ""
        ):
            supplementary_data_available = False
        else:
            supplementary_data_available = True
        return supplementary_data_available

    def _mark_collections_for_deletion(
            self, list_dataset_metadata: list[DatasetMetadata], end_date: str
    ) -> list[str] | None:
        time_now = DatetimeService.get_current_date_and_time().strftime(settings.TIME_FORMAT)

        try:
            for dataset_metadata in list_dataset_metadata:
                logger.debug(f"Dataset_metadata {dataset_metadata}")
                delete_metadata: DeleteMetadata = DeleteMetadata(
                    **{
                        "dataset_guid": dataset_metadata.dataset_id,
                        "period_id": dataset_metadata.period_id,
                        "survey_id": dataset_metadata.survey_id,
                        "end_date": end_date,
                        "sds_dataset_version": dataset_metadata.sds_dataset_version,
                        "status": "pending",
                        "mark_deleted_at": time_now,
                        "deleted_at": "n/a",
                    }
                )

                logger.debug(f"Marking dataset for deletion {delete_metadata}")
                self.dataset_deletion_repository.mark_dataset_for_deletion(delete_metadata)
        except Exception as exc:
            logger.exception(f"Error occurred marking dataset for deletion : exception raised: {exc}")
            raise exceptions.GlobalException from exc
        else:
            logger.info("Dataset marked for deletion successfully")

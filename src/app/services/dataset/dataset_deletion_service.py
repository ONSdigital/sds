from config.config_factory import config
from logging_config import logging
from models.collection_exericise_end_data import CollectionExerciseEndData
from models.dataset_models import DatasetMetadata
from models.deletion_models import DeleteMetadata
from repositories.firebase.deletion_firebase_repository import (
    DeletionMetadataFirebaseRepository,
)
from services.dataset.dataset_processor_service import DatasetProcessorService
from services.shared.datetime_service import DatetimeService

logger = logging.getLogger(__name__)


class DatasetDeletionService:

    def __init__(self) -> None:
        self.delete_repository = DeletionMetadataFirebaseRepository()
        self.dataset_processor_service = DatasetProcessorService()

    def process_collection_exercise_end_message(
        self, collection_exercise_end_data: CollectionExerciseEndData
    ):
        # todo: validation on period_id and survey_id once we have go the 'real' message
        collection_has_dataset_guid = (
            self._check_if_collection_has_dataset_guid(
                collection_exercise_end_data
            )
        )

        if collection_has_dataset_guid:
            list_dataset_metadata = self._collect_metadata_for_period_and_survey(
                collection_exercise_end_data
            )
            self._mark_collections_for_deletion(list_dataset_metadata)
        else:
            logger.debug("Supplementary data not data found")

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


    def _collect_metadata_for_period_and_survey(
        self, collection_exercise_end_data: CollectionExerciseEndData
    ) -> list[DatasetMetadata]:
        logger.info("Collecting all dataset versions for period and survey")
        logger.info(f"Collecting all dataset versions for survey_id: {collection_exercise_end_data.survey_id} and period_id: {collection_exercise_end_data.period_id}")
        return self.dataset_processor_service.get_dataset_metadata_collection(
            collection_exercise_end_data.survey_id, collection_exercise_end_data.period_id
        )


    def _mark_collections_for_deletion(
        self, list_dataset_metadata: list[DatasetMetadata]
    ):
        time_now = DatetimeService.get_current_date_and_time().strftime(config.TIME_FORMAT)
        for dataset_metadata in list_dataset_metadata:
            logger.debug(f"Dataset_metadata {dataset_metadata}")
            delete_metadata: DeleteMetadata = DeleteMetadata(
                **{
                    "dataset_guid": dataset_metadata["dataset_id"],
                    "period_id": dataset_metadata["period_id"],
                    "survey_id": dataset_metadata["survey_id"],
                    "sds_dataset_version": dataset_metadata["sds_dataset_version"],
                    "status": "Pending",
                    "mark_deleted_at": time_now,
                    "deleted_at": "n/a",
                }
            )
            logger.debug(f"Marking dataset for deletion {delete_metadata}")
            self.delete_repository.mark_dataset_for_deletion(delete_metadata)

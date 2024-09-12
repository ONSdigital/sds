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
        collection_has_supplementary_data = (
            self._check_if_collection_has_supplementary_data(
                collection_exercise_end_data
            )
        )

        if collection_has_supplementary_data:
            list_supplementary_metadata = self._collect_metadata_for_period_and_survey(
                collection_exercise_end_data
            )
            self._mark_collections_for_deletion(list_supplementary_metadata)
        else:
            logger.info("Supplementary not data found")

    def _check_if_collection_has_supplementary_data(
        self, collection_exercise_end_data: CollectionExerciseEndData
    ) -> bool:
        if (
            collection_exercise_end_data.dataset_guid is None
            or collection_exercise_end_data.dataset_guid == ""
        ):
            return False
        return True

    def _collect_metadata_for_period_and_survey(
        self, collection_exercise_end_data: CollectionExerciseEndData
    ) -> list[DatasetMetadata]:
        logger.debug("Collecting all datasets for period and survey")
        return self.dataset_processor_service.get_dataset_metadata_collection(
            collection_exercise_end_data.survey_id, collection_exercise_end_data.period
        )

    def _mark_collections_for_deletion(
        self, list_dataset_metadata: list[DatasetMetadata]
    ):
        time_now = DatetimeService.get_current_date_and_time()
        for dataset_metadata in list_dataset_metadata:
            logger.debug("dataset_metadata {}", dataset_metadata)
            delete_metadata: DeleteMetadata = DeleteMetadata(
                **{
                    "dataset_guid": dataset_metadata["dataset_id"],
                    "period_id": dataset_metadata["period_id"],
                    "survey_id": dataset_metadata["survey_id"],
                    "sds_dataset_version": dataset_metadata["sds_dataset_version"],
                    "status": "pending",
                    "mark_deleted_at": time_now,
                    "deleted_at": "n/a",
                }
            )
            logger.debug("marking dataset for deletion {}", delete_metadata)
            self.delete_repository.mark_dataset_for_deletion(delete_metadata)

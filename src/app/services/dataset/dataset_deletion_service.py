import json

from models.collection_exericise_end_data import CollectionExerciseEndData
from models.dataset_models import DatasetMetadata
from models.deletion_models import DeleteMetadata
from repositories.firebase.deletion_firebase_repository import (
    DeletionMetadataFirebaseRepository,
)
from services.dataset.dataset_processor_service import DatasetProcessorService
from services.shared.datetime_service import DatetimeService


class DatasetDeletionService:
    def process_collection_exercise_end_message(self, json_string: str):
        collection_exercise_end = self._json_to_object(json_string)
        supplementary_data = self._check_if_supplementary_data(collection_exercise_end)

        if supplementary_data:
            list_supplementary_metadata = self._collect_metadata_for_period_and_survey(
                collection_exercise_end
            )
            self._mark_collections_for_deletion(list_supplementary_metadata)

    def _json_to_object(self, json_string: str) -> DeleteMetadata:
        collection_exercise_end_dict = json.loads(json_string)
        collection_exercise_end_obj = CollectionExerciseEndData(
            **collection_exercise_end_dict
        )
        return collection_exercise_end_obj

    def _check_if_supplementary_data(
        self, collection_exercise_end_data: CollectionExerciseEndData
    ) -> bool:
        if collection_exercise_end_data.dataset_guid == "":
            return False
        return True

    def _collect_metadata_for_period_and_survey(
        self, collection_exercise_end_data: CollectionExerciseEndData
    ) -> list[DatasetMetadata]:
        return DatasetProcessorService.dataset_processor_service.get_dataset_metadata_collection(
            collection_exercise_end_data.survey_id, collection_exercise_end_data.period
        )

    def _mark_collections_for_deletion(
        self, list_dataset_metadata: list[DatasetMetadata]
    ):
        time_now = DatetimeService.get_current_date_and_time()
        for dataset_meta in list_dataset_metadata:
            delete_metadata: DeleteMetadata = {
                "dataset_guid": dataset_meta.dataset_guid,
                "period_id": dataset_meta.period_id,
                "survey_id": dataset_meta.survey_id,
                "sds_dataset_version": dataset_meta.sds_dataset_version,
                "status": "status",
                "mark_deleted_at": time_now,
                "deleted_at": "n/a",
            }
            DeletionMetadataFirebaseRepository.create_delete_in_transaction(
                delete_metadata
            )

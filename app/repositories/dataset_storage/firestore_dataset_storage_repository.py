from dataclasses import fields
from typing import Any

from firebase_admin import firestore

from app.interfaces.dataset_storage_repository_interface import DatasetStorageRepositoryInterface
from app.logging_config import logging
from app.models.dataset_models import DatasetMetadata, UnitDataset
from app.util.firebase_loader import FirebaseLoader

logger = logging.getLogger(__name__)


def _dataclass_fields(dataclass_type: type[Any]) -> set[str]:
    return {field.name for field in fields(dataclass_type)}


class FirestoreDatasetStorageRepository(DatasetStorageRepositoryInterface):

    def __init__(self, firebase_loader: FirebaseLoader) -> None:
        self.client = firebase_loader.get_client()
        self.datasets_collection = firebase_loader.get_datasets_collection()

    @staticmethod
    def _create_dataclass(
            dataclass_type: type[Any], model_data: dict[str, Any], **extra_fields: Any
    ) -> Any:
        """
        Helper method to create dataclass instance, will add
        fields specified in extra_fields and then remove all fields not in the dataclass
        :param dataclass_type: data class type
        :param model_data: model data
        :param extra_fields: extra fields
        """
        data_with_extras = {**model_data, **extra_fields}
        allowed_fields = _dataclass_fields(dataclass_type)
        filtered_model_data = {
            key: value for key, value in data_with_extras.items() if key in allowed_fields
        }

        return dataclass_type(**filtered_model_data)

    def get_unit_supplementary_data(
            self, dataset_id: str, identifier: str
    ) -> UnitDataset | None:
        returned_unit_data = self.datasets_collection.document(dataset_id).collection("units").document(
            identifier).get()

        if not returned_unit_data.exists:
            return None

        return self._create_dataclass(UnitDataset, returned_unit_data.to_dict())

    def get_metadata(
            self, survey_id: str, period_id: str
    ) -> list[DatasetMetadata]:
        returned_dataset_metadata = (
            self.datasets_collection.where("survey_id", "==", survey_id)
            .where("period_id", "==", period_id)
            .order_by("sds_dataset_version", direction=firestore.Query.DESCENDING)
            .stream()
        )

        dataset_metadata_list: list[DatasetMetadata] = []
        for dataset_metadata in returned_dataset_metadata:
            metadata_dict = dataset_metadata.to_dict()
            metadata = self._create_dataclass(
                DatasetMetadata,
                metadata_dict,
                dataset_id=dataset_metadata.id,
            )
            dataset_metadata_list.append(metadata)

        return dataset_metadata_list

    def get_all_metadata(self) -> list[DatasetMetadata]:
        returned_dataset_metadata = (
            self.datasets_collection
            .order_by("survey_id")
            .order_by("sds_dataset_version", direction=firestore.Query.DESCENDING)
            .stream()
        )
        dataset_metadata_list: list[DatasetMetadata] = []
        for dataset_metadata in returned_dataset_metadata:
            metadata_dict = dataset_metadata.to_dict()
            metadata = self._create_dataclass(
                DatasetMetadata,
                metadata_dict,
                dataset_id=dataset_metadata.id,
            )
            dataset_metadata_list.append(metadata)

        return dataset_metadata_list

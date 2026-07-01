from abc import ABC, abstractmethod

from app.models.dataset_models import UnitDataset, DatasetMetadata


class DatasetStorageRepositoryInterface(ABC):
    """
    This interface defines where datasets are
    stored

    """

    @abstractmethod
    def get_unit_supplementary_data(
            self,
            dataset_id: str,
            identifier: str
    ) -> UnitDataset | None:
        """
        Get the unit supplementary data of a specified
        unit from a dataset collection

        :param dataset_id: The id of the dataset
        :param identifier: The identifier of the dataset
        """
        raise NotImplementedError

    @abstractmethod
    def get_metadata(
            self,
            survey_id: str,
            period_id: str
    ) -> list[DatasetMetadata]:
        """
        Get a collection of dataset metadata for a specific
        survey and period

        :param survey_id: The id of the dataset survey
        :param period_id: The period id of the unit of the dataset
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_metadata(self) -> list[DatasetMetadata]:
        """
        Get all the metadata of all datasets
        """
        raise NotImplementedError
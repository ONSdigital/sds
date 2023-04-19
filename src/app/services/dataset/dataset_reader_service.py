import database
from models import DatasetMetadataDto
from repositories.dataset_repository import DatasetRepository


class DatasetReaderService:
    def __init__(self, dataset_repository: DatasetRepository) -> None:
        self.dataset_repository = dataset_repository
        pass

    def get_dataset_with_survey_id(self, survey_id: str) -> list[DatasetMetadataDto]:
        """
        Returns a dataset associated with a specific survey id.

        Parameters:
        survey_id (str): survey_id used for query match
        """
        return self.dataset_repository.get_dataset_with_survey_id(survey_id)

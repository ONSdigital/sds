from app.models.collection_exericise_end_data import CollectionExerciseEndData
from app.models.dataset_models import DatasetMetadata, UnitDataset


class DatasetService:

    def __init__(self):
        pass

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
        pass

    def get_all_dataset_metadata_collection(
            self
    ) -> list[DatasetMetadata]:
        """
        Gets the collection of dataset metadata
        for ALL surveys held in SDS.
        """
        pass

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
        pass

    def end_collection_exercise(
            self,
            collection_exercise_end_data: CollectionExerciseEndData
    ):
        """
        When a collection exercise ends, the message is received
        and the dataset is marked for deletion

        :param collection_exercise_end_data: The collection exercise end data.
        """
        pass

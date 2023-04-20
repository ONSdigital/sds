import firebase_admin
from firebase_admin import firestore
from models import DatasetMetadataDto, DatasetMetadataWithoutIdDto, NewDatasetWithMetadata


class DatasetRepository:
    def __init__(self):
        firebase_admin.initialize_app()
        self.db = firestore.client()
        self.datasets_collection = self.db.collection("datasets")

    def get_dataset_with_survey_id(self, survey_id: str) -> list[DatasetMetadataDto]:
        """
        Gets a single dataset from firestore with a specific survey_id.

        Parameters:
        survey_id (str): survey_id of the specified dataset.
        """
        return (
            self.datasets_collection.where("survey_id", "==", survey_id)
            .order_by("sds_dataset_version", direction=firestore.Query.DESCENDING)
            .limit(1)
            .stream()
        )

    def create_new_dataset(
        self, dataset_id: str, dataset: DatasetMetadataWithoutIdDto
    ) -> None:
        """
        Creates a new dataset in firestore with a specified ID and data.

        Parameters:
        dataset_id (str): uniquely generated GUID id of the dataset.
        dataset (UnitData): unit dataset being created in firestore.
        """
        self.datasets_collection.document(dataset_id).set(dataset)

    def get_dataset_unit_collection(self, dataset_id: str) -> list[object]:
        """
        Gets the collection of units associated with a particular dataset.

        Parameters:
        dataset_id (str): uniquely generated GUID id of the dataset.
        """
        return self.datasets_collection.document(dataset_id).collection("units")

    def append_unit_to_dataset_units_collection(
        self, units_collection, unit_data
    ) -> None:
        """
        Appends a new unit to the collection of units associated with a particular dataset.

        Parameters:
        units_collection (any): The collection of units that data is being appended to.
        unit_data (any): The unit being appended
        """
        units_collection.document(unit_data["ruref"]).set(unit_data)

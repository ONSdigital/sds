import firebase_admin
from firebase_admin import firestore
from models.schema_models import SchemaMetadataWithGuid

firebase_admin.initialize_app()
db = firestore.client()
datasets_collection = db.collection("datasets")
schemas_collection = db.collection("schemas")


def get_schemas_metadata(survey_id) -> list[SchemaMetadataWithGuid]:
    """
    Return all the schema meta-data that corresponds to a particular survey_id.

    Parameters:
        survey_id (str): the corresponding ID of the survey for the desired schema

    Returns:
        list[SchemaMetadata]: a list of all the metadata corresponding to the given ID
    """

    dataset_schemas = list()
    schemas_result = schemas_collection.where("survey_id", "==", survey_id).stream()

    for schema in schemas_result:
        return_schema = schema.to_dict()
        return_schema["guid"] = schema.id
        dataset_schemas.append(return_schema)

    return dataset_schemas

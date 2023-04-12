import uuid

import database
import storage


def process_schema_metadata(schema):
    schema_id = str(uuid.uuid4())
    schema_location = storage.store_schema(schema=schema, schema_id=schema_id)

    posted_schema_metadata = database.set_schema_metadata(
        survey_id=schema.survey_id, schema_location=schema_location, schema_id=schema_id
    )
    posted_schema_metadata.guid = schema_id

    return posted_schema_metadata

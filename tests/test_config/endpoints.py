from typing import TypedDict

POST_SCHEMA: str = "post_schema"
GET_SCHEMA: str = "get_schema"
GET_SCHEMA_WITH_GUID: str = "get_schema_with_guid"
GET_SCHEMA_METADATA: str = "get_schema_metadata"
GET_DATASET_METADATA: str = "get_dataset_metadata"
GET_UNIT_DATA: str = "get_unit_data"
GET_ALL_DATASET_METADATA: str = "get_all_dataset_metadata"
GET_ALL_SCHEMA_METADATA: str = "get_all_schema_metadata"
GET_STATUS: str = "get_status"
COLLECTION_END: str = "collection_end"
GET_SURVEYS_MAPPING: str = "get_surveys_mapping"

PLACEHOLDERS: dict[str, str] = {
    "guid": "{guid}",
    "dataset_id": "{dataset_id}",
    "identifier": "{identifier}",
}

class EndpointConfig(TypedDict):
    url: str
    method: str
    query_parameters: bool


ENDPOINTS: dict[str, EndpointConfig] = {
    POST_SCHEMA: {
        "url": "/schemas",
        "method": "POST",
        "query_parameters": True,
    },
    GET_SCHEMA: {
        "url": "/schemas",
        "method": "GET",
        "query_parameters": True,
    },
    GET_SCHEMA_WITH_GUID: {
        "url": f"/schemas/{PLACEHOLDERS['guid']}",
        "method": "GET",
        "query_parameters": False,
    },
    GET_SCHEMA_METADATA: {
        "url": "/schemas/metadata",
        "method": "GET",
        "query_parameters": True,
    },
    GET_DATASET_METADATA: {
        "url": "/datasets/metadata",
        "method": "GET",
        "query_parameters": True,
    },
    GET_UNIT_DATA: {
        "url": f"/datasets/{PLACEHOLDERS['dataset_id']}/unit-data/{PLACEHOLDERS['identifier']}",
        "method": "GET",
        "query_parameters": False,
    },
    GET_ALL_DATASET_METADATA: {
        "url": "/datasets/all-metadata",
        "method": "GET",
        "query_parameters": False,
    },
    GET_ALL_SCHEMA_METADATA: {
        "url": "/schemas/all-metadata",
        "method": "GET",
        "query_parameters": False,
    },
    COLLECTION_END: {
        "url": "/collection-exercises-end",
        "method": "POST",
        "query_parameters": False,
    },
    GET_SURVEYS_MAPPING: {
        "url": "/surveys",
        "method": "GET",
        "query_parameters": False,
    },
    GET_STATUS: {
        "url": "/status",
        "method": "GET",
        "query_parameters": False,
    }
}

ENDPOINTS_DEPRECATED: dict[str, EndpointConfig] = {
    POST_SCHEMA: {
        "url": "/v1/schema",
        "method": "POST",
        "query_parameters": True,
    },
    GET_SCHEMA: {
        "url": "/v1/schema",
        "method": "GET",
        "query_parameters": True,
    },
    GET_SCHEMA_WITH_GUID: {
        "url": f"/v2/schema",
        "method": "GET",
        "query_parameters": True,
    },
    GET_SCHEMA_METADATA: {
        "url": "/v1/schema_metadata",
        "method": "GET",
        "query_parameters": True,
    },
    GET_DATASET_METADATA: {
        "url": "/v1/dataset_metadata",
        "method": "GET",
        "query_parameters": True,
    },
    GET_UNIT_DATA: {
        "url": "v1/unit_data",
        "method": "GET",
        "query_parameters": True,
    },
    GET_ALL_DATASET_METADATA: {
        "url": "/v1/all_dataset_metadata",
        "method": "GET",
        "query_parameters": False,
    },
    GET_ALL_SCHEMA_METADATA: {
        "url": "/v1/all_schema_metadata",
        "method": "GET",
        "query_parameters": False,
    },
    COLLECTION_END: {
        "url": "/collection-exercise-end",
        "method": "POST",
        "query_parameters": False,
    },
    GET_SURVEYS_MAPPING: {
        "url": "/v1/survey_list",
        "method": "GET",
        "query_parameters": False,
    },
    GET_STATUS: {
        "url": "/status",
        "method": "GET",
        "query_parameters": False,
    },
}

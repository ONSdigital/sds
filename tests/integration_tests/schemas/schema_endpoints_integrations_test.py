import os

import pytest

from app.config import settings
from tests.integration_tests.helpers.integration_helpers import is_json_response
from tests.integration_tests.helpers.utils import make_iap_request
from tests.test_config.endpoints import ENDPOINTS, GET_SCHEMA_METADATA, GET_ALL_SCHEMA_METADATA, GET_SCHEMA, \
    GET_SCHEMA_WITH_GUID, GET_SURVEYS_MAPPING, POST_SCHEMA
from tests.test_config.endpoints_loader import EndpointsLoader
from tests.test_data.schema_test_data import test_survey_id_map
from tests.test_data.shared_test_data import test_survey_id_list
from tests.test_data.schema_test_data import invalid_survey_id, invalid_data, test_survey_id

endpoints_loader = EndpointsLoader(ENDPOINTS)


class TestSchemaEndpoints:

    def test_get_schema_metadata_v1(self, setup_schema, test_schema_list):
        """
        Test the GET /v1/schema_metadata endpoint by retrieving the schema metadata for each test_survey_id
        and checking the response.

        * We retrieve and verify schema metadata
        """
        for survey_id in test_survey_id_list:

            url, method = endpoints_loader.formulate_url_and_method(
                key=GET_SCHEMA_METADATA,
                params={
                    "survey_id": survey_id,
                }
            )

            schema_metadata_response = make_iap_request(method, url)


            assert schema_metadata_response.status_code == 200
            schema_metadata_list = schema_metadata_response.json()
            # Verify there are 2 metadata entries for each survey_id
            total_versions = len(schema_metadata_list)
            assert total_versions == 2
        
            # Verify schema metadata - ensure that the sds_schema_version is incremented by 1 for each schema
            # and the title and schema_version is as expected.
            for index, schema_metadata in enumerate(schema_metadata_list):
                expected_schema = test_schema_list[index]
                assert schema_metadata == {
                    "guid": schema_metadata["guid"],
                    "survey_id": survey_id,
                    "schema_location": f"{survey_id}/{schema_metadata['guid']}.json",
                    "sds_schema_version": total_versions - index,
                    "sds_published_at": schema_metadata["sds_published_at"],
                    "schema_version": expected_schema["properties"]["schema_version"]["const"],
                    "title": expected_schema["title"],
                }


    def test_get_all_schema_metadata_v1(self, setup_schema, test_schema_list):
        """
        Test the GET /v1/schema_metadata endpoint by retrieving all schema metadata and checking the response.

        * We retrieve and verify all schema metadata
        """
        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_ALL_SCHEMA_METADATA,
        )

        all_schema_metadata_response = make_iap_request(method, url)

        expected_schema_count = len(test_schema_list) * len(test_survey_id_list)
        assert all_schema_metadata_response.status_code == 200

        all_schema_metadata_response = all_schema_metadata_response.json()
        schemas = []
        for schema in all_schema_metadata_response:
            if schema["survey_id"] in test_survey_id_list:
                schemas.append(schema)
        assert len(schemas) == expected_schema_count


    def test_get_schema_v1(self, setup_schema, test_schema_list):
        """
        Test the GET /v1/schema endpoint by retrieving the schema both by version and latest version and
        checking the response.

        * We retrieve the first version of the schema and check the response
        * We retrieve the latest version of the schema and check the response
        """
        for survey_id in test_survey_id_list:
            url, method = endpoints_loader.formulate_url_and_method(
                key=GET_SCHEMA,
                params={
                    "survey_id": survey_id,
                    "version": "1",
                }
            )

            set_version_schema_response = make_iap_request(method, url)

            assert set_version_schema_response.status_code == 200
            assert set_version_schema_response.json() == test_schema_list[1]

            # verify schema retrieval by latest version
            url, method = endpoints_loader.formulate_url_and_method(
                key=GET_SCHEMA,
                params={
                    "survey_id": survey_id,
                }
            )

            latest_version_schema_response = make_iap_request(method, url)

            assert latest_version_schema_response.status_code == 200
            assert latest_version_schema_response.json() == test_schema_list[0]
        

    def test_get_schema_v2(self, setup_schema, test_schema_list):
        """
        Test the GET /v2/schema endpoint by retrieving the schema by GUID and checking the response.

        * We retrieve the schema by GUID and check the response compared to the expected schema
        """
        for survey_id in test_survey_id_list:
            url, method = endpoints_loader.formulate_url_and_method(
                key=GET_SCHEMA_METADATA,
                params={
                    "survey_id": survey_id,
                }
            )

            schema_metadata_response = make_iap_request(method, url)

            schema_metadata_list = schema_metadata_response.json()

            for index, schema_metadata in enumerate(schema_metadata_list):
                # Verify schema retrieval by GUID
                url, method = endpoints_loader.formulate_url_and_method(
                    key=GET_SCHEMA_WITH_GUID,
                    params={
                        "guid": schema_metadata['guid'],
                    }
                )

                set_guid_schema_response = make_iap_request(method, url)

                assert set_guid_schema_response.status_code == 200
                assert set_guid_schema_response.json() == test_schema_list[index]


    def test_survey_id_map(self):
        """
        Retrieve survey mapping data using the /survey_list endpoint.
        Verify that the retrieved data matches the expected survey mapping data.

        * We retrieve the survey mapping data and check the response
        """
        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_SURVEYS_MAPPING,
        )

        set_survey_id_map_response = make_iap_request(method, url)

        assert set_survey_id_map_response.status_code == 200
        assert set_survey_id_map_response.json() == test_survey_id_map


    def test_post_schema_unauthorized(self, test_schema_list):
        """
        Test unauthorized access by providing incorrect authorization token for POST /v1/schema.

        * Send a request to POST /v1/schema with an invalid token.
        * Assert status code: 401 Unauthorized.
        """
        if settings.CONF == "local-int-tests":
            pytest.skip("Skipping test_post_schema_unauthorized on local environment")

        url, method = endpoints_loader.formulate_url_and_method(
            key=POST_SCHEMA,
            params={
                "survey_id": test_survey_id,
            }
        )

        response = make_iap_request(
            method=method,
            path=url,
            json=test_schema_list[0],
            unauthenticated=True
        )

        assert response.status_code == 401


    def test_post_schema_validation_error(self):
        """
        Test validation issue by providing invalid data for POST /v1/schema.

        * We test the POST /v1/schema endpoint by providing invalid data.
        * Assert status code: 400 Bad Request.
        """
        url, method = endpoints_loader.formulate_url_and_method(
            key=POST_SCHEMA,
            params={
                "survey_id": test_survey_id,
            }
        )

        response = make_iap_request(
            method=method,
            path=url,
            json=invalid_data
        )

        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()

        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "Validation has failed", f"Unexpected message: {response_data['message']}"


    def test_get_schema_404_not_found(self):
        """
        Test data not found by requesting nonexistent schema for GET /v1/schema.
        
        * We send a request to the GET /v1/schema endpoint providing an invalid survey_id.
        * Assert status code: 404 Not Found.
        """
        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_SCHEMA,
            params={
                "survey_id": invalid_survey_id,
            }
        )

        response = make_iap_request(method, url)

        assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()
        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "No schema found", f"Unexpected message: {response_data['message']}"


    def test_get_schema_unauthorized(self):
        """
        Test unauthorized access by providing incorrect authorization token for GET /v1/schema.

        * Send a request to GET /v1/schema with an invalid token.
        * Assert status code: 401 Unauthorized.
        """
        if settings.CONF == "local-int-tests":
            pytest.skip("Skipping test_get_schema_unauthorized on local environment")

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_SCHEMA,
            params={
                "survey_id": test_survey_id,
            }
        )

        response = make_iap_request(
            method=method,
            path=url,
            unauthenticated=True
        )

        assert response.status_code == 401
    

    def test_get_schema_validation_error(self):
        """
        Test validation issue by providing an invalid or nonsensical survey_id for GET /v1/schema.

        * We test the GET /v1/schema endpoint by providing invalid data (missing survey_id) 
        * Assert status code: 400 Bad Request.
        * We test the GET /v1/schema endpoint by providing invalid data (nonsensical parameter)
        * Assert status code: 400 Bad Request.
        """
        # Test missing survey_id
        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_SCHEMA,
        )

        response = make_iap_request(method, url)

        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()
        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "Invalid search provided", f"Unexpected message: {response_data['message']}"

        # Test nonsensical parameter
        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_SCHEMA,
            params={
                "randomparam": "nonsense",
            }
        )
        response = make_iap_request(method, url)

        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()
        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "Invalid search provided", f"Unexpected message: {response_data['message']}"


    def test_get_schema_metadata_unauthorized(self):
        """
        Test unauthorized access by providing incorrect authorization token for GET /v1/schema_metadata.

        * Send a request to GET /v1/schema_metadata with an invalid token.
        * Assert status code: 401 Unauthorized.
        """
        if settings.CONF == "local-int-tests":
            pytest.skip("Skipping test_get_schema_metadata_unauthorized on local environment")

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_SCHEMA_METADATA,
            params={
                "survey_id": test_survey_id,
            }
        )

        response = make_iap_request(
            method=method,
            path=url,
            unauthenticated=True
        )

        assert response.status_code == 401


    def test_get_schema_metadata_validation_error(self):
        """
        Test validation issue by providing an invalid data for GET /v1/schema_metadata.
        * Assert status code: 400 Bad Request.
        Test the GET /v1/schema_metadata endpoint by providing nonsensical parameter
        * Assert status code: 400 Bad Request.
        """
        #Missing survey_id
        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_SCHEMA_METADATA,
        )

        response = make_iap_request(method, url)

        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()
        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "Invalid search provided", f"Unexpected message: {response_data['message']}"

        #Nonsensical parameter
        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_SCHEMA_METADATA,
            params={
                "invalidparam": "123",
            }
        )

        response = make_iap_request(method, url)

        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()
        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "Invalid search provided", f"Unexpected message: {response_data['message']}"


    def test_get_schema_metadata_404_not_found(self):
        """
        Test data not found by requesting nonexistent schema metadata for GET /v1/schema_metadata.

        * We send a request to the GET /v1/schema_metadata endpoint providing an invalid survey_id.
        * Assert status code: 404 Not Found.
        """
        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_SCHEMA_METADATA,
            params={
                "survey_id": invalid_survey_id,
            }
        )

        response = make_iap_request(method, url)

        assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()
        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "No results found", f"Unexpected message: {response_data['message']}"


    def test_get_all_schema_metadata_unauthorized(self):
        """
        Test unauthorized access by providing incorrect authorization token for GET /v1/all_schema_metadata.

        * Send a request to GET /v1/all_schema_metadata with an invalid token.
        * Assert status code: 401 Unauthorized.
        """
        if settings.CONF == "local-int-tests":
            pytest.skip("Skipping test_get_all_schema_metadata_unauthorized on local environment")

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_ALL_SCHEMA_METADATA,
        )

        response = make_iap_request(
            method=method,
            path=url,
            unauthenticated=True
        )

        assert response.status_code == 401


    def test_get_schema_v2_unauthorized(self):
        """
        Test unauthorized access by providing incorrect authorization token for GET /v2/schema.

        * Send a request to GET /v2/schema with an invalid token.
        * Assert status code: 401 Unauthorized.
        """
        if settings.CONF == "local-int-tests":
            pytest.skip("Skipping test_get_schema_v2_unauthorized on local environment")

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_SCHEMA_WITH_GUID,
            params={
                "guid": "some_guid",
            }
        )

        response = make_iap_request(
            method=method,
            path=url,
            unauthenticated=True
        )

        assert response.status_code == 401


    def test_get_schema_v2_validation_error(self):
        """
        Test validation issue by providing an invalid GUID for GET /v2/schema.

        * We test the GET /v2/schema endpoint by providing an invalid GUID.
        * Assert status code: 400 Bad Request.
        """
        if not endpoints_loader.endpoints_deprecated:
            pytest.skip("Skipping test_get_schema_v2_validation_error on new endpoint")

        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_SCHEMA_WITH_GUID,
        )

        response = make_iap_request(method, url)

        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()
        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "Invalid parameter provided", f"Unexpected message: {response_data['message']}"


    def test_get_schema_v2_404_not_found(self):
        """
        Test data not found by requesting a nonexistent GUID for GET /v2/schema.

        * We send a request to the GET /v2/schema endpoint providing an invalid GUID.
        * Assert status code: 404 Not Found.
        """
        url, method = endpoints_loader.formulate_url_and_method(
            key=GET_SCHEMA_WITH_GUID,
            params={
                "guid": "nonexistent_guid",
            }
        )

        response = make_iap_request(method, url)

        assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
        assert is_json_response(response), "Response is not valid JSON"

        response_data = response.json()
        assert "message" in response_data, f"Response JSON: {response_data}"
        assert response_data["message"] == "No schema found", f"Unexpected message: {response_data['message']}"

from tests.integration_tests.helpers.pubsub_helper import schema_pubsub_helper
from tests.integration_tests.helpers.utils import make_iap_request
from tests.test_data.shared_test_data import test_schema_subscriber_id, test_survey_id_list


class TestPostSchemaEndpoint:
    def test_post_schema_v1(self, setup_post_schema, test_schema_list):
        """
        Test the POST /v1/schema endpoint by publishing schemas from test_survey_id_list and checking the response
        and the pub/sub message.

        * We post a schema for each survey_id in survey_id_list and check the response
        * We retrieve and verify received messages from Pub/Sub
        """
        # Post v1 schema for each survey_id - v1 is stored in the second index of the test_schemas list
        for survey_id in test_survey_id_list:

            schema_post_response = make_iap_request(
                "POST",
                f"/v1/schema?survey_id={survey_id}",
                json=test_schema_list[1]
            )

            assert schema_post_response.status_code == 200
            assert "guid" in schema_post_response.json()

            received_messages = schema_pubsub_helper.pull_and_acknowledge_messages(
                test_schema_subscriber_id
            )
            
            assert len(received_messages) > 0, "No messages received from Pub/Sub"

            # Retrieve and verify received messages from Pub/Sub
            received_messages_json = received_messages[0]
            assert received_messages_json == schema_post_response.json()

        # Post v2 schema for each survey_id - v2 is stored in the first index of the test_schemas list
        for survey_id in test_survey_id_list:

            schema_post_response = make_iap_request(
                "POST",
                f"/v1/schema?survey_id={survey_id}",
                json=test_schema_list[0]
            )

            assert schema_post_response.status_code == 200
            assert "guid" in schema_post_response.json()

            received_messages = schema_pubsub_helper.pull_and_acknowledge_messages(
                test_schema_subscriber_id
            )

            # Retrieve and verify received messages from Pub/Sub
            received_messages_json = received_messages[0]
            assert received_messages_json == schema_post_response.json()

import json
import os
import time

from config.config_factory import config
from google.cloud import pubsub_v1


class PubSubHelper:
    def __init__(self, topic_id: str):
        if config.OAUTH_CLIENT_ID.__contains__("local"):
            os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"

        self.subscriber_client = pubsub_v1.SubscriberClient()
        self.publisher_client = pubsub_v1.PublisherClient()
        self.topic_id = topic_id

        if config.OAUTH_CLIENT_ID.__contains__("local"):
            self._try_create_topic()

    def _try_create_topic(self) -> None:
        """
        Try to create a topic for publisher if not exists
        """
        topic_path = self.publisher_client.topic_path(config.PROJECT_ID, self.topic_id)

        try:
            if not self._topic_exists(topic_path):
                self.publisher_client.create_topic(request={"name": topic_path})
        except Exception as e:
            print(f"Fail to create topic. Topic path: {topic_path} Error: {e}")

    def _topic_exists(self, topic_path: str) -> bool:
        """
        Returns True if the topic exists otherwise returns False.
        """
        try:
            self.publisher_client.get_topic(request={"topic": topic_path})
            return True
        except Exception:
            return False

    def try_create_subscriber(self, subscriber_id: str) -> None:
        """
        Creates a subscriber with a unique subscriber id if one does not already exist.

        Parameters:
        subscriber_id: the unique id of the subscriber being created.
        """
        topic_path = self.publisher_client.topic_path(config.PROJECT_ID, self.topic_id)

        subscription_path = self.subscriber_client.subscription_path(
            config.PROJECT_ID, subscriber_id
        )

        if not self._subscription_exists(subscriber_id):
            self.subscriber_client.create_subscription(
                request={
                    "name": subscription_path,
                    "topic": topic_path,
                    "enable_message_ordering": True,
                }
            )

            self._wait_and_check_subscription_exists(subscriber_id)

    def pull_and_acknowledge_messages(self, subscriber_id: str) -> dict:
        """
        Pulls all messages published to a topic via a subscriber.

        Parameters:
        subscriber_id: the unique id of the subscriber being created.
        """
        subscription_path = self.subscriber_client.subscription_path(
            config.PROJECT_ID, subscriber_id
        )
        NUM_MESSAGES = 5

        response = self.subscriber_client.pull(
            request={"subscription": subscription_path, "max_messages": NUM_MESSAGES},
            timeout=10.0,
        )

        messages = []
        ack_ids = []
        for received_message in response.received_messages:
            messages.append(self.format_received_message_data(received_message))
            ack_ids.append(received_message.ack_id)

        if ack_ids:
            self.subscriber_client.acknowledge(
                request={"subscription": subscription_path, "ack_ids": ack_ids}
            )
        else:
            print("No Ack IDs found in the response, messages cannot be acknowledged")

        return messages

    def format_received_message_data(self, received_message) -> dict:
        """
        Formats a messages received from a topic.

        Parameters:
        received_message: The message received from the topic.
        """
        return json.loads(
            received_message.message.data.decode("utf-8").replace("'", '"')
        )

    def try_delete_subscriber(self, subscriber_id: str) -> None:
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = self.subscriber_client.subscription_path(
            config.PROJECT_ID, subscriber_id
        )

        if self._subscription_exists(subscriber_id):
            with subscriber:
                subscriber.delete_subscription(
                    request={"subscription": subscription_path}
                )

            self._wait_and_check_subscription_deleted(subscriber_id)

    def _subscription_exists(self, subscriber_id: str) -> None:
        """
        Checks a subscription exists.

        Parameters:
        subscriber_id: the unique id of the subscriber being checked.
        """
        subscription_path = self.subscriber_client.subscription_path(
            config.PROJECT_ID, subscriber_id
        )

        try:
            self.subscriber_client.get_subscription(
                request={"subscription": subscription_path}
            )
            return True
        except Exception:
            return False

    def _wait_and_check_subscription_exists(
        self,
        subscriber_id: str,
        attempts: int = 5,
        backoff: int = 0.5,
    ) -> None:
        """
        Waits for a subscription to be created and checks if it exists.

        Parameters:
        subscriber_id: the unique id of the subscriber being checked.
        attempts: the number of attempts to check if the subscription exists.
        backoff: the time to wait between attempts.
        """
        while attempts != 0:
            if self._subscription_exists(subscriber_id):
                return

            attempts -= 1
            time.sleep(backoff)
            backoff += backoff

    def _wait_and_check_subscription_deleted(
        self,
        subscriber_id: str,
        attempts: int = 5,
        backoff: int = 0.5,
    ) -> None:
        """
        Waits for a subscription to be created and checks if it is deleted.

        Parameters:
        subscriber_id: the unique id of the subscriber being checked.
        attempts: the number of attempts to check if the subscription is deleted.
        backoff: the time to wait between attempts.
        """
        while attempts != 0:
            if not self._subscription_exists(subscriber_id):
                return

            attempts -= 1
            time.sleep(backoff)
            backoff += backoff


dataset_pubsub_helper = PubSubHelper(config.PUBLISH_DATASET_TOPIC_ID)
dataset_error_pubsub_helper = PubSubHelper(config.PUBLISH_DATASET_ERROR_TOPIC_ID)
schema_pubsub_helper = PubSubHelper(config.PUBLISH_SCHEMA_TOPIC_ID)

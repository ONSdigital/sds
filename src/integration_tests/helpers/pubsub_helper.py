import json
import os

from config.config_factory import config
from google.cloud import pubsub_v1

from src.test_data.shared_test_data import test_subscriber_id


class PubSubHelper:
    def __init__(self, topic_id: str, subscriber_id: str):
        if config.API_URL.__contains__("local"):
            os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"

        self.subscriber_client = pubsub_v1.SubscriberClient()
        self.publisher_client = pubsub_v1.PublisherClient()

        if config.API_URL.__contains__("local"):
            self._create_topic(topic_id)

        self._try_create_subscriber(topic_id, subscriber_id)

    def _create_topic(self, topic_id: str) -> None:
        """
        Creates a topic with a specified topic id.

        Parameters:
        topic_id: The unique id of the topic being created.
        """
        self.topic_path = self.publisher_client.topic_path(config.PROJECT_ID, topic_id)

        try:
            if not self._topic_exists():
                self.publisher_client.create_topic(request={"name": self.topic_path})
        except Exception as e:
            print(f"Fail to create topic. Topic path: {self.topic_path} Error: {e}")

    def _topic_exists(self) -> bool:
        """
        Returns `true` if the topic defined by `self.topic_path` exists otherwise returns `false`.
        """
        try:
            self.publisher_client.get_topic(request={"topic": self.topic_path})
            return True
        except Exception:
            return False

    def _try_create_subscriber(self, topic_id: str, subscriber_id: str) -> None:
        """
        Creates a subscriber with a unique subscriber id if one does not already exist.

        Parameters:
        topic_id: the unique id of the topic the subscriber is being created on.
        subscriber_id: the unique id of the subscriber being created.
        """

        subscription_path = self.subscriber_client.subscription_path(
            config.PROJECT_ID, subscriber_id
        )
        topic_path = self.publisher_client.topic_path(config.PROJECT_ID, topic_id)

        if not self._subscription_exists(subscriber_id):
            self.subscriber_client.create_subscription(
                request={
                    "name": subscription_path,
                    "topic": topic_path,
                    "enable_message_ordering": True,
                }
            )

    def pull_messages(self, subscriber_id: str) -> dict:
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


dataset_pubsub_helper = PubSubHelper(config.DATASET_TOPIC_ID, test_subscriber_id)

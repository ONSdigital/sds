import json

from google.cloud import exceptions
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.publisher import exceptions as pubsub_exceptions

from app.config import settings
from app.exception.exceptions import ExceptionTopicNotFound
from app.logging_config import logging
from app.models.schema_models import SchemaMetadata

logger = logging.getLogger(__name__)


class PublisherService:
    """Methods to publish pub/sub messages using the `pubsub_v1.PublisherClient()`"""
    publisher_client: PublisherClient

    def __init__(self, publisher_client: PublisherClient) -> None:
        self.publisher_client = publisher_client

        if settings.CONF == "unit":
            return

        topic_path = self.publisher_client.topic_path(settings.PROJECT_ID, settings.PUBLISH_SCHEMA_TOPIC_ID)

        # In local docker, we create the topic if it does not exist
        if settings.CONF == "docker-dev" and not self._verify_topic_exists(topic_path):
            self._create_topic(topic_path)

    def publish_data_to_topic(
        self,
        publish_data: SchemaMetadata,
        topic_id: str,
    ) -> None:
        """
        Publishes data to the pubsub topic.

        Parameters:
        publish_data: data to be sent to the pubsub topic,
        topic_id: unique identifier of the topic the data is published to
        """
        topic_path = self.publisher_client.topic_path(settings.PROJECT_ID, topic_id)
        self._verify_topic_exists(topic_path)

        data_str = json.dumps(publish_data.__dict__)

        # Data must be a bytestring
        data = data_str.encode("utf-8")

        # Publishes a message
        try:
            future = self.publisher_client.publish(topic_path, data=data)
            result = future.result()  # Verify the publishing succeeded
            logger.debug(f"Message published. {result}")
        except (RuntimeError, pubsub_exceptions.MessageTooLargeError) as exc:
            logger.debug(exc)

            raise RuntimeError("Error publishing message") from exc

    def _verify_topic_exists(self, topic_path: str) -> bool:
        """
        If the topic does not exist raises 500 global error.
        """
        try:
            self.publisher_client.get_topic(request={"topic": topic_path})
            return True
        except exceptions.NotFound as exc:
            logger.debug("Error getting topic")

            if settings.CONF == "docker-dev":
                return False

            raise ExceptionTopicNotFound from exc

    def _create_topic(self, topic_path) -> None:
        self.publisher_client.create_topic(request={"name": topic_path})
        logger.debug(f"Topic created: {topic_path}")


publisher_service = PublisherService(PublisherClient())

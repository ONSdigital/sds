import json

from config.config_factory import config
from google.cloud.pubsub_v1 import PublisherClient
from logging_config import logging
from models.dataset_models import DatasetMetadata
from models.schema_models import SchemaMetadata

logger = logging.getLogger(__name__)


class PublisherService:
    def __init__(self):
        self.publisher = None if config.CONF == "unit" else PublisherClient()

    def publish_data_to_topic(
        self, publish_data: DatasetMetadata | SchemaMetadata, topic_id: str
    ) -> None:
        """
        Publishes data to the pubsub topic.

        Parameters:
        publish_data: data to be sent to the pubsub topic,
        topic_id: unique identifier of the topic the data is published to
        """
        topic_path = self.publisher.topic_path(config.PROJECT_ID, topic_id)
        self._try_create_topic(topic_path)

        self.publisher.publish(
            topic_path, data=json.dumps(publish_data).encode("utf-8")
        )


    def _try_create_topic(self, topic_path: str) -> None:
        """
        Try to creates a topic with a specified topic id if none exists.

        Parameters:
        topic_id: The unique id of the topic being created.
        """
        try:
            if not self._topic_exists(topic_path):
                logger.debug("Topic does not exists. Creating topic...")
                self.publisher.create_topic(request={"name": topic_path})

                logger.debug(f"Topic with path {topic_path} created successfully")
        except Exception as e:
            print(f"Fail to create topic. Topic path: {topic_path} Error: {e}")

    def _topic_exists(self, topic_path: str) -> bool:
        """
        Returns True if the topic exists otherwise returns False.
        """
        try:
            self.publisher.get_topic(request={"topic": topic_path})
            return True
        except Exception:
            return False


publisher_service = PublisherService()

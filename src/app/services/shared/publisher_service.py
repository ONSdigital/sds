import json

from config.config_factory import config
from exception import exceptions
from google.cloud.pubsub_v1 import PublisherClient
from logging_config import logging
from models.dataset_models import DatasetMetadata
from models.schema_models import SchemaMetadata

logger = logging.getLogger(__name__)


class PublisherService:
    def __init__(self):
        self.publisher = None if config.CONF == "unit" else PublisherClient()

    def publish_data_to_topic(
        self,
        publish_data: DatasetMetadata | SchemaMetadata,
        topic_id: str,
    ) -> None:
        """
        Publishes data to the pubsub topic.

        Parameters:
        publish_data: data to be sent to the pubsub topic,
        topic_id: unique identifier of the topic the data is published to
        """
        topic_path = self.publisher.topic_path(config.PROJECT_ID, topic_id)
        self._verify_topic_exists(topic_path)

        self.publisher.publish(
            topic_path, data=json.dumps(publish_data).encode("utf-8")
        )

    def _verify_topic_exists(self, topic_path: str) -> None:
        """
        If the topic does not exist raises 500 global error.
        """
        try:
            self.publisher.get_topic(request={"topic": topic_path})
        except Exception as exc:
            # Create topic automatically in local docker-dev environment
            if config.CONF == "docker-dev":
                self._create_topic(topic_path)
                return

            raise exceptions.ExceptionTopicNotFound from exc

    def _create_topic(self, topic_path) -> None:
        self.publisher.create_topic(request={"name": topic_path})


publisher_service = PublisherService()

import json

import exception.exceptions as exceptions
from config.config_factory import config
from google.cloud import pubsub_v1
from logging_config import logging
from models.schema_models import SchemaMetadata

logger = logging.getLogger(__name__)


class Publisher:
    def __init__(self):
        self.client = pubsub_v1.PublisherClient()
        self.topic_path = None

    def publish_message_for_schema(self, topic_id: str, data: SchemaMetadata) -> None:
        """ """
        self._publish_message(topic_id, data)

    def _create_topic(self, topic_id: str) -> None:
        """ """
        self.topic_path = self.client.topic_path(config.PROJECT_ID, topic_id)

        logger.debug("Creating topic...")

        try:
            if not self._topic_exists():
                topic = self.client.create_topic(request={"name": self.topic_path})
                logger.debug(f"Created topic: {topic.name}")
        except Exception as e:
            logger.error(
                f"Fail to create topic. Topic path: {self.topic_path} Error: {e}"
            )

    def _topic_exists(self) -> bool:
        """
        Returns `true` if the topic defined by `self.topic_path` exists otherwise returns `false`.
        """
        try:
            self.client.get_topic(request={"topic": self.topic_path})
            return True
        except Exception as e:
            return False

    def _publish_message(self, topic_id: str, data) -> None:
        """ """
        self._create_topic(topic_id)
        data_bytestring = json.dumps(data.__dict__).encode("utf-8")

        try:
            future = self.client.publish(
                self.topic_path, data=data_bytestring, timeout=100
            )
            result = future.result()
            logger.debug(f"Message published. {result}")
        except Exception as e:
            logger.error(f"Fail to publish message. Error: {e}")
            raise exceptions.GlobalException


publisher = Publisher()

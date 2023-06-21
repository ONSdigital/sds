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
        self, publish_data: DatasetMetadata, topic_id: str
    ) -> None:
        """"""
        self._set_topic_path(topic_id)
        self._try_create_topic()

        self.publisher.publish(self.topic_path, data=str(publish_data).encode("utf-8"))

    def publish_schema_data_to_topic(
        self, publish_data: SchemaMetadata, topic_id: str
    ) -> None:
        """"""
        self._set_topic_path(topic_id)
        self._try_create_topic()

        data_bytestring = json.dumps(publish_data.__dict__).encode("utf-8")
        self.publisher.publish(self.topic_path, data=data_bytestring)

    def _set_topic_path(self, topic_id: str) -> None:
        """
        Set a topic path
        """
        self.topic_path = self.publisher.topic_path(config.PROJECT_ID, topic_id)

    def _try_create_topic(self) -> None:
        """
        Try to create a topic for publisher. Necessary for local docker development
        """
        try:
            if not self._topic_exists():
                logger.debug("Topic does not exists. Creating topic...")
                self.publisher.create_topic(request={"name": self.topic_path})

                logger.debug(f"Topic with path {self.topic_path} created successfully")
        except Exception as e:
            print(f"Fail to create topic. Topic path: {self.topic_path} Error: {e}")

    def _topic_exists(self) -> bool:
        """
        Returns `true` if the topic defined by `self.topic_path` exists otherwise returns `false`.
        """
        try:
            self.publisher.get_topic(request={"topic": self.topic_path})
            return True
        except Exception:
            return False


publisher_service = PublisherService()

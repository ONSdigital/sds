from config.config_factory import config
from google.cloud.pubsub_v1 import PublisherClient
from models.dataset_models import DatasetMetadata
from models.schema_models import SchemaMetadata
from logging_config import logging
import json

logger = logging.getLogger(__name__)

class PublisherService:
    def __init__(self):
        self.publisher = None if config.CONF == "unit" else PublisherClient()

    def publish_data_to_topic(
        self, publish_data: DatasetMetadata, topic_id: str
    ) -> None:
        """"""
        topic_path = self.publisher.topic_path(config.PROJECT_ID, topic_id)
        self.publisher.publish(topic_path, data=str(publish_data).encode("utf-8"))

    def publish_schema_data_to_topic(
        self, publish_data: SchemaMetadata, topic_id: str
    ) -> None:
        """"""
        topic_path = self.publisher.topic_path(config.PROJECT_ID, topic_id)
        data_bytestring = json.dumps(publish_data.__dict__).encode("utf-8")
        self.publisher.publish(topic_path, data=data_bytestring)


publisher_service = PublisherService()
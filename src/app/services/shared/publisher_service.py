from config.config_factory import config
from google.cloud.pubsub_v1 import PublisherClient
from models.dataset_models import DatasetMetadata


class PublisherService:
    def __init__(self):
        self.publisher = None if config.CONF == "unit" else PublisherClient()

    def publish_data_to_topic(
        self, publish_data: DatasetMetadata, topic_id: str
    ) -> None:
        """"""
        topic_path = self.publisher.topic_path(config.PROJECT_ID, topic_id)
        self.publisher.publish(topic_path, data=str(publish_data).encode("utf-8"))


publisher_service = PublisherService()

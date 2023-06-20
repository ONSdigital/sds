from config.config_factory import config
from google.cloud.pubsub_v1 import PublisherClient
from models.dataset_models import DatasetMetadata


class PublisherService:
    def __init__(self):
        self.publisher = None if config.CONF == "unit" else PublisherClient()

    def publish_data_to_topic(
        self, publish_data: DatasetMetadata, topic_id: str
    ) -> None:
        """
        Publishes data to the pubsub topic.

        Parameters:
        publish_data: data to be sent to the pubsub topic,
        topic_id: unique identifier of the topic the data is published to
        """
        topic_path = self.publisher.topic_path(config.PROJECT_ID, topic_id)
        self.publisher.publish(topic_path, data=str(publish_data).encode("utf-8"))


publisher_service = PublisherService()

from config.config_factory import config
from google.cloud import pubsub_v1
from logging_config import logging

logger = logging.getLogger(__name__)


class Subscriber:
    def __init__(self):
        self.client = pubsub_v1.SubscriberClient()
        self.subscription_path = None
        self.topic_path = None

    def _create_topic_path(self, topic_id: str) -> None:
        """ """
        self.topic_path = self.client.topic_path(config.PROJECT_ID, topic_id)

    def _create_subscription(self, subscription_id: str) -> None:
        self.subscription_path = self.client.subscription_path(
            config.PROJECT_ID, subscription_id
        )
        logger.info(f"Subscription path: {self.subscription_path}")
        logger.debug("Creating subscription...")

        try:
            if not self._subscription_exists():
                subscription = self.client.create_subscription(
                    request={
                        "name": self.subscription_path,
                        "topic": self.topic_path,
                        "enable_message_ordering": True,
                    }
                )
                logger.debug(f"Created subscription: {subscription.name}")
        except Exception as e:
            logger.error(
                f"Fail to create subscription. Subscription path: {self.subscription_path} Error: {e}"
            )

    def _subscription_exists(self) -> bool:
        """ """
        try:
            self.client.get_subscription(
                request={"subscription": self.subscription_path}
            )
            return True
        except Exception:
            return False

    def pull_messages_and_acknowledge(
        self, topic_id: str, subscription_id: str
    ) -> list:
        """ """
        self._create_topic_path(topic_id)
        self._create_subscription(subscription_id)

 
        response = self.client.pull(
            request={
                "subscription": self.subscription_path,
                "max_messages": 50,
            }
        )
        
        messages = []
        ack_ids = []
        if len(response.received_messages) > 0:
            
            for msg in response.received_messages:
                message_data = msg.message.data.decode("utf-8")
                messages.append(message_data)
                ack_ids.append(msg.ack_id)

            self.client.acknowledge(
                request={
                    "subscription": self.subscription_path,
                    "ack_ids": ack_ids,
                }
            )
            logger.info(f"Received and acknowledged {len(response.received_messages)} messages from {self.subscription_path}.")
        else:
            logger.info("No message received")

        return messages

        """def callback(message: pubsub_v1.subscriber.message.Message) -> None:
            message.ack()

        streaming_pull_future = self.client.subscribe(
            self.subscription_path, callback=callback
        )

        with self.client:
            try:
                result = streaming_pull_future.result(timeout=20.0)
                return result
            except TimeoutError:
                logger.error("Pull message has timeouted")
                streaming_pull_future.cancel()
                streaming_pull_future.result()"""


subscriber = Subscriber()

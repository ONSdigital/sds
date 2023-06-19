from config.config_factory import config
from google.api_core import retry
from google.cloud import pubsub_v1


class SubscriberHelper:
    def __init__(self):
        self.subscriber_client = pubsub_v1.SubscriberClient()
        self.publisher_client = pubsub_v1.PublisherClient()

    def try_create_subscriber(self, topic_id: str, subscriber_id: str) -> None:
        """Create a new pull subscription on the given topic."""

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

    def pull_messages(self, subscriber_id: str) -> any:
        """Pulling messages synchronously."""

        subscription_path = self.subscriber_client.subscription_path(
            config.PROJECT_ID, subscriber_id
        )
        NUM_MESSAGES = 5

        response = self.subscriber_client.pull(
            request={"subscription": subscription_path, "max_messages": NUM_MESSAGES},
            retry=retry.Retry(deadline=300),
        )

        messages = []
        ack_ids = []
        for received_message in response.received_messages:
            messages.append(received_message.message.decode("utf8"))
            ack_ids.append(received_message.ack_id)

        if ack_ids:
            self.subscriber_client.acknowledge(
                request={"subscription": subscription_path, "ack_ids": ack_ids}
            )
        else:
            print("No Ack IDs found in the response, messages cannot be acknowledged")

        return messages

    def delete_subscriber_if_exists(self, subscriber_id: str) -> None:
        subscription_path = self.subscriber_client.subscription_path(
            config.PROJECT_ID, subscriber_id
        )

        if self._subscription_exists(subscriber_id):
            self.subscriber_client.delete_subscription(
                request={"subscription": subscription_path}
            )

    def _subscription_exists(self, subscriber_id: str) -> None:
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


subscriber_helper = SubscriberHelper()

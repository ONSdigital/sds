from config.config_factory import config
from google.cloud import pubsub_v1
from logging_config import logging

logger = logging.getLogger(__name__)


class CollectionExerciseEndSubscriber:

    def __init__(self) -> None:
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        self.create_topic()
        self.create_subscription()

    def pull_message(self):
        subscription_path = self.subscriber.subscription_path(
            config.PROJECT_ID, config.COLLECTION_EXERCISE_END_SUBSCRIPTION_ID
        )

        # Wrap the subscriber in a 'with' block to automatically call close() to
        # close the underlying gRPC channel when done.
        with self.subscriber:
            # The subscriber pulls a specific number of messages. The actual
            # number of messages pulled may be smaller than max_messages.
            response = self.subscriber.pull(
                subscription=subscription_path,
                return_immediately=True,
                max_messages=1,
            )

            ack_ids = []
            for received_message in response.received_messages:
                ack_ids.append(received_message.ack_id)

            # Acknowledges the received messages so they will not be sent again.
            if ack_ids:
                self.subscriber.acknowledge(
                    subscription=subscription_path, ack_ids=ack_ids
                )
                print(f"Cleared {len(ack_ids)} messages")
            else:
                print("No messages found")

    def pull_messages(self):
        subscription_path = self.subscriber.subscription_path(
            config.PROJECT_ID, config.COLLECTION_EXERCISE_END_SUBSCRIPTION_ID
        )

        pull_response = self.subscriber.pull(
            subscription=subscription_path, max_messages=1
        )

        for msg in pull_response.received_messages:
            message = msg.message.data.decode("utf-8")
            print(message)
            self.subscriber.acknowledge(subscription_path, [msg.ack_id])

    def read_pubsub_messages(self, service_account_file: str):
        subscription_path = self.subscriber.subscription_path(
            config.PROJECT_ID, config.COLLECTION_EXERCISE_END_SUBSCRIPTION_ID
        )

        # Initialize the Pub/Sub client
        subscriber = pubsub_v1.SubscriberClient.from_service_account_file(
            service_account_file
        )

        # Define the subscription path
        subscription_path = subscriber.subscription_path(subscription_path)

        def callback(message):
            # Process the received message
            print(f"Received message: {message.data}")
            # Acknowledge the message to mark it as processed
            message.ack()

        # Subscribe to the specified subscription and start receiving messages
        streaming_pull_future = subscriber.subscribe(
            subscription_path, callback=callback
        )

        print(f"Listening for messages on {subscription_path}...\n")

        # Keep the script running to continue receiving messages
        try:
            streaming_pull_future.result()
        except KeyboardInterrupt:
            streaming_pull_future.cancel()

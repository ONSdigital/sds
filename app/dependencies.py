from fastapi import Depends
from google.cloud.pubsub_v1 import PublisherClient

from app.services.schema.schema_processor_service import SchemaProcessorService
from app.services.shared.publisher_service import PublisherService


def get_publisher_service() -> PublisherService:
    return PublisherService(PublisherClient())


def get_schema_processor_service(
        publisher_service: PublisherService = Depends(get_publisher_service)
) -> SchemaProcessorService:
    return SchemaProcessorService(
        publisher_service=publisher_service
    )

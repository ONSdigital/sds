from fastapi import Depends
from google.cloud import storage
from google.cloud.pubsub_v1 import PublisherClient

from app.config import settings
from app.repositories.buckets.bucket_loader import BucketLoader
from app.services.schema.schema_processor_service import SchemaProcessorService
from app.services.shared.publisher_service import PublisherService


def get_publisher_service() -> PublisherService:
    return PublisherService(PublisherClient())


def get_bucket_loader() -> BucketLoader:
    return BucketLoader(storage.Client(project=settings.PROJECT_ID))


def get_schema_processor_service(
        bucket_loader: BucketLoader = Depends(get_bucket_loader),
        publisher_service: PublisherService = Depends(get_publisher_service)
) -> SchemaProcessorService:
    return SchemaProcessorService(
        bucket_loader=bucket_loader,
        publisher_service=publisher_service
    )

from fastapi import Depends
from google.cloud import firestore
from google.cloud.pubsub_v1 import PublisherClient

from app.config import settings
from app.util.firebase_loader import FirebaseLoader
from app.services.dataset.dataset_deletion_service import DatasetDeletionService
from app.services.dataset.dataset_service import DatasetService
from app.services.schema_service import SchemaService
from app.services.shared.publisher_service import PublisherService


def get_publisher_service() -> PublisherService:
    return PublisherService(PublisherClient())

def get_firebase_loader() -> FirebaseLoader:
    return FirebaseLoader(firestore.Client(project=settings.PROJECT_ID, database=settings.FIRESTORE_DB_NAME))

def get_schema_processor_service(
        firebase_loader: FirebaseLoader = Depends(get_firebase_loader),
        publisher_service: PublisherService = Depends(get_publisher_service),
) -> SchemaService:
    return SchemaService(
        firebase_loader=firebase_loader,
        publisher_service=publisher_service
    )

def get_dataset_deletion_service(
        firebase_loader: FirebaseLoader = Depends(get_firebase_loader),
) -> DatasetDeletionService:
    return DatasetDeletionService(
        firebase_loader=firebase_loader,
    )

def get_dataset_service(
        firebase_loader: FirebaseLoader = Depends(get_firebase_loader),
) -> DatasetService:
    return DatasetService(
        firebase_loader=firebase_loader,
    )

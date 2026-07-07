from fastapi import Depends
from google.cloud import firestore
from google.cloud.pubsub_v1 import PublisherClient

from app.config import settings
from app.repositories.dataset_deletion.firestore_dataset_deletion_repository import FirestoreDatasetDeletionRepository
from app.repositories.dataset_storage.firestore_dataset_storage_repository import FirestoreDatasetStorageRepository
from app.repositories.schema_storage.firestore_schema_storage_repository import FirestoreSchemaStorageRepository
from app.services.dataset_service import DatasetService
from app.util.firebase_loader import FirebaseLoader
from app.services.schema_service import SchemaService
from app.services.shared.publisher_service import PublisherService

# ------------------------
# New
# ------------------------


def get_publisher_service() -> PublisherService:
    return PublisherService(PublisherClient())


def get_firebase_loader() -> FirebaseLoader:
    return FirebaseLoader(firestore.Client(project=settings.PROJECT_ID, database=settings.FIRESTORE_DB_NAME))


def get_schema_service(
    firebase_loader: FirebaseLoader = Depends(get_firebase_loader),
    publisher_service: PublisherService = Depends(get_publisher_service)
) -> SchemaService:

    # TODO use profiles to change config
    return SchemaService(
        schema_repository=FirestoreSchemaStorageRepository(
            firebase_loader=firebase_loader,
        ),
        publisher_service=publisher_service
    )


def get_dataset_service(
    firebase_loader: FirebaseLoader = Depends(get_firebase_loader)
) -> DatasetService:

    # TODO use profiles to change config
    return DatasetService(
        dataset_deletion_repository=FirestoreDatasetDeletionRepository(
            firebase_loader=firebase_loader,
        ),
        dataset_storage_repository=FirestoreDatasetStorageRepository(
            firebase_loader=firebase_loader,
        )
    )


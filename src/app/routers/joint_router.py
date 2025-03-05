import exception.exception_response_models as erm
from exception.exception_response_models import ExceptionResponseModel
from fastapi import APIRouter, Depends
from logging_config import logging
from models.joint_models import JointMetadata
from services.dataset.dataset_service import DatasetService

from src.app.models.dataset_models import DatasetMetadata
from src.app.models.schema_models import SchemaMetadata
from src.app.services.schema.schema_processor_service import SchemaProcessorService

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/v1/all_metadata",
    response_model=JointMetadata,
    responses={
        500: {
            "model": ExceptionResponseModel,
            "content": {"application/json": {"example": erm.erm_500_global_exception}},
        },
    },
)
async def get_all_metadata(
        dataset_service: DatasetService = Depends(),
        schema_service: SchemaProcessorService = Depends()
) -> list[JointMetadata]:
    """
    Retrieve metadata for all datasets and schemas.
    """
    logger.info("Retrieving all datasets and schemas...")
    dataset_metadata_collection: DatasetMetadata = dataset_service.get_all_dataset_metadata_collection()
    schema_metadata_collection: SchemaMetadata = schema_service.get_all_schema_metadata_collection_with_guid()
    joint_data = JointMetadata(datasets=dataset_metadata_collection, schemas=schema_metadata_collection)
    logger.info("Datasets and schemas retrieved successfully.")
    return joint_data

import exception.exception_response_models as erm
from exception.exception_response_models import ExceptionResponseModel
from fastapi import APIRouter, Depends
from logging_config import logging
from models.baddy_models import BaddyData
from services.dataset.dataset_service import DatasetService

from src.app.services.schema.schema_processor_service import SchemaProcessorService

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/v1/baddy_data",
    response_model=BaddyData,
    responses={
        400: {
            "model": ExceptionResponseModel,
            "content": {
                "application/json": {
                    "example": erm.erm_400_incorrect_key_names_exception
                }
            },
        },
        500: {
            "model": ExceptionResponseModel,
            "content": {"application/json": {"example": erm.erm_500_global_exception}},
        },
        404: {
            "model": ExceptionResponseModel,
            "content": {
                "application/json": {"example": erm.erm_404_no_datasets_exception}
            },
        },
    },
)
async def get_baddy_data(
        dataset_service: DatasetService = Depends(),
        schema_service: SchemaProcessorService = Depends()
) -> list[BaddyData]:
    """
    Retrieve all datasets and schemas.
    """
    logger.info("Retrieving all datasets and schemas...")
    dataset_metadata_collection = dataset_service.get_all_dataset_metadata_collection()
    schema_metadata_collection = schema_service.get_all_schema_metadata_collection_with_guid()
    baddy_data = BaddyData(datasets=dataset_metadata_collection, schemas=schema_metadata_collection)
    return baddy_data

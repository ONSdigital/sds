from fastapi import APIRouter, Depends, HTTPException
from logging_config import logging
from models.dataset_models import DatasetMetadata
from repositories.dataset_repository import DatasetRepository
from services.dataset.dataset_processor_service import DatasetProcessorService

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/v1/unit_data")
async def get_unit_supplementary_data(
    dataset_id: str,
    unit_id: str,
    dataset_repository: DatasetRepository = Depends(),
):
    """
    Retrieve supplementary data for a particular unit given the unit id
    and the dataset id, return 404 if no data is returned.
    """
    logger.info("Getting unit supplementary data...")
    logger.debug(f"Input data: dataset_id={dataset_id}, unit_id={unit_id}")

    unit_supplementary_data = dataset_repository.get_unit_supplementary_data(
        dataset_id, unit_id
    )

    if not unit_supplementary_data:
        logger.error("Item not found")
        raise HTTPException(status_code=404, detail="Item not found")

    logger.info("Unit supplementary data outputted successfully.")
    logger.debug(f"Unit supplementary data: {unit_supplementary_data}")

    return unit_supplementary_data


@router.get("/v1/dataset_metadata", response_model=list[DatasetMetadata])
async def get_dataset_metadata_collection(
    survey_id: str,
    period_id: str,
    dataset_processor_service: DatasetProcessorService = Depends(),
) -> list[DatasetMetadata]:
    """
    Retrieve the matching dataset metadata, given the survey_id and period_id.
    The matching metadata are returned as an array of dictionaries.
    """
    logger.info("Getting dataset metadata collection...")
    logger.debug(f"Input data: survey_id={survey_id}, period_id={period_id}")

    dataset_metadata_collection = (
        dataset_processor_service.get_dataset_metadata_collection(survey_id, period_id)
    )

    if not dataset_metadata_collection:
        logger.error("Dataset metadata collection not found.")
        raise HTTPException(
            status_code=404, detail="Dataset metadata collection not found."
        )

    logger.info("Dataset metadata collection successfully retrieved.")
    logger.debug(f"Dataset metadata collection: {dataset_metadata_collection}")

    return dataset_metadata_collection

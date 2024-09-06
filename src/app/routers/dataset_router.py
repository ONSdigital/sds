import exception.exception_response_models as erm
import exception.exceptions as exceptions
from exception.exception_response_models import ExceptionResponseModel
from fastapi import APIRouter, Depends
from logging_config import logging
from models.dataset_models import DatasetMetadata
from repositories.firebase.dataset_firebase_repository import DatasetFirebaseRepository
from services.dataset.dataset_processor_service import DatasetProcessorService
from services.validators.query_parameter_validator_service import (
    QueryParameterValidatorService,
)

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/new-sub")
async def pull_subscription():
    logger.info("endpoint hit")


@router.get(
    "/v1/unit_data",
    responses={
        400: {
            "model": ExceptionResponseModel,
            "content": {
                "application/json": {"example": erm.erm_400_validation_exception}
            },
        },
        500: {
            "model": ExceptionResponseModel,
            "content": {"application/json": {"example": erm.erm_500_global_exception}},
        },
        404: {
            "model": ExceptionResponseModel,
            "content": {
                "application/json": {"example": erm.erm_404_no_unit_data_exception}
            },
        },
    },
)
async def get_unit_supplementary_data(
    dataset_id: str,
    identifier: str,
    dataset_repository: DatasetFirebaseRepository = Depends(),
):
    """
    Retrieve supplementary data for a particular unit given the dataset id and identifier, return 404 if no data is returned.

    Parameters:
    dataset_id (str): The unique id of the dataset being queried.
    identifier (str): The identifier of the particular unit on the data being queried.
    """
    logger.info("Getting unit supplementary data...")
    logger.debug(f"Input data: dataset_id={dataset_id}, identifier={identifier}")

    unit_supplementary_data = dataset_repository.get_unit_supplementary_data(
        dataset_id, identifier
    )

    if not unit_supplementary_data:
        logger.error("Item not found")
        raise exceptions.ExceptionNoUnitData

    logger.info("Unit supplementary data outputted successfully.")
    logger.debug(f"Unit supplementary data: {unit_supplementary_data}")

    return unit_supplementary_data


@router.get(
    "/v1/dataset_metadata",
    response_model=list[DatasetMetadata],
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
async def get_dataset_metadata_collection(
    survey_id: str = None,
    period_id: str = None,
    dataset_processor_service: DatasetProcessorService = Depends(),
) -> list[DatasetMetadata]:
    """
    Retrieve the matching dataset metadata, given the survey_id and period_id.

    Parameters:
    survey_id (str): The survey id of the dataset being queried.
    period_id (str): The period id of the dataset being queried.
    """
    QueryParameterValidatorService.validate_survey_and_period_id_from_dataset_metadata(
        survey_id, period_id
    )

    logger.info("Getting dataset metadata collection...")
    logger.debug(f"Input data: survey_id={survey_id}, period_id={period_id}")

    dataset_metadata_collection = (
        dataset_processor_service.get_dataset_metadata_collection(survey_id, period_id)
    )

    if not dataset_metadata_collection:
        logger.error("Dataset metadata collection not found.")
        raise exceptions.ExceptionNoDatasetMetadata

    logger.info("Dataset metadata collection successfully retrieved.")
    logger.debug(f"Dataset metadata collection: {dataset_metadata_collection}")

    return dataset_metadata_collection

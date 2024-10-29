import exception.exception_response_models as erm
from exception import exceptions
from exception.exception_response_models import ExceptionResponseModel
from fastapi import APIRouter, Depends
from logging_config import logging
from models.collection_exericise_end_data import CollectionExerciseEndData
from models.dataset_models import DatasetMetadata
from services.dataset.dataset_deletion_service import DatasetDeletionService
from services.dataset.dataset_service import DatasetService

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/collection-exercise-end", status_code=200)
async def post_collection_exercise_end_message(
    collection_end_data: CollectionExerciseEndData,
    dataset_deletion_service: DatasetDeletionService = Depends(),
):
    logger.info("collection_exercise_end message received")
    logger.debug(f"collection_exercise_end message received {collection_end_data}")
    dataset_deletion_service.process_collection_exercise_end_message(
        collection_end_data
    )
    return {"message": "accepted"}


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
    dataset_service: DatasetService = Depends(),
):
    """
    Retrieve supplementary data for a particular unit given the dataset id and identifier, return 404 if no data is returned.

    Parameters:
    dataset_id (str): The unique id of the dataset being queried.
    identifier (str): The identifier of the particular unit on the data being queried.
    """
    logger.info("Getting unit supplementary data...")
    logger.debug(f"Input data: dataset_id={dataset_id}, identifier={identifier}")

    unit_supplementary_data = dataset_service.get_dataset_metadata_collection(dataset_id, identifier)

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
    survey_id: str | None = None,
    period_id: str | None = None,
    dataset_service: DatasetService = Depends(),
) -> list[DatasetMetadata]:
    """
    Retrieve the matching dataset metadata, given the survey_id and period_id.

    Parameters:
    survey_id (str): The survey id of the dataset being queried.
    period_id (str): The period id of the dataset being queried.
    """

    logger.info("Getting dataset metadata collection...")
    logger.debug(f"Input data: survey_id={survey_id}, period_id={period_id}")

    dataset_metadata_collection = (
        dataset_service.get_dataset_metadata_collection(survey_id, period_id)
    )

    if not dataset_metadata_collection:
        logger.error("Dataset metadata collection not found.")
        raise exceptions.ExceptionNoDatasetMetadata

    logger.info("Dataset metadata collection successfully retrieved.")
    logger.debug(f"Dataset metadata collection: {dataset_metadata_collection}")

    return dataset_metadata_collection

from dataclasses import asdict

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from logging_config import logging
from models.status_models import BadRequest, DeploymentStatus
from services.shared.utility_functions import UtilityFunctions

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/status",
    responses={
        status.HTTP_200_OK: {
            "model": DeploymentStatus,
            "description": ("Deployment done succuessfully"),
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": BadRequest,
            "description": "Internal error. This is triggered when something an unexpected error occurs on the server side.",
        },
    },
)
async def http_get_status():
    """
    GET method that returns `SDS_APPLICATION_VERSION` if the deployment is successful
    """
    application_version = UtilityFunctions.get_application_version()
    if application_version:
        response_content = DeploymentStatus(version=application_version)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=asdict(response_content)
        )
    else:
        response_content = BadRequest(message="Internal server error")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=asdict(response_content),
        )

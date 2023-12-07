from fastapi import APIRouter, Body, Depends
from logging_config import logging
from config.config_factory import config

from src.app.models.status_models import DeploymentStatus

router = APIRouter()

logger = logging.getLogger(__name__)


@app.get(
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
    application_version = config.SDS_APPLICATION_VERSION
    if application_version:
        response_content = DeploymentStatus(version=config.SDS_APPLICATION_VERSION)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=asdict(response_content)
        )
    else:
        response_content = BadRequest(message="Internal server error")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=asdict(response_content),
        )

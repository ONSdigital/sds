import os

import yaml
from fastapi.openapi.utils import get_openapi

from src.app.app import app

OUTPUT_PATH = os.path.join(os.getcwd(), "openapi.yaml")


if __name__ == "__main__":
    # Writes the FastApi schema to an output yaml file
    with open(OUTPUT_PATH, "w+") as f:
        yaml.dump(
            get_openapi(
                title=app.title,
                version=app.version,
                openapi_version=app.openapi_version,
                description=app.description,
                routes=app.routes,
            ),
            f,
        )

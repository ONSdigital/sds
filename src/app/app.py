from fastapi import FastAPI
from logging_config import logging
from routers import dataset_router, schema_router

logger = logging.getLogger(__name__)
app = FastAPI()

app.include_router(dataset_router.router)
app.include_router(schema_router.router)

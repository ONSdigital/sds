import exception.exceptions as exceptions
from config.config_factory import config
from exception.exception_interceptor import ExceptionInterceptor
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from google.cloud import pubsub_v1
from logging_config import logging
from routers import dataset_router, schema_router, status_router

logger = logging.getLogger(__name__)
app = FastAPI()

app.description = "Open api schema for SDS"
app.title = "Supplementary Data Service"
app.version = "1.0.0"


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    for _, method_item in openapi_schema.get("paths").items():
        for _, param in method_item.items():
            responses = param.get("responses")
            # remove 422 response, also can remove other status code
            if "422" in responses:
                del responses["422"]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.add_exception_handler(
    exceptions.ExceptionIncorrectSchemaKey,
    ExceptionInterceptor.throw_400_incorrect_schema_key_exception,
)
app.add_exception_handler(
    exceptions.ExceptionIncorrectSchemaV2Key,
    ExceptionInterceptor.throw_400_incorrect_schema_v2_key_exception,
)
app.add_exception_handler(
    exceptions.ExceptionNoSchemaMetadataCollection,
    ExceptionInterceptor.throw_404_no_schemas_metadata_exception,
)
app.add_exception_handler(
    exceptions.ExceptionNoSchemaFound,
    ExceptionInterceptor.throw_404_no_schema_exception,
)
app.add_exception_handler(
    exceptions.ExceptionIncorrectDatasetKey,
    ExceptionInterceptor.throw_400_incorrect_key_names_exception,
)
app.add_exception_handler(
    exceptions.ExceptionNoDatasetMetadata,
    ExceptionInterceptor.throw_404_no_result_exception,
)
app.add_exception_handler(
    exceptions.ExceptionNoUnitData,
    ExceptionInterceptor.throw_404_unit_data_no_response_exception,
)
app.add_exception_handler(
    exceptions.GlobalException,
    ExceptionInterceptor.throw_500_global_exception,
)
app.add_exception_handler(
    exceptions.ValidationException,
    ExceptionInterceptor.throw_400_validation_exception,
)
app.add_exception_handler(
    exceptions.ExceptionNoSurveyIDs,
    ExceptionInterceptor.throw_404_no_survey_id_exception,
)
app.add_exception_handler(
    exceptions.ExceptionBucketNotFound,
    ExceptionInterceptor.throw_500_global_exception,
)
app.add_exception_handler(
    exceptions.ExceptionTopicNotFound,
    ExceptionInterceptor.throw_500_global_exception,
)


@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    """
    Override the global exception handler (500 internal server error) in
    FastAPI and throw error in JSON format
    """
    return ExceptionInterceptor.throw_500_global_exception(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    When a request contains invalid data, FastAPI internally raises a
    RequestValidationError. This function override the default
    validation exception handler to return 400 instead of 422
    """
    return ExceptionInterceptor.throw_400_validation_exception(request, exc)


subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()
subscription_path = subscriber.subscription_path(
    config.PROJECT_ID, config.COLLECTION_EXERCISE_END_SUBSCRIPTION_ID
)


def create_topic() -> None:
    topic_path = subscriber.topic_path(
        config.PROJECT_ID, config.COLLECTION_EXERCISE_END_TOPIC_ID
    )
    """Create a new Pub/Sub topic."""
    logger.debug("create_topic")
    topic = publisher.create_topic(request={"name": topic_path})
    logger.debug(f"Created topic: {topic.name}")


def create_subscription() -> None:
    topic_path = subscriber.topic_path(
        config.PROJECT_ID, config.COLLECTION_EXERCISE_END_TOPIC_ID
    )
    """Creates a subscription using `self.subscription_path`"""

    subscription = subscriber.create_subscription(
        request={
            "name": subscription_path,
            "topic": topic_path,
            "enable_message_ordering": True,
        }
    )

    logger.debug(f"Subscription created: {subscription}")


async def process_subscription():
    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        logger.info("Collection Exercise End Message received")
        logger.debug(f"Collection Exercise End Message received : {message}")
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)
    logger.debug(f"Listening for messages on subscription path : {subscription_path}")


@app.on_event("startup")
async def startup_event():
    create_topic()
    create_subscription()
    # Start the background task to receive and process messages
    await process_subscription()


app.include_router(dataset_router.router)
app.include_router(schema_router.router)
app.include_router(status_router.router)

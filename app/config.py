from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    CONF: str = ""
    TIME_FORMAT: str = "%Y-%m-%dT%H:%M:%SZ"
    LOG_LEVEL: str = "INFO"
    PROJECT_ID: str = "ons-sds-ci"
    PUBLISH_SCHEMA_TOPIC_ID: str = "ons-sds-publish-schema"
    SURVEY_MAP_URL: str = "https://raw.githubusercontent.com/ONSdigital/sds-schema-definitions/main/mapping/survey_map.json"
    FIRESTORE_DB_NAME: str = "(default)"
    SDS_APPLICATION_VERSION: str = "development"
    TEST_SCHEMA_PATH: str = "tests/test_data/json/"
    API_URL: str = "only required for integration tests"
    URL_SCHEME: str = "only required for integration tests"
    PUBSUB_EMULATOR_HOST: str = "only required for local development environment"
    FIRESTORE_EMULATOR_HOST: str = "only required for local development environment"


settings = Settings()

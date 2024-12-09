from config.config_helpers import get_value_from_env
from pydantic_settings import BaseSettings

TIME_FORMAT_STRING = "%Y-%m-%dT%H:%M:%SZ"


class Config(BaseSettings):
    def __init__(self):
        super().__init__()
        self.CONF = get_value_from_env("CONF")
        self.TIME_FORMAT = TIME_FORMAT_STRING
        self.SCHEMA_BUCKET_NAME = get_value_from_env("SCHEMA_BUCKET_NAME")
        self.LOG_LEVEL = get_value_from_env("LOG_LEVEL")
        self.PROJECT_ID = get_value_from_env("PROJECT_ID")
        self.PUBLISH_SCHEMA_TOPIC_ID = get_value_from_env("PUBLISH_SCHEMA_TOPIC_ID")
        self.SURVEY_MAP_URL = get_value_from_env("SURVEY_MAP_URL")
        self.FIRESTORE_DB_NAME = get_value_from_env("FIRESTORE_DB_NAME")
        self.SDS_APPLICATION_VERSION = get_value_from_env("SDS_APPLICATION_VERSION")

    CONF: str
    TIME_FORMAT: str = TIME_FORMAT_STRING
    SCHEMA_BUCKET_NAME: str
    LOG_LEVEL: str
    PROJECT_ID: str
    PUBLISH_SCHEMA_TOPIC_ID: str
    SURVEY_MAP_URL: str
    FIRESTORE_DB_NAME: str
    SDS_APPLICATION_VERSION: str


class IntegrationTestConfig(BaseSettings):
    def __init__(self):
        super().__init__()
        self.CONF = get_value_from_env("CONF")
        self.TIME_FORMAT = TIME_FORMAT_STRING
        self.SCHEMA_BUCKET_NAME = get_value_from_env(
            "SCHEMA_BUCKET_NAME", "test_schema_bucket"
        )
        self.TEST_SCHEMA_PATH = get_value_from_env(
            "TEST_SCHEMA_PATH", "src/test_data/json/schema.json"
        )
        self.GOOGLE_APPLICATION_CREDENTIALS = get_value_from_env(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )
        self.PROJECT_ID = get_value_from_env("PROJECT_ID")
        self.PUBLISH_SCHEMA_TOPIC_ID = get_value_from_env("PUBLISH_SCHEMA_TOPIC_ID")
        self.API_URL = get_value_from_env("API_URL", "localhost")
        self.OAUTH_CLIENT_ID = get_value_from_env("OAUTH_CLIENT_ID", "localhost")
        self.SURVEY_MAP_URL = get_value_from_env(
            "SURVEY_MAP_URL",
            "https://raw.githubusercontent.com/ONSdigital/sds-schema-definitions/main/mapping/survey_map.json",
        )
        self.FIRESTORE_DB_NAME = get_value_from_env("FIRESTORE_DB_NAME")
        self.SDS_APPLICATION_VERSION = get_value_from_env("SDS_APPLICATION_VERSION")

    CONF: str
    TIME_FORMAT: str = TIME_FORMAT_STRING
    SCHEMA_BUCKET_NAME: str
    TEST_SCHEMA_PATH: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    PROJECT_ID: str
    PUBLISH_SCHEMA_TOPIC_ID: str
    API_URL: str
    OAUTH_CLIENT_ID: str
    SURVEY_MAP_URL: str
    FIRESTORE_DB_NAME: str
    SDS_APPLICATION_VERSION: str


class IntegrationTestCloudbuildConfig(BaseSettings):
    def __init__(self):
        super().__init__()
        self.CONF = get_value_from_env("CONF")
        self.TIME_FORMAT = TIME_FORMAT_STRING
        self.SCHEMA_BUCKET_NAME = get_value_from_env(
            "SCHEMA_BUCKET_NAME", "testSchemaBucket"
        )
        self.TEST_SCHEMA_PATH = get_value_from_env(
            "TEST_SCHEMA_PATH", "src/test_data/json/schema.json"
        )
        self.PROJECT_ID = get_value_from_env("PROJECT_ID")
        self.PUBLISH_SCHEMA_TOPIC_ID = get_value_from_env("PUBLISH_SCHEMA_TOPIC_ID")
        self.API_URL = get_value_from_env("API_URL", "localhost")
        self.OAUTH_CLIENT_ID = get_value_from_env("OAUTH_CLIENT_ID", "localhost")
        self.SURVEY_MAP_URL = get_value_from_env(
            "SURVEY_MAP_URL",
            "https://raw.githubusercontent.com/ONSdigital/sds-schema-definitions/main/mapping/survey_map.json",
        )
        self.FIRESTORE_DB_NAME = get_value_from_env("FIRESTORE_DB_NAME")
        self.SDS_APPLICATION_VERSION = get_value_from_env("SDS_APPLICATION_VERSION")

    CONF: str
    TIME_FORMAT: str = TIME_FORMAT_STRING
    SCHEMA_BUCKET_NAME: str
    TEST_SCHEMA_PATH: str
    PROJECT_ID: str
    PUBLISH_SCHEMA_TOPIC_ID: str
    API_URL: str
    OAUTH_CLIENT_ID: str
    SURVEY_MAP_URL: str
    FIRESTORE_DB_NAME: str
    SDS_APPLICATION_VERSION: str


class CloudBuildConfig(BaseSettings):
    def __init__(self):
        super().__init__()
        self.CONF = get_value_from_env("CONF")
        self.TIME_FORMAT = TIME_FORMAT_STRING
        self.SCHEMA_BUCKET_NAME = get_value_from_env("SCHEMA_BUCKET_NAME")
        self.LOG_LEVEL = get_value_from_env("LOG_LEVEL")
        self.PROJECT_ID = get_value_from_env("PROJECT_ID")
        self.PUBLISH_SCHEMA_TOPIC_ID = get_value_from_env("PUBLISH_SCHEMA_TOPIC_ID")
        self.SURVEY_MAP_URL = get_value_from_env("SURVEY_MAP_URL")
        self.FIRESTORE_DB_NAME = get_value_from_env("FIRESTORE_DB_NAME")
        self.SDS_APPLICATION_VERSION = get_value_from_env("SDS_APPLICATION_VERSION")

    CONF: str
    TIME_FORMAT: str = TIME_FORMAT_STRING
    SCHEMA_BUCKET_NAME: str
    LOG_LEVEL: str
    PROJECT_ID: str
    PUBLISH_SCHEMA_TOPIC_ID: str
    SURVEY_MAP_URL: str
    FIRESTORE_DB_NAME: str
    SDS_APPLICATION_VERSION: str


class ServiceEmulatorDevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self.FIRESTORE_EMULATOR_HOST = get_value_from_env("FIRESTORE_EMULATOR_HOST")
        self.STORAGE_EMULATOR_HOST = get_value_from_env("STORAGE_EMULATOR_HOST")
        self.PUBSUB_EMULATOR_HOST = get_value_from_env("PUBSUB_EMULATOR_HOST")
        self.FIRESTORE_DB_NAME = "(default)"

    FIRESTORE_EMULATOR_HOST: str
    STORAGE_EMULATOR_HOST: str
    PUBSUB_EMULATOR_HOST: str
    FIRESTORE_DB_NAME: str


class CloudDevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self.GOOGLE_APPLICATION_CREDENTIALS = get_value_from_env(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )

    GOOGLE_APPLICATION_CREDENTIALS: str


class UnitTestingConfig(Config):
    def __init__(self):
        super().__init__()
        self.TEST_SCHEMA_PATH = get_value_from_env("TEST_SCHEMA_PATH")

    TEST_SCHEMA_PATH: str

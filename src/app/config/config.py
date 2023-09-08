from config.config_helpers import get_value_from_env
from pydantic import BaseSettings

TIME_FORMAT_STRING = "%Y-%m-%dT%H:%M:%SZ"


class Config(BaseSettings):
    def __init__(self):
        super().__init__()
        self.CONF = get_value_from_env("CONF")
        self.TIME_FORMAT = TIME_FORMAT_STRING
        self.DATASET_BUCKET_NAME = get_value_from_env("DATASET_BUCKET_NAME")
        self.SCHEMA_BUCKET_NAME = get_value_from_env("SCHEMA_BUCKET_NAME")
        self.AUTODELETE_DATASET_BUCKET_FILE = get_value_from_env(
            "AUTODELETE_DATASET_BUCKET_FILE"
        )
        self.RETAIN_DATASET_FIRESTORE = get_value_from_env(
            "RETAIN_DATASET_FIRESTORE"
        )
        self.LOG_LEVEL = get_value_from_env("LOG_LEVEL")
        self.PROJECT_ID = get_value_from_env("PROJECT_ID")
        self.PUBLISH_SCHEMA_TOPIC_ID = get_value_from_env("PUBLISH_SCHEMA_TOPIC_ID")
        self.PUBLISH_DATASET_TOPIC_ID = get_value_from_env("PUBLISH_DATASET_TOPIC_ID")

    CONF: str
    TIME_FORMAT: str = TIME_FORMAT_STRING
    DATASET_BUCKET_NAME: str
    SCHEMA_BUCKET_NAME: str
    AUTODELETE_DATASET_BUCKET_FILE: bool
    RETAIN_DATASET_FIRESTORE: bool
    LOG_LEVEL: str
    PROJECT_ID: str
    PUBLISH_SCHEMA_TOPIC_ID: str
    PUBLISH_DATASET_TOPIC_ID: str


class IntegrationTestConfig(BaseSettings):
    def __init__(self):
        super().__init__()
        self.CONF = get_value_from_env("CONF")
        self.TIME_FORMAT = TIME_FORMAT_STRING
        self.DATASET_BUCKET_NAME = get_value_from_env(
            "DATASET_BUCKET_NAME", "test_dataset_bucket"
        )
        self.SCHEMA_BUCKET_NAME = get_value_from_env(
            "SCHEMA_BUCKET_NAME", "test_schema_bucket"
        )
        self.AUTODELETE_DATASET_BUCKET_FILE = get_value_from_env(
            "AUTODELETE_DATASET_BUCKET_FILE"
        )
        self.RETAIN_DATASET_FIRESTORE = get_value_from_env(
            "RETAIN_DATASET_FIRESTORE"
        )
        self.TEST_DATASET_PATH = get_value_from_env(
            "TEST_DATASET_PATH", "src/test_data/json/dataset.json"
        )
        self.TEST_SCHEMA_PATH = get_value_from_env(
            "TEST_SCHEMA_PATH", "src/test_data/json/schema.json"
        )
        self.GOOGLE_APPLICATION_CREDENTIALS = get_value_from_env(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )
        self.PROJECT_ID = get_value_from_env("PROJECT_ID")
        self.PUBLISH_SCHEMA_TOPIC_ID = get_value_from_env("PUBLISH_SCHEMA_TOPIC_ID")
        self.PUBLISH_DATASET_TOPIC_ID = get_value_from_env("PUBLISH_DATASET_TOPIC_ID")
        self.API_URL = get_value_from_env("API_URL", "localhost")
        self.OAUTH_CLIENT_ID = get_value_from_env("OAUTH_CLIENT_ID", "localhost")

    CONF: str
    TIME_FORMAT: str = TIME_FORMAT_STRING
    DATASET_BUCKET_NAME: str
    SCHEMA_BUCKET_NAME: str
    AUTODELETE_DATASET_BUCKET_FILE: bool
    RETAIN_DATASET_FIRESTORE: bool
    TEST_DATASET_PATH: str
    TEST_SCHEMA_PATH: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    PROJECT_ID: str
    PUBLISH_SCHEMA_TOPIC_ID: str
    PUBLISH_DATASET_TOPIC_ID: str
    API_URL: str
    OAUTH_CLIENT_ID: str


class IntegrationTestCloudbuildConfig(BaseSettings):
    def __init__(self):
        super().__init__()
        self.CONF = get_value_from_env("CONF")
        self.TIME_FORMAT = TIME_FORMAT_STRING
        self.DATASET_BUCKET_NAME = get_value_from_env(
            "DATASET_BUCKET_NAME", "testDatasetBucket"
        )
        self.SCHEMA_BUCKET_NAME = get_value_from_env(
            "SCHEMA_BUCKET_NAME", "testSchemaBucket"
        )
        self.AUTODELETE_DATASET_BUCKET_FILE = get_value_from_env(
            "AUTODELETE_DATASET_BUCKET_FILE"
        )
        self.RETAIN_DATASET_FIRESTORE = get_value_from_env(
            "RETAIN_DATASET_FIRESTORE"
        )
        self.TEST_DATASET_PATH = get_value_from_env(
            "TEST_DATASET_PATH", "src/test_data/json/dataset.json"
        )
        self.TEST_SCHEMA_PATH = get_value_from_env(
            "TEST_SCHEMA_PATH", "src/test_data/json/schema.json"
        )
        self.PROJECT_ID = get_value_from_env("PROJECT_ID")
        self.PUBLISH_SCHEMA_TOPIC_ID = get_value_from_env("PUBLISH_SCHEMA_TOPIC_ID")
        self.PUBLISH_DATASET_TOPIC_ID = get_value_from_env("PUBLISH_DATASET_TOPIC_ID")
        self.API_URL = get_value_from_env("API_URL", "localhost")
        self.OAUTH_CLIENT_ID = get_value_from_env("OAUTH_CLIENT_ID", "localhost")

    CONF: str
    TIME_FORMAT: str = TIME_FORMAT_STRING
    DATASET_BUCKET_NAME: str
    SCHEMA_BUCKET_NAME: str
    AUTODELETE_DATASET_BUCKET_FILE: bool
    RETAIN_DATASET_FIRESTORE: bool
    TEST_DATASET_PATH: str
    TEST_SCHEMA_PATH: str
    PROJECT_ID: str
    PUBLISH_SCHEMA_TOPIC_ID: str
    PUBLISH_DATASET_TOPIC_ID: str
    API_URL: str
    OAUTH_CLIENT_ID: str


class CloudBuildConfig(BaseSettings):
    def __init__(self):
        super().__init__()
        self.CONF = get_value_from_env("CONF")
        self.TIME_FORMAT = TIME_FORMAT_STRING
        self.SCHEMA_BUCKET_NAME = get_value_from_env("SCHEMA_BUCKET_NAME")
        self.DATASET_BUCKET_NAME = get_value_from_env("DATASET_BUCKET_NAME")
        self.AUTODELETE_DATASET_BUCKET_FILE = get_value_from_env(
            "AUTODELETE_DATASET_BUCKET_FILE"
        )
        self.RETAIN_DATASET_FIRESTORE = get_value_from_env(
            "RETAIN_DATASET_FIRESTORE"
        )
        self.LOG_LEVEL = get_value_from_env("LOG_LEVEL")
        self.PROJECT_ID = get_value_from_env("PROJECT_ID")
        self.PUBLISH_SCHEMA_TOPIC_ID = get_value_from_env("PUBLISH_SCHEMA_TOPIC_ID")
        self.PUBLISH_DATASET_TOPIC_ID = get_value_from_env("PUBLISH_DATASET_TOPIC_ID")

    CONF: str
    TIME_FORMAT: str = TIME_FORMAT_STRING
    SCHEMA_BUCKET_NAME: str
    DATASET_BUCKET_NAME: str
    AUTODELETE_DATASET_BUCKET_FILE: bool
    RETAIN_DATASET_FIRESTORE: bool
    LOG_LEVEL: str
    PROJECT_ID: str
    PUBLISH_SCHEMA_TOPIC_ID: str
    PUBLISH_DATASET_TOPIC_ID: str


class ServiceEmulatorDevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self.FIRESTORE_EMULATOR_HOST = get_value_from_env("FIRESTORE_EMULATOR_HOST")
        self.STORAGE_EMULATOR_HOST = get_value_from_env("STORAGE_EMULATOR_HOST")
        self.PUBSUB_EMULATOR_HOST = get_value_from_env("PUBSUB_EMULATOR_HOST")

    FIRESTORE_EMULATOR_HOST: str
    STORAGE_EMULATOR_HOST: str
    PUBSUB_EMULATOR_HOST: str


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
        self.TEST_DATASET_PATH = get_value_from_env("TEST_DATASET_PATH")
        self.TEST_SCHEMA_PATH = get_value_from_env("TEST_SCHEMA_PATH")

    TEST_DATASET_PATH: str
    TEST_SCHEMA_PATH: str

from config.config_helpers import get_value_from_env
from pydantic import BaseSettings


class Config(BaseSettings):
    def __init__(self):
        super().__init__()
        self.CONF = get_value_from_env("CONF")
        self.TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
        self.DATASET_BUCKET_NAME = get_value_from_env("DATASET_BUCKET_NAME")
        self.AUTODELETE_DATASET_BUCKET_FILE = get_value_from_env(
            "AUTODELETE_DATASET_BUCKET_FILE"
        )
        self.LOG_LEVEL = get_value_from_env("LOG_LEVEL")

    CONF: str
    TIME_FORMAT: str = "%Y-%m-%dT%H:%M:%SZ"
    DATASET_BUCKET_NAME: str
    AUTODELETE_DATASET_BUCKET_FILE: bool
    LOG_LEVEL: str


class CloudBuildConfig(BaseSettings):
    def __init__(self):
        super().__init__()
        self.CONF = get_value_from_env("CONF")
        self.TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
        self.SCHEMA_BUCKET_NAME = get_value_from_env("SCHEMA_BUCKET_NAME")
        self.AUTODELETE_DATASET_BUCKET_FILE = get_value_from_env(
            "AUTODELETE_DATASET_BUCKET_FILE"
        )
        self.LOG_LEVEL = get_value_from_env("LOG_LEVEL")

    CONF: str
    TIME_FORMAT: str = "%Y-%m-%dT%H:%M:%SZ"
    SCHEMA_BUCKET_NAME: str
    AUTODELETE_DATASET_BUCKET_FILE: bool
    LOG_LEVEL: str


class ServiceEmulatorDevelopementConfig(Config):
    def __init__(self):
        super().__init__()
        self.FIRESTORE_EMULATOR_HOST = get_value_from_env("FIRESTORE_EMULATOR_HOST")
        self.STORAGE_EMULATOR_HOST = get_value_from_env("STORAGE_EMULATOR_HOST")
        self.SCHEMA_BUCKET_NAME = get_value_from_env("SCHEMA_BUCKET_NAME")

    SCHEMA_BUCKET_NAME: str
    FIRESTORE_EMULATOR_HOST: str
    STORAGE_EMULATOR_HOST: str


class CloudDevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self.SCHEMA_BUCKET_NAME = get_value_from_env("SCHEMA_BUCKET_NAME")
        self.GOOGLE_APPLICATION_CREDENTIALS = get_value_from_env(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )

    SCHEMA_BUCKET_NAME: str
    GOOGLE_APPLICATION_CREDENTIALS: str


class TestingConfig(Config):
    def __init__(self):
        super().__init__()
        self.TEST_DATASET_PATH = get_value_from_env("TEST_DATASET_PATH")
        self.TEST_SCHEMA_PATH = get_value_from_env("TEST_SCHEMA_PATH")

    TEST_DATASET_PATH: str
    TEST_SCHEMA_PATH: str


class IntegrationTestingRemoteCloudConfig(TestingConfig):
    def __init__(self):
        super().__init__()
        self.API_URL = get_value_from_env("API_URL")
        self.SCHEMA_BUCKET_NAME = get_value_from_env("SCHEMA_BUCKET_NAME")

    SCHEMA_BUCKET_NAME: str
    API_URL: str


class IntegrationTestingLocalCloudConfig(TestingConfig):
    def __init__(self):
        super().__init__()
        self.API_URL = get_value_from_env("API_URL")
        self.GOOGLE_APPLICATION_CREDENTIALS = get_value_from_env(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )

    API_URL: str
    GOOGLE_APPLICATION_CREDENTIALS: str


class IntegrationTestingLocalSDSConfig(TestingConfig):
    def __init__(self):
        super().__init__()
        self.GOOGLE_APPLICATION_CREDENTIALS = get_value_from_env(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )
        self.SCHEMA_BUCKET_NAME = get_value_from_env("SCHEMA_BUCKET_NAME")

    SCHEMA_BUCKET_NAME: str
    GOOGLE_APPLICATION_CREDENTIALS: str


class IntegrationTestingLocalConfig(TestingConfig):
    def __init__(self):
        super().__init__()
        self.FIRESTORE_EMULATOR_HOST = get_value_from_env("FIRESTORE_EMULATOR_HOST")
        self.STORAGE_EMULATOR_HOST = get_value_from_env("STORAGE_EMULATOR_HOST")

    FIRESTORE_EMULATOR_HOST: str
    STORAGE_EMULATOR_HOST: str


class UnitTestingConfig(TestingConfig):
    def __init__(self):
        super().__init__()
        self.SCHEMA_BUCKET_NAME = get_value_from_env("SCHEMA_BUCKET_NAME")

    SCHEMA_BUCKET_NAME: str

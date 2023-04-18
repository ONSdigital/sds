import os

from pydantic import BaseSettings


def get_value_from_env(env_value, default_value="") -> str:
    """
    Method to determine if a desired enviroment variable has been set and return it.
    If an enviroment variable or default value are not set an expection is raised.

    Parameters:
        env_value: value to check environment for
        default_value: optional argument to allow defaulting of values

    Returns:
        str: the environment value corresponding to the input
    """
    value = os.environ.get(env_value)
    if value:
        return value
    elif default_value != "":
        return default_value
    else:
        raise Exception(f"The environment variable {env_value} must be set to proceed")


try:
    CONF = get_value_from_env("CONF")
except Exception:
    CONF = "default"


class Config(BaseSettings):
    def __init__(self):
        super().__init__()
        self.CONF = get_value_from_env("CONF")
        self.TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
        self.DATASET_BUCKET_NAME = get_value_from_env("DATASET_BUCKET_NAME")

    CONF: str
    TIME_FORMAT: str = "%Y-%m-%dT%H:%M:%SZ"
    DATASET_BUCKET_NAME: str


class CloudBuildConfig(BaseSettings):
    def __init__(self):
        super().__init__()
        self.CONF = get_value_from_env("CONF")
        self.TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
        self.SCHEMA_BUCKET_NAME = get_value_from_env("SCHEMA_BUCKET_NAME")

    CONF: str
    TIME_FORMAT: str = "%Y-%m-%dT%H:%M:%SZ"
    SCHEMA_BUCKET_NAME: str


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


match CONF:
    case "docker-dev":
        config = ServiceEmulatorDevelopementConfig()
    case "cloud-dev":
        config = CloudDevelopmentConfig()
    case "IntegrationTestingLocalSDS":
        config = IntegrationTestingLocalSDSConfig()
    case "IntegrationTestingCloud":
        config = IntegrationTestingLocalCloudConfig()
    case "IntegrationTestingDocker":
        config = IntegrationTestingLocalConfig()
    case "unit":
        config = UnitTestingConfig()
    case "cloud-build":
        config = CloudBuildConfig()
    case "cloud-intergration-test":
        config = IntegrationTestingRemoteCloudConfig()
    case "default":
        config = Config()

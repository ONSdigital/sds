from app.config.config import (
    CloudBuildConfig,
    CloudDevelopmentConfig,
    Config,
    IntegrationTestCloudbuildConfig,
    IntegrationTestConfig,
    ServiceEmulatorDevelopmentConfig,
    UnitTestingConfig,
)
from app.config.config_helpers import get_value_from_env


class ConfigFactory:
    def get_config():
        env_conf = get_value_from_env("CONF")

        config_mapping = {
            "docker-dev": ServiceEmulatorDevelopmentConfig,
            "cloud-dev": CloudDevelopmentConfig,
            "unit": UnitTestingConfig,
            "cloud-build": CloudBuildConfig,
            "int-test": IntegrationTestConfig,
            "int-test-cloudbuild": IntegrationTestCloudbuildConfig,
        }

        return config_mapping.get(env_conf, Config)()


config = ConfigFactory.get_config()

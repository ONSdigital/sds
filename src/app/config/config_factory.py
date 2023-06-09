from config.config import (
    CloudBuildConfig,
    CloudDevelopmentConfig,
    Config,
    IntegrationTestCloudbuildConfig,
    IntegrationTestConfig,
    ServiceEmulatorDevelopmentConfig,
    UnitTestingConfig,
)
from config.config_helpers import get_value_from_env


class ConfigFactory:
    def get_config():
        env_conf = get_value_from_env("CONF")

        match env_conf:
            case "docker-dev":
                return ServiceEmulatorDevelopmentConfig()
            case "cloud-dev":
                return CloudDevelopmentConfig()
            case "unit":
                return UnitTestingConfig()
            case "cloud-build":
                return CloudBuildConfig()
            case "int-test":
                return IntegrationTestConfig()
            case "int-test-cloudbuild":
                return IntegrationTestCloudbuildConfig()
            case "default":
                return Config()


config = ConfigFactory.get_config()

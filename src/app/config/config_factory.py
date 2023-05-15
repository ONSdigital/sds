from config.config import (
    CloudBuildConfig,
    CloudDevelopmentConfig,
    Config,
    IntegrationTests,
    ServiceEmulatorDevelopementConfig,
    UnitTestingConfig,
)
from config.config_helpers import get_value_from_env


class ConfigFactory:
    def get_config():
        env_conf = get_value_from_env("CONF")

        match env_conf:
            case "docker-dev":
                return ServiceEmulatorDevelopementConfig()
            case "cloud-dev":
                return CloudDevelopmentConfig()
            case "unit":
                return UnitTestingConfig()
            case "cloud-build":
                return CloudBuildConfig()
            case "int-test":
                return IntegrationTests()
            case "default":
                return Config()

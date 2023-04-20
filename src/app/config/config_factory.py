from src.app.config.config import (
    CloudBuildConfig,
    CloudDevelopmentConfig,
    Config,
    IntegrationTestingLocalCloudConfig,
    IntegrationTestingLocalConfig,
    IntegrationTestingLocalSDSConfig,
    IntegrationTestingRemoteCloudConfig,
    ServiceEmulatorDevelopementConfig,
    UnitTestingConfig,
)
from src.app.config.config_helpers import get_value_from_env


class ConfigFactory:
    def get_config():
        env_conf = get_value_from_env("CONF")

        match env_conf:
            case "docker-dev":
                return ServiceEmulatorDevelopementConfig()
            case "cloud-dev":
                return CloudDevelopmentConfig()
            case "IntegrationTestingLocalSDS":
                return IntegrationTestingLocalSDSConfig()
            case "IntegrationTestingCloud":
                return IntegrationTestingLocalCloudConfig()
            case "IntegrationTestingDocker":
                return IntegrationTestingLocalConfig()
            case "unit":
                return UnitTestingConfig()
            case "cloud-build":
                return CloudBuildConfig()
            case "cloud-integration-test":
                return IntegrationTestingRemoteCloudConfig()
            case "default":
                return Config()

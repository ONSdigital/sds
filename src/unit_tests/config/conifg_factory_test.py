import os

from config.config import (
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
from config.config_factory import ConfigFactory


def test_docker_dev_factory():
    os.environ["CONF"] = "docker-dev"

    assert ConfigFactory.get_config() == ServiceEmulatorDevelopementConfig()
    del os.environ["CONF"]


def test_cloud_dev_factory():
    os.environ["CONF"] = "cloud-dev"

    assert ConfigFactory.get_config() == CloudDevelopmentConfig()
    del os.environ["CONF"]


def test_integration_localSDS_factory():
    os.environ["CONF"] = "int-test-localSDS"

    assert ConfigFactory.get_config() == IntegrationTestingLocalSDSConfig()
    del os.environ["CONF"]


def test_cloud_integration_local_factory():
    os.environ["CONF"] = "cloud-int-test-local"

    assert ConfigFactory.get_config() == IntegrationTestingLocalCloudConfig()
    del os.environ["CONF"]


def test_docker_integration_factory():
    os.environ["CONF"] = "int-test-docker"

    assert ConfigFactory.get_config() == IntegrationTestingLocalConfig()
    del os.environ["CONF"]


def test_unit_factory():
    os.environ["CONF"] = "unit"

    assert ConfigFactory.get_config() == UnitTestingConfig()
    del os.environ["CONF"]


def test_cloud_build_factory():
    os.environ["CONF"] = "cloud-build"

    assert ConfigFactory.get_config() == CloudBuildConfig()
    del os.environ["CONF"]


def test_cloud_integration_remote_factory():
    os.environ["CONF"] = "cloud-int-test-remote"

    assert ConfigFactory.get_config() == IntegrationTestingRemoteCloudConfig()
    del os.environ["CONF"]


def test_default_factory():
    os.environ["CONF"] = "default"

    assert ConfigFactory.get_config() == Config()
    del os.environ["CONF"]

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

from src.unit_tests.config.config_test import testConfigVars


def teardown():
    os.environ["CONF"] = "unit"


def setup():
    os.environ["CONF"] = testConfigVars.conf
    os.environ["DATASET_BUCKET_NAME"] = testConfigVars.datset_bucket_name
    os.environ["TEST_DATASET_PATH"] = testConfigVars.dataset_path
    os.environ["TEST_SCHEMA_PATH"] = testConfigVars.schema_path
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = testConfigVars.app_credentials
    os.environ["FIRESTORE_EMULATOR_HOST"] = testConfigVars.firestore_host
    os.environ["STORAGE_EMULATOR_HOST"] = testConfigVars.storage_host
    os.environ["SCHEMA_BUCKET_NAME"] = testConfigVars.schema_bucket_name
    os.environ["API_URL"] = testConfigVars.api_url


def test_docker_dev_factory():
    os.environ["CONF"] = "docker-dev"

    assert ConfigFactory.get_config() == ServiceEmulatorDevelopementConfig()
    teardown()


def test_cloud_dev_factory():
    os.environ["CONF"] = "cloud-dev"

    assert ConfigFactory.get_config() == CloudDevelopmentConfig()
    teardown()


def test_integration_localSDS_factory():
    os.environ["CONF"] = "int-test-localSDS"

    assert ConfigFactory.get_config() == IntegrationTestingLocalSDSConfig()
    teardown()


def test_cloud_integration_local_factory():
    os.environ["CONF"] = "cloud-int-test-local"

    assert ConfigFactory.get_config() == IntegrationTestingLocalCloudConfig()
    teardown()


def test_docker_integration_factory():
    os.environ["CONF"] = "int-test-docker"

    assert ConfigFactory.get_config() == IntegrationTestingLocalConfig()
    teardown()


def test_unit_factory():
    os.environ["CONF"] = "unit"

    assert ConfigFactory.get_config() == UnitTestingConfig()
    teardown()


def test_cloud_build_factory():
    os.environ["CONF"] = "cloud-build"

    assert ConfigFactory.get_config() == CloudBuildConfig()
    teardown()


def test_cloud_integration_remote_factory():
    os.environ["CONF"] = "cloud-int-test-remote"

    assert ConfigFactory.get_config() == IntegrationTestingRemoteCloudConfig()
    teardown()


def test_default_factory():
    os.environ["CONF"] = "default"

    assert ConfigFactory.get_config() == Config()
    teardown()

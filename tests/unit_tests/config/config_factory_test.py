import os
from unittest import TestCase

from app.config.config import (
    CloudBuildConfig,
    CloudDevelopmentConfig,
    Config,
    IntegrationTestCloudbuildConfig,
    IntegrationTestConfig,
    ServiceEmulatorDevelopmentConfig,
    UnitTestingConfig,
)
from app.config.config_factory import ConfigFactory

from tests.unit_tests.config.config_test import testConfigVars

INITIAL_CONF = os.environ.get("CONF")
INITIAL_TEST_DATASET_PATH = os.environ.get("TEST_DATASET_PATH")
INITIAL_TEST_SCHEMA_PATH = os.environ.get("TEST_SCHEMA_PATH")


class ConfigFactoryTest(TestCase):
    def setUp(self):
        os.environ["CONF"] = testConfigVars.conf
        os.environ["TEST_SCHEMA_PATH"] = testConfigVars.schema_path
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = testConfigVars.app_credentials
        os.environ["FIRESTORE_EMULATOR_HOST"] = testConfigVars.firestore_host
        os.environ["STORAGE_EMULATOR_HOST"] = testConfigVars.storage_host
        os.environ["PUBSUB_EMULATOR_HOST"] = testConfigVars.pubsub_emulator_host
        os.environ["SCHEMA_BUCKET_NAME"] = testConfigVars.schema_bucket_name
        os.environ["API_URL"] = testConfigVars.api_url
        os.environ["OAUTH_CLIENT_ID"] = testConfigVars.oauth_client_id
        os.environ["SURVEY_MAP_URL"] = testConfigVars.survey_map_url

    def tearDown(self):
        os.environ["CONF"] = INITIAL_CONF
        os.environ["TEST_SCHEMA_PATH"] = INITIAL_TEST_SCHEMA_PATH
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""
        os.environ["FIRESTORE_EMULATOR_HOST"] = ""
        os.environ["STORAGE_EMULATOR_HOST"] = ""
        os.environ["SCHEMA_BUCKET_NAME"] = ""
        os.environ["API_URL"] = ""
        os.environ["OAUTH_CLIENT_ID"] = ""
        os.environ["SURVEY_MAP_URL"] = ""

    def test_docker_dev_factory(self):
        os.environ["CONF"] = "docker-dev"

        assert ConfigFactory.get_config() == ServiceEmulatorDevelopmentConfig()

    def test_cloud_dev_factory(self):
        os.environ["CONF"] = "cloud-dev"

        assert ConfigFactory.get_config() == CloudDevelopmentConfig()

    def test_unit_factory(self):
        os.environ["CONF"] = "unit"

        assert ConfigFactory.get_config() == UnitTestingConfig()

    def test_cloud_build_factory(self):
        os.environ["CONF"] = "cloud-build"

        assert ConfigFactory.get_config() == CloudBuildConfig()

    def test_integration_factory(self):
        os.environ["CONF"] = "int-test"

        assert ConfigFactory.get_config() == IntegrationTestConfig()

    def test_integration_cloud_factory(self):
        os.environ["CONF"] = "int-test-cloudbuild"

        assert ConfigFactory.get_config() == IntegrationTestCloudbuildConfig()

    def test_default_factory(self):
        os.environ["CONF"] = "default"

        assert ConfigFactory.get_config() == Config()

import os
from unittest import TestCase

from config.config import (
    CloudBuildConfig,
    CloudDevelopmentConfig,
    Config,
    ServiceEmulatorDevelopementConfig,
    UnitTestingConfig,
)
from config.config_factory import ConfigFactory

from src.unit_tests.config.config_test import testConfigVars

INITIAL_CONF = os.environ.get("CONF")
INITIAL_DATASET_BUCKET_NAME = os.environ.get("DATASET_BUCKET_NAME")
INITIAL_TEST_DATASET_PATH = os.environ.get("TEST_DATASET_PATH")
INITIAL_TEST_SCHEMA_PATH = os.environ.get("TEST_SCHEMA_PATH")
INITIAL_GOOGLE_APPLICATION_CREDENTIALS = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS"
)
INITIAL_FIRESTORE_EMULATOR_HOST = os.environ.get("FIRESTORE_EMULATOR_HOST")
INITIAL_STORAGE_EMULATOR_HOST = os.environ.get("STORAGE_EMULATOR_HOST")
INITIAL_SCHEMA_BUCKET_NAME = os.environ.get("SCHEMA_BUCKET_NAME")
INITIAL_API_URL = os.environ.get("API_URL")


class ConfigFactoryTest(TestCase):
    def setUp(self):
        os.environ["CONF"] = testConfigVars.conf
        os.environ["DATASET_BUCKET_NAME"] = testConfigVars.datset_bucket_name
        os.environ["TEST_DATASET_PATH"] = testConfigVars.dataset_path
        os.environ["TEST_SCHEMA_PATH"] = testConfigVars.schema_path
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = testConfigVars.app_credentials
        os.environ["FIRESTORE_EMULATOR_HOST"] = testConfigVars.firestore_host
        os.environ["STORAGE_EMULATOR_HOST"] = testConfigVars.storage_host
        os.environ["SCHEMA_BUCKET_NAME"] = testConfigVars.schema_bucket_name
        os.environ["API_URL"] = testConfigVars.api_url

    def tearDown(self):
        os.environ["CONF"] = INITIAL_CONF
        os.environ["DATASET_BUCKET_NAME"] = INITIAL_DATASET_BUCKET_NAME
        os.environ["TEST_DATASET_PATH"] = INITIAL_TEST_DATASET_PATH
        os.environ["TEST_SCHEMA_PATH"] = INITIAL_TEST_SCHEMA_PATH
        os.environ[
            "GOOGLE_APPLICATION_CREDENTIALS"
        ] = INITIAL_GOOGLE_APPLICATION_CREDENTIALS
        os.environ["FIRESTORE_EMULATOR_HOST"] = INITIAL_FIRESTORE_EMULATOR_HOST
        os.environ["STORAGE_EMULATOR_HOST"] = INITIAL_STORAGE_EMULATOR_HOST
        os.environ["SCHEMA_BUCKET_NAME"] = INITIAL_SCHEMA_BUCKET_NAME
        os.environ["API_URL"] = INITIAL_API_URL

    def test_docker_dev_factory(self):
        os.environ["CONF"] = "docker-dev"

        assert ConfigFactory.get_config() == ServiceEmulatorDevelopementConfig()

    def test_cloud_dev_factory(self):
        os.environ["CONF"] = "cloud-dev"

        assert ConfigFactory.get_config() == CloudDevelopmentConfig()

    def test_unit_factory(self):
        os.environ["CONF"] = "unit"

        assert ConfigFactory.get_config() == UnitTestingConfig()

    def test_cloud_build_factory(self):
        os.environ["CONF"] = "cloud-build"

        assert ConfigFactory.get_config() == CloudBuildConfig()

    def test_default_factory(self):
        os.environ["CONF"] = "default"

        assert ConfigFactory.get_config() == Config()

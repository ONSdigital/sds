import os
from unittest import TestCase

from app.config import config


class testConfigVars:
    conf = "unit"
    schema_bucket_name = "test_schema_bucket_name"
    firestore_host = "test_firestore_emulator_host"
    storage_host = "test_storage_emulator_host"
    pubsub_emulator_host = "test_pubsub_emulator_host"
    app_credentials = "test_app_credentials"
    schema_path = "test_schema_path"
    api_url = "test_api_url"
    oauth_client_id = "test_oauth_client_id"
    survey_map_url = "test_survey_map_url"


class ConfigTest(TestCase):
    def test_get_value_from_env(self):
        """
        Test that when an enviroment variable has been set the function works as expected.
        """
        os.environ["test"] = "test123"

        env_value = config.get_value_from_env("test")

        assert env_value == "test123"
        del os.environ["test"]

    def test_get_value_from_env_default(self):
        """
        Test that when a default variable has been set the function works as expected.
        """
        test_value = "default test value"
        env_value = config.get_value_from_env("test", test_value)

        assert env_value == test_value

    def test_get_value_from_env_exception(self):
        """
        Test that when nothing has been set the function returns the expected exception.
        """
        try:
            config.get_value_from_env("test")
        except Exception as e:
            assert str(e).__contains__("test")

    def test_get_bool_value_from_env(self):
        """
        Test that when the env value is a boolean it casts correctly.
        """
        bool_env_test_cases = {
            "true": True,
            "True": True,
            "tRuE": True,
            "false": False,
            "False": False,
            "fAlSe": False,
        }

        for key, value in bool_env_test_cases.items():
            os.environ["test"] = key

            assert config.get_value_from_env("test") is value
            del os.environ["test"]

    def test_set_Config(self):
        """
        Test that setting the default config object works as intended.
        """
        os.environ["CONF"] = testConfigVars.conf

        testConfig = config.Config()

        os.environ["CONF"] = "unit"

        assert (
            testConfigVars.conf == testConfig.CONF
            and testConfig.TIME_FORMAT == "%Y-%m-%dT%H:%M:%SZ"
        )

    def test_set_CloudBuildConfig(self):
        """
        Test that setting the cloud build config object works as intended.
        """
        os.environ["CONF"] = testConfigVars.conf
        os.environ["SCHEMA_BUCKET_NAME"] = testConfigVars.schema_bucket_name

        testConfig = config.CloudBuildConfig()

        assert (
            testConfigVars.conf == testConfig.CONF
            and testConfig.TIME_FORMAT == "%Y-%m-%dT%H:%M:%SZ"
            and testConfigVars.schema_bucket_name == testConfig.SCHEMA_BUCKET_NAME
        )

    def test_set_ServiceEmulatorDevelopementConfig(self):
        """
        Test that setting the service emulator for development config object works as intended.
        """
        os.environ["CONF"] = testConfigVars.conf
        os.environ["SCHEMA_BUCKET_NAME"] = testConfigVars.schema_bucket_name
        os.environ["FIRESTORE_EMULATOR_HOST"] = testConfigVars.firestore_host
        os.environ["STORAGE_EMULATOR_HOST"] = testConfigVars.storage_host

        testConfig = config.ServiceEmulatorDevelopmentConfig()

        assert (
            testConfigVars.conf == testConfig.CONF
            and testConfig.TIME_FORMAT == "%Y-%m-%dT%H:%M:%SZ"
            and testConfigVars.schema_bucket_name == testConfig.SCHEMA_BUCKET_NAME
            and testConfigVars.firestore_host == testConfig.FIRESTORE_EMULATOR_HOST
            and testConfigVars.storage_host == testConfig.STORAGE_EMULATOR_HOST
        )

    def test_set_CloudDevelopmentConfig(self):
        """
        Test that setting the cloud development config object works as intended.
        """
        os.environ["CONF"] = testConfigVars.conf
        os.environ["SCHEMA_BUCKET_NAME"] = testConfigVars.schema_bucket_name
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = testConfigVars.app_credentials

        testConfig = config.CloudDevelopmentConfig()

        assert (
            testConfigVars.conf == testConfig.CONF
            and testConfig.TIME_FORMAT == "%Y-%m-%dT%H:%M:%SZ"
            and testConfigVars.schema_bucket_name == testConfig.SCHEMA_BUCKET_NAME
            and testConfigVars.app_credentials
            == testConfig.GOOGLE_APPLICATION_CREDENTIALS
        )

    def test_set_UnitTestingConfig(self):
        """
        Test that setting the unit testing config object works as intended.
        """
        os.environ["CONF"] = testConfigVars.conf
        os.environ["TEST_SCHEMA_PATH"] = testConfigVars.schema_path
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = testConfigVars.app_credentials
        os.environ["SCHEMA_BUCKET_NAME"] = testConfigVars.schema_bucket_name

        testConfig = config.UnitTestingConfig()

        assert (
            testConfigVars.conf == testConfig.CONF
            and testConfig.TIME_FORMAT == "%Y-%m-%dT%H:%M:%SZ"
            and testConfigVars.schema_path == testConfig.TEST_SCHEMA_PATH
            and testConfigVars.schema_bucket_name == testConfig.SCHEMA_BUCKET_NAME
        )

    def test_set_IntegrationTestConfig(self):
        """
        Test that setting the unit testing config object works as intended.
        """
        os.environ["CONF"] = testConfigVars.conf
        os.environ["SCHEMA_BUCKET_NAME"] = testConfigVars.schema_bucket_name
        os.environ["TEST_SCHEMA_PATH"] = testConfigVars.schema_path
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = testConfigVars.app_credentials

        testConfig = config.IntegrationTestConfig()

        assert (
            testConfigVars.conf == testConfig.CONF
            and testConfig.TIME_FORMAT == "%Y-%m-%dT%H:%M:%SZ"
            and testConfigVars.schema_path == testConfig.TEST_SCHEMA_PATH
            and testConfigVars.schema_bucket_name == testConfig.SCHEMA_BUCKET_NAME
            and testConfigVars.app_credentials
            == testConfig.GOOGLE_APPLICATION_CREDENTIALS
        )

    def test_set_IntegrationTestCloudBuildConfig(self):
        """
        Test that setting the unit testing config object works as intended.
        """
        os.environ["CONF"] = testConfigVars.conf
        os.environ["SCHEMA_BUCKET_NAME"] = testConfigVars.schema_bucket_name
        os.environ["TEST_SCHEMA_PATH"] = testConfigVars.schema_path

        testConfig = config.IntegrationTestCloudbuildConfig()

        assert (
            testConfigVars.conf == testConfig.CONF
            and testConfigVars.schema_path == testConfig.TEST_SCHEMA_PATH
            and testConfigVars.schema_bucket_name == testConfig.SCHEMA_BUCKET_NAME
        )

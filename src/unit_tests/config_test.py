import os

import config


def test_get_value_from_env():
    """
    Test that when an enviroment variable has been set the function works as expected.
    """
    os.environ["test"] = "test123"

    env_value = config.get_value_from_env("test")

    assert env_value == "test123"
    del os.environ["test"]


def test_get_value_from_env_default():
    """
    Test that when a default variable has been set the function works as expected.
    """
    test_value = "default test value"
    env_value = config.get_value_from_env("test", test_value)

    assert env_value == test_value


def test_get_value_from_env_exception():
    """
    Test that when nothing has been set the function returns the expected exception.
    """
    try:
        config.get_value_from_env("test")
    except Exception as e:
        assert str(e).__contains__("test")


class testConfigVars:
    conf = "testConf"
    datset_bucket_name = "testDatasetBucket"
    schema_bucket_name = "testSchemaBucketName"
    firestore_host = "testFirestoreEmulatorHost"
    storage_host = "testStorageEmulatorHost"
    app_credentials = "testAppCredentials"
    dataset_path = "testDatasetPath"
    schema_path = "testSchemaPath"
    api_url = "testAPIUrl"


def test_set_Config():
    """
    Test that setting the default config object works as intended.
    """
    os.environ["CONF"] = testConfigVars.conf
    os.environ["DATASET_BUCKET_NAME"] = testConfigVars.datset_bucket_name

    testConfig = config.Config()

    del os.environ["CONF"], os.environ["DATASET_BUCKET_NAME"]

    assert (
        testConfig.CONF == testConfigVars.conf
        and testConfig.TIME_FORMAT == "%Y-%m-%dT%H:%M:%SZ"
        and testConfig.DATASET_BUCKET_NAME == testConfigVars.datset_bucket_name
    )


def test_set_CloudBuildConfig():
    """
    Test that setting the cloud build config object works as intended.
    """
    os.environ["CONF"] = testConfigVars.conf
    os.environ["SCHEMA_BUCKET_NAME"] = testConfigVars.schema_bucket_name

    testConfig = config.CloudBuildConfig()

    assert (
        testConfig.CONF == testConfigVars.conf
        and testConfig.TIME_FORMAT == "%Y-%m-%dT%H:%M:%SZ"
        and testConfig.SCHEMA_BUCKET_NAME == testConfigVars.schema_bucket_name
    )


def test_set_ServiceEmulatorDevelopementConfig():
    """
    Test that setting the service emulator for development config object works as intended.
    """
    os.environ["CONF"] = testConfigVars.conf
    os.environ["DATASET_BUCKET_NAME"] = testConfigVars.datset_bucket_name
    os.environ["SCHEMA_BUCKET_NAME"] = testConfigVars.schema_bucket_name
    os.environ["FIRESTORE_EMULATOR_HOST"] = testConfigVars.firestore_host
    os.environ["STORAGE_EMULATOR_HOST"] = testConfigVars.storage_host

    testConfig = config.ServiceEmulatorDevelopementConfig()

    assert (
        testConfig.CONF == testConfigVars.conf
        and testConfig.TIME_FORMAT == "%Y-%m-%dT%H:%M:%SZ"
        and testConfig.DATASET_BUCKET_NAME == testConfigVars.datset_bucket_name
        and testConfig.SCHEMA_BUCKET_NAME == testConfigVars.schema_bucket_name
        and testConfig.FIRESTORE_EMULATOR_HOST == testConfigVars.firestore_host
        and testConfig.STORAGE_EMULATOR_HOST == testConfigVars.storage_host
    )


def test_set_CloudDevelopmentConfig():
    """
    Test that setting the cloud development config object works as intended.
    """
    os.environ["CONF"] = testConfigVars.conf
    os.environ["DATASET_BUCKET_NAME"] = testConfigVars.datset_bucket_name
    os.environ["SCHEMA_BUCKET_NAME"] = testConfigVars.schema_bucket_name
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = testConfigVars.app_credentials

    testConfig = config.CloudDevelopmentConfig()

    assert (
        testConfig.CONF == testConfigVars.conf
        and testConfig.TIME_FORMAT == "%Y-%m-%dT%H:%M:%SZ"
        and testConfig.DATASET_BUCKET_NAME == testConfigVars.datset_bucket_name
        and testConfig.SCHEMA_BUCKET_NAME == testConfigVars.schema_bucket_name
        and testConfig.GOOGLE_APPLICATION_CREDENTIALS == testConfigVars.app_credentials
    )


def test_set_TestingConfig():
    """
    Test that setting the testing config object works as intended.
    """
    os.environ["CONF"] = testConfigVars.conf
    os.environ["DATASET_BUCKET_NAME"] = testConfigVars.datset_bucket_name
    os.environ["TEST_DATASET_PATH"] = testConfigVars.dataset_path
    os.environ["TEST_SCHEMA_PATH"] = testConfigVars.schema_path

    testConfig = config.TestingConfig()

    assert (
        testConfig.CONF == testConfigVars.conf
        and testConfig.TIME_FORMAT == "%Y-%m-%dT%H:%M:%SZ"
        and testConfig.DATASET_BUCKET_NAME == testConfigVars.datset_bucket_name
        and testConfig.TEST_DATASET_PATH == testConfigVars.dataset_path
        and testConfig.TEST_SCHEMA_PATH == testConfigVars.schema_path
    )


def test_set_IntegrationTestingCloudConfig():
    """
    Test that setting the integration testing for cloud config object works as intended.
    """
    os.environ["CONF"] = testConfigVars.conf
    os.environ["DATASET_BUCKET_NAME"] = testConfigVars.datset_bucket_name
    os.environ["TEST_DATASET_PATH"] = testConfigVars.dataset_path
    os.environ["TEST_SCHEMA_PATH"] = testConfigVars.schema_path
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = testConfigVars.app_credentials
    os.environ["API_URL"] = testConfigVars.api_url

    testConfig = config.IntegrationTestingCloudConfig()

    assert (
        testConfig.CONF == testConfigVars.conf
        and testConfig.TIME_FORMAT == "%Y-%m-%dT%H:%M:%SZ"
        and testConfig.DATASET_BUCKET_NAME == testConfigVars.datset_bucket_name
        and testConfig.TEST_DATASET_PATH == testConfigVars.dataset_path
        and testConfig.TEST_SCHEMA_PATH == testConfigVars.schema_path
        and testConfig.GOOGLE_APPLICATION_CREDENTIALS == testConfigVars.app_credentials
        and testConfig.API_URL == testConfigVars.api_url
    )


def test_set_IntegrationTestingLocalSDSConfig():
    """
    Test that setting the integration testing for a local SDS instance config object works as intended.
    """
    os.environ["CONF"] = testConfigVars.conf
    os.environ["DATASET_BUCKET_NAME"] = testConfigVars.datset_bucket_name
    os.environ["TEST_DATASET_PATH"] = testConfigVars.dataset_path
    os.environ["TEST_SCHEMA_PATH"] = testConfigVars.schema_path
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = testConfigVars.app_credentials
    os.environ["SCHEMA_BUCKET_NAME"] = testConfigVars.schema_bucket_name

    testConfig = config.IntegrationTestingLocalSDSConfig()

    assert (
        testConfig.CONF == testConfigVars.conf
        and testConfig.TIME_FORMAT == "%Y-%m-%dT%H:%M:%SZ"
        and testConfig.DATASET_BUCKET_NAME == testConfigVars.datset_bucket_name
        and testConfig.TEST_DATASET_PATH == testConfigVars.dataset_path
        and testConfig.TEST_SCHEMA_PATH == testConfigVars.schema_path
        and testConfig.SCHEMA_BUCKET_NAME == testConfigVars.schema_bucket_name
    )


def test_set_IntegrationTestingLocalConfig():
    """
    Test that setting the integration testing for local config object works as intended.
    """
    os.environ["CONF"] = testConfigVars.conf
    os.environ["DATASET_BUCKET_NAME"] = testConfigVars.datset_bucket_name
    os.environ["TEST_DATASET_PATH"] = testConfigVars.dataset_path
    os.environ["TEST_SCHEMA_PATH"] = testConfigVars.schema_path
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = testConfigVars.app_credentials
    os.environ["FIRESTORE_EMULATOR_HOST"] = testConfigVars.firestore_host
    os.environ["STORAGE_EMULATOR_HOST"] = testConfigVars.storage_host

    testConfig = config.IntegrationTestingLocalConfig()

    assert (
        testConfig.CONF == testConfigVars.conf
        and testConfig.TIME_FORMAT == "%Y-%m-%dT%H:%M:%SZ"
        and testConfig.DATASET_BUCKET_NAME == testConfigVars.datset_bucket_name
        and testConfig.TEST_DATASET_PATH == testConfigVars.dataset_path
        and testConfig.TEST_SCHEMA_PATH == testConfigVars.schema_path
        and testConfig.FIRESTORE_EMULATOR_HOST == testConfigVars.firestore_host
        and testConfig.STORAGE_EMULATOR_HOST == testConfigVars.storage_host
    )


def test_set_UnitTestingConfig():
    """
    Test that setting the unit testing config object works as intended.
    """
    os.environ["CONF"] = testConfigVars.conf
    os.environ["DATASET_BUCKET_NAME"] = testConfigVars.datset_bucket_name
    os.environ["TEST_DATASET_PATH"] = testConfigVars.dataset_path
    os.environ["TEST_SCHEMA_PATH"] = testConfigVars.schema_path
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = testConfigVars.app_credentials
    os.environ["SCHEMA_BUCKET_NAME"] = testConfigVars.schema_bucket_name

    testConfig = config.UnitTestingConfig()

    assert (
        testConfig.CONF == testConfigVars.conf
        and testConfig.TIME_FORMAT == "%Y-%m-%dT%H:%M:%SZ"
        and testConfig.DATASET_BUCKET_NAME == testConfigVars.datset_bucket_name
        and testConfig.TEST_DATASET_PATH == testConfigVars.dataset_path
        and testConfig.TEST_SCHEMA_PATH == testConfigVars.schema_path
        and testConfig.SCHEMA_BUCKET_NAME == testConfigVars.schema_bucket_name
    )

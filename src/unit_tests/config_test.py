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
        env_value = config.get_value_from_env("test")
    except Exception as e:
        assert str(e).__contains__("test")

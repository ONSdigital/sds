import os

from pydantic import BaseSettings


def get_value_from_env(env_value, default_value="") -> str:
    """
    Method to determine if a desired enviroment variable has been set and return it.
    If an enviroment variable or default value are not set an expection is raised.

    Parameters:
        env_value: value to check environment for
        default_value: optional argument to allow defaulting of values

    Returns:
        str: the environment value corresponding to the input
    """
    value = os.environ.get(env_value)
    if value:
        return value
    elif default_value != "":
        return default_value
    else:
        raise Exception(f"The environment variable {env_value} must be set to proceed")


class Config(BaseSettings):
    def __init__(self):
        super().__init__()
        self.DATASET_BUCKET_NAME = get_value_from_env("DATASET_BUCKET_NAME")
        self.SCHEMA_BUCKET_NAME = get_value_from_env("SCHEMA_BUCKET_NAME")

    SCHEMA_BUCKET_NAME: str
    DATASET_BUCKET_NAME: str


class ConfigFactory:
    def get_config():
        return Config()
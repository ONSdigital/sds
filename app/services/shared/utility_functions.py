from app.config.config_factory import config


class UtilityFunctions:
    @staticmethod
    def get_application_version():
        return config.SDS_APPLICATION_VERSION

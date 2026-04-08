from app.config import settings


class UtilityFunctions:
    @staticmethod
    def get_application_version():
        return settings.SDS_APPLICATION_VERSION

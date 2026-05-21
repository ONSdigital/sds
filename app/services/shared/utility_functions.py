import requests

from app.config import settings


class UtilityFunctions:
    @staticmethod
    def get_application_version():
        return settings.SDS_APPLICATION_VERSION

    @staticmethod
    def request_survey_id_mapping() -> requests.Response:
        url = settings.SURVEY_MAP_URL

        response = requests.get(url=url, timeout=30)

        return response

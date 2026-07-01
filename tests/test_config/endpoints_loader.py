import os
from urllib.parse import quote, urlencode

from tests.test_config.endpoints import ENDPOINTS_DEPRECATED, EndpointConfig


class EndpointsLoader:
    endpoints: dict[str, EndpointConfig]
    endpoints_deprecated: bool

    def __init__(self, endpoints: dict[str, EndpointConfig]):
        """
        Load the endpoints config

        :param endpoints: dictionary containing the endpoint and the url and method for that endpoint
        """

        # Temporary logic to load deprecated endpoints if `ENDPOINTS_DEPRECATED` environment variable is set to "true".
        # This allows us to run tests against both the new and deprecated endpoints without needing to change the code in multiple places.
        # This logic can be removed once the deprecated endpoints are removed.
        if os.environ.get("ENDPOINTS_DEPRECATED") == "true":
            self.endpoints = ENDPOINTS_DEPRECATED
            self.endpoints_deprecated = True
        else:
            self.endpoints = endpoints
            self.endpoints_deprecated = False

    def send_request(self, client, key: str, params: dict[str, str]|None = None, body: dict[str, str]|str|None = None):
        url, method = self.formulate_url_and_method(key, params)

        if method == "GET":
            return client.get(url)
        elif method == "POST":
            return client.post(url, json=body)
        elif method == "PUT":
            return client.put(url, json=body)
        elif method == "DELETE":
            return client.delete(url)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

    def formulate_url_and_method(self, key: str, params: dict[str, str]|None = None) -> tuple[str, str]:
        url = self.endpoints.get(key)["url"]
        method = self.endpoints.get(key)["method"]
        has_query_parameters = self.endpoints.get(key).get("query_parameters", False)

        if params:
            encoded_params = self.encode_params(params)
            url = url.format(**encoded_params)
            if has_query_parameters:
                url = f"{url}?{urlencode(encoded_params)}"

        return url, method

    @staticmethod
    def encode_params(params: dict[str, str]):
        """
        Safely return the params dictionary, or an empty dictionary if None is passed in.

        :param params: dictionary containing the parameters to be used in the URL
        :return: dictionary containing the parameters to be used in the URL
        """
        return {key: quote(str(val)) for key, val in params.items()}

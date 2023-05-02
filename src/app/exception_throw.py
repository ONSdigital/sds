from fastapi import status
from fastapi.responses import JSONResponse


class exception_response:
    status_code: int
    status: str
    message: str

    def __init__(self, status_code: int, status: str, message: str):
        self.status_code = status_code
        self.status = status
        self.message = message

    def throw_er_with_json(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.status_code,
            content={"status": self.status, "message": self.message},
        )


def throw_500_global_exception() -> JSONResponse:
    """
    When an exception is raised and a global error 500 HTTP response is returned.
    """
    er = exception_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR, "error", "Unable to process request"
    )
    return er.throw_er_with_json()


def throw_400_validation_exception() -> JSONResponse:
    """
    When a validation fails and a 400 HTTP response is returned.
    """
    er = exception_response(
        status.HTTP_400_BAD_REQUEST, "error", "Validation has failed"
    )
    return er.throw_er_with_json()


def throw_400_incorrect_schema_key_exception() -> JSONResponse:
    """
    When wrong search parameters are supplied for schema metadata query and a 400 HTTP response is returned.
    """
    er = exception_response(
        status.HTTP_400_BAD_REQUEST, "error", "Invalid search provided"
    )
    return er.throw_er_with_json()


def throw_400_no_result_exception() -> JSONResponse:
    """
    When there is no schema metadata and a 400 HTTP response is returned.
    """
    er = exception_response(status.HTTP_400_BAD_REQUEST, "error", "No results found")
    return er.throw_er_with_json()


def throw_404_no_schemas_metadata_exception() -> JSONResponse:
    """
    When there is no schema metadata and a 404 HTTP response is returned.
    """
    er = exception_response(status.HTTP_404_NOT_FOUND, "error", "No results found")
    return er.throw_er_with_json()


def throw_404_no_schema_exception() -> JSONResponse:
    """
    When there is no schema found and a 404 HTTP response is returned
    Triggered when either schema metadata or schema json file is not found
    """
    er = exception_response(status.HTTP_404_NOT_FOUND, "error", "No schema found")
    return er.throw_er_with_json()


def throw_400_incorrect_key_names_exception() -> JSONResponse:
    """
    When searching for the dataset metadata endpoint with the incorrect search
    queries a 400 HTTP response is returned
    """
    er = exception_response(
        status.HTTP_400_BAD_REQUEST, "error", "Invalid search parameters provided"
    )
    return er.throw_er_with_json()


def throw_404_no_result_exception() -> JSONResponse:
    """
    When there is no dataset metadata endpoint and a 404 HTTP response is returned
    """
    er = exception_response(status.HTTP_404_NOT_FOUND, "error", "No datasets found")
    return er.throw_er_with_json()


def throw_404_unit_data_no_response_exception() -> JSONResponse:
    """
    Querying the dataset unit data with no result found triggers a 404
    HTTP response
    """
    er = exception_response(status.HTTP_404_NOT_FOUND, "error", "No unit data found")
    return er.throw_er_with_json()

from fastapi.responses import JSONResponse

class CustomErrorResponder:
    error_messages = {
        400: "Bad Request",
        404: "Not Found",
        500: "Internal Server Error",
    }

    @classmethod
    def get_error_response(cls, status_code: int) -> JSONResponse:
        if status_code in cls.error_messages:
            message = cls.error_messages[status_code]
        else:
            message = "Unknown Error"

        return JSONResponse(
            status_code=status_code,
            content={"status": "error", "message": message},
        )

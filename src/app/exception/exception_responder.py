from fastapi.responses import JSONResponse


class ExceptionResponder:
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

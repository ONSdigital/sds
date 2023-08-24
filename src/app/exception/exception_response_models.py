from pydantic import BaseModel

class ExceptionResponseModel(BaseModel):
    status: str
    message: str

erm_500_global_exception = ExceptionResponseModel(status = "error", message = "Unable to process request")
erm_400_validation_exception = ExceptionResponseModel(status = "error", message = "Validation has failed")
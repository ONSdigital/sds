from dataclasses import dataclass


@dataclass
class DeploymentStatus:
    """Model for Successful deployment response"""

    version: str
    status: str = "OK"


@dataclass
class BadRequest:
    """Model for a generic bad request response"""

    message: str
    status: str = "error"

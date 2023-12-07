@dataclass
class DeploymentStatus:
    """Model for Successful deployment response"""

    version: str
    status: str = "OK"
from pydantic import BaseModel


class ServiceStatus(BaseModel):
    name: str
    endpoint: str | None = None
    healthy: bool

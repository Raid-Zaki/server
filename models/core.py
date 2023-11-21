"""Here we are using Pydantic's BaseModel to create a schema for our models."""
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """The health response model."""
    status: str

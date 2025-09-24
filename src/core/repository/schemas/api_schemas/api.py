"""Schema configuration for constructing API endpoint paths."""

# -- Imports

from pydantic import BaseModel


# -- Exports

__all__ = ["ApiSchema"]

# --


class ApiSchema(BaseModel):
    """Configuration schema for base API endpoints."""

    v1: str = "/v1"
    calls: str = "/calls"

    @property
    def v1_data_url(self) -> str:
        """Full path for set data route."""

        return f"{self.calls}{self.v1}"

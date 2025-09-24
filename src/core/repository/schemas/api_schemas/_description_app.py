"""Description App."""

# -- Imports

from pydantic import BaseModel

# -- Exports

__all__ = ["DescriptionAppSchema"]

#


class DescriptionAppSchema(BaseModel):
    title: str = "FlowAI"
    description: str = "AI calls handler."
    version: str = "1.0.0"

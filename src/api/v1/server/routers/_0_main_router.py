"""Main router."""

# -- Imports

from fastapi import APIRouter
from .calls_router import calls_r

# -- Exports

__all__ = ["main_router"]

# --


main_router = APIRouter()
main_router.include_router(calls_r)

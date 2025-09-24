"""FastAPI application instance."""

# -- Imports

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from src.core.config import settings
from src.api.v1.server.routers import main_router
from src.core.repository.log import conf_logging


# -- Exports

__all__ = ["app"]

# --


def getUP() -> FastAPI:

    conf_logging(level=logging.INFO)

    app = FastAPI(
        title=settings._description.title,
        description=settings._description.description,
        version=settings._description.version,
        default_response_class=ORJSONResponse,
        docs_url="/docs",
    )

    # Routers
    app.include_router(main_router)

    # Middleware
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=["*"],
    )

    return app


app = getUP()

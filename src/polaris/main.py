"""
Entry point for the POLARIS-IR FastAPI application.

This module sets up the API server, configures CORS for ease of integration
with a front‑end client or GPT, and includes the routers that define
the available endpoints.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from polaris.api import events, brief, scenario, llm, datasources


def create_app() -> FastAPI:
    """Create and configure a FastAPI instance."""
    app = FastAPI(
        title="POLARIS-IR API",
        description="API for POLARIS-IR (Policy & Open-source LLM Analytics for Relations & International Security)",
        version="0.1.0",
    )

    # Allow CORS from any origin.  In production, restrict this to your domain.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: restrict origins in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount the static directory (use package-relative path so it works in Docker)
    package_dir = os.path.dirname(__file__)
    static_dir = os.path.join(package_dir, "static")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    # Root endpoint to serve the chat interface
    @app.get("/")
    async def read_index() -> FileResponse:
        """Return the chat interface."""
        return FileResponse(os.path.join(static_dir, "index.html"))

    # Health check endpoint
    @app.get("/health")
    def health() -> dict:
        """Return a simple health check response."""
        return {"status": "ok"}

    # Include API routers
    app.include_router(events.router)
    app.include_router(brief.router)
    app.include_router(scenario.router)
    app.include_router(llm.router)
    app.include_router(datasources.router)

    return app


# The ASGI application for Uvicorn
app = create_app()
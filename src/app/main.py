"""Definition of FastAPI based web service."""

from fastapi import FastAPI
from app import routers

import version
from log import get_logger
from configuration import configuration
from utils.common import register_mcp_servers

logger = get_logger(__name__)

logger.info("Initializing app")

service_name = configuration.configuration.name


app = FastAPI(
    title=f"{service_name} service - OpenAPI",
    description=f"{service_name} service API specification.",
    version=version.__version__,
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

logger.info("Including routers")
routers.include_routers(app)


@app.on_event("startup")
async def startup_event() -> None:
    """Perform logger setup on service startup."""
    get_logger("app.endpoints.handlers")
    logger.info("Starting up: registering MCP servers")
    register_mcp_servers(logger, configuration.configuration)
    logger.info("Including routers")
    routers.include_routers(app)

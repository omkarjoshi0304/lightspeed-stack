"""Lightspeed stack."""

from argparse import ArgumentParser
import logging

from rich.logging import RichHandler

from runners.uvicorn import start_uvicorn
from configuration import configuration


FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger(__name__)


def create_argument_parser() -> ArgumentParser:
    """Create and configure argument parser object."""
    parser = ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        help="make it verbose",
        action="store_true",
        default=None,
    )
    parser.add_argument(
        "-d",
        "--dump-configuration",
        dest="dump_configuration",
        help="dump actual configuration into JSON file and quit",
        action="store_true",
        default=None,
    )
    return parser


def main() -> None:
    """Entry point to the web service."""
    logger.info("Lightspeed stack startup")
    parser = create_argument_parser()
    args = parser.parse_args()

    configuration.load_configuration("lightspeed-stack.yaml")
    logger.info("Configuration: %s", configuration.configuration)
    logger.info(
        "Llama stack configuration: %s", configuration.llama_stack_configuration
    )

    if args.dump_configuration:
        configuration.configuration.dump()
    else:
        start_uvicorn(configuration.service_configuration)
    logger.info("Lightspeed stack finished")


if __name__ == "__main__":
    main()

import logging

logging.basicConfig(
    filename="security.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("gateway_logger")


def log_event(event: str):
    logger.info(event)
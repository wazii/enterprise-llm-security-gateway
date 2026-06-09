from config.constants import LOG_LEVELS


def validate_log_level(level: str):
    if level not in LOG_LEVELS:
        raise ValueError(
            f"Invalid log level: {level}"
        )
    return level
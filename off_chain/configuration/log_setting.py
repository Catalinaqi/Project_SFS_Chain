import logging
import logging.config
import yaml
import os


class LogConfig:
    """
    Loads logging configuration from logging.yaml and ensures correct application.
    """

    LOGGING_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "log_load_setting.yaml")

    @staticmethod
    def setup_logger():
        """Loads and applies logging configuration from YAML."""

        # Verify that the logging configuration file exists
        if not os.path.exists(LogConfig.LOGGING_CONFIG_PATH):
            raise FileNotFoundError(f"Logging configuration file not found: {LogConfig.LOGGING_CONFIG_PATH}")

        try:
            # Load YAML configuration
            with open(LogConfig.LOGGING_CONFIG_PATH, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)
                if not config or "logging" not in config:
                    raise KeyError("Missing 'logging' section in log_load_setting.yaml or the file is empty")

                # Ensure the handlers include "file"
                enable_file_logging = config["logging"].get("enable_file_logging", False)

                active_handlers = ["console"]
                if enable_file_logging:
                    active_handlers.append("file")

                config["logging"]["loggers"]["app_logger"]["handlers"] = active_handlers
                config["logging"]["root"]["handlers"] = active_handlers

                logging.config.dictConfig(config["logging"])
        except yaml.YAMLError as e:
            raise ValueError(f"Error loading logging.yaml: {str(e)}")

        # Get logger and test file logging
        logger = logging.getLogger("app_logger")
        logger.info("Logger initialized successfully. (File logging: " + (
            "enabled" if enable_file_logging else "disabled") + ")")
        return logger


# ===================== LOGGING CONFIGURATION =====================

# Initialize global logger
logger = LogConfig.setup_logger()

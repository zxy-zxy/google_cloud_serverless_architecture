import logging
import logging.config

import google.cloud.logging


def logging_dev_handlers():
    return {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG",
        },
    }


def logging_prod_handlers():
    return {
        "google_cloud_logging_handler": {
            "class": "google.cloud.logging.handlers.CloudLoggingHandler",
            "formatter": "standard",
            "level": "INFO",
            "client": google.cloud.logging.Client(),
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        },
    }


def setup_logging(app_settings):
    log_format = "%(asctime)s — %(name)s — %(levelname)s — %(message)s"

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"standard": {"format": log_format}},
        "handlers": dict(),
        "loggers": dict(),
    }

    logging_loggers = {
        "dev": {"": {"handlers": ["console"], "level": "DEBUG", "propagate": True}},
        "prod": {
            "": {
                "handlers": ["console", "google_cloud_logging_handler"],
                "level": "INFO",
                "propagate": True,
            }
        },
    }

    handlers_map = {"dev": logging_dev_handlers, "prod": logging_prod_handlers}
    logging_handlers_callable = handlers_map[app_settings]

    logging_config["handlers"].update(logging_handlers_callable())
    logging_config["loggers"].update(logging_loggers[app_settings])

    logging.config.dictConfig(logging_config)


class Config:
    def __init__(self):
        pass

    def __repr__(self):
        current_config = [
            "key: {} value: {}".format(attribute, getattr(self, attribute))
            for attribute in self.__dir__()
            if not attribute.startswith("__")
        ]
        return ",".join(current_config)

    def __str__(self):
        return self.__repr__()


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self.DEBUG = True


class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        self.DEBUG = False


def setup_config(app_settings):
    config_map = {"dev": DevelopmentConfig, "prod": ProductionConfig}

    config_class = config_map.get(app_settings)
    config_instance = config_class()
    return config_instance

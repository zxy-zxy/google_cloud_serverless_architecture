import os
import logging

from flask import Flask, request

from src.main import handler
from src.main import current_config


def main():
    logging.info("Current config: {}".format(current_config))

    app = Flask(__name__)

    @app.route("/", methods=["POST", "GET"])
    def index():
        return handler(request)

    app.run("0.0.0.0", debug=current_config.DEBUG)


if __name__ == "__main__":
    main()

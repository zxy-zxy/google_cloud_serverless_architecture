import os

from flask import Flask, request

from src.main import handler


def main():
    app = Flask(__name__)

    @app.route("/", methods=["POST", "GET"])
    def index():
        return handler(request)

    app.run("0.0.0.0", debug=True)


if __name__ == '__main__':
    main()

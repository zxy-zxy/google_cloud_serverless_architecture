import os
import logging
import json

from google.cloud import pubsub_v1
from flask import Flask, request, jsonify, make_response
from marshmallow import ValidationError

from my_local_package.utils import status
from my_local_package.utils.config import setup_config, setup_logging
from my_local_package.events.serializers import EventActionSchema

app_settings = os.getenv("app_settings")
pubsub_topic_id = os.getenv("pubsub_topic_id")
google_project_id = os.getenv("google_project_id")

setup_config(app_settings)
setup_logging(app_settings)

logging.info("Start function with settings: {}".format(app_settings))

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(google_project_id, pubsub_topic_id)
event_action_schema = EventActionSchema()


def handler(request):
    if request.method == "GET":
        return make_response(
            jsonify({"status": "error", "message": "Not available"}),
            status.HTTP_400_BAD_REQUEST,
        )

    response = {"status": "error", "message": "Unexpected input"}

    try:
        post_data = request.get_json()
    except json.JSONDecodeError as e:
        log_msg = "An error occurred during parsing the request message.\
            Message: {},  error: {},".format(
            request.data, str(e)
        )
        logging.error(log_msg)
        return make_response(jsonify(response), status.HTTP_400_BAD_REQUEST)

    logging.debug("post data :{}".format(post_data))

    if post_data is None:
        logging.debug("Cannot continue with empty request, response to send: {}".format(response))
        return make_response(jsonify(response), status.HTTP_400_BAD_REQUEST)

    try:
        event_action = event_action_schema.load(post_data).data
    except ValidationError as err:
        logging.error("An error occurred during loading object :{}".format(str(err)))
        response["errors"] = err.messages
        return make_response(jsonify(response), status.HTTP_400_BAD_REQUEST)

    logging.debug("event action: {}".format(event_action))

    event_action_dumped = event_action_schema.dumps(event_action)
    logging.debug("dumped message: {}".format(event_action_dumped.data))
    publisher.publish(topic_path, event_action_dumped.data.encode())

    response = {"status": "success", "message": "Processed"}
    logging.debug("response: {}".format(response))
    return make_response(jsonify(response), status.HTTP_201_CREATED)

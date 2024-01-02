import json
import os

from monitoring_status.lambda_handler import lambda_function


def test_lambda_function():
    # prepare
    event_filepath = os.path.join(os.path.dirname(__file__), "event.json")
    with open(event_filepath, "r") as f:
        event = json.load(f)

    # execute
    lambda_function(event, {})

    # verify

import json
import os
import urllib.parse
import urllib.request
from logging import getLogger

if os.getenv("LOGLEVEL"):
    log_level = os.getenv("LOGLEVEL")
else:
    log_level = "INFO"
logger = getLogger(__name__)
logger.setLevel(log_level)

ENDPOINT_ROOT = "https://api.notion.com/v1"


def _get_default_header():
    SECRET_KEY = os.environ["SECRET_KEY"]
    return {
        "Authorization": f"Bearer {SECRET_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }


def _build_filter_conditions(
    property_name_status, property_value_status_done, property_name_publish
):
    cond = {
        "and": [
            {
                "property": property_name_status,
                "status": {
                    "equals": property_value_status_done,
                },
            },
            {
                "property": property_name_publish,
                "checkbox": {
                    "equals": False,
                },
            },
        ]
    }
    return cond


def query_database(database_id, filter_conditions):
    logger.debug("query_database filter conditions: %s", filter_conditions)

    url = f"{ENDPOINT_ROOT}/databases/{database_id}/query"
    logger.debug("query_database url: %s", url)

    results = []
    next_cursor = ""
    has_more = True
    while has_more:
        body = {
            "filter": filter_conditions,
            "page_size": 100,
        }
        if next_cursor:
            body["start_cursor"] = next_cursor

        default_header = _get_default_header()
        headers = dict(**default_header)
        # "Add connect" is required in the Notion database settings
        req = urllib.request.Request(url, json.dumps(body).encode(), headers)
        with urllib.request.urlopen(req) as res:
            body = json.load(res)

        results += body["results"]

        next_cursor = body["next_cursor"]
        has_more = body["has_more"]

    return results


def update_page_properties(id_, properties):
    url = f"{ENDPOINT_ROOT}/pages/{id_}"
    logger.debug("update_page_properties url: %s", url)
    body = {
        "properties": properties,
    }

    headers = _get_default_header()
    req = urllib.request.Request(
        url, json.dumps(body).encode(), headers, method="PATCH"
    )
    with urllib.request.urlopen(req) as res:
        body = json.load(res)

    return body


def lambda_function(event, context):
    database_id = event["DATABASE_ID"]
    property_name_status = event["PROPERTY_NAME_STATUS"]
    property_value_status_done = event["PROPERTY_VALUE_STATUS_DONE"]
    property_name_publish = event["PROPERTY_NAME_PUBLISH"]
    property_name_publish_date = event["PROPERTY_NAME_PUBLISH_DATE"]

    filter_conditions = _build_filter_conditions(
        property_name_status, property_value_status_done, property_name_publish
    )
    results = query_database(database_id, filter_conditions)

    for r in results:
        id_ = r["id"]
        logger.info("page id: %s", id_)
        last_edited_time = r["last_edited_time"]
        properties = {
            property_name_publish: {"checkbox": True},
            property_name_publish_date: {
                "date": {
                    "start": last_edited_time,
                }
            },
        }
        update_page_properties(id_, properties)

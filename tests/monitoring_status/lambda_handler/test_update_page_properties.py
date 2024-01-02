from datetime import datetime

from monitoring_status.lambda_handler import update_page_properties


def test_2():
    # prepare
    id_ = "0d10f790-f452-4aa7-90f2-c738840c7a75"
    properties = {
        "Publish": {"checkbox": False},
        "PublishDate": {
            "date": {
                "start": datetime(2024, 1, 2, 12, 34, 56).isoformat(),
            }
        },
    }

    # execute
    update_page_properties(id_, properties)

    # verify
    assert False

from monitoring_status.lambda_handler import (_build_filter_conditions,
                                              query_database)


def test_1():
    # prepare
    filter_conditions = _build_filter_conditions()

    # execute
    results = query_database(filter_conditions)

    # verify
    assert len(results) > 0

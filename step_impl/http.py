from getgauge.python import step, data_store


@step("check that the response had no error")
def check_that_the_response_had_no_error():
    response = data_store.scenario["response"]
    status_code = response.status_code
    assert 200 <= status_code and status_code <= 299, "Response Code had an error but it shoudn't"


@step("check that the response had an error")
def check_that_the_response_had_an_error():
    response = data_store.scenario["response"]
    status_code = response.status_code
    assert status_code <= 200 or 299 <= status_code, "Response Code had no error but it should"


@step("check that the response had the status code <int>")
def check_that_the_response_had_the_status_code(expected):
    response = data_store.scenario["response"]
    status_code = response.status_code
    assert status_code == int(
        expected), f"response status code was {status_code} but expected {expected}"

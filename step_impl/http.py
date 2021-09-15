# ---license-start
# eu-digital-green-certificates / dgc-api-tests
# ---
# Copyright (C) 2021 T-Systems International GmbH and all other contributors
# ---
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ---license-end

from getgauge.python import data_store, step
from requests import Response


@step("check that the response had no error")
def check_that_the_response_had_no_error():
    response: Response = data_store.scenario["response"]
    assert response.ok, f"Response Code had an error but it shoudn't. Status Code {response.status_code}"


@step("check that the response had an error")
def check_that_the_response_had_an_error():
    response: Response = data_store.scenario["response"]
    assert not response.ok, f"Response Code had no error but it should. Status Code {response.status_code}"


@step("check that the response had the status code <int>")
def check_that_the_response_had_the_status_code(expected):
    response = data_store.scenario["response"]
    status_code = response.status_code
    assert status_code == int(
        expected), f"response status code was {status_code} but expected {expected}"

@step("check that the response had the status code <int> or None")
def check_that_the_response_had_the_status_code(expected):
    response = data_store.scenario["response"]
    status_code = response.status_code
    assert status_code is None or status_code == int(
        expected), f"response status code was {status_code} but expected {expected} or None"



@step("check that the response is not empty")
def check_that_the_response_is_not_empty():
    response: Response = data_store.scenario["response"]
    assert response.text != "", "response was empty"


@step("check that all responses had no error")
def check_that_all_repsonses_had_no_error():
    responses: List[Response] = data_store.scenario["responses"]
    for response in responses:
        assert response.ok, "Response Code had an error but it shoudn't"


@step("check that all repsonses had an error")
def check_that_all_repsonses_had_an_error():
    responses: List[Response] = data_store.scenario["responses"]
    for response in responses:
        assert not response.ok, "Response Code had no error but it should"


@step("check that all responses had the status code <200>")
def check_that_all_responses_had_the_status_code(expected):
    responses: List[Response] = data_store.scenario["responses"]
    for response in responses:
        assert int(expected) == response.status_code, f"response code should be {expected} but it was {response.status_code}"


@step("check that all responses had the status code <200> or None")
def check_that_all_responses_had_the_status_code(expected):
    responses: List[Response] = data_store.scenario["responses"]
    for response in responses:
        assert response.status_code is None or int(expected) == response.status_code


@step("check that all responses are not empty")
def check_that_all_responses_are_not_empty():
    responses: List[Response] = data_store.scenario["responses"]
    for response in responses:
        assert response.text != "", "response was empty"

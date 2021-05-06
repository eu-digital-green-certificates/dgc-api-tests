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

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
from os import path

import requests
from getgauge.python import data_store, step
from requests import Response
from step_impl.util import baseurl, certificateFolder


@step("get all valuesets IDs")
def get_all_valuesets():
    response = requests.get(baseurl + f"/valuesets", cert=(
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem")))
    data_store.scenario["response"] = response


@step("get all valuesets with custom certificate")
def get_all_valuesets_with_custom_certificate():
    cert_location = path.join(certificateFolder, "custom_auth.pem")
    key_location = path.join(certificateFolder, "custom_key_auth.pem")
    response = requests.get(baseurl + f"/valuesets", cert=(
        cert_location, key_location))
    data_store.scenario["response"] = response

def get_valueset_by_id(valuesetId):
    return requests.get(baseurl + f"/valuesets/{valuesetId}", cert=(
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem")))
@step("get details of first Valueset in list")
def get_details_of_first_valueset_in_list():
    response: Response = data_store.scenario["response"]
    valueSetIds = response.json()
    valueSetId = valueSetIds[0]
    response = get_valueset_by_id(valueSetId)
    data_store.scenario["response"] = response

@step("get all valuesets")
def get_all_valuesets():
    response: Response = data_store.scenario["response"]
    valueSetIds = response.json()
    valueSets = [get_valueset_by_id(valuesetId) for valuesetId in valueSetIds]
    data_store.scenario["responses"] = valueSets

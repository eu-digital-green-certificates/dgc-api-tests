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
import json
from os import path

import requests
from cryptography import x509
from cryptography.x509.oid import NameOID
from getgauge.python import data_store, step
from requests import Response
from requests.exceptions import SSLError
from step_impl.util import baseurl, certificateFolder, FailedResponse
from step_impl.util.certificates import get_own_country_name
from step_impl.util.rules import (download_rule_of_country,
                                  get_rules_from_rulelist)


@step("get all onboarded countries")
def get_all_onboarded_countries():
    response = requests.get(baseurl + "/countrylist", cert=(
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem")))
    data_store.scenario["response"] = response


@step("get all onboarded countries with custom certificate")
def get_all_onboarded_countries_with_custom_certificate():
    cert_location = path.join(certificateFolder, "custom_auth.pem")
    key_location = path.join(certificateFolder, "custom_key_auth.pem")
    try:
        response = requests.get(url=baseurl + "/countrylist",
                                cert=(cert_location, key_location))
        data_store.scenario["response"] = response
    except SSLError:
        data_store.scenario["response"] = FailedResponse()

@step("check that own country is in onboared countries list")
def check_that_own_country_is_in_onboared_countries_list():
    csca = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "csca.pem"), "rb").read())
    countryName = csca.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[
        0].value
    response: Response = data_store.scenario["response"]
    countries = response.json()
    assert countryName in countries, f"country: {countryName} not in country list: {', '.join(countries)}"


@step("download rules of all countries")
def download_rules_of_all_countries():
    response: Response = data_store.scenario["response"]
    countries = response.json()
    cert_location = path.join(certificateFolder, "auth.pem")
    key_location = path.join(certificateFolder, "key_auth.pem")
    responses = [download_rule_of_country(
        country, cert_location, key_location) for country in countries]
    data_store.scenario["responses"] = responses


@step("download rules of all countries with custom certificate")
def download_rules_of_all_countries_with_custom_certificate():
    def do_requests(*args, **kwargs):
        try:
            response = requests.get( *args, **kwargs )
        except SSLError:
            response = FailedResponse()
        return response

    response: Response = data_store.scenario["response"]
    countries = response.json()
    cert_location = path.join(certificateFolder, "custom_auth.pem")
    key_location = path.join(certificateFolder, "custom_key_auth.pem")
    responses = [ do_requests(url=baseurl + f"/rules/{country}", cert=(
        cert_location, key_location)) for country in countries]
    data_store.scenario["responses"] = responses


@step("get acceptance Rule from Rule list of own country")
def get_acceptance_rule_from_rule_list_of_own_country():
    countryName = get_own_country_name()
    cert_location = path.join(certificateFolder, "auth.pem")
    key_location = path.join(certificateFolder, "key_auth.pem")
    response = download_rule_of_country(
        countryName, cert_location, key_location)
    assert response.ok, f"response had an error. Status code {response.status_code}"
    rules = get_rules_from_rulelist(response.json())
    rule = [rule for rule in rules if rule["Type"] == "Acceptance"][0]
    data_store.scenario["rule"] = rule


@step("get Rules of own Country")
def get_rules_of_own_country():
    countryName = get_own_country_name()
    cert_location = path.join(certificateFolder, "auth.pem")
    key_location = path.join(certificateFolder, "key_auth.pem")
    response = download_rule_of_country(
        countryName, cert_location, key_location)
    data_store.scenario["response"] = response
    if response.ok:
        ruleList = response.json()
        rules = get_rules_from_rulelist(ruleList)
        data_store.scenario["rules"] = rules

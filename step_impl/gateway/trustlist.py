from os import path

import requests
from getgauge.python import data_store, step
from requests import Response

from . import baseurl, certificateFolder


@step("get complete trustlist")
def get_complete_trustlist():
    response = requests.get(baseurl + "/trustList", cert=(
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem")))
    data_store.scenario["response"] = response


@step("check that created keys are in trustlist")
def check_that_created_keys_are_in_trustlist():
    response: Response = data_store.scenario["response"]
    data = response.json()
    assert len(data) > 0, "No certificates in trustlist"


@step("get the trustList with the type <type>")
def get_the_trustlist_with_the_type(type):
    response = requests.get(baseurl + f"/trustList/{type}", cert=(
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem")))
    data_store.scenario["response"] = response


@step("check that only entries of the type <type> are present")
def check_that_only_entries_of_the_type_are_present(type):
    response: Response = data_store.scenario["response"]
    data = response.json()
    assert all(x == type for x in [y["certificateType"]
               for y in data]), f"found not only type {type}"


@step("get the trustList with the type <type> and country <country>")
def get_the_trustlist_with_the_type_and_country(type, country):
    response = requests.get(baseurl + f"/trustList/{type}/{country}", cert=(
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem")))
    data_store.scenario["response"] = response


@step("check that only entries of the type <type> and <country> are present")
def check_that_only_entries_of_the_type_and_county_are_present(type, country):
    check_that_only_entries_of_the_type_are_present(type)
    response: Response = data_store.scenario["response"]
    data = response.json()
    assert all(x == country for x in [y["country"]
               for y in data]), f"found not only country {country}"

from os import path

import requests
from requests import Response
from getgauge.python import step, data_store

from .. import baseurl, certificateFolder
from cryptography import x509
from cryptography.x509.oid import NameOID


@step("get all onboarded countries")
def get_all_onboarded_countries():
    response = requests.get(baseurl + "/countrylist", cert=(
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem")))
    data_store.scenario["response"] = response

@step("get all onboarded countries with custom certificate")
def get_all_onboarded_countries_with_custom_certificate():
    cert_location = path.join(certificateFolder, "custom_auth.pem")
    key_location = path.join(certificateFolder, "custom_key_auth.pem")
    response = requests.get(url=baseurl + "/countrylist",
                            cert=(cert_location, key_location))

@step("check that own country is in onboared countries list")
def check_that_own_country_is_in_onboared_countries_list():
    csca = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "csca.pem"), "rb").read())
    countryName = csca.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[
        0].value
    response: Response = data_store.scenario["response"]
    countries = response.json()
    assert countryName in countries,f"country: {countryName} not in country list: {', '.join(countries)}"

@step("download rules of all countries")
def download_rules_of_all_countries():
    response: Response = data_store.scenario["response"]
    countries = response.json()
    cert_location = path.join(certificateFolder, "auth.pem")
    key_location = path.join(certificateFolder, "key_auth.pem")
    responses = [requests.get(url=baseurl + f"/rules/{country}", cert=(cert_location, key_location)) for country in countries]
    data_store.scenario["responses"]

@step("download rules of all countries with custom certificate")
def download_rules_of_all_countries_with_custom_certificate():
    response: Response = data_store.scenario["response"]
    countries = response.json()
    cert_location = path.join(certificateFolder, "custom_auth.pem")
    key_location = path.join(certificateFolder, "custom_key_auth.pem")
    responses = [requests.get(url=baseurl + f"/rules/{country}", cert=(
        cert_location, key_location)) for country in countries]
    data_store.scenario["responses"]

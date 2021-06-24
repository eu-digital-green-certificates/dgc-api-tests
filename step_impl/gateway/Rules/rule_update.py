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
from step_impl.gateway.Rules.rule_upload import upload_rule
from step_impl.util.certificates import get_own_country_name
from os import path
from step_impl.util import certificateFolder
from step_impl.util.rules import download_rule_of_country, get_rule_from_cms, get_rules_from_rulelist


@step("update Rule to new version")
def update_rule_to_new_version():
    rule = data_store.scenario["rule"]
    newVersion = "1.0.1"
    rule["Version"] = newVersion
    data_store.scenario["new_version"] = newVersion
    # normal upload rule step which uses the new version because of the data_store
    upload_rule()


@step("check that Rule has the new version")
def check_that_rule_has_the_new_version():
    countryName = get_own_country_name()
    cert_location = path.join(certificateFolder, "auth.pem")
    key_location = path.join(certificateFolder, "key_auth.pem")
    response = download_rule_of_country(
        countryName, cert_location, key_location)
    ruleList = response.json()
    scenarioRule = rule = data_store.scenario["rule"]
    newVersion = data_store.scenario["new_version"]
    rules = get_rules_from_rulelist(ruleList)
    rule = [rule for rule in rules if rule["Identifier"] == scenarioRule["Identifier"]][0]
    assert rule['Version'] == newVersion, f"expected version to be {newVersion} but was {rule['Version']}"


@step("update Rule to new version with lower version number")
def update_rule_to_new_version_with_lower_version_number():
    rule = data_store.scenario["rule"]
    newVersion = "0.9.0"
    rule["Version"] = newVersion
    data_store.scenario["new_version"] = newVersion
    # normal upload rule step which uses the new version because of the data_store
    upload_rule()


@step("update Rule with version in wrong format")
def update_rule_with_version_in_wrong_format():
    rule = data_store.scenario["rule"]
    newVersion = "10"
    rule["Version"] = newVersion
    data_store.scenario["new_version"] = newVersion
    # normal upload rule step which uses the new version because of the data_store
    upload_rule()

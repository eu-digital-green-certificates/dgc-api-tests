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
from step_impl.util.rules import download_rule_of_country, get_rule_from_cms


@step("check that Rule has the new version")
def check_that_rule_has_the_new_version():
    scenarioRule = data_store.scenario["rule"]
    newVersion = data_store.scenario["new_version"]
    rules = data_store.scenario["rules"]
    rule = [rule for rule in rules if rule["Identifier"]
            == scenarioRule["Identifier"]][0]
    assert scenarioRule['Version'] == newVersion, f"expected version to be {newVersion} but was {rule['Version']}"

@step("check that both versions of the rule exist")
def check_that_both_versions_of_the_rule_exist():
    response = data_store.scenario["response"]
    ruleObj = response.json()
    scenarioRule = data_store.scenario["rule"]
    ruleId = scenarioRule["Identifier"]
    assert ruleId in ruleObj.keys(), f"ruleid {ruleId} not in response {ruleObj}"
    rules = ruleObj[ruleId]
    versions = [x["version"] for x in rules]
    assert "1.0.0" in versions, f"version 1.0.0 not in id list {versions}"
    newVersion = scenarioRule['Version']
    assert newVersion in versions, f"version {newVersion} not in id list {versions}"


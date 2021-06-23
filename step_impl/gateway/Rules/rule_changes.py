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
from datetime import datetime, timedelta


def change_rule(changeFunc):
    rule = data_store.scenario["rule"]
    changeFunc(rule)
    data_store.scenario["rule"] = rule


@step("change countrycode to a wrong format")
def change_countrycode_to_a_wrong_format():
    def change_countrycode(rule):
        rule["Country"] = rule["Country"] + "-"
    change_rule(change_countrycode)


@step("change countrycode to a wrong country")
def change_countrycode_to_a_wrong_country():
    def change_to_wrong_country(rule):
        if (rule["Country"] == "en"):
            rule["Country"] = "de"
        else:
            rule["Country"] = "en"
    change_rule(change_to_wrong_country)


@step("change ValidFrom less than <48>h")
def change_validfrom_less_than_h(hourStr: str):
    changeHours = int(hourStr)

    def change_valid_from(rule):
        # substract some time so that it definitly is less than
        rule["ValidFrom"] = datetime.now() + timedelta(hours=changeHours) - \
            timedelta(seconds=5)
    change_rule(change_valid_from)


@step("change ValidTo less than <72>h")
def change_validto_less_than_h(hourStr: str):
    changeHours = int(hourStr)

    def change_valid_from(rule):
        # substract some time so that it definitly is less than
        rule["ValidTo"] = datetime.now() + timedelta(hours=changeHours) - \
            timedelta(seconds=5)
    change_rule(change_valid_from)


@step("remove description of the Rule")
def remove_description_of_the_rule():
    def change_countrycode(rule):
        rule["Description"] = []
    change_rule(change_countrycode)


@step("use only german in the description of the Rule")
def use_only_german_in_the_description_of_the_rule():
    def change_description(rule):
        rule["Description"] = [
            {"lang": "de", "desc": "api-test-rule for use in api test"}]
    change_rule(change_description)


@step("add language <en-> in description")
def add_language_in_description(language: str):
    def change_description(rule):
        rule["Description"] = [{"lang": "en", "desc": "api-test-rule for use in api test"}, {
            "lang": language, "desc": "api-test-rule for use in api test"}]
    change_rule(change_description)

@step("set version of the Rule to <10>")
def set_version_of_the_rule_to(version):
    def change_version(rule):
        rule["Version"] = version
    change_rule(change_version)

@step("set version of the schema to <10>")
def set_version_of_the_schema_to(version):
    def change_schema_version(rule):
        rule["SchemaVersion"] = version
    change_rule(change_schema_version)

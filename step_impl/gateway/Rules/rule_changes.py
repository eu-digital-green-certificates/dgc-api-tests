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
        if (rule["Country"] == "EN"):
            rule["Country"] = "DE"
        else:
            rule["Country"] = "EN"
    change_rule(change_to_wrong_country)


@step("change countrycode in Identifier to a wrong country")
def change_countrycode_in_identifier_to_a_wrong_country():
    def change_rule_identifier_to_wrong_country(rule):
        ruleId = rule["Identifier"]
        currentCountry = ruleId[3:5]
        if ( currentCountry == "EN"):
            newCountry = "DE"
        else:
            newCountry = "EN"
        rule["Identifier"] = ruleId[:3]+newCountry+ruleId[5:]
    change_rule(change_rule_identifier_to_wrong_country)


@step("change ValidFrom less than <48>h")
def change_validfrom_less_than_h(hourStr: str):
    changeHours = int(hourStr)

    def change_valid_from(rule):
        # substract some time so that it definitly is less than
        rule["ValidFrom"] = datetime.now() + timedelta(hours=changeHours) - \
            timedelta(seconds=5)
    change_rule(change_valid_from)


@step("remove description of the Rule")
def remove_description_of_the_rule():
    def remove_description(rule):
        rule["Description"] = []
    change_rule(remove_description)


@step("change description to have less than <20> characters")
def change_description_to_have_less_than_characters(strLength):
    def change_description(rule):
        rule["Description"] = [
            {"lang": "en", "desc": "api-test-rule for use in api test"[:(int(strLength)-1)]}]
    change_rule(change_description)


@step("use only german in the description of the Rule")
def use_only_german_in_the_description_of_the_rule():
    def change_description(rule):
        rule["Description"] = [
            {"lang": "de", "desc": "api-test-rule for use in api test"}]
    change_rule(change_description)


@step("add language <en-> in description")
def add_language_in_description(language: str):
    def change_description(rule):
        rule["Description"] = [{"lang": language, "desc": "api-test-rule for use in api test"}, {
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

@step("set ValidFrom more than <14> days in the future")
def set_validfrom_more_than_days_in_the_future(dayStr):
    changeDays = int(dayStr)

    def change_valid_from(rule):
        rule["ValidFrom"] = datetime.now() + timedelta(days=changeDays)
    change_rule(change_valid_from)

@step("set ValidFrom after ValidTo value")
def set_validfrom_after_validto_value():
    def change_valid_to_before_valid_from(rule):
        rule["ValidTo"] = rule["ValidFrom"] - timedelta(hours=2)
    change_rule(change_valid_to_before_valid_from)

@step("change ValidTo to <1>h before the current ValidTo")
def change_validto_to_1h_before_the_current_validto(hoursStr):
    hours = int(hoursStr)
    def change_valid_to(rule):
        rule["ValidTo"] = rule["ValidTo"] - timedelta(hours=hours)
    change_rule(change_valid_to)


@step("change ValidTo to <1>h after the current ValidFrom")
def change_validto_to_1h_before_the_current_validto(hoursStr):
    hours = int(hoursStr)
    def change_valid_to(rule):
        rule["ValidTo"] = rule["ValidFrom"] + timedelta(hours=hours)
    change_rule(change_valid_to)


def change_version_to(version):
    def change_version(rule):
        rule["Version"] = version
        data_store.scenario["new_version"] = version
    return change_version
@step("change Rule to new version")
def change_rule_to_new_version():
    newVersion = "1.0.1"
    change_rule(change_version_to(newVersion))

@step("change Rule to lower version")
def change_rule_to_lower_version():
    newVersion = "0.9.0"
    change_rule(change_version_to(newVersion))

@step("change rule to version in wrong format")
def change_rule_to_version_in_wrong_format():
    newVersion = "10"
    change_rule(change_version_to(newVersion))


@step("change ValidFrom to <10>sec in the future")
def change_validfrom_to_sec_in_the_future(secStr):
    changeSeconds = int(secStr)

    def change_valid_from(rule):
        rule["ValidFrom"] = datetime.now() + timedelta(seconds=changeSeconds)
    change_rule(change_valid_from)

@step("change ValidTo to <15>sec in the future")
def change_validto_to_sec_in_the_future(secStr):
    changeSeconds = int(secStr)

    def change_valid_to(rule):
        rule["ValidFrom"] = datetime.now() + timedelta(seconds=changeSeconds)
    change_rule(change_valid_to)

@step("change CertificateType to be invalid")
def change_certificatetype_to_be_invalid():
    def change_valid_to(rule):
        (ruleType,country,counter) = rule["Identifier"].split("-")
        rule["CertificateType"] = "General" if ruleType=="VR" else "Vaccination"
    change_rule(change_valid_to)

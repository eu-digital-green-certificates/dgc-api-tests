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
from datetime import datetime, timedelta
from os import getcwd, path

from cryptography import x509
from cryptography.x509.oid import NameOID
from getgauge.python import data_store, step
from step_impl.util import certificateFolder
from step_impl.util.certificates import get_own_country_name

@step("create a valid <Ruletype> Rule")
def create_a_valid_rule(ruletype):
    countryName = get_own_country_name()
    if ruletype == "Invalidation":
        ValidFrom = datetime.now() + timedelta(seconds=10)
    else:
        ValidFrom = datetime.now() + timedelta(days=2, seconds=10)
    ValidTo = ValidFrom + timedelta(days=5)
    RuleID = "GR" if ruletype=="Acceptance" else "IR"
    # rule mostly from examole in specification
    rule = {
        "Identifier": f"{RuleID}-{countryName}-1001",
        "Type": ruletype,
        "Country": countryName,
        "Version": "1.0.0",
        "SchemaVersion": "1.0.0",
        "Engine": "CERTLOGIC",
        "EngineVersion": "2.0.1",
        "CertificateType": "General",
        "Description": [{"lang": "en", "desc": "api-test-rule for use in api test"}],
        "ValidFrom": ValidFrom,
        "ValidTo": ValidTo,
        "AffectedFields": ["dt", "nm"],
        "Logic": {
            "and": [
                {">=": [{"var": "dt"}, "23.12.2012"]},
                {">=": [{"var": "nm"}, "ABC"]}
            ]
        }
    }
    data_store.scenario["rule"] = rule

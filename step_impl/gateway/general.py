
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
from getgauge.python import data_store, step
from step_impl.util import certificateFolder, secondCountryFolder 

@step("use default certificates")
def select_default_certs():
    data_store.scenario['certs.auth.crt'] = path.join(certificateFolder, "auth.pem")
    data_store.scenario['certs.auth.key'] = path.join(certificateFolder, "key_auth.pem")
    data_store.scenario['certs.upload.crt'] = path.join(certificateFolder, "upload.pem")
    data_store.scenario['certs.upload.key'] = path.join(certificateFolder, "key_upload.pem")

@step("use 2nd country for upload signature")
def select_second_country_upload():
    data_store.scenario['certs.upload.crt'] = path.join(certificateFolder, secondCountryFolder, "upload.pem")
    data_store.scenario['certs.upload.key'] = path.join(certificateFolder, secondCountryFolder, "key_upload.pem")

@step("use 2nd country for authentication")
def select_second_country_tls():
    data_store.scenario['certs.auth.crt'] = path.join(certificateFolder, secondCountryFolder, "auth.pem")
    data_store.scenario['certs.auth.key'] = path.join(certificateFolder, secondCountryFolder, "key_auth.pem")
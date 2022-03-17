
from base64 import b64decode
import json
from webbrowser import get
import requests
from asn1crypto import cms
from cryptography import x509
from getgauge.python import data_store, step
from step_impl.util import baseurl
from step_impl.util.json import DateTimeEncoder
from step_impl.gateway.Rules.rule_upload import get_signed_rule

@step("get the list of migratables")
def get_the_list_of_migratables(update_data_store=True):
    certs = ( data_store.scenario['certs.auth.crt'], data_store.scenario['certs.auth.key'] )
    response = requests.get(baseurl + "/cms-migration", cert=certs)
    if update_data_store:
        data_store.scenario["response"] = response
        data_store.scenario["migratables"] = None
    return response
  
@step("check that the rule is in the list of migratables")
def check_that_the_rule_is_in_the_list_of_migratables():
    if data_store.scenario["migratables"] is None: 
        decode_migratables_from_response()

    rule = bytes(json.dumps(data_store.scenario["rule"], cls=DateTimeEncoder), 'utf-8')
    entry = get_matching_migratable( data_store.scenario["migratables"], rule )

    assert entry is not None, "Rule not found in list of migratables"

def get_matching_migratable( list_of_migratables, payload ):
    'Return the migratable with the same payload or None if there is no match'
    for entry in list_of_migratables:
        if entry['payload'] == payload:
            return entry
    return None

def use_upload2_cert(func):
    'Decorator to make the decorated function use the upload2 cert instead of upload cert'
    def decorated():
        # Backup the current UPLOAD cert
        backup_cert = data_store.scenario['certs.upload.crt']
        backup_key = data_store.scenario['certs.upload.key']
        # Set UPLOAD2 as new UPLOAD cert
        data_store.scenario['certs.upload.crt'] = data_store.scenario['certs.upload.crt'].replace('upload.pem','upload2.pem')
        data_store.scenario['certs.upload.key'] = data_store.scenario['certs.upload.key'].replace('upload.pem','upload2.pem')

        return_value = func()

        # Restore original UPLOAD cert
        data_store.scenario['certs.upload.crt'] = backup_cert
        data_store.scenario['certs.upload.key'] = backup_key

        return return_value
    return decorated

@use_upload2_cert
@step("migrate Rule") 
def migrate_rule():
    if data_store.scenario["migratables"] is None: 
        decode_migratables_from_response()

    rule = bytes(json.dumps(data_store.scenario["rule"], cls=DateTimeEncoder), 'utf-8')
    entry = get_matching_migratable( data_store.scenario["migratables"], rule )
    assert entry is not None, "Rule not found in list of migratables"

    data_store.scenario['cms.before.migration'] = entry['cms']
    entry['cms']= str(get_signed_rule(), 'utf-8') # Replace the CMS in the migratable with the one signed by UPLOAD2 
    del entry['payload'] # Remove payload attribute

    response = requests.post(url=baseurl + "/cms-migration",
                             json=entry, 
                             cert=(data_store.scenario['certs.auth.crt'], data_store.scenario['certs.auth.key']))
    data_store.scenario["response"] = response        
    

@step("check that the rule's new CMS differs from the old one")
def rule_new_cms_different_from_old():
    rule = bytes(json.dumps(data_store.scenario["rule"], cls=DateTimeEncoder), 'utf-8')
    entry = get_matching_migratable( data_store.scenario["migratables"], rule )
    assert entry is not None, "Rule not found in list of migratables"
    assert entry['cms'] != data_store.scenario['cms.before.migration'], 'CMS was not changed'

@step("decode the list of migratables")
def decode_migratables_from_response():
    jsondata = data_store.scenario["response"].json()

    data_store.scenario["migratables"] = []

    for entry in jsondata: 
        if entry.get('cms') is not None: 
            try: 
                cInfo = cms.ContentInfo.load(b64decode(entry['cms']))
                payload = dict(dict(dict(cInfo.native)['content'])['encap_content_info'])['content']
                migratable = entry.copy()
                migratable['payload'] = payload
                data_store.scenario["migratables"].append(migratable)
            except ValueError:
                print(f'Error parsing entityId {entry["entityId"]} {entry["type"]}')



#@step("check that DSC is in the list of migratables")
def check_that_dsc_is_in_the_list_of_migratables():
    assert False, "Add implementation code"

@step("sign DSC with UPLOAD2 certificate")
def sign_dsc_with_upload2_certificate():
    assert False, "Add implementation code"

@step("migrate DSC")
def migrate_dsc():
    assert False, "Add implementation code"
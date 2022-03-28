from getgauge.python import data_store, step
from step_impl.util import baseurl
from hashlib import sha256
import requests
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization

_max_pages = 1000

@step("prepare trust list hash buffer for comparison")
def prepare_trust_list_hash_buffer_for_comparison():
    data_store.scenario['hashbuffer.trustlist'] = []

@step("load unfiltered trust list with pagination size <size>")
def load_unfiltered_trust_list_with_pagination_size(size):
    do_paginated_trust_list_download(f"{baseurl}/trustList", size)

def do_paginated_trust_list_download(path, size):
    auth = (data_store.scenario['certs.auth.crt'], data_store.scenario['certs.auth.key'] )

    hashlist = []
    data_store.scenario['hashbuffer.trustlist'].append(hashlist)

    for page in range(_max_pages): 
        url = path + f"?page={page}&pagesize={size}"
        response = requests.get(url=url, cert=auth)        
        assert response.ok, "Failed to load trustList: {url} -> {response.status_code}"
        entries = response.json()

        hashlist.extend([entry['thumbprint'] for entry in entries])

        if len(entries) < int(size):
            return response # return last response for 

@step("compare downloaded trust lists")
def compare_downloaded_trust_lists():
    for i in range(1, len(data_store.scenario['hashbuffer.trustlist'])):
        left = data_store.scenario['hashbuffer.trustlist'][i-1]
        right = data_store.scenario['hashbuffer.trustlist'][i]
        assert set(left) == set(right), f'List {i-1} and {i} do not match'

@step("load <type> trust list with pagination size <size>")
def load_trust_list_with_pagination_size(type, size):
    do_paginated_trust_list_download(f"{baseurl}/trustList/{type}", size)

@step("load <type> trust list of <country> with pagination size <size>")
def load_trust_list_of_with_pagination_size(type, country, size):
    do_paginated_trust_list_download(f"{baseurl}/trustList/{type}/{country}", size)


@step("check that DSC is in trustlist of <days> days ago")
def check_dsc_is_in_trustlist_days_ago(days):  
    auth = (data_store.scenario['certs.auth.crt'], data_store.scenario['certs.auth.key'] )
    lm_time = (datetime.utcnow() - timedelta(days=float(days))).isoformat(timespec='seconds') + 'Z'
    response = requests.get(url=f"{baseurl}/trustList", cert=auth, headers={'If-Modified-Since': lm_time})        
    assert response.ok, 'Could not load trust list '

    thumbprint = sha256(data_store.scenario["dsc"].public_bytes(serialization.Encoding.DER)).digest().hex()

    for entry in response.json():
        if entry['thumbprint'] == thumbprint:
            if entry['signature'] is None: 
                assert False, 'DSC is in trust list but is marked as deleted'
            else: 
                return True

    assert False, 'DSC is not in trust list'


@step("check that DSC is marked deleted in trustlist of <days> days ago")
def check_dsc_is_deleted_in_trustlist_days_ago(days):  
    auth = (data_store.scenario['certs.auth.crt'], data_store.scenario['certs.auth.key'] )
    lm_time = (datetime.utcnow() - timedelta(days=float(days))).isoformat(timespec='seconds') + 'Z'
    response = requests.get(url=f"{baseurl}/trustList", cert=auth, headers={'If-Modified-Since': lm_time})        
    assert response.ok, 'Could not load trust list '

    thumbprint = sha256(data_store.scenario["dsc"].public_bytes(serialization.Encoding.DER)).digest().hex()

    for entry in response.json():
        if entry['thumbprint'] == thumbprint:
            if entry['signature'] is not None: 
                assert False, 'DSC is in trust list but is not deleted'
            else: 
                return True

    assert False, 'DSC is not in trust list'

@step("load trust list last modified <days> days ago date format <format_name>")
def load_trust_list_last_modified_days_ago_date_format(days, format_name):
    pivot_date = datetime.combine( datetime.utcnow() - timedelta(days=int(days)), datetime.min.time() )
    format_name = format_name.strip().upper()

    if format_name == "RFC 2616": 
        dt = pivot_date.ctime().split()
        date_string = f'{dt[0]}, {dt[2]} {dt[1]} {dt[4]} {dt[3]} GMT'
    elif format_name == "ISO 8601":
        date_string = pivot_date.isoformat(timespec='seconds') + 'Z'
    elif format_name == "SHORT":
        date_string = pivot_date.isoformat().replace('-','')[:8]
    else: 
        assert False, "Unknown date format"

    auth = (data_store.scenario['certs.auth.crt'], data_store.scenario['certs.auth.key'] )
    response = requests.get(url=f"{baseurl}/trustList", cert=auth, headers={'If-Modified-Since': date_string})        
    data_store.scenario["response"] = response     

    if response.ok: 
        hashlist = [entry['thumbprint'] for entry in response.json()]
        data_store.scenario['hashbuffer.trustlist'].append(hashlist)
    else: 
        data_store.scenario['hashbuffer.trustlist'].append([]) # Error leads to empty list for comparison

    return response 


@step("load trust list last modified <days> days ago page <page> size <size>")
def load_trust_list_last_modified_days_ago_page_size(days, page, size):
    auth = (data_store.scenario['certs.auth.crt'], data_store.scenario['certs.auth.key'] )
    lm_time = (datetime.utcnow() - timedelta(days=float(days))).isoformat(timespec='seconds') + 'Z'

    arguments = []
    try:
        arguments.append(f'page={int(page)}')
    except ValueError: 
        pass

    try:
        arguments.append(f'pagesize={int(size)}')
    except ValueError: 
        pass


    response = requests.get(url=f"{baseurl}/trustList?{'&'.join(arguments)}", cert=auth, headers={'If-Modified-Since': lm_time})        
    data_store.scenario["response"] = response     

    if response.ok: 
        hashlist = [entry['thumbprint'] for entry in response.json()]
        data_store.scenario['hashbuffer.trustlist'].append(hashlist)
    else: 
        data_store.scenario['hashbuffer.trustlist'].append([]) # Error leads to empty list for comparison

    return response 

@step("check that first trust list is shorter than second")
def first_trust_list_shorter_than_second():
    assert len(data_store.scenario['hashbuffer.trustlist'][0])\
         < len(data_store.scenario['hashbuffer.trustlist'][1]),\
             "First trust list is not shorter than second"
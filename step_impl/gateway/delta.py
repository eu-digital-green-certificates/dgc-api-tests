from getgauge.python import data_store, step
from step_impl.util import baseurl
from hashlib import sha256
import requests
import json

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
        print(len(entries))
        hashlist.extend([entry['thumbprint'] for entry in entries])

        if len(entries) < int(size):
            break

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

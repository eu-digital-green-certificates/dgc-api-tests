# Revoke a Pulbic Key

tags: DGC_GW

All test cases for revoking certificates

## revoke a public key

tags:

Revoke a DSC certificate of a country

* create a valid public key
* upload public key
* check that the response had no error
* check that key is in keylist
* revoke public key created
* check that the response had no error
* check that key is not in keylist

## revoke a dsc with unauthorized authentication

tags: negative_test

Revoke a DSC of a country with an unauthorized client certificate.

* get the trustList with the type "DSC"
* revoke random dsc of trustlist with unauthorized AUTHENTICATION certificate
* check that the response had an error
* check that the response had the error "Unauthorized"

## revoke a dsc with client certificate of another country

tage: negative_test

revoke a dsc of another country with the client certificate not authorized to change public keys of that country. The error Code should be 403 "Forbidden"

* get the trustList with the type "DSC"
* get random dsc from trustlist from another country
* delete dsc from another country
* check that the response had an error
* check that the response had the error "Forbidden"
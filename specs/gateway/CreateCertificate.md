# Create a Public Key

tags: DGC_GW

all tests for uploading public keys

## upload country code certificate

tags:

Upload a public key of a country

* create a valid public key
* upload public key
* check that the response had no error
* check that key is in keylist

## upload country code certificate without client certificate

tags: negative_test

Upload a public key of a country without a client certificate. The response should be with the status code 401 Unauthorized

* create a valid public key
* upload public key without client certificate
* check that the response had an error
* check that the response had the error "Unauthorized"

## upload country code certificate with mismatched certificate

tags: negative_test

Upload a public key of a country with a public key (country certificate) of a different country. The response code should be 403 Forbidden

* create a public key for another country
* upload public key
* check that the response had an error
* check that the response had the error "Forbidden"

## upload country code certificate in a wrong format

tags: negative_test

Upload a public key of a country with the wrong format to trigger Error Code 406

* create a valid public key
* upbload key as text
* check that the response had an error
* check that the response had the error "Content Not Acceptable"

## upload country code certificate with a dublicate uuid

tags: negative_test

Upload a public key of a country with a UUID which is already in the database. The API should respond with the error Code 409.

* create a valid public key with the uuid "..."
* upload public key
* check that the response had an error
* check that the response hat the error "Conflict"
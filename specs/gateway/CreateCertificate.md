# Create a DSC

tags: DGC_GW

all tests for uploading DSCs

## upload DSC

tags:

Upload a DSC for a country

* create a valid DSC
* upload DSC
* check that the response had no error
* check that key is in trustlist

## upload DSC without client certificate

tags: negative_test

Upload a DSC of a country without a client certificate. The response should be with the status code 401 Unauthorized

* create a valid DSC
* upload DSC without client certificate
* check that the response had an error
* check that the response had the error "Unauthorized"

## upload DSC with mismatched certificate

tags: negative_test

Upload a DSC signed with CSCA certificate of a different country. The response code should be 403 Forbidden

* create a DSC for another country
* upload DSC
* check that the response had an error
* check that the response had the error "Forbidden"

## upload DSC in a wrong format

tags: negative_test

Upload a DSC of a country with the wrong format to trigger Error Code 406

* create a DSC
* upbload DSC as text
* check that the response had an error
* check that the response had the error "Content Not Acceptable"

## upload DSC with a dublicate uuid

tags: negative_test

Upload a DSC of a country with a UUID which is already in the database. The API should respond with the error Code 409.

* create a valid DSC with the uuid "..."
* upload DSC
* check that the response had an error
* check that the response hat the error "Conflict"
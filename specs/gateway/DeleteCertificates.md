# Delete a DSC

tags: DGC_GW

All test cases for revoking certificates

## delete a dsc created

tags: 

Revoke a DSC certificate of a country

* create a valid DSC
* sign DSC with UPLOAD certificate
* upload DSC
* check that the response had no error
* check that DSC is in trustlist
* delete DSC created
* check that the response had no error
* check that DSC is not in trustlist

## delete a DSC with unauthorized authentication

tags: negative_test


Delete a DSC of a country with an unauthorized client certificate.

* get the trustList with the type "DSC"
* create custom authentication certificate
* delete random DSC with custom client certificate
* check that the response had an error
* check that the response had the status code "401"

## delete a DSC with client certificate of another country

tags: negative_test

delete a DSC of another country with the client certificate not authorized to change a DSC of that country. The error code should be 400 "Bad Request"

* get the trustList with the type "DSC"
* get random DSC from trustlist from another country
* delete DSC from another country
* check that the response had an error
* check that the response had the status code "400"

## delete a DSC not in database

tags: negative_test

delete a DSC of a country which is not in the database. The error code should be 400 "Bad Request"

* create a valid DSC
* sign DSC with UPLOAD certificate
* delete DSC created

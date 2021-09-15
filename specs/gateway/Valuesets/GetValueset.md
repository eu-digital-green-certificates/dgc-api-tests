# Get Valueset

tags: DGC_GW, Valueset

All tests to check the download of Valuesets

## Get all Valuesets

Get All Valuesets. Response code should be 200.

* get all valuesets IDs
* check that the response is not empty
* check that the response had no error
* check that the response had the status code "200"
* get all valuesets
* check that all responses are not empty
* check that all responses had no error
* check that all responses had the status code "200"

## Get specific Valueset

Get data of a specific Valueset. The test first downloads all Valuesets and then checks if it can download the specirif Valueset.

* get all valuesets IDs
* get details of first Valueset in list
* check that the response is not empty
* check that the response had no error

## Get Valueset with unauthenticated NBTLS

tags: negative_test

Use an NBTLS to try to authenticate when downloading the Valuesets

* create custom authentication certificate
* get all valuesets with custom certificate
* check that the response had an error
* check that the response had the status code "401" or None

## Check that RAT Valueset equal data of JRC Database

The National Backend should update the RAT Valuesets from the JRC database.

* get RAT Valuesets from JRC database
* get RAT Valuesets from Gateway
* check that RAT Valuesets from JRC database and Gateway match
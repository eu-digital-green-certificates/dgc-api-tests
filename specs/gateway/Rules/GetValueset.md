# Get Valueset

tags: DGC_GW

All tests to check the download of Valuesets

## Get all Valuesets

Get All Valuesets. Response code should be 200.

* get all valuesets
* check that the response had no error
* check that the response had the status code "200"

## Get specific Valueset

Get data of a specific valueset. The test first downloads all Valuesets

* get all valuesets
* get details of first valueset in list
* check that the response had no error

## Get Valueset with unauthenticated certificate

tags: negative_test

Use an unauthorized certificate to try to authenticate when downloading the Valuesets

* create custom authentication certificate
* get all valuesets with custom certificate
* check that the response had an error
* check that the response had the status code "401"

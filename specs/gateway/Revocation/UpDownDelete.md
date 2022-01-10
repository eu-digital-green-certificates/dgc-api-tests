# Upload, download and delete revocation lists

tags: DGC_GW, Revocation

* get the trustList with the type "UPLOAD"

Test cases for the upload and download of revocation lists 

| days_ago | 
|----------|
|        1 |
|        7 | 


## Download revocation list from <days_ago> days ago

* use default certificates
* download revocation list from <days_ago> days ago
* check that only results from <days_ago> days ago are in the response
* check that the response had no error

## Cannot download revocation list from future

* use default certificates
* download revocation list from "0" days ago
* check that the response had the status code "400" or None

## First country uploads, second country downloads

* use default certificates
* create a revocation list of type "SIGNATURE" with "500" entries
* sign revocation list
* upload revocation list
* check that the response had no error
* use 2nd country for authentication
* download revocation list from "1" days ago
* check that the response had no error

## Upload with more than 10000 entries is blocked

* use default certificates
* create a revocation list of type "SIGNATURE" with "10001" entries
* sign revocation list
* upload revocation list
* check that the response had an error


## Upload with auth certificate from different country is blocked

* use default certificates
* create a revocation list of type "SIGNATURE" with "500" entries
* use 2nd country for authentication
* sign revocation list
* upload revocation list
* check that the response had an error

## Upload of list signed by different country is blocked

* use default certificates
* create a revocation list of type "SIGNATURE" with "500" entries
* use 2nd country for upload signature
* sign revocation list
* upload revocation list
* check that the response had an error

____________________

* delete all uploaded revocation lists

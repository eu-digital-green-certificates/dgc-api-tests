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


____________________

* delete all uploaded revocation lists

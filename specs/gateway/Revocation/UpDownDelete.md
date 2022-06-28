# Upload, download and delete revocation lists

tags: DGC_GW, Revocation

* use default certificates


Test cases for the upload and download of revocation lists 


| days_ago | 
|----------|
|        1 |
|        7 |
## Download revocation list from <days_ago> days ago
* Reference "TXR-4896"
* download revocation list from <days_ago> days ago
* check that the response had no error
* check that only results from <days_ago> days ago are in the response
* check that the response had no error


## Revocation list download forbidden
* Reference "TXR-4897"
* create custom authentication certificate
* use unauthorized country for authentication
* download revocation list from "1" days ago
* check that the response had an error


## Cannot download revocation list from future
* download revocation list from "-1" days ago
* check that the response had the status code "400" or None


## Revocation batch upload type SIGNATURE expiring in 2 days
* Reference "TXR-4898"
* create revocation batch: type="SIGNATURE", entries="500", expiry="2"
* sign revocation batch
* upload revocation batch
* check that the response had no error
* download revocation list from "5" minutes ago
* check that the response had no error
* batch can be found


## Revocation batch upload type UCI expiring in 30 days
* Reference "TXR-6004"
* create revocation batch: type="UCI", entries="500", expiry="30"
* sign revocation batch
* upload revocation batch
* check that the response had no error
* download revocation list from "5" minutes ago
* check that the response had no error
* batch can be found


## Revocation batch upload type COUNTRYCODEUCI expiring in 365 days
* Reference "TXR-6005"
* create revocation batch: type="COUNTRYCODEUCI", entries="500", expiry="365"
* sign revocation batch
* upload revocation batch
* check that the response had no error
* download revocation list from "5" minutes ago
* check that the response had no error
* batch can be found


## Revocation batch upload fails bc wrong country
* Reference "TXR-4900"
* use 2nd country for authentication
* use 2nd country for upload signature
* create revocation batch: type="SIGNATURE", entries="500", expiry="2"
* sign revocation batch
* upload revocation batch
* check that the response had an error


## Revocation batch upload fails bc wrong country using first country
* Reference "TXR-4900"
* use default certificates
* create a revocation batch of type "SIGNATURE" with "500" entries for country "DE"
* sign revocation batch
* upload revocation batch
* check that the response had an error


## Revocation batch upload fails bc expired
* Reference "TXR-4901"
* use default certificates
* create revocation batch: type="SIGNATURE", entries="500", expiry="-2"
* sign revocation batch
* upload revocation batch
* check that the response had an error


## Revocation batch upload fails bc list too big
* Reference "TXR-4902"
* use default certificates
* create revocation batch: type="SIGNATURE", entries="1001", expiry="2"
* sign revocation batch
* upload revocation batch
* check that the response had an error


## Revocation batch upload fails bc schema invalid
* Reference "TXR-4903"
* use default certificates
* create revocation batch: type="INVALID TYPE", entries="500", expiry="2"
* sign revocation batch
* upload revocation batch
* check that the response had an error


## Revocation batch delete
* Reference "TXR-4904"
* use default certificates
* create revocation batch: type="SIGNATURE", entries="500", expiry="2"
* sign revocation batch
* upload revocation batch
* check that the response had no error
* delete uploaded revocation batches
* check that deletion responses are ok
* download revocation list from "5" minutes ago
* check that the response had no error
* check that deleted batches are deleted


## Revocation batch delete alternative endpoint
* Reference "TXR-4905"
* use default certificates
* create revocation batch: type="SIGNATURE", entries="500", expiry="2"
* sign revocation batch
* upload revocation batch
* check that the response had no error
* delete uploaded revocation batches using alternate endpoint
* check that deletion responses are ok
* download revocation list from "5" minutes ago
* check that the response had no error
* check that deleted batches are deleted

## Revocation batch download forbidden
* Reference "TXR-4906"
* use default certificates
* create revocation batch: type="SIGNATURE", entries="500", expiry="2"
* sign revocation batch
* upload revocation batch
* check that the response had no error
* download revocation list from "5" minutes ago
* check that the response had no error
* create custom authentication certificate
* use unauthorized country for authentication
* download uploaded batch
* check that the response had an error


## Revocation batch download forbidden for non EU
* Skip: Cancelled
* Reference "TXR-5580"
* use 2nd country for authentication
* use 2nd country for upload signature
* create a revocation batch of type "SIGNATURE" with "500" entries for country "DE"
* sign revocation batch
* upload revocation batch
* check that the response had no error
* use default certificates
* download uploaded batch
* check that the response had an error


## Revocation batch delete fails bc wrong country
* Reference "TXR-4907"
* use default certificates
* create revocation batch: type="SIGNATURE", entries="500", expiry="2"
* sign revocation batch
* upload revocation batch
* check that the response had no error
* use 2nd country for authentication
* use 2nd country for upload signature
* delete uploaded revocation batches using current certificates
* use default certificates
* download revocation list from "5" minutes ago
* check that the response had no error
* check that deleted batches are not deleted
____

* delete uploaded revocation batches
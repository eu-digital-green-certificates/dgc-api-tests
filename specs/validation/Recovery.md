# Validate recovery DCCs

tags: validationservice

* The validation service must be available

Validation of recovery DCCs. 

## Valid recovery DCC is accepted
* Reference "TXR-4215"
* Start a new checkin procedure with callback
* Create a recovery payload
* Set rDCC field "df" to "2021-11-01"
* Set rDCC field "du" to "2022-11-01"
* Set rDCC field "fr" to "2021-10-01"
* Add claim keys valid from "2021-11-01" until "2022-11-01"
* Sign with DSC of "DX"
* Set departure country "DX"
* Set arrival country "DE"
* Set departure date "2021-12-01"
* Set arrival date "2021-12-01"
* Validate DCC
* Check that the result is valid
* Check that callback result is identical to polling result

## Recovery DCC with du before DoA is rejected
* Reference "TXR-4218"
* Start a new checkin procedure with callback
* Create a recovery payload
* Set rDCC field "df" to "2021-11-01"
* Set rDCC field "du" to "2021-11-30"
* Set rDCC field "fr" to "2021-10-01"
* Add claim keys valid from "2021-11-01" until "2022-11-01"
* Sign with DSC of "DX"
* Set departure country "DX"
* Set arrival country "DE"
* Set departure date "2021-12-01"
* Set arrival date "2021-12-01"
* Validate DCC
* Check that the result is invalid
* Check that callback result is identical to polling result


## Recovery DCC with df after DoD is rejected
* Reference "TXR-4219"
* Start a new checkin procedure with callback
* Create a recovery payload
* Set rDCC field "df" to "2022-01-01"
* Set rDCC field "du" to "2022-11-01"
* Set rDCC field "fr" to "2021-10-01"
* Add claim keys valid from "2021-11-01" until "2022-11-01"
* Sign with DSC of "DX"
* Set departure country "DX"
* Set arrival country "DE"
* Set departure date "2021-12-01"
* Set arrival date "2021-12-01"
* Validate DCC
* Check that the result is invalid
* Check that callback result is identical to polling result

## Non-Covid-Recovery is rejected
* Reference "TXR-4217"
* Start a new checkin procedure with callback
* Create a recovery payload
* Set rDCC field "df" to "2021-11-01"
* Set rDCC field "du" to "2022-11-01"
* Set rDCC field "fr" to "2021-10-01"
* Set rDCC field "tg" to "123456789"
* Add claim keys valid from "2021-11-01" until "2022-11-01"
* Sign with DSC of "DX"
* Set departure country "DX"
* Set arrival country "DE"
* Set departure date "2021-12-01"
* Set arrival date "2021-12-01"
* Validate DCC
* Check that the result is invalid
* Check that callback result is identical to polling result
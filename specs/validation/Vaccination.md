# Validate vaccination DCCs

tags: validationservice

* The validation service must be available

Validation of vaccination DCCs. 

## Vaccination 2/2 from 15 days ago is valid
* Reference "TXR-4200"
* Start a new checkin procedure with callback
* Create a vaccination payload
* Set vDCC field "dt" to "2021-11-01" 
* Set vDCC dose "2" of "2"
* Add claim keys valid from "2021-11-01" until "2022-11-01"
* Sign with DSC of "DX"
* Set departure country "DE"
* Set arrival country "DE"
* Set departure date "2021-12-01"
* Set arrival date "2021-12-01"
* Validate DCC
* Check that the result is valid


## Vaccination 2/2 from 3 days ago is invalid
* Reference "TXR-4201"
* Start a new checkin procedure
* Create a vaccination payload
* Set vDCC field "dt" to "2021-12-01"
* Set vDCC dose "2" of "2"
* Add claim keys valid from "2021-11-01" until "2022-11-01"
* Sign with DSC of "DX"
* Set departure country "DE"
* Set arrival country "DE"
* Set departure date "2021-12-03"
* Set arrival date "2021-12-03"
* Validate DCC
* Check that the result is invalid


## Expired vaccination DCC is invalid
* Reference "TXR-4202"
* Start a new checkin procedure
* Create a vaccination payload
* Add claim keys valid from "2021-01-01" until "2021-11-01"
* Sign with DSC of "DX"
* Set departure country "BE"
* Set arrival country "DE"
* Set departure date "2021-11-02"
* Set arrival date "2021-11-02"
* Validate DCC
* Check that the result is invalid


## Vaccination DCC signed with expired DSC is invalid
* Reference "TXR-4203"
* Start a new checkin procedure
* Create a vaccination payload
* Add claim keys valid from "2021-01-01" until "2024-11-01"
* Sign with DSC of "DX"
* Set departure country "DE"
* Set arrival country "DE"
* Set departure date "2024-11-02"
* Set arrival date "2024-11-02"
* Validate DCC
* Check that the result is invalid




## Vaccination 1/2 is invalid
* Reference "TXR-4201"
* Start a new checkin procedure
* Create a vaccination payload
* Set vDCC field "ma" to "ORG-100030215"
* Set vDCC field "mp" to "EU/1/20/1528"
* Set vDCC field "dt" to "2021-11-01"
* Set vDCC dose "1" of "2"
* Add claim keys valid from "2021-11-01" until "2022-11-01"
* Sign with DSC of "DX"
* Set departure country "DE"
* Set arrival country "DE"
* Set departure date "2021-12-01"
* Set arrival date "2021-12-01"
* Validate DCC
* Check that the result is invalid


## Vaccination with unknown vaccine is invalid
* Reference "TXR-4204"
* Start a new checkin procedure
* Create a vaccination payload
* Set vDCC field "ma" to "ORG-100030215"
* Set vDCC field "mp" to "EU/1/55/9999"
* Set vDCC field "dt" to "2021-11-01"
* Set vDCC dose "2" of "2"
* Add claim keys valid from "2021-11-01" until "2022-11-01"
* Sign with DSC of "DX"
* Set departure country "DE"
* Set arrival country "DE"
* Set departure date "2021-12-01"
* Set arrival date "2021-12-01"
* Validate DCC
* Check that the result is invalid

## Vaccination is rejected for issuance date in future
* Reference "TXR-4213"
* Start a new checkin procedure with callback
* Create a vaccination payload
* Set vDCC field "dt" to "2021-11-01" 
* Set vDCC dose "2" of "2"
* Add claim keys valid from "2022-02-01" until "2023-02-01"
* Sign with DSC of "DX"
* Set departure country "DE"
* Set arrival country "DE"
* Set departure date "2022-03-01"
* Set arrival date "2022-03-01"
* Validate DCC
* Check that the result is invalid


## Vaccination is rejected for vaccination date in future
* Reference "TXR-4212"
* Start a new checkin procedure with callback
* Create a vaccination payload
* Set vDCC field "dt" to "2022-02-01" 
* Set vDCC dose "2" of "2"
* Add claim keys valid from "2021-02-01" until "2023-02-01"
* Sign with DSC of "DX"
* Set departure country "DE"
* Set arrival country "DE"
* Set departure date "2022-03-01"
* Set arrival date "2022-03-01"
* Validate DCC
* Check that the result is invalid

# Get trustlist

tags: DGC_GW

all test cases for getting the DSC (Signing Certificates)

   |type  |country|
   |------|-------|
   |CSCA  |DE     |
   |UPLOAD|DE     |
   |DSC   |DE     |

## get trustlist

Get all trusted public keys

* create a valid DSC
* sign DSC with UPLOAD certificate
* check that DSC is not in trustlist
* upload DSC
* check that DSC is in trustlist
* delete DSC created
* check that DSC is not in trustlist

## get trustlist with specific type

get all trusted public keys of a specific type

* get the trustList with the type <type>
* check that the response had no error
* check that only entries of the type <type> are present

## get trustlist with specific type and country

get all trusted public keys of a specific type and country

* get the trustList with the type <type> and country <country>
* check that the response had no error
* check that only entries of the type <type> and <country> are present

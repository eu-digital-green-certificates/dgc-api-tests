# Get trustlist

tags: DGC_GW

all test cases for getting the DSC (Signing Certificates)

## get trustlist

Get all trusted public keys

* get complete trustlist
* check that created keys are in trustlist

## get trustlist with specific type

get all trusted public keys of a specific type

| type   |
| ------ |
| CSCA   |
| UPLOAD |
| DSC    |

* get the trustList with the type "<type>"
* check that only entries of the type "<type>" are present

## get trustlist with specific type and country

get all trusted public keys of a specific type and country

| type   | country |
| ------ | ------- |
| CSCA   | DE      |
| UPLOAD | DE      |
| DSC    | DE      |

* get the trustList with the type "<type>" and country "<country>"
* check that only entries of the type "<type>" and "<country>" are present

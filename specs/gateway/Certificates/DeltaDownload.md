# Test cases for Delta Download 

* prepare trust list hash buffer for comparison

Test data for DSC download: 
   |type  |country|
   |------|-------|
   |CSCA  |DE     |
   |UPLOAD|DE     |
   |DSC   |DE     |

## Pagination full trust list
* Reference "TXR-6359"
* load unfiltered trust list with pagination size "50"
* load unfiltered trust list with pagination size "80"
* compare downloaded trust lists

## Pagination trust list by type
* Reference "TXR-6423"
* load <type> trust list with pagination size "10"
* load <type> trust list with pagination size "20"
* compare downloaded trust lists

## Pagination trust list by type and country
* Reference "TXR-6429"
* load <type> trust list of <country> with pagination size "10"
* load <type> trust list of <country> with pagination size "20"
* compare downloaded trust lists

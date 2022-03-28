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

## Date formats 
* Reference "TXR-6427"
* load trust list last modified "30" days ago date format "ISO 8601"
* check that the response had no error
* Reference "TXR-6426"
* load trust list last modified "30" days ago date format "RFC 2616"
* check that the response had no error
* Reference "TXR-6428"
* load trust list last modified "30" days ago date format "SHORT"
* check that the response had no error
* compare downloaded trust lists

## Pagination Default Values
* Reference "TXR-6430"
* load trust list last modified "60" days ago page "0" size "100"
* check that the response had no error
* load trust list last modified "60" days ago page "None" size "100"
* check that the response had no error
* load trust list last modified "60" days ago page "0" size "None"
* check that the response had no error
* compare downloaded trust lists

## Pagination is optional
* Reference "TXR-"
* load trust list last modified "60" days ago page "0" size "10"
* check that the response had no error
* load trust list last modified "60" days ago page "None" size "None"
* check that the response had no error
* check that first trust list is shorter than second


## Changes in Trust List 
* Reference "TXR-6424"
* create a valid DSC
* sign DSC with UPLOAD certificate
* upload DSC
* check that the response had no error
* check that DSC is in trustlist of "1" days ago
* Reference "TXR-6425"
* delete DSC created
* check that the response had no error
* check that DSC is marked deleted in trustlist of "1" days ago
* Reference "TXR-6431"
* upload DSC
* check that the response had no error
* check that DSC is in trustlist of "1" days ago

___
* delete all created certificates

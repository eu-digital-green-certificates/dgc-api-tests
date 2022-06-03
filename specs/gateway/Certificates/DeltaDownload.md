# Test cases for Delta Download 

* prepare trust list hash buffer for comparison

Test data for DSC download: 
   |type  |country|
   |------|-------|
   |CSCA  |DE     |
   |UPLOAD|DE     |
   |DSC   |DE     |

## Pagination full trust list

Load the full trust list in different paginations.
Finally, compare the downloaded lists and check that they have the same content.

* Reference "TXR-6359"
* load unfiltered trust list with pagination size "50"
* load unfiltered trust list with pagination size "80"
* compare downloaded trust lists

## Pagination trust list by type

Load the trust list filtered by type in different paginations.
Finally, compare the downloaded lists and check that they have the same content.

* Reference "TXR-6423"
* load <type> trust list with pagination size "10"
* load <type> trust list with pagination size "20"
* compare downloaded trust lists

## Pagination trust list by type and country

Load the trust list filtered by type and country in different paginations.
Finally, compare the downloaded lists and check that they have the same content.

* Reference "TXR-6429"
* load <type> trust list of <country> with pagination size "10"
* load <type> trust list of <country> with pagination size "20"
* compare downloaded trust lists

## Date formats 

Check that both ISO 8601 and RFC 2616 date formats are accepted
Known Bug: https://github.com/eu-digital-green-certificates/dgc-gateway/issues/174

* Reference "TXR-6427"
* load trust list last modified "30" days ago date format "ISO 8601"
* check that the response had no error
* Reference "TXR-6426"
* load trust list last modified "30" days ago date format "RFC 2616"
* check that the response had no error
* compare downloaded trust lists

## Pagination Default Values

Check that the default values for page size and page number are 
used when one of the parameters is missing. 

* Reference "TXR-6430"
* load trust list last modified "60" days ago page "0" size "100"
* check that the response had no error
* load trust list last modified "60" days ago page "None" size "100"
* check that the response had no error
* load trust list last modified "60" days ago page "0" size "None"
* check that the response had no error
* compare downloaded trust lists

## Pagination is optional

Check that pagination is optional and when no pagination is requested, 
the full trust list is returned (backwards compatibility)

* Reference "TXR-"
* load trust list last modified "60" days ago page "0" size "10"
* check that the response had no error
* load trust list last modified "60" days ago page "None" size "None"
* check that the response had no error
* check that first trust list is shorter than second


## Changes in Trust List 

A freshly uploaded DSC should appear in the trust list and if it is deleted, a deletion entry should appear in its place. 
When the same DSC is uploaded then again, it should be accepted and re-appear in the trust list, replacing the deletion entry. 

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

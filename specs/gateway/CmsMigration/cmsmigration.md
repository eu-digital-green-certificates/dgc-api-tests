# Migrate CMS entities

tags: DGC_GW

Feature: CMS update / migration

## Get list of CMSs
* Reference "TXR-6343"
* get the list of migratables
* check that the response had no error
* decode the list of migratables

## Migrate a DSC

* Reference "TXR-6344"
* create a valid DSC
* sign DSC with UPLOAD certificate
* upload DSC
* get the list of migratables
* check that the response had no error
* check that DSC is in the list of migratables
* migrate DSC
* check that DSC is in trustlist
* get the list of migratables
* check that the response had no error
* check that DSC is in the list of migratables
* check that the DSC's new CMS differs from the old one

## Migrate a Rule
* Reference "TXR-6345"
* create a valid "Acceptance" Rule
* upload Rule
* check that the response had no error
* check that the response had the status code "201"
* check that Rule is in Rulelist
* get the list of migratables
* check that the response had no error
* check that the rule is in the list of migratables
* migrate Rule
* check that the response had no error
* get the list of migratables
* check that the response had no error
* check that the rule is in the list of migratables
* check that the rule's new CMS differs from the old one

## Attempt to migrate a Rule from other country
* Reference "TXR-6379"
* create a valid "Acceptance" Rule
* upload Rule
* check that the response had no error
* check that the response had the status code "201"
* check that Rule is in Rulelist
* get the list of migratables
* check that the response had no error
* check that the rule is in the list of migratables
* use 2nd country for upload signature
* use 2nd country for authentication
* migrate Rule
* check that the response had an error
* use default certificates

## Migrate a Revocation Batch
* Reference "TXR-6346"
* create revocation batch: type="SIGNATURE", entries="500", expiry="2"
* sign revocation batch
* upload revocation batch
* check that the response had no error
* get the list of migratables
* check that the response had no error
* check that the revocation batch is in the list of migratables
* migrate revocation batch
* check that the response had no error
* get the list of migratables
* check that the response had no error
* check that the revocation batch is in the list of migratables
* check that the batch's new CMS differs from the old one

## Attempt switching payload
* Reference "TXR-6347"
* create a valid "Acceptance" Rule
* upload Rule
* check that the response had no error
* check that the response had the status code "201"
* check that Rule is in Rulelist
* get the list of migratables
* check that the response had no error
* check that the rule is in the list of migratables
* migrate Rule with modified payload
* check that the response had an error

___
* delete all created certificates
* delete all created rules
* delete uploaded revocation batches
# Upload Rules

tags: DGC_GW, Rules

Tests to upload new rules

   |Ruletype    |
   |------------|
   |Acceptance  |
   |Invalidation|

## upload valid Rule

Upload a valid invalidation Rule. Invalidation Rule is used because it can be deleted automatically

* create a valid <Ruletype> Rule
* upload Rule
* check that the response had no error
* check that the response had the status code "201"
* check that Rule is in Rulelist

## upload valid Rule with cms header

The content type header of rules normally in the test is "application/cms-text" but it can also be "application/cms" like for the certificates

* create a valid <Ruletype> Rule
* upload Rule with cms header
* check that the response had no error
* check that the response had the status code "201"
* check that Rule is in Rulelist

## upload Rule with unauthenticated certificate

tags: negative_test

Upload a Rule with an unauthenticated certificate. There should be an error and the Response Code should be 401.

* create a valid <Ruletype> Rule
* create custom authentication certificate
* upload Rule with custom authentication certificate
* check that the response had an error
* check that the response had the status code "401" or None
* check that Rule is not in Rulelist

## upload Rule with authentication certificate of another country

tags: negative_test

Upload a Rule with a NBTLS certificate of another country. There should be an error and the status code should be 400.

* create a valid <Ruletype> Rule
* upload Rule with certificate from another country
* check that the response had an error
* check that Rule is not in Rulelist

## upload rule with trailing characters

tags: negative_test

Upload a Rule with trailing data after the main payload. The API should reject the rule. 

* create a valid <Ruletype> Rule
* upload Rule with extra data
* check that the response had an error
* check that the response had the status code "400" or None
* check that Rule is not in Rulelist


___
* delete all created rules

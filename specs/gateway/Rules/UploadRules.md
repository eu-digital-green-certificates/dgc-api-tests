# Upload Rules

tags: DGC_GW, Rules

Tests to upload new rules

## upload valid Rule

Upload a valid invalidation Rule. Invalidation Rule is used because it can be deleted automatically

* create a valid Invalidation Rule
* upload Rule
* check that the response had no error
* check that the response had the status code "200"
* check that Rule is in Rulelist

## upload Rule with unauthenticated certificate

tags: negative_test

Upload a Rule with an unauthenticated certificate. There should be an error and the Response Code should be 401.

* create a valid Invalidation Rule
* create custom authentication certificate
* upload Rule with custom authentication certificate
* check that the response had an error
* check that the response had the status code "401"
* check that Rule is not in Rulelist

## upload Rule with authentication certificate of another country

tags: negative_test

Upload a Rule with a NBTLS certificate of another country. There should be an error and the status code should be 400.

* create a valid Invalidation Rule
* upload Rule with certificate from another country
* check that the response had an error
* check that Rule is not in Rulelist

___
* delete all created rules

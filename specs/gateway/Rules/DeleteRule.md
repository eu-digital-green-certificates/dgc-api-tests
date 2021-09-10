# Delete Rule

tags: DGC_GW, Rules

Test for deletion of the rules

   |Ruletype    |
   |------------|
   |Acceptance  |
   |Invalidation|

## delete Rule

Delete a Rule.

* create a valid <Ruletype> Rule
* upload Rule
* check that Rule is in Rulelist
* delete Rule
* check that the response had no error
* check that Rule is not in Rulelist

## delete rule with alias endpoint

Delete a Rule by using the POST endpoint. This is used so that a body can be used in a POST request instead of a DELETE request.

* create a valid <Ruletype> Rule
* upload Rule
* check that Rule is in Rulelist
* delete Rule using alias Endpoint
* check that the response had no error
* check that Rule is not in Rulelist

## delete Rule of another country

tags: negative_test

Delete a Rule of another country. This should not be possible.

* create a valid <Ruletype> Rule
* upload Rule
* check that Rule is in Rulelist
* delete Rule with certificate of another country
* check that the response had an error
* check that Rule is in Rulelist
* delete Rule

## delete invalidation Rule with unauthenticated NBTLS

tags: negative_test

Delete a Rule with unauthenticated certificate. This should not be possible.

* create a valid <Ruletype> Rule
* upload Rule
* check that Rule is in Rulelist
* create custom authentication certificate
* delete Rule created with custom client certificate
* check that the response had an error
* check that Rule is in Rulelist
* delete Rule

## delete Rule not in database

tags: negative_test

Delete a Rule which is not in the database. There should be an error in that case.

* delete Rule not in rulelist
* check that the response had an error

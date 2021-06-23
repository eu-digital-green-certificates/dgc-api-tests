# Delete Rule

tags: DGC_GW, Rules

Test for deletion of the rules

## delete invalidation Rule

Delete an Invalidation Rule. This should be no problem as Invalidation Rules can be deleted.

* create a valid Invalidation Rule
* upload Rule
* check that Rule is in Rulelist
* delete Rule
* check that the response had no error
* check that Rule is not in Rulelist

## delete acceptance Rule

tags: negative_test

Delete an Acceptance Rule. This should be an error because Acceptance Rules cannot be deleted.

* get acceptance Rule from Rule list of own country
* delete Rule
* check that the response had an error
* check that Rule is in Rulelist

## delete invalidation Rule of another country

tags: negative_test

Delete an Invalidation Rule of another country. This should not be possible.

* create a valid Invalidation Rule
* upload Rule
* check that Rule is in Rulelist
* delete Rule with certificate of another country
* check that the response had an error
* check that Rule is in Rulelist
* delete Rule

## delete invalidation Rule with unauthenticated NBTLS

tags: negative_test

Delete an Invalidation Rule with unauthenticated certificate. This should not be possible.

* create a valid Invalidation Rule
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

# Update Rules

tags: DGC_GW, Rules

Tests to update rules

## update Rule to a new version

Update a Rule created to a new version.

* create a valid Invalidation Rule
* upload Rule
* change Rule to new version
* upload Rule
* check that the response had no error
* check that the response had the status code "201"
* get Rules of own Country
* check that Rule has the new version

## update Rule to a new version and ValidFrom later than old rule

Update a Rule created to a new version and ValidFrom value later than old rule. In the end both Versions of the rule should be downloaded.

* create a valid Invalidation Rule
* upload Rule
* change Rule to new version
* upload Rule
* check that the response had no error
* check that the response had the status code "201"
* get Rules of own Country
* check that Rule has the new version
* check that both versions of the rule exist

## update Rule with lower version than the old Rule

tags: negative_test

Update a Rule with a Rule lower than the current version. There should be an error.

* create a valid Invalidation Rule
* upload Rule
* change Rule to lower version
* upload Rule
* check that the response had an error
* check that the response had the status code "400"

## update Rule Rule without semver

tags: negative_test

Update a Rule without following the semantic versioning scheme (e.g. 1.3 instead of 1.3.0)

* create a valid Invalidation Rule
* upload Rule
* change rule to version in wrong format
* upload Rule
* check that the response had an error
* check that the response had the status code "400"

## Update Rule with ValidFrom less than ValidFrom of older Version

tags: negative_test

Update Rule with ValidFrom less than ValidFrom of older Version

* create a valid Invalidation Rule
* upload Rule
* change ValidTo to "1"h before the current ValidTo
* change Rule to new version
* upload Rule
* check that the response had no error
* check that the response had the status code "201"
* get Rules of own Country
* check that Rule has the new version

## Updating a rule automatically removes the old version

After a rule is updated and valid the old rule should not be in the downloaded list

* create a valid Invalidation Rule
* upload Rule
* change Rule to new version
* change ValidFrom to "10"sec in the future
* upload Rule
* get Rules of own Country
* check that both version of the rule are in the rulelist
* wait for "10" seconds
* get Rules of own Country
* check that only the new version of the rule is in the list

___
* delete all created rules

# Update Rules

tags: DGC_GW, Rules

Tests to update rules

## update Rule to a new version

Update a Rule created to a new version.

* create a valid Invalidation Rule
* upload Rule
* update Rule to new version
* check that the response had no error
* check that the response had the status code "200"
* get Rules of own Country
* check that Rule has the new version

## update Rule with lower version than the old Rule

tags: negative_test

Update a Rule with a Rule lower than the current version. There should be an error.

* create a valid Invalidation Rule
* upload Rule
* update Rule to new version with lower version number
* check that the response had no error
* check that the response had the status code "400"

## update Rule Rule without semver

tags: negative_test

Update a Rule without following the semantic versioning scheme (e.g. 1.3 instead of 1.3.0)

* create a valid Invalidation Rule
* upload Rule
* update Rule with version in wrong format
* check that the response had no error
* check that the response had the status code "400"

___
* delete all created rules

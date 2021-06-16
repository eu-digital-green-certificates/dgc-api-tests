# Update Rules

tags: DGC_GW

Tests to update rules

## update rule to a new version
* create a valid Invalidation Rule
* upload Rule
* update Rule to new version
* check that the response had no error
* check that the response had the status code "200"
* delete Rule created

## update rule with lower version than the old rule
* create a valid Invalidation Rule
* upload Rule
* update Rule to new version with lower version number
* check that the response had no error
* check that the response had the status code "200"
* delete Rule created

## update rule rule without semver
* create a valid Invalidation Rule
* upload Rule
* update Rule with version in wrong format
* check that the response had no error
* check that the response had the status code "200"
* delete Rule created

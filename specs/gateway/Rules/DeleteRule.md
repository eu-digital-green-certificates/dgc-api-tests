# Delete Rule

tags: DGC_GW

Test for deletion of the rules

## delete invalidation Rule
* create a valid Invalidation Rule
* upload Rule
* check that Rule is in Rulelist
* delete Rule created
* check that the response had no error
* check that Rule is not in Rulelist

## delete acceptance Rule
* get acceptance Rule from rule list
* delete Rule created
* check that the response had no error
* check that Rule is not in Rulelist

## delete invalidation Rule with client certificate of another country
* create a valid Invalidation Rule
* upload Rule
* check that Rule is in Rulelist
* delete Rule created with certificate of another country
* check that the response had an error
* check that Rule is in Rulelist
* delete Rule created

## delete invalidation Rule with unauthenticated certificate
* create a valid Invalidation Rule
* upload Rule
* check that Rule is in Rulelist
* delete Rule created with custom client certificate
* check that the response had an error
* check that Rule is in Rulelist
* delete Rule created

## delete Rule not in database
* delete Rule not in rulelist
* check that the response had an error

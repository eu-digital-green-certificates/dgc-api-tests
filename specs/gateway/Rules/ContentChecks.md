# Content Checks

tags: DGC_GW

Test cases for the content checks

## upload rule with uploader country with wrong format
* create a valid Invalidation Rule
* change countrycode to a wrong format
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

## upload rule with wrong uploader country
* create a valid Invalidation Rule
* change countrycode to a wrong country
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

## upload rule with ValidFrom less than 48h in the future
* create a valid Invalidation Rule
* change ValidFrom less than "48"h
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

## upload rule with validTo less than 72h in the future
* create a valid Invalidation Rule
* change ValidTo less than "72"h
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

## upload rule with description not available
* create a valid Invalidation Rule
* remove description of the rule
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

## upload rule with description filled with one language without english
* create a valid Invalidation Rule
* use only german in the description of the rule
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

## upload rule with an invalid language in description
* create a valid Invalidation Rule
* add language "en-" in description
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

## upload rule wich doesn't follow semVer
* create a valid Invalidation Rule
* set version of the rule to "10"
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

## upload rule with invalid schema version
* create a valid Invalidation Rule
* set version of the schema to "10"
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist


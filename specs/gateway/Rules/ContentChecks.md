# Content Checks

tags: DGC_GW, Rules

Test cases for the content checks which are used for all rules.


   |Ruletype    |
   |------------|
   |Acceptance  |
   |Invalidation|

## upload Rule with uploader country in wrong format

tags: negative_test

Country attribute in a Rule should be like "en". Otherwise there should be an error

* create a valid <Ruletype> Rule
* change countrycode to a wrong format
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

## upload Rule with wrong uploader country

tags: negative_test

Upload a Rule from another country. There should be an error.

* create a valid <Ruletype> Rule
* change countrycode to a wrong country
* upload Rule
* check that the response had an error
* check that the response had the status code "403"
* check that Rule is not in Rulelist

## upload Rule with wrong Country in Identifier

tags: negative_test

Upload a Rule with the Identifier of another Country

* create a valid <Ruletype> Rule
* change countrycode in Identifier to a wrong country
* upload Rule
* check that the response had an error
* check that the response had the status code "403"
* check that Rule is not in Rulelist

## upload Rule with description not available

tags: negative_test

A Rule must have a description. An empty description should be an error.

* create a valid <Ruletype> Rule
* remove description of the Rule
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

## upload Rule with description text length smaller than 20 characters

tags: negative_test

A Rule must have a description. Those descriptions must have a length of at least 20 characters.

* create a valid <Ruletype> Rule
* change description to have less than "20" characters
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

## upload Rule with description filled with one language without english

tags: negative_test

A Rule must have a description in english. Only having a description in another language should be an error.

* create a valid <Ruletype> Rule
* use only german in the description of the Rule
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

## upload Rule with an invalid language in description

tags: negative_test

Languages of a Rule should have the formatting like "en" or "en-uk". Otherwise there should be an error.

* create a valid <Ruletype> Rule
* add language "en-" in description
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

## upload Rule wich doesn't follow semVer

tags: negative_test

Rule Version should be created with semantic versioning (like "1.2.3" and not like "1.2"). Otherwise there should be an error.

* create a valid <Ruletype> Rule
* set version of the Rule to "10"
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

## upload Rule which Schema version doesn't follow semVer

tags: negative_test

Rule Schema Version should be created with semantic versioning (like "1.2.3" and not like "1.2"). Otherwise there should be an error.

* create a valid <Ruletype> Rule
* set version of the schema to "10"
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

## Value of ValidFrom must be before value of ValidTo

tags: negative_test

Value of ValidFrom must be before value of ValidTo

* create a valid <Ruletype> Rule
* set ValidFrom after ValidTo value
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

## Value of ValidFrom must be within 2 weeks from today

tags: negative_test

Value of ValidFrom must be within 2 weeks from today

* create a valid <Ruletype> Rule
* set ValidFrom more than "14" days in the future
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

___
* delete all created rules

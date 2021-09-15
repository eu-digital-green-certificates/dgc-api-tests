# Content Checks for Acceptance Rules

tags: DGC_GW, Rules

Test cases for the content checks which are used for Acceptance rules.

## upload Rule with ValidFrom less than 48h in the future

tags: negative_test

Upload a Acceptance Rule which is valid ealier than 48h. There should be an error.

* create a valid Acceptance Rule
* change ValidFrom less than "48"h
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist


## Value of ValidTo must more than 120h future from now

tags: negative_test

Test that the Gateway responds with an error message if the ValidTo Value is less than 120h in the future

* create a valid Acceptance Rule
* change ValidTo to "71"h after the current ValidFrom
* upload Rule
* check that the response had an error
* check that the response had the status code "400"


## upload Rule with CertificateType not matching RuleId

tags: negative_test

Upload a Acceptance Rule where the CertificateType is not matching the Rule Identifier of the Rule

* create a valid Acceptance Rule
* change CertificateType to be invalid
* upload Rule
* check that the response had an error
* check that the response had the status code "400"
* check that Rule is not in Rulelist

___
* delete all created rules
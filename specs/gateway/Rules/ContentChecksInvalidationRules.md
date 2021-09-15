# Content Checks for Invalidation Rules

tags: DGC_GW, Rules

Test cases for the content checks which are used for Invalidation rules.

## Value of ValidFrom must be in future from today

tags: negative_test

Test that the Gateway responds with an error message if the ValidFrom Value is not in the Future

* create a valid Invalidation Rule
* change ValidFrom less than "0"h
* upload Rule
* check that the response had an error
* check that the response had the status code "400"


## Value of ValidTo must more than 72h future from now

tags: negative_test

Test that the Gateway responds with an error message if the ValidTo Value is less than 72h in the future

* create a valid Invalidation Rule
* change ValidTo to "71"h after the current ValidFrom
* upload Rule
* check that the response had an error
* check that the response had the status code "400"


___
* delete all created rules
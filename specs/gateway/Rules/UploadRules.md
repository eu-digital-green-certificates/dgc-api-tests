# Upload Rules

tags: DGC_GW

Tests to upload new rules

## upload Rule with valid Identifier
* create a valid Invalidation Rule
* upload Rule
* check that the response had no error
* check that Rule is in Rulelist
* delete Rule created

## upload rule with unauthenticated certificate
* create a valid Invalidation Rule
* upload Rule with unauthenticated certificate
* check that the response had an error
* check that Rule is not in Rulelist

## upload rule with authentication certificate of another country
* create a valid Invalidation Rule
* upload Rule with unauthenticated certificate
* check that the response had an error
* check that Rule is not in Rulelist

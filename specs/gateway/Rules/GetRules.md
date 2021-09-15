# Get Rules

tags: DGC_GW, Rules

All Tests for downloading Rules from the Gateway

## get list of onboarded countries

Get all onboarded countries. Should have at least the own country in the list.

* get all onboarded countries
* check that the response had no error
* check that the response had the status code "200"
* check that own country is in onboared countries list

## get list of onboarded countries with unauthenticated certificate

tags: negative_test

Get all onboarded countries with unauthenticated NBTLS. Should lead to an error.

* create custom authentication certificate
* get all onboarded countries with custom certificate
* check that the response had an error
* check that the response had the status code "401" or None

## download all rules

Download Rules of all Countries.

* get all onboarded countries
* download rules of all countries
* check that all responses had no error
* check that all responses had the status code "200"


## download rules with unauthenticated certificate

tags: negative_test

Get Rules from any country with an unauthenticated NBTLS. Should lead to an error.

* get all onboarded countries
* create custom authentication certificate
* download rules of all countries with custom certificate
* check that all repsonses had an error
* check that all responses had the status code "401" or None

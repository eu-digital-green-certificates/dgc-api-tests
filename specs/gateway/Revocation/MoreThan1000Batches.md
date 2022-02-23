# Tests gateway behaviour if there are more than 1000 batches on the gateway

tags: DGC_GW, Revocation

* get the trustList with the type "UPLOAD"

Test-Cases for the gateway if more than 1000 batches are on it. Because of this requirement these Test-Cases are usually
disabled. If there are not enough batches on the gateway the 'Upload more than 1000 batches' Script can be used, but I
wouldn't recommend it.

| days_ago |
|----------|
|    100000|

## Download revocation list from <days_ago> days ago

* Remove this step to enable this Test-Case.
* Reference "TXR-5702"
* use default certificates
* download revocation list from <days_ago> days ago
* check that the response had no error
* check that only results from <days_ago> days ago are in the response
* check that the response had no error
* check that there are more batches
* check that revocation list is full
* check that batches are sorted by ascending date
* download revocation list with If-Modified-Since after last list
* check that the response had no error
* check that revocation list is not empty
* check that the last batch from the last revocation list is not in the new list

## Upload more than 1000 batches

* Remove this step to run this script. (Setup for TXR-5702, might take hours and also puts the gw under heavy load)
* use default certificates
* upload "1010" batches for country "DX"

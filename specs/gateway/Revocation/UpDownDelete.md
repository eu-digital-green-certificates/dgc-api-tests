# Upload, download and delete revocation lists

tags: DGC_GW, Revocation

* get the trustList with the type "UPLOAD"

Test cases for the upload and download of revocation lists 

## Country A uploads, country B downloads

Country A creates a revocation list and encrypts it for country B. 
Country B proceeds to download the list 

* create a revocation list of type "UVCI" with "500" entries
* add revocation list recipient "DE"
* add revocation list recipient "BE"
* encrypt and sign CMS as "DX"
* upload CMS as "DX"
* download CSM as "DE"

## Operation


### ssl_check

This Operation check if the domain has a valid SSL certificate.

The app download the ssl certificate and read it to find when expire and set a status for the domain:

| Code 	| Info                                                         	|
|------	|--------------------------------------------------------------	|
|  OK  	|           There are more than 30 day before expired          	|
|  KO  	|                 Expired or no SSL certificate                	|
|  XX  	| There are less than 30 day before expire but is not expired 	|

### dns_lookup
Save the DNS lookup for the domain in question. Get ONE DNS lookup son, if you change it recently, can be the old records.

### dns_checker

Make a whois and save the domain expiration day.

| Code 	| Info                                                         	|
|------	|--------------------------------------------------------------	|
|  OK  	|           There are more than 30 day before expired          	|
|  KO  	|                 Error with the domain                       	|
|  XX  	| There are less than 30 day before expire but is not expired 	|


### page_checker

Get the status code of the url. It is consider an "Error status" if is not between 200 and 399.

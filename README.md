# Authorize.net Accept Hosted
---
Setup application with a virtual environment for Python 3.12
Install packages:
* authorizenet
* python-dotenv
* flask 

To setup the environment variables:
* Setup a .env file
* Set "AUTHORIZE_LOGIN" to the Authorize.net Login ID
* Set "AUTHORIZE_KEY" to the Authorize.net Transaction Key 

Flask Routes 
* /create - creates a customer
* /find - find the customer and the payment profiles
* /delete - delete the customer
* /payment - provides a page with a token to redirect to the accept hosted page 


# Authorize.net Accept Hosted
---
Setup application with a virtual environment for Python 3.12
Activate the corresponding virtual environment

Install packages (requirements.txt added - "make install_deps"):
* cryptography
* authorizenet
* python-dotenv
* flask

To setup the environment variables:
* Setup a .env file
* Set "AUTHORIZE_LOGIN" to the Authorize.net Login ID
* Set "AUTHORIZE_KEY" to the Authorize.net Transaction Key 

Use flask_ssl to run an adhoc ssl instantce. Required for setting up the iframe communicator.

Also for ease of use "make flask_ssl_watch"

Page is set to create a profile for interactions. Simple actions for creating a response and validating the transactions. Get Embedded Payment either retrieves the last created token or sets a new one for ease of use.


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
* Set "AUTHORIZE_LOGIN" to the Authorize.net API Login ID
* Set "AUTHORIZE_KEY" to the Authorize.net API Transaction Key 
* Set "AUTHORIZE_CLIENT_KEY" to be the Authorize.net Client Key 

The Makefile is provided with several commands for ease of use:
* "flask" - run the app using the flask command
* "flask_watch" - run the app with watch enabled for server reload on save
* "flask_ssl" - run the app with an adhoc certificate for SSL
* "flask_ssl_watch" - run the app with an adhoce certificate + watch enabled for reload on save

NOTE: To utilize the custom payment form action please use one of the ssl commands. HTTPS needs to be enabled for communication for this form. Another option for HTTPS, if needed, is to use a reverse proxy service (ngrok, tunnelmole etc.).
 
Page is set to create a profile for interactions. Simple actions for creating a response and validating the transactions. 

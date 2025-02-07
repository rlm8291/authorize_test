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

Use "make flask_ssl" to run an adhoc ssl instantce. Required for setting up the iframe communicator.

Also for ease of use "make flask_ssl_watch" is available for development.

Page is set to create a profile for interactions. Simple actions for creating a response and validating the transactions. "Get Embedded Payment" either retrieves the last created token or sets a new one for ease of use.

One route has been added for testing:
* /dev_token - this requires a JSON Object be posted. It will respond with a token
    - this endpoint is expected to receive an JSON Object 

    ```json
        {'firstName': '', 'lastName': '', 'iframe_url': ''}
    ```

For the iframe_url it has to be the iframe_communicator HTML file hosted on the same domain as the location the embedded payment form.

An example of this setup is present within the application. Refer to /payment_page under app.py.

from flask import Flask, render_template
from dotenv import dotenv_values
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import * 

from funcs import create_customer, find_customer, delete_customer, accept_host_page

config = dotenv_values(".env")
print(config)

customer = create_customer()
profileId = str(customer.customerProfileId)

find_customer(profileId)

app = Flask(__name__)

@app.route("/")
def hello_payment():
    return "<p>Hellope!!!</p>"

@app.route("/payment")
def get_payment():
    token = accept_host_page(profileId).token
    return render_template("payment.html", token=token)

@app.route("/find")
def find():
    find_customer(profileId)
    return "<p>FOUND</p>"

@app.route("/delete")
def delete():
    print(profileId)
    delete_customer(profileId)
    return "<p>Deleted Customer</p>"


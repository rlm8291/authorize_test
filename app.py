from flask import Flask, render_template
from dotenv import dotenv_values
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import * 

from funcs import create_customer, find_customer, delete_customer, accept_host_page

config = dotenv_values(".env")
print(config)

profile = {
    "id": ""
}

app = Flask(__name__)

@app.route("/")
def hello_payment():
    return "<p>Hellope!!!</p>"

@app.route("/create")
def create():
    customer = create_customer()
    profile["id"] = str(customer.customerProfileId)
    return "<p>CREATED</p>"

@app.route("/find")
def find():
    find_customer(profile["id"])
    return "<p>FOUND</p>"

@app.route("/delete")
def delete():
    delete_customer(profile["id"])
    return "<p>Deleted Customer</p>"

@app.route("/payment")
def get_payment():
    token = accept_host_page(profile["id"]).token
    return render_template("payment.html", token=str(token))
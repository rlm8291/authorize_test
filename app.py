from flask import Flask, render_template
from dotenv import dotenv_values

from funcs import create_customer, find_customer, delete_customer, accept_host_page

config = dotenv_values(".env")
print(config)

profile = {"id": ""}

app = Flask(__name__)


@app.route("/")
def hello_payment():
    return render_template("main.html", response="Push any of the buttons to test a route")


@app.route("/create")
def create():
    customer = create_customer()
    profile["id"] = str(customer.customerProfileId)
    return render_template("main.html", profileId=profile["id"])


@app.route("/find")
def find():
    customer = find_customer(profile["id"])
    return render_template("find.html", customer=customer)


@app.route("/delete")
def delete():
    delete_customer(profile["id"])
    return render_template("delete.html")


@app.route("/payment")
def get_payment():
    token = accept_host_page(profile["id"]).token
    return render_template("payment.html", token=str(token))


@app.route("/test", methods=["POST"])
def test():
    return render_template("response.html", response="Hello HTMX!!!!")
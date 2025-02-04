from flask import Flask, render_template, redirect
from dotenv import dotenv_values
from funcs import create_customer, find_customer, delete_customer, accept_host_page

config = dotenv_values(".env")
print(config)

profile = {"id": ""}

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_payment():
    new_customer = create_customer()
    profile["id"] = new_customer["profileId"]
    return render_template("main.html", response=new_customer["response"])


@app.route("/find", methods=["GET"])
def find():
    if bool(profile["id"]) is not True:
        new_customer = create_customer()
        profile["id"] = new_customer["profileId"]
        return render_template("response.html", response=new_customer["response"])

    customer = find_customer(profile["id"])
    return render_template("response.html", response=customer)


@app.route("/delete", methods=["DELETE"])
def delete():
    deleted_customer = delete_customer(profile["id"])
    profile["id"] = ""
    return render_template("response.html", response=deleted_customer)


@app.route("/payment_token", methods=["POST"])
def get_payment():
    response_token = accept_host_page(profile["id"])
    return render_template("response.html", response=response_token)


@app.route("/test", methods=["POST"])
def test():
    return render_template("response.html", response="Hello HTMX!!!!")

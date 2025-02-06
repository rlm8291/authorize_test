from flask import Flask, render_template, request
from json import loads, dumps
from dotenv import dotenv_values
from funcs import create_customer, find_customer, delete_customer, accept_host_page

config = dotenv_values(".env")
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
    return render_template(
        "response.html",
        response=response_token["response"],
        token=response_token["token"],
    )


@app.route("/payment_page", methods=["POST"])
def send_payment():
    return render_template("embedded_payment.html", token=request.values["token"])


@app.route("/receipt", methods=["POST"])
def send_receipt():
    details = request.values["iframe_response"]
    parsed = loads(details)
    formatted = dumps(parsed, indent=2)

    return render_template("receipt.html", content=formatted)

from flask import Flask, render_template, redirect
from dotenv import dotenv_values
from funcs import (
    create_customer,
    find_customer,
    get_customer_subscriptions,
    get_unsettled_transaction_list,
    get_customer_profile_transaction_list,
    delete_customer,
)


config = dotenv_values(".env")
profile = {"id": ""}
app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_payment():
    if profile["id"] != "":
        customer = find_customer(profile["id"])
        return render_template("main.html", response=customer)

    new_customer = create_customer()
    profile["id"] = new_customer["profileId"]
    return render_template("main.html", response=new_customer["response"])


@app.route("/find", methods=["GET"])
def search_customer():
    if profile["id"] == "":
        new_customer = create_customer()
        profile["id"] = new_customer["profileId"]
        return render_template("response.html", response=new_customer["response"])

    customer = find_customer(profile["id"])
    return render_template("response.html", response=customer)


@app.route("/get_unsettled_transactions", methods=["GET"])
def unsettled_transactions():
    unsettled_transactions = get_unsettled_transaction_list()
    return render_template("response.html", response=unsettled_transactions)


@app.route("/get_transactions", methods=["GET"])
def get_transactions():
    if profile["id"] == "":
        return render_template("action_required.html")

    customer_transactions = get_customer_profile_transaction_list(profile["id"])
    return render_template("response.html", response=customer_transactions)


@app.route("/get_subscriptions", methods=["GET"])
def get_subscriptions():
    subscriptions = get_customer_subscriptions()
    return render_template("response.html", response=subscriptions)


@app.route("/reset", methods=["PUT"])
def reset_customer():
    if profile["id"] == "":
        return render_template("action_required.html")
    
    deleted_customer = delete_customer(profile["id"])

    if deleted_customer["result"] != "Ok":
        return render_template("response.html", response=deleted_customer)

    new_customer = create_customer("Delete")
    profile["id"] = new_customer["profileId"]

    return render_template("response.html", response=new_customer["response"])

@app.route("/delete", methods=["DELETE"])
def delete():
    if profile["id"] == "":
        return render_template("action_required.html")
    
    deleted_customer = delete_customer(profile["id"])
    
    if deleted_customer["result"] == "Ok":
        profile["id"] = ""

    return render_template("response.html", response=deleted_customer)


@app.route("/get_hosted_form", methods=["GET"])
def get_payment():
    client = {
        "login": config["AUTHORIZE_LOGIN"],
        "key": config["AUTHORIZE_CLIENT_KEY"]
    }

    return render_template("accept_ui_form.html", client=client)


@app.route("/custom_payment", methods=["GET"])
def custom_payment():
    client = {
        "login": config["AUTHORIZE_LOGIN"],
        "key": config["AUTHORIZE_CLIENT_KEY"]
    }

    return render_template("custom_form.html", client=client)


from flask import Flask, render_template, request
from dotenv import dotenv_values
from json import loads
from funcs import (
    create_customer,
    find_customer,
    get_customer_subscriptions,
    get_unsettled_transaction_list,
    get_customer_profile_transaction_list,
    delete_customer,
    create_payment_transaction,
    save_payment_profile,
    save_customer_profile_from_transaction
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
        "key": config["AUTHORIZE_CLIENT_KEY"],
        "text": "Use the Hosted Add Payment Method button above to get a Opaque Payment Data object"
    }

    return render_template("accept_ui_form.html", client=client, profile=profile["id"])


@app.route("/custom_form", methods=["GET"])
def custom_form():
    client = {
        "login": config["AUTHORIZE_LOGIN"],
        "key": config["AUTHORIZE_CLIENT_KEY"],
        "text": "Use the Add Payment Method button above to get a Opaque Payment Data object"
    }

    return render_template("custom_form.html", client=client, profile=profile["id"])


@app.route("/create_transaction", methods=["POST"])
def create_transaction():
    data = loads(request.values["opaque_data"])
    response = create_payment_transaction(data["opaqueData"])

    return render_template("response.html", response=response["response"])

@app.route("/save_payment", methods=["PUT"])
def save_payment():
    data = loads(request.values["opaque_data"])
    response = save_payment_profile(profile["id"], data["opaqueData"])

    return render_template("response.html", response=response)


@app.route("/ui_form", methods=["GET"])
def ui_forms():
    form = request.values["form"]
    client = {
        "login": config["AUTHORIZE_LOGIN"],
        "key": config["AUTHORIZE_CLIENT_KEY"]
    }
    
    if form == "ui":
        client["text"] = "Use the Hosted Add Payment Method button above to get a Opaque Payment Data object"
        return render_template("reference/accept_ui.html", client=client)
    
    if form == "custom":
        client["text"] = "Use the Add Payment Method button above to get a Opaque Payment Data object"
        return render_template("reference/custom_form_ui.html", client=client)
    

@app.route("/profile_actions", methods=["POST"])
def profile_actions():
    opaque_data = request.values["opaque_data"]
    disabled_profile = "Create a transaction!!!"
    disabled_subscription = "Create a profile!!!"

    return render_template("profile_actions.html", text=opaque_data, opaque_data=opaque_data, disabled_profile=disabled_profile, disabled_subscription=disabled_subscription)


@app.route("/create_profile_transaction", methods=["POST"])
def create_profile_transaction():
    data = loads(request.values["opaque_data"])
    payment = create_payment_transaction(data["opaqueData"])

    response = payment["response"]
    transaction_id = payment["transaction"]
    disabled_subscription = "Create a profile!!!"

    if response["result"] != "Ok":
        return render_template("response.html", response)
    
    return render_template("profile_actions.html", text=response["xml_string"], transaction=transaction_id, disabled_subscription=disabled_subscription)


@app.route("/save_profile", methods=["POST"])
def save_profile():
    transaction = request.values["transaction_id"]
    profile = save_customer_profile_from_transaction(transaction)

    response = profile["response"]
    profile_id = profile["profile_id"]
    disabled_profile = "Profile was created!!!"

    if response["result"] != "Ok":
        return render_template("response.html", response=profile["response"])

    return render_template("profile_actions.html", text=response["xml_string"], profile=profile_id, disabled_profile=disabled_profile)


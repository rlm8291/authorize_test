from flask import Flask, render_template
from dotenv import dotenv_values
from funcs import create_customer, find_customer, delete_customer, accept_host_page

config = dotenv_values(".env")
print(config)

profile = {"id": ""}

app = Flask(__name__)


@app.route("/")
def hello_payment():
    new_customer = create_customer()
    profile["id"] = new_customer["profileId"]
    return render_template("main.html", response=new_customer["response"])


@app.route("/find")
def find():
    customer = find_customer(profile["id"])
    return render_template("response.html", response=customer)


@app.route("/delete", methods=["DELETE"])
def delete():
    deleted_customer = delete_customer(profile["id"])
    return render_template("response.html", response=deleted_customer)


@app.route("/payment")
def get_payment():
    token = accept_host_page(profile["id"]).token
    return render_template("payment.html", token=str(token))


@app.route("/test", methods=["POST"])
def test():
    return render_template("response.html", response="Hello HTMX!!!!")

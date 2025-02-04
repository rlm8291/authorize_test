import random
from lxml import etree as et
from dotenv import dotenv_values
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import (
    createCustomerProfileController,
    getCustomerProfileController,
    deleteCustomerProfileController,
    getHostedPaymentPageController,
)

from decimal import Decimal

config = dotenv_values(".env")


def response_builder(response, message):
    xml_string = et.tostring(response, pretty_print=True).decode()
    return {
        "result": response.messages.resultCode,
        "code": response.messages.message.code,
        "xml_string": xml_string,
        "message": message,
    }


def create_customer():
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    create_customer_profile = apicontractsv1.createCustomerProfileRequest()
    create_customer_profile.merchantAuthentication = merchant_auth
    create_customer_profile.profile = apicontractsv1.customerProfileType(
        "grivia" + str(random.randint(0, 10000)),
        "Geralt of Rivia",
        "geralt@kaermorhen.com",
    )

    controller = createCustomerProfileController(create_customer_profile)
    controller.execute()

    response = controller.getresponse()

    if response.messages.resultCode != "Ok":
        return {
            "profileId": "",
            "response": response_builder(
                response, "Failed to make the witchers profile!!"
            ),
        }

    return {
        "profileId": str(response.customerProfileId),
        "response": response_builder(
            response,
            str("Success! Geralt of Rivias ID is: %s" % response.customerProfileId),
        ),
    }


def find_customer(profileId):
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    get_customer_profile = apicontractsv1.getCustomerProfileRequest()
    get_customer_profile.merchantAuthentication = merchant_auth
    get_customer_profile.customerProfileId = profileId

    controller = getCustomerProfileController(get_customer_profile)
    controller.execute()

    response = controller.getresponse()
    message = ""

    if response.messages.resultCode != "Ok":
        message = "Failed to get the witchers profile!!!"
        return response_builder(response, message)

    message += str(
        "Successfully retrieved the witchers profile. His profile id %s and customer id %s"
        % (
            response.profile.customerProfileId,
            response.profile.merchantCustomerId,
        )
    )
    if hasattr(response.profile, "paqymentProfiles"):
        message += (
            " (Payment Profiles: " + str(len(response.profile.paymentProfiles)) + ")"
        )
    if hasattr(response, "subscriptionIds"):
        message += " (Subscriptions: " + str(len(response.subscriptionIds)) + ")"

    return response_builder(response, message)


def delete_customer(profileId):
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    delete_customer_profile = apicontractsv1.deleteCustomerProfileRequest()
    delete_customer_profile.merchantAuthentication = merchant_auth
    delete_customer_profile.customerProfileId = profileId

    controller = deleteCustomerProfileController(delete_customer_profile)
    controller.execute()

    response = controller.getresponse()

    if response.messages.resultCode != "Ok":
        return response_builder(
            response, "Failed to kill the witcher with your wyvern trap!!!"
        )

    return response_builder(
        response, "Successfully villed the witcher luring him into a nest of wyverns!!!"
    )


def accept_host_page(profileId):
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    payment_button_options = apicontractsv1.settingType()
    payment_button_options.settingName = (
        apicontractsv1.settingNameEnum.hostedPaymentButtonOptions
    )
    payment_button_options.settingValue = '{"text": "Pay"}'

    payment_order_options = apicontractsv1.settingType()
    payment_order_options.settingName = (
        apicontractsv1.settingNameEnum.hostedPaymentOrderOptions
    )
    payment_order_options.settingValue = '{"show": true}'

    hosted_payment_options = apicontractsv1.settingType()
    hosted_payment_options.settingName = (
        apicontractsv1.settingNameEnum.hostedPaymentPaymentOptions
    )
    hosted_payment_options.settingValue = (
        '{"showCreditCard": true, "showBankAccount":false, "cardCodeRequired": true}'
    )

    payment_customer_options = apicontractsv1.settingType()
    payment_customer_options.settingName = (
        apicontractsv1.settingNameEnum.hostedPaymentCustomerOptions
    )
    payment_customer_options.settingValue = '{"addPaymentProfile": true}'

    hosted_payment_security = apicontractsv1.settingType()
    hosted_payment_security.settingName = (
        apicontractsv1.settingNameEnum.hostedPaymentSecurityOptions
    )
    hosted_payment_security.settingValue = '{"captcha": true}'

    payment_billing_options = apicontractsv1.settingType()
    payment_billing_options.settingName = (
        apicontractsv1.settingNameEnum.hostedPaymentBillingAddressOptions
    )
    payment_billing_options.settingValue = '{"show": true, "required": true}'

    settings = apicontractsv1.ArrayOfSetting()
    settings.setting.append(payment_button_options)
    settings.setting.append(payment_order_options)
    settings.setting.append(payment_customer_options)
    settings.setting.append(hosted_payment_options)
    settings.setting.append(hosted_payment_security)

    transaction_request = apicontractsv1.transactionRequestType()
    transaction_request.transactionType = "authCaptureTransaction"
    transaction_request.amount = Decimal(110)
    transaction_request.order = "Witcher-Services-111"
    transaction_request.profile = profileId

    payment_page_request = apicontractsv1.getHostedPaymentPageRequest()
    payment_page_request.merchantAuthentication = merchant_auth
    payment_page_request.transactionRequest = transaction_request
    payment_page_request.hostedPaymentSettings = settings

    payment_page_controller = getHostedPaymentPageController(payment_page_request)
    payment_page_controller.execute()

    response = payment_page_controller.getresponse()

    if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
        print("Successfully paying the witcher his gold!")
        print("Token : %s" % response.token)
    if response.messages is not None:
        print("Message Code : %s" % response.messages.message[0]["code"].text)
        print("Message Text : %s" % response.messages.message[0]["text"].text)

    return response

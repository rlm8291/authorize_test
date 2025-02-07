import random
from dotenv import dotenv_values
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import (
    createCustomerProfileController,
    getHostedPaymentPageController,
)

from decimal import Decimal

config = dotenv_values(".env")


def create_api_customer(first_name, last_name, email):
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    create_customer_profile = apicontractsv1.createCustomerProfileRequest()
    create_customer_profile.merchantAuthentication = merchant_auth
    create_customer_profile.profile = apicontractsv1.customerProfileType(
        first_name + str(random.randint(0, 10000)),
        last_name,
        email,
    )

    controller = createCustomerProfileController(create_customer_profile)
    controller.execute()

    response = controller.getresponse()
    if response.messages.resultCode != apicontractsv1.messageTypeEnum.Ok:
        return str("Failed to create customer! %s" % response.messages.message.code)

    return str(response.customerProfileId)


def api_accept_host_page(profileId, iframe_url):
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    payment_return_options = apicontractsv1.settingType()
    payment_return_options.settingName = (
        apicontractsv1.settingNameEnum.hostedPaymentReturnOptions
    )
    payment_return_options.settingValue = '{"showReceipt": false}'

    payment_button_options = apicontractsv1.settingType()
    payment_button_options.settingName = (
        apicontractsv1.settingNameEnum.hostedPaymentButtonOptions
    )
    payment_button_options.settingValue = '{"text": "Pay Now"}'

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

    iframe_communicator = apicontractsv1.settingType()
    iframe_communicator.settingName = (
        apicontractsv1.settingNameEnum.hostedPaymentIFrameCommunicatorUrl
    )
    iframe_communicator.settingValue = str('{"url": "%s"}' % iframe_url)

    settings = apicontractsv1.ArrayOfSetting()
    settings.setting.append(payment_return_options)
    settings.setting.append(payment_button_options)
    settings.setting.append(payment_order_options)
    settings.setting.append(payment_customer_options)
    settings.setting.append(hosted_payment_options)
    settings.setting.append(hosted_payment_security)
    settings.setting.append(iframe_communicator)

    transaction_request = apicontractsv1.transactionRequestType()
    transaction_request.transactionType = "authCaptureTransaction"
    transaction_request.amount = Decimal(110)
    transaction_request.order = "Test-Membership-111"
    transaction_request.profile = profileId

    payment_page_request = apicontractsv1.getHostedPaymentPageRequest()
    payment_page_request.merchantAuthentication = merchant_auth
    payment_page_request.transactionRequest = transaction_request
    payment_page_request.hostedPaymentSettings = settings

    payment_page_controller = getHostedPaymentPageController(payment_page_request)
    payment_page_controller.execute()

    response = payment_page_controller.getresponse()

    if response.messages.resultCode != apicontractsv1.messageTypeEnum.Ok:
        return str("Failed to generate payment token: %s" % response.messages.code)

    return response.token

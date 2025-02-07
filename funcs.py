import random
from lxml import etree as et
from dotenv import dotenv_values
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import (
    createCustomerProfileController,
    getCustomerProfileController,
    getUnsettledTransactionListController,
    getTransactionListForCustomerController,
    deleteCustomerProfileController,
    getHostedPaymentPageController,
    ARBGetSubscriptionListController,
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


def create_customer(action=""):
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
    if response.messages.resultCode != apicontractsv1.messageTypeEnum.Ok:
        return {
            "profileId": "",
            "response": response_builder(
                response, "Failed to make the witchers profile!!"
            ),
        }

    response_message = str(
        "Success! Geralt of Rivias ID is: %s" % response.customerProfileId
    )

    if action == "Delete":
        response_message = str(
            "Success! You've killed + revived the witcher! His new ID is: %s"
            % response.customerProfileId
        )

    return {
        "profileId": str(response.customerProfileId),
        "response": response_builder(response, response_message),
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

    if response.messages.resultCode != apicontractsv1.messageTypeEnum.Ok:
        message = "Failed to get the witchers profile!!!"
        return response_builder(response, message)

    message += str(
        "Successfully retrieved the witchers profile. His profile id %s and customer id %s"
        % (
            response.profile.customerProfileId,
            response.profile.merchantCustomerId,
        )
    )
    if hasattr(response.profile, "paymentProfiles"):
        message += (
            " (Payment Profiles: " + str(len(response.profile.paymentProfiles)) + ")"
        )
    if hasattr(response, "subscriptionIds"):
        message += " (Subscriptions: " + str(len(response.subscriptionIds)) + ")"

    return response_builder(response, message)


def get_unsettled_transaction_list():
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    sorting = apicontractsv1.TransactionListSorting()
    sorting.orderBy = apicontractsv1.TransactionListOrderFieldEnum.id
    sorting.orderDescending = True

    paging = apicontractsv1.Paging()
    paging.limit = 20
    paging.offset = 1

    unsettled_transactions_request = apicontractsv1.getUnsettledTransactionListRequest()
    unsettled_transactions_request.merchantAuthentication = merchant_auth
    unsettled_transactions_request.refId = "Sample"
    unsettled_transactions_request.sorting = sorting
    unsettled_transactions_request.paging = paging

    unsettled_transaction_list = getUnsettledTransactionListController(
        unsettled_transactions_request
    )
    unsettled_transaction_list.execute()

    response = unsettled_transaction_list.getresponse()

    return response_builder(response, "Retrieved all unsettled payments!")


def get_customer_profile_transaction_list(profileId):
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    transaction_customer_list = apicontractsv1.getTransactionListForCustomerRequest()
    transaction_customer_list.merchantAuthentication = merchant_auth
    transaction_customer_list.customerProfileId = profileId

    transaction_customer_list = getTransactionListForCustomerController(
        transaction_customer_list
    )
    transaction_customer_list.execute()

    response = transaction_customer_list.getresponse()

    if response.messages.resultCode != apicontractsv1.messageTypeEnum.Ok:
        return response_builder(
            response, "Failed to retrieve the witchers transactions!!!"
        )

    return response_builder(
        response, "Rectrieved a list of the witchers transactions!!!"
    )


def get_customer_subscriptions():
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    sorting = apicontractsv1.ARBGetSubscriptionListSorting()
    sorting.orderBy = apicontractsv1.ARBGetSubscriptionListOrderFieldEnum.id
    sorting.orderDescending = True

    paging = apicontractsv1.Paging()
    paging.limit = 20
    paging.offset = 1

    subscription_list_request = apicontractsv1.ARBGetSubscriptionListRequest()
    subscription_list_request.merchantAuthentication = merchant_auth
    subscription_list_request.searchType = (
        apicontractsv1.ARBGetSubscriptionListSearchTypeEnum.subscriptionActive
    )
    subscription_list_request.sorting = sorting
    subscription_list_request.paging = paging

    subscription_list_controller = ARBGetSubscriptionListController(
        subscription_list_request
    )
    subscription_list_controller.execute()

    response = subscription_list_controller.getresponse()

    if response.messages.resultCode != apicontractsv1.messageTypeEnum.Ok:
        return response_builder(
            response, "Failed to retrieve the witchers list of subscriptions!!!"
        )

    return response_builder(
        response, "Successfully retrieved the witchers list of subscriptions!!!"
    )


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

    if response.messages.resultCode != apicontractsv1.messageTypeEnum.Ok:
        return response_builder(
            response, "Failed to kill the witcher with your wyvern trap!!!"
        )

    return response_builder(
        response, "Successfully killed the witcher luring him into a nest of wyverns!!!"
    )


def accept_host_page(profileId):
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
    iframe_communicator.settingValue = (
        '{"url": "https://127.0.0.1:5000/static/communicator.html"}'
    )

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
    transaction_request.order = "Witcher-Services-111"
    transaction_request.profile = profileId

    payment_page_request = apicontractsv1.getHostedPaymentPageRequest()
    payment_page_request.merchantAuthentication = merchant_auth
    payment_page_request.transactionRequest = transaction_request
    payment_page_request.hostedPaymentSettings = settings

    payment_page_controller = getHostedPaymentPageController(payment_page_request)
    payment_page_controller.execute()

    response = payment_page_controller.getresponse()

    if response.messages.resultCode != apicontractsv1.messageTypeEnum.Ok:
        return {
            "token": "",
            "response": response_builder(
                response, "Failed to generate a pyament page to collect your gold!"
            ),
        }

    return {
        "token": response.token,
        "response": response_builder(
            response,
            "Successfully setup a payment page to earn your gold from the witcher!!!",
        ),
    }

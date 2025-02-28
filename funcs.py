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
    ARBGetSubscriptionListController,
    createTransactionController,
    createCustomerPaymentProfileController, 
    createCustomerProfileFromTransactionController
)


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
        "Test" + str(random.randint(0, 10000)),
        "Tester",
        "test@test.com",
    )

    controller = createCustomerProfileController(create_customer_profile)
    controller.execute()

    response = controller.getresponse()
    if response.messages.resultCode != apicontractsv1.messageTypeEnum.Ok:
        return {
            "profileId": "",
            "response": response_builder(
                response, "Failed to make Test Tester's profile!"
            ),
        }

    response_message = str(
        "Success! Test Tester's ID is: %s" % response.customerProfileId
    )

    if action == "Delete":
        response_message = str(
            "Success! You've reset Test Tester's profile! Their new ID is: %s"
            % response.customerProfileId
        )

    return {
        "profileId": str(response.customerProfileId),
        "response": response_builder(response, response_message),
    }


def find_customer(profile_id):
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    get_customer_profile = apicontractsv1.getCustomerProfileRequest()
    get_customer_profile.merchantAuthentication = merchant_auth
    get_customer_profile.customerProfileId = profile_id

    controller = getCustomerProfileController(get_customer_profile)
    controller.execute()

    response = controller.getresponse()

    if response.messages.resultCode != apicontractsv1.messageTypeEnum.Ok:
        message = "Failed to get Test Tester's profile!"
        return response_builder(response, message)

    message = str(
        "Successfully retrieved Test Tester's profile. Their profile id %s and customer id %s"
        % (
            response.profile.customerProfileId,
            response.profile.merchantCustomerId,
        )
    )

    formatted_response = response_builder(response, message)

    if hasattr(response.profile, "paymentProfiles"):
        formatted_response["payment_profiles"] = (
            "(Payment Profiles: " + str(len(response.profile.paymentProfiles)) + ")"
        )

    if hasattr(response, "subscriptionIds"):
        formatted_response["subscriptions"] += "| (Subscriptions: " + str(len(response.subscriptionIds)) + ")"

    return formatted_response


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


def get_customer_profile_transaction_list(profile_id):
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    transaction_customer_list = apicontractsv1.getTransactionListForCustomerRequest()
    transaction_customer_list.merchantAuthentication = merchant_auth
    transaction_customer_list.customerProfileId = profile_id

    transaction_customer_list = getTransactionListForCustomerController(
        transaction_customer_list
    )
    transaction_customer_list.execute()

    response = transaction_customer_list.getresponse()

    if response.messages.resultCode != apicontractsv1.messageTypeEnum.Ok:
        return response_builder(
            response, "Failed to retrieve Test Tester's transactions!"
        )

    return response_builder(
        response, "Rectrieved a list of Test Tester's transactions!"
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
            response, "Failed to retrieve Test Tester's list of subscriptions!"
        )

    return response_builder(
        response, "Successfully retrieved Test Tester's list of subscriptions!"
    )


def delete_customer(profile_id):
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    delete_customer_profile = apicontractsv1.deleteCustomerProfileRequest()
    delete_customer_profile.merchantAuthentication = merchant_auth
    delete_customer_profile.customerProfileId = profile_id

    controller = deleteCustomerProfileController(delete_customer_profile)
    controller.execute()

    response = controller.getresponse()

    if response.messages.resultCode != apicontractsv1.messageTypeEnum.Ok:
        return response_builder(response, "Failed to delete Test Tester's profile!")

    return response_builder(response, "Successfully deleted Test Tester's profile!")


def create_payment_transaction(data):
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    refId = "ref {}".format(random.randint(0, 100000))    

    opaque_data = apicontractsv1.opaqueDataType()
    opaque_data.dataDescriptor = data["dataDescriptor"]
    opaque_data.dataValue = data["dataValue"]

    payment_method = apicontractsv1.paymentType()
    payment_method.opaqueData = opaque_data
    
    order = apicontractsv1.orderType()
    order.invoiceNumber = str(random.randint(0, 100000))
    order.description = "Black Teapot"
    
    customer_address = apicontractsv1.customerAddressType()
    customer_address.firstName = "Test"
    customer_address.lastName = "Tester"
    customer_address.address = "14 Test Street"
    customer_address.city = "Test Springs"
    customer_address.state = "TX"
    customer_address.zip = "101010"
    customer_address.country = "USA"
    
    customer_data = apicontractsv1.customerDataType()
    customer_data.type = "individual"
    customer_data.id = "99999456654"
    customer_data.email = "test@test.com"
    
    duplicate_window_setting = apicontractsv1.settingType()
    duplicate_window_setting.settingName = "duplicateWindow"
    duplicate_window_setting.settingValue = "418"
    settings = apicontractsv1.ArrayOfSetting()
    settings.setting.append(duplicate_window_setting)

    transaction_request = apicontractsv1.transactionRequestType()
    transaction_request.transactionType = "authCaptureTransaction"
    transaction_request.amount = 418.00
    transaction_request.order = order
    transaction_request.payment = payment_method
    transaction_request.billTo = customer_address
    transaction_request.customer = customer_data
    transaction_request.transactionSettings = settings

    create_transaction_request = apicontractsv1.createTransactionRequest()
    create_transaction_request.merchantAuthentication = merchant_auth
    create_transaction_request.refId = refId
    create_transaction_request.transactionRequest = transaction_request
    
    create_transaction_controller = createTransactionController(create_transaction_request)
    create_transaction_controller.execute()

    response = create_transaction_controller.getresponse()

    if response.messages.resultCode != apicontractsv1.messageTypeEnum.Ok:
        return response_builder(response, "Failed to create a transaction with the opaque data!")

    return {
        "transaction": response.transactionResponse.transId,
        "response": response_builder(response, "Successfully created a transaction with the opaque data!")
    }


def save_payment_profile(profile_id, data):
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    opaque_data = apicontractsv1.opaqueDataType()
    opaque_data.dataDescriptor = data["dataDescriptor"]
    opaque_data.dataValue = data["dataValue"]

    payment_method = apicontractsv1.paymentType()
    payment_method.opaqueData = opaque_data

    bill_to = apicontractsv1.customerAddressType()
    bill_to.firstName = "Test" + str(random.randint(0, 10000))
    bill_to.lastName = "Test" + str(random.randint(0, 10000))

    payment_profile = apicontractsv1.customerPaymentProfileType()
    payment_profile.payment = payment_method
    payment_profile.billTo = bill_to

    create_payment_profile = apicontractsv1.createCustomerPaymentProfileRequest()
    create_payment_profile.merchantAuthentication = merchant_auth
    create_payment_profile.paymentProfile = payment_profile
    create_payment_profile.customerProfileId = profile_id

    payment_profile_controller = createCustomerPaymentProfileController(create_payment_profile)
    payment_profile_controller.execute()

    response = payment_profile_controller.getresponse()

    if response.messages.resultCode != apicontractsv1.messageTypeEnum.Ok:
        return response_builder(response, "Failed to save the payment profile!!!")
    
    return response_builder(response, "Successfully saved the payment profile with opaque data!!!")


def save_customer_profile_from_transaction(transaction_id):
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    profile = apicontractsv1.customerProfileBaseType()
    profile.merchantCustomerId = str(random.randint(0, 100000))

    create_profile_from_transaction = apicontractsv1.createCustomerProfileFromTransactionRequest()
    create_profile_from_transaction.merchantAuthentication = merchant_auth
    create_profile_from_transaction.transId = transaction_id
    create_profile_from_transaction.customer = profile

    profile_controller = createCustomerProfileFromTransactionController(create_profile_from_transaction)
    profile_controller.execute()

    response = profile_controller.getresponse()

    if response.messages.resultCode != apicontractsv1.messageTypeEnum.Ok:
        return {
            "profile_id": "",
            "response": response_builder(response, "Failed to create a customer profile from the transaction!!!")
        }
    
    return {
        "profile_id": response.customerProfileId,
        "response": response_builder(response, "")
    }


import random
from dotenv import dotenv_values
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *

from decimal import Decimal

config = dotenv_values(".env")

def create_customer():
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    create_customer_profile = apicontractsv1.createCustomerProfileRequest()
    create_customer_profile.merchantAuthentication = merchant_auth
    create_customer_profile.profile = apicontractsv1.customerProfileType("grivia" + str(random.randint(0,10000)), "Geralt of Rivia", "geralt@kaermorhen.com")

    controller = createCustomerProfileController(create_customer_profile)
    controller.execute()

    response = controller.getresponse()

    if (response.messages.resultCode == "Ok"):
        print("Success! Geralt of Rivias ID is: %s" % response.customerProfileId)
    else:
        print("Failed to make the witchers profile!!")

    return response

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

    if (response.messages.resultCode=="Ok"):
        print("Successfully retrieved the witchers profile. His profile id %s and customer id %s" % (get_customer_profile.customerProfileId, response.profile.merchantCustomerId))
        if hasattr(response, 'profile') == True:
            if hasattr(response.profile, 'paymentProfiles') == True:
                for paymentProfile in response.profile.paymentProfiles:
                    print("paymentProfile in get_customerprofile is: %s" % paymentProfile)
                    print("Payment Profile ID %s" % str(paymentProfile.customerPaymentProfileId))
        if hasattr(response, 'subscriptionIds') == True:
            if hasattr(response.subscriptionIds, 'subscriptionId') == True:
                print("list of subscriptionid:")
                for subscriptionid in (response.subscriptionIds.subscriptionId):
                    print(subscriptionid)
    else:
        print("response code: %s" % response.messages.resultCode)
        print("Failed to get customer profile information with id %s" % get_customer_profile.customerProfileId)

    return response

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

    if (response.messages.resultCode == "Ok"):
        print("Successfully killed the witcher luring him into a nest of wyverns!!!")
    else:
        print("Failed to kill the witcher with a trap!!!")

    return response

def accept_host_page(profileId):
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = config["AUTHORIZE_LOGIN"]
    merchant_auth.transactionKey = config["AUTHORIZE_KEY"]

    payment_button_options = apicontractsv1.settingType()
    payment_button_options.settingName = apicontractsv1.settingNameEnum.hostedPaymentButtonOptions
    payment_button_options.settingValue = "{\"text\": \"Pay\"}"

    payment_order_options = apicontractsv1.settingType()
    payment_order_options.settingName = apicontractsv1.settingNameEnum.hostedPaymentOrderOptions
    payment_order_options.settingValue = "{\"show\": false}"

    settings = apicontractsv1.ArrayOfSetting()
    settings.setting.append(payment_button_options)
    settings.setting.append(payment_order_options)

    transaction_request = apicontractsv1.transactionRequestType()
    transaction_request.transactionType = "authCaptureTransaction"
    transaction_request.amount = Decimal(110)

    payment_page_request = apicontractsv1.getHostedPaymentPageRequest()
    payment_page_request.merchantAuthentication = merchant_auth
    payment_page_request.transactionRequest = transaction_request
    payment_page_request.hostedPaymentSettings = settings

    payment_page_controller = getHostedPaymentPageController(payment_page_request)
    payment_page_controller.execute()

    response = payment_page_controller.getresponse()

    if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
        print('Successfully paying the witcher his gold!')
        print('Token : %s' % response.token)
    if response.messages is not None:
        print('Message Code : %s' % response.messages.message[0]['code'].text)
        print('Message Text : %s' % response.messages.message[0]['text'].text)

    return response

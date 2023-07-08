from django.conf import settings
from twilio.rest import Client

import random 

ACCOUNT_SID='AC77ce7b3192872803a56df59d644c417e'
AUTH_TOKEN='0e949d1c3c43c626e0d4e72acdc25dc4'

class MessaHandler:
    phone_number=None
    otp=None
    def __init__(self,phone_number,otp)-> None:
        self.phone_number=phone_number
        self.otp=otp

    def send_otp_on_mobile(self):
        client=Client(ACCOUNT_SID,AUTH_TOKEN)
        message = client.messages.create(
        body=f"Your OTP is {self.otp}",
        from_="+18145095269",
        to=self.phone_number)





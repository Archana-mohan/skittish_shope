from django.conf import settings
from twilio.rest import Client

import random 

ACCOUNT_SID='ACc70a61b98d26ab2f718c0e4ddca0ea4a'
AUTH_TOKEN='15ba5bd18933f9331b3c862c059e1898'

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
        from_="+15416381134",
        to=self.phone_number)





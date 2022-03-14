import os
from twilio.rest import Client
import twilio_mod.Threat


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def sendMessage(threat = Threat("None", 0)): 

    if threat.level > 0 :

        message = client.messages.create(
                                    body='Threat Detected \n Type: {}',
                                    from_='+918822334422',
                                    to='+919884051234'
                                    )
        print(message.sid)

def sendWhatsApp(threat = Threat("None", 0)): 
    if threat.level > 0 :
        message = client.messages.create(
                              body='Hello there!',
                              from_='whatsapp:+14155238886',
                              to='whatsapp:+15005550006'
                              )
        print(message.sid)
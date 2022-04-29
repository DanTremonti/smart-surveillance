import os
from twilio.rest import Client
from twilio_mod.Threat import Threat


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

class send: 

    def __init__(self):
        self.account_sid = os.environ['TWILIO_ACCOUNT_SID']
        self.auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(self.account_sid, self.auth_token)
        self.can_send_message = True

    def sendMessage(self,threat = Threat("None", 0)): 

        if threat.level > 0 and self.can_send_message:
            message = 'Threat Detected \nType: ' + threat.type
            message = self.client.messages.create(
                                        body=message,
                                        from_='+19897350611',
                                        to='+917373025959'
                                        )
            print(message.sid)

    def sendWhatsApp(self,threat = Threat("None", 0)): 
        if threat.level > 0 and self.can_send_message:
            message = client.messages.create(
                                body='Threat Detected \n Type: {threat.type}',
                                from_='whatsapp:+1989735061',
                                to='whatsapp:+917373025959'
                                )
            print(message.sid)
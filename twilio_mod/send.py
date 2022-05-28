from ast import arg
import twilio_mod.env as my_environ
from twilio.rest import Client
from twilio_mod.Threat import Threat
import twilio_mod.upload_file as my_uploader
import threading


class send: 

    def __init__(self):
        self.account_sid = my_environ.env_keys['TWILIO_ACCOUNT_SID']
        self.auth_token = my_environ.env_keys['TWILIO_AUTH_TOKEN']
        self.sms_num = my_environ.env_keys['SMS_NUM']
        self.whatspp_num = my_environ.env_keys['WHATSAPP_NUM']
        self.client = Client(self.account_sid, self.auth_token)
        self.can_send_message = True

    def sendMessage(self,message_text: str): 
        message = self.client.messages.create(
                                    body=message_text,
                                    from_=self.sms_num,
                                    to='+917373025959'
                                    )
        print(message.sid)
        print("SMS alert sent")

    def sendWhatsApp(self,message_text: str): 
        message = self.client.messages.create(
                            body=message_text,
                            from_=self.whatspp_num,
                            to='whatsapp:+917373025959'
                            )
        print(message.sid)
        print("Whatsapp sent")


    def sendAlert(self, path: str, threat = Threat('None', 0)):
        if threat.level > 0 and self.can_send_message: 
            print("Sending alert.....")
            message_text = 'Threat Detected \nType: ' + threat.type
            self.smsThread = threading.Thread(target=self.sendMessage, args=(message_text,), daemon=True)
            self.smsThread.start()
            self.whatsAppThread = threading.Thread(target=self.sendWhatsApp, args=(path, message_text), daemon=True)
            self.whatsAppThread.start()
            self.can_send_message = False


    def sendWhatsApp(self, path: str, message_text: str): 
        result = my_uploader.upload_cimage(path, 'threat')
        url = result.get('url')
        path_dict = [url]
        message = self.client.messages.create(
                            body=message_text,
                            media_url=path_dict,
                            from_=self.whatspp_num,
                            to='whatsapp:+917373025959'
                            )
        print(message.sid)
        print("Whatsapp Alert Sent")
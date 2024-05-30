from twilio.rest import Client
import os

class NotificationManager:
    def __init__(self):
        self.client = Client(os.environ['twilio_sid'], os.environ['twilio_token'])

    def send_message(self, message_body):
        message = self.client.messages.create(from_=os.environ['twilio_number'],
                                              body=message_body,
                                              to=os.environ['personal_number'])

        print(message.sid)

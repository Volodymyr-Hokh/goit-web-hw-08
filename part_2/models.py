from mongoengine import Document
from mongoengine.fields import StringField, BooleanField


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone_number = StringField(required=True)
    choice_for_message = StringField(default='email')
    send_email = BooleanField(default=False)
    send_sms = BooleanField(default=False)
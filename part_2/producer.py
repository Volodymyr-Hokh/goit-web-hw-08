import random

from faker import Faker

import connect_mongo
from connect_rabbitmq import channel, connection
from models import Contact


faker = Faker('uk-UA')
message_options = ['sms', 'email']

channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')


def generate_random_contacts(amount: int) -> list[dict]:
    result = []
    for _ in range(amount):
        result.append({
            'fullname': faker.name(),
            'email': faker.email(),
            'phone_number': faker.msisdn(),
            'choice_for_message': random.choice(message_options),
            'send_email': False,
            'send_sms': False
        })
    return result


def save_to_db(contacts: list[dict]):
    for contact_data in contacts:
        contact = Contact(**contact_data)
        contact.save()

        if contact.choice_for_message == 'email' and not contact.send_email:
            channel.basic_publish(exchange='', routing_key='email_queue', body=str(contact.id).encode())

        elif contact.choice_for_message == 'sms' and not contact.send_sms:
            channel.basic_publish(exchange='', routing_key='sms_queue', body=str(contact.id).encode())

    connection.close()


if __name__ == '__main__':
    contacts = generate_random_contacts(100)
    save_to_db(contacts)
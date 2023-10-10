from connect_rabbitmq import channel
import connect_mongo
from models import Contact


channel.queue_declare(queue='sms_queue')


def send_sms(contact_id):
    contact = Contact.objects.get(id=contact_id)
    print(f"Send sms to {contact.phone_number}")
    contact.send_sms = True
    contact.save()


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    send_sms(contact_id)


if __name__ == '__main__':
    channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
from connect_rabbitmq import channel
import connect_mongo
from models import Contact


channel.queue_declare(queue='email_queue')


def send_email(contact_id):
    contact = Contact.objects.get(id=contact_id)
    print(f"Send email to {contact.email}")
    contact.send_email = True
    contact.save()


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    send_email(contact_id)


if __name__ == '__main__':
    channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
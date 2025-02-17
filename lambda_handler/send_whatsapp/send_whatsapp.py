from twilio.rest import Client
import os

def lambda_handler(event, context):
    user_phone = event.get('phone')
    phone_number = 'whatsapp:+972' + user_phone

    message = event.get('message')

    if not phone_number or not message:
        return {
            "statusCode": 400,
            "body": "Phone and message are required"
        }
    user_phone = user_phone.lstrip('0')
    phone_number = 'whatsapp:+972' + user_phone
    try:

        account_sid = os.environ['ACCOUNT_SID']
        auth_token = os.environ['TWILLO_TOKEN']
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message,
            to=phone_number
        )
        print(message.sid)

        return {
            "statusCode": 200,
            "body": f"Message sent successfully to {phone_number}"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"An error occurred: {str(e)}"
        }

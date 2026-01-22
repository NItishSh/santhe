from twilio.rest import Client
import sendgrid
from sendgrid.helpers.mail import Mail
from fastapi import HTTPException
from config.settings import settings

def send_sms(recipient_id, title, content):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    
    try:
        message = client.messages.create(
            body=f"{title}: {content}",
            from_="YOUR_TWILIO_PHONE_NUMBER",
            to=f"+{recipient_id}"
        )
        return message.sid
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def send_email(recipient_id, title, content):
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    from_email = "your-email@example.com"
    to_email = f"user-{recipient_id}@example.com"  # Replace with actual email logic
    
    mail = Mail(from_email, to_email, subject=title, html_content=content)
    
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        return response.status_code
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def send_in_app_notification(recipient_id, title, content):
    # Implement in-app notification logic here
    pass

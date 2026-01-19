from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse

def send_verification_email(user, request):
    
   
    token = user.generate_email_verification_token()

    
    verification_link = f"{request.scheme}://{request.get_host()}/api/accounts/verify-email/{token}/"

    
    html_message = render_to_string(
        'verify_email.html', 
        {'user': user, 'link': verification_link}
    )

    
    try:
        send_mail(
            subject='Verify Your Email Address',
            message='Please verify your email.',  # plain text fallback
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message
        )
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False 
 
 
def send_password_reset_email(user, request):
    token = user.set_reset_token()
    reset_link = f"{request.scheme}://{request.get_host()}/api/accounts/reset-password-confirm/{token}/"
    
    html_message = render_to_string('reset_password.html', {'user': user, 'link': reset_link})
    
    send_mail(
        subject='Reset Your Password',
        message='Reset your password',  # fallback plain text
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        html_message=html_message
    ) 
    
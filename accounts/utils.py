from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def send_verification_email(user, request):
    token = user.generate_email_verification_token()
    verification_url = request.build_absolute_uri(reverse('accounts:verify-email',kwargs={'token':token}))
    
    subject = 'Verify Your Email Address'
    message = f''' 
    Hello {user.username or user.email},
    Thank you for registering! Please verify your email address by clicking the link below:
    {verification_url}
    
    If you didnot create an account,please ignore this email.
    
    Best regards,
    Your App team'''
    
    try:
        send_mail(
            subject = subject,
            message=message,from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return True

    except Exception as e:
        print(f"Error sending email:{e}")  
        
        return False  
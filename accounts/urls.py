from django.urls import path
from .views import signup,login,verify_email,resend_verification_email

app_name = 'accounts'

urlpatterns = [
    path('signup/',signup,name='signup'),
    path('login/', login, name='login'),
     path('verify-email/<uuid:token>/', verify_email, name='verify-email'),
      path('resend-verification-email/', resend_verification_email, name='resend-verification-email'),
]
from django.urls import path
from .views import signup,login,verify_email,resend_verification_email,password_reset_request, password_reset_confirm

app_name = 'accounts'

urlpatterns = [
    path('signup/',signup,name='signup'),
    path('login/', login, name='login'),
     path('verify-email/<uuid:token>/', verify_email, name='verify-email'),
      path('resend-verification-email/', resend_verification_email, name='resend-verification-email'),
     path('password-reset/', password_reset_request, name='password-reset'),
    path('reset-password-confirm/<uuid:token>/', password_reset_confirm, name='reset-password-confirm'),
]
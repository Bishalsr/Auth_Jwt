🔐 Django REST Authentication System

A secure user authentication system built with Django and Django REST Framework, providing:

Email-based signup and verification

JWT login authentication

Password reset with secure token and expiration

Custom user model

HTML email templates for verification and password reset

This project is ideal for web applications that require secure user management with email verification and token-based authentication.

🚀 Features

User Registration with email and password

Email Verification using UUID token

JWT Login (SimpleJWT) after email verification

Password Reset via secure token

Token Expiration for added security (default: 1 hour)

Email Templates for verification & reset

Clean API responses for frontend integration

🏗️ Tech Stack

Python 3.x

Django 6.x

Django REST Framework

SimpleJWT

SQLite (can switch to PostgreSQL)

SMTP email (Gmail, Mailtrap, etc.)

📂 Project Structure
auth_system/
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── utils.py
│
├── templates/
│   ├── verify_email.html
│   ├── reset_password.html
│
├── auth_system/
│   ├── settings.py
│   ├── urls.py
│
└── manage.py

🔐 User Model (Custom)
class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, null=True, blank=True)
    password_reset_token = models.UUIDField(null=True, blank=True, unique=True)
    password_reset_token_expiry = models.DateTimeField(null=True, blank=True)

📝 API Endpoints
1. Signup

URL: /api/accounts/signup/

Method: POST

Description: Registers a new user. Sends a verification email.

Request Body Example:

{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "StrongPass123!",
  "confirm_password": "StrongPass123!"
}


Response: Success message + email sent status.

2. Login

URL: /api/accounts/login/

Method: POST

Description: Authenticates user and returns JWT tokens. Warns if email not verified.

Request Body Example:

{
  "email": "testuser@example.com",
  "password": "StrongPass123!"
}


Response: User info, JWT tokens, and email verification warning.

3. Verify Email

URL: /api/accounts/verify-email/<uuid:token>/

Method: GET

Description: Verifies the user’s email using a UUID token from the verification email.

Response: Success or error message.

4. Resend Verification Email

URL: /api/accounts/resend-verification-email/

Method: POST

Description: Resends the verification email if the user is not verified.

Request Body Example:

{
  "email": "testuser@example.com"
}


Response: Success message or error.

5. Request Password Reset

URL: /api/accounts/password-reset/

Method: POST

Description: Sends password reset email with secure UUID token (expires after 1 hour).

Request Body Example:

{
  "email": "testuser@example.com"
}


Response: Success message confirming reset email sent.

6. Confirm Password Reset

URL: /api/accounts/reset-password-confirm/<uuid:token>/

Method: POST

Description: Reset password using the UUID token from email.

Request Body Example:

{
  "new_password": "NewStrongPass123!",
  "confirm_password": "NewStrongPass123!"
}


Response: Success or error message if token invalid/expired.

📧 Email Templates

Templates located in auth_system/templates/:

verify_email.html – sent on signup

reset_password.html – sent on password reset request

They are rendered using Django’s render_to_string.

⚙️ Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'

🧪 Setup & Testing
git clone https://github.com/yourusername/auth-system.git
cd auth-system
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver


Use Postman to test all endpoints with the provided request bodies.

🔒 Security Practices

No JWT issued before email verification

UUID tokens for verification and password reset

Tokens expire after a set time

Tokens invalidated after use

📄 License

MIT License

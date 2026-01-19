from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer,LoginSerializer
from .utils import send_verification_email
from .models import User
from django.utils import timezone
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from .utils import send_password_reset_email

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        email_sent = send_verification_email(user,request)
        
        # refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User registered successfully. Please check your email to verify your account.',
            'user':{
                'id': user.id,
                'email':user.email,
                'is_email_verified': user.is_email_verified,
                
            },
            # 'tokens':{
            #     'refresh': str(refresh),
            #     'access':str(refresh.access_token),
            # },
            'email_sent':email_sent,
            
            
        },status=status.HTTP_201_CREATED)
    
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """User login endpoint with email verification status"""
    serializer = LoginSerializer(data= request.data, context ={'request':request})
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        response_data ={
            'message':'Login successful',
            'user': {
                'id':user.id,
                'email':user.email,
               
                'is_email_verified': user.is_email_verified,
                
            },
            'tokens':{
                'refresh':str(refresh),
                'access':str(refresh.access_token),
            }
        }
        
        if not user.is_email_verified:
            response_data['warning'] = 'Please verify your email address to access all features anish noob. '
            
        return Response(response_data, status=status.HTTP_200_OK) 
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request,token):
    """Email verification endpoint"""
    try:
        user = User.objects.get(email_verification_token = token)
        
        if user.is_email_verified:
            return Response(
                {
                    'message': 'Email already verified.'
                },status=status.HTTP_200_OK)
            
        user.is_email_verified = True
        user.is_active = True
        user.email_verification_token = None
        user.save()
            
        return Response({
           'message': 'Email verified successfully! You can nowaccess all features.'
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({
            'error':'Invalid or expired verificaiton token.'
        }, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification_email(request):
    
    """Resend verification email endpoint"""
    email = request.data.get('email')
    
    if not email:
        return Response({
            'error':'Email is required.'
        },status=status.HTTP_400_BAD_REQUEST
        )   
        
    try:
        user = User.objects.get(email=email)
        
        
        if user.is_email_verified:
            return Response({
                'message':'Email is already verified.'
                
            },status.HTTP_200_OK)  
            
        email_sent = send_verification_email(user,request)
        
        
        if email_sent:
            return Response({
                 'message': 'Verification email sent successfully. Please check your inbox.'
            },status=status.HTTP_200_OK)    
            
        else:
            return Response({
                'error': 'Failed to send verification email. Please try again later.'
                
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)      
    
    except User.DoesNotExist:
        return Response({
            'error':'User with this email does not exist.'
        },status= status.HTTP_404_NOT_FOUND)     
        
        
        
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    """
    Send password reset email with token if email exists.
    """
    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            send_password_reset_email(user, request)
        except User.DoesNotExist:
            pass  # Do not reveal if email exists, for security

        return Response({
            "message": "If your email exists, a reset link has been sent."
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request, token):
    """
    Verify token and set new password
    """
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = User.objects.get(password_reset_token=token)
        except User.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if token expired
        if user.password_reset_token_expiry < timezone.now():
            return Response({"error": "Token expired"}, status=status.HTTP_400_BAD_REQUEST)

        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.clear_reset_token()

        return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from django.utils import timezone
from datetime import timedelta

from accountapp.authentication import JWTAuthentication, create_access_token, create_refresh_token
from accountapp.models import  User, UserToken
from accountapp.permissions import IsAdmin,IsResumeOwner,IsResumeOwnerOrAdmin
from accountapp.serializers import UserSerializer,UserRegisterSerializer, AdminRegisterSerializer


# APIView is the base class for all views in Django REST Framework.
# It provides request.data, request.user, request.auth, authentication_classes, permission_classes and methods like .get(), .post()
# class RegisterAPIView(APIView):
#     permission_classes = [AllowAny] # anyone can access this endpoint
#     authentication_classes = []
    
#     def post(self, request: Request):
#         user = request.data
#         print(f'User data received: {user}')
        
#         if User.objects.filter(email=user['email']).exists():
#             raise exceptions.APIException('Email already exists!')

#         if User.objects.filter(username=user['username']).exists():
#             raise exceptions.APIException('Username already exists!')

#         if user['password'] != user['password_confirm']:
#             raise exceptions.APIException('Passwords do not match!')

#         serializer = UserSerializer(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AdminRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = AdminRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
# User Login with JWT
class LoginAPIView(APIView):
    permission_classes = [AllowAny]  # Anyone can login
    authentication_classes = []  # No authentication required for login

    def post(self, request: Request):
        email = request.data['email']
        password = request.data['password']        

        # Check if user exists
        user = User.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed('Invalid credentials')
        
        # Check if password is correct
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Invalid password')
        
        # Generate access and refresh tokens
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        # Save refresh token of a specific user with an expiration date of 7 days
        UserToken.objects.create(
            user=user, 
            token=refresh_token, 
            expired_at = timezone.now() + timedelta(days=7)
        )
        
        response = Response()
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return response
    
# Check Authenticated User      
class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsResumeOwnerOrAdmin]  # Ensure only authenticated users who can be a professors or students can access this view

    def get(self, request: Request):
        user = request.user
        # Django models can have built-in permissions which are set in the model's Meta class
        # permissions = request.user.get_all_permissions()
        # "permissions": list(permissions)
        # is_admin = request.auth.get('is_admin', False)

        serializer = UserSerializer(user)
        return Response({
            'user': serializer.data,
            'role': user.role,
            'is_professor': user.role == 'professor',
            'is_student': user.role == 'student',
            'is_admin': user.role == 'admin'            
        })

# Logout User    
class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def post(self, request: Request):
        refresh_token = request.data.get('refresh_token') or request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'detail': 'Refresh token missing'}, status=400)

        UserToken.objects.filter(token=refresh_token).delete()

        response: Response = Response({
            'status': 'success',
            'message': 'Logged out successfully'
        }, status=200)

        response.delete_cookie(key='refresh_token')
        return response



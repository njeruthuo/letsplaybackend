# views.py
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import UserProfile

from rest_framework import generics, status

from rest_framework.decorators import api_view, permission_classes


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'id': user.id, 'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name})
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=401)

    return JsonResponse({'message': 'Invalid request method'}, status=405)


def profile_data(request, id):
    if request.method == 'GET':
        user_profile = get_object_or_404(UserProfile, user_id=id)
        serializer = UserProfileSerializer(user_profile)
        return JsonResponse(serializer.data, safe=False)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile_data_update(request):
    # Get the user's profile
    profile = get_object_or_404(UserProfile, user=request.user)

    # Determine whether the request is a full update (PUT) or a partial update (PATCH)
    partial = request.method == 'PATCH'

    # Serialize the data for updating the profile
    serializer = UserProfileSerializer(
        profile, data=request.data, partial=partial)

    if serializer.is_valid():
        # Save the updated profile
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # If the data is invalid, return a 400 error with the validation errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful'})

    return JsonResponse({'message': 'Invalid request method'}, status=405)


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the user's profile or create a new one if it doesn't exist
        profile, created = UserProfile.objects.get_or_create(
            user=self.request.user)
        return profile

    def update(self, request, *args, **kwargs):
        # Allow partial updates to the profile
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # If the profile exists, it will update; otherwise, it will create one
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

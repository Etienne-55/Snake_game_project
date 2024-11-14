from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
import json
from rest_framework import viewsets
from .models import Coffee
from .serializers import CoffeeSerializer


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')

            if not email or not password or not confirm_password:
                return JsonResponse({"message": "Missing fields"}, status=400)

            if password == confirm_password:
                if User.objects.filter(username=email).exists():
                    return JsonResponse({"message": "User already exists"}, status=400)
                user = User.objects.create_user(username=email, email=email, password=password)
                user.save()
                return JsonResponse({"message": "User registered successfully"}, status=201)
            else:
                return JsonResponse({"message": "Passwords do not match"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Server error: {str(e)}"}, status=500)
    return JsonResponse({"message": "Invalid method"}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({"message": "Missing fields"}, status=400)

            user = authenticate(username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return JsonResponse({"message": "Login successful"}, status=200)
            else:
                return JsonResponse({"message": "Invalid credentials"}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Server error: {str(e)}"}, status=500)
    return JsonResponse({"message": "Invalid method"}, status=405)

class HelloWorld(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the snake game :)"}, status=status.HTTP_200_OK)

class Hello(APIView):
    def get(self, request):
        return Response({"message": "Game menu."}, status=status.HTTP_200_OK)

class CoffeeViewSet(viewsets.ModelViewSet):
    queryset = Coffee.objects.all()
    serializer_class = CoffeeSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from .models import Profile, Score
from .serializers import ScoreSerializer, ProfileSerializer
import json
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import JsonResponse
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


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
                Profile.objects.create(user=user)
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
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token) 

                return JsonResponse({
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": str(refresh)
                }, status=200)
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_score(request):
    click_count = request.data.get('click_count')
    
    if click_count is not None and click_count > 0:
        score, created = Score.objects.get_or_create(user=request.user)
        score.score += click_count 
        score.save()
        return Response({"message": "Score updated successfully!"}, status=status.HTTP_200_OK)
    
    return Response({"error": "Invalid click count data!"}, status=status.HTTP_400_BAD_REQUEST)


class LeaderboardView(APIView):
    def get(self, request):
        try:
            profiles = Profile.objects.order_by('-highest_score')[:10]
            leaderboard = [
                {"username": profile.user.username, "highest_score": profile.highest_score}
                for profile in profiles
            ]
            return Response({"leaderboard": leaderboard}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"Server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all().order_by('-score') 
    serializer_class = ScoreSerializer



@csrf_exempt
def update_score(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            score = data.get('score') 
            
            if not score:
                return JsonResponse({"message": "Score is required!"}, status=400)
            
            
            return JsonResponse({"message": "Score updated successfully!"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"Server error: {str(e)}"}, status=500)
    return JsonResponse({"message": "Invalid method"}, status=405)


class UpdateScoreView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        score = request.data.get('score')
        if score is not None:
            user = request.user
            leaderboard, created = Score.objects.get_or_create(user=user)
            leaderboard.score = score
            leaderboard.save()
            return Response({"message": "Score updated"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid score"}, status=status.HTTP_400_BAD_REQUEST)


class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all().order_by('-score') 
    serializer_class = ScoreSerializer 
    permission_classes = [IsAuthenticated]

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all().order_by('-score') 
    serializer_class = ScoreSerializer 
    permission_classes = [IsAuthenticated] 

class LeaderboardView(APIView):
    def get(self, request):
        profiles = Profile.objects.order_by('-highest_score')[:10]
        serializer = ProfileSerializer(profiles, many=True)
        return Response({"leaderboard": serializer.data})
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import HelloWorld
from .views import signin, login, Hello
from .views import update_score
from .views import LeaderboardView
from . import views
from .views import LeaderboardViewSet

router = DefaultRouter()
router.register(r'leaderboard', LeaderboardViewSet)

urlpatterns = [
    path('api/hello/', HelloWorld.as_view(), name='hello-world'),
    path('login/', login, name='login'),
    path('signin/', signin, name='signin'),
    path('hello/', Hello.as_view(), name='hello'),
    path('api/', include(router.urls)),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('update-score/', views.update_score, name='update_score'),
    path('update-score/', update_score, name='update-score'),
]

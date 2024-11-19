from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import HelloWorld, signin, login, Hello, update_score, LeaderboardViewSet

router = DefaultRouter()
router.register(r'score', LeaderboardViewSet) 

urlpatterns = [
    path('api/hello/', HelloWorld.as_view(), name='hello-world'),
    path('login/', login, name='login'),
    path('signin/', signin, name='signin'),
    path('hello/', Hello.as_view(), name='hello'),
    path('api/', include(router.urls)), 
    path('update-score/', update_score, name='update_score'),
]

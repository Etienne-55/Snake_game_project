from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stock_app.urls')),
    path('signin/', auth_views.LoginView.as_view(), name='signin'),  
    path('login/', auth_views.LoginView.as_view(), name='login'),  
]

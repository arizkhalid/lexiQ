from .views import LoginView, RefreshView, RegisterView
from django.urls import path

urlpatterns = [
    path('token/', LoginView.as_view()),
    path('token/refresh/', RefreshView.as_view()),  
    path('register/', RegisterView.as_view()),
]

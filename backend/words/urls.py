from rest_framework.routers import DefaultRouter
from .views import WordViewSet, ParagraphViewSet, UserWordViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include

router = DefaultRouter()
router.register(r'words', WordViewSet)
router.register(r'paragraph', ParagraphViewSet)
router.register(r'user-words', UserWordViewSet)

urls = [
    path('api/token/', TokenObtainPairView.as_view()),       # login → get tokens
    path('api/token/refresh/', TokenRefreshView.as_view()),  
]
urlpatterns = router.urls + urls

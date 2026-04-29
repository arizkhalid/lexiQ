from rest_framework.routers import DefaultRouter
from .views import ParagraphViewSet, UserWordViewSet, WordAPIView
from django.urls import path, include

router = DefaultRouter()
router.register(r'paragraph', ParagraphViewSet)
router.register(r'user-words', UserWordViewSet)

urlpatterns = [
    path("words/<str:word>/", WordAPIView.as_view()),
    path("", include(router.urls))
]

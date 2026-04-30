from django.urls import include, path
from .views import GenerateQuizView, McqSolvedView
urlpatterns = [
    path("generate/", view=GenerateQuizView.as_view()),
    path("mcq_solved/", view=McqSolvedView.as_view())
]

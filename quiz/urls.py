from django.urls import path
from .views import create_quiz, dashboard, play_quiz, quiz_list, delete_quiz, student_quizzes

urlpatterns = [
    path('create_quiz/', create_quiz),
    path('', quiz_list, name='quiz-list'),
    path('delete_quiz/<str:quiz_id>/', delete_quiz, name='delete-quiz'),
    path('quizzes/', student_quizzes, name='quizzes'),
    path('play-quiz/<str:quiz_id>/<str:qn_no>', play_quiz, name='play-quiz'),
    path('dashboard/', dashboard, name='dashboard')
]

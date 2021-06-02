from django.db import models

# Create your models here.


class QuizAuthor(models.Model):
    quiz_name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.quiz_name


class Questions(models.Model):
    question = models.CharField(max_length=100)
    option1 = models.CharField(max_length=50)
    option2 = models.CharField(max_length=50)
    option3 = models.CharField(max_length=50)
    option4 = models.CharField(max_length=50)
    answer = models.CharField(max_length=20)
    explanation = models.CharField(max_length=200)
    quiz = models.ForeignKey(QuizAuthor, on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class UserResult(models.Model):
    user = models.CharField(max_length=50)
    score = models.CharField(max_length=2)
    quiz_id = models.CharField(max_length=50)

    def __str__(self):
        return self.user

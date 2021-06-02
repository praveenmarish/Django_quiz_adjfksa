from django.shortcuts import render
from .models import Questions, QuizAuthor

# Create your views here.

def create_quiz(request):
    if request.method == "POST":
            quiz_name = request.POST["quiz_name"]
            quiz_obj = QuizAuthor(
                quiz_name=quiz_name, author=request.user.username
            )
            quiz_obj.save()
            for i in range(10):
                question = request.POST["question" + str(i)]
                option1 = request.POST["question" + str(i) + "option1"]
                option2 = request.POST["question" + str(i) + "option2"]
                option3 = request.POST["question" + str(i) + "option3"]
                option4 = request.POST["question" + str(i) + "option4"]
                correct_answer = request.POST["question" + str(i) + "correct_answer"]
                explanation = request.POST["question" + str(i) + "explanation"]
                questions_obj = Questions(
                    question=question,
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    answer=correct_answer,
                    explanation=explanation,
                    quiz=quiz_obj,
                )
                questions_obj.save()
            return render(request,'alert.html',{"message":"Quiz Updated","url":""})
    else:
            return render(request, "create_quiz.html", {"range": range(10)})
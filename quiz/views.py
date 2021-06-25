from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from .models import Questions, QuizAuthor, UserResult
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
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
            correct_answer = request.POST["question" +
                                          str(i) + "correct_answer"]
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
        return render(request, 'alert.html', {"message": "Quiz Updated", "url": "/quiz"})
    else:
        return render(request, "create_quiz.html", {"range": range(10)})


@login_required
def quiz_list(request):
    return render(
        request, "quiz_list.html", {"quizzes_list": QuizAuthor.objects.all()}
    )


@login_required
def delete_quiz(request, quiz_id):
    QuizAuthor.objects.get(id=quiz_id).delete()
    return redirect("/")


@login_required
def student_quizzes(request):
    return render(
        request,
        "student_quizzes.html",
        {"quizzes": QuizAuthor.objects.all()},
    )


@login_required
def play_quiz(request, quiz_id):
    all_q = Questions.objects.filter(quiz_id=int(quiz_id))
    question_obj = all_q[0]
    return render(
        request,
        "play_quiz.html",
        {"qn_no": 1, "question": question_obj.question, "option1": question_obj.option1, "option2": question_obj.option2, "option3": question_obj.option3,
            "option4": question_obj.option4, "explanation": question_obj.explanation, "answer": question_obj.answer, "quiz_id": quiz_id},
    )


@login_required
def play_next(request):
    if request.is_ajax and request.method == "POST":
        quiz_id = int(request.POST["quiz_id"])
        all_q = Questions.objects.filter(quiz_id=quiz_id)
        qn_no = int(request.POST["qn_no"])
        question_obj = all_q[qn_no+1]
        answer_choosed = request.POST["result"]
        time = int(request.POST["time"])
        if UserResult.objects.filter(user=request.user.username, quiz_id=quiz_id).exists():
            u = UserResult.objects.get(
                user=request.user.username, quiz_id=quiz_id)
            if answer_choosed == "correct":
                u.score = str(int(u.score) + 1)
            u.time = str(int(u.time) + time)
            u.save()
        else:
            score = 0
            if answer_choosed == "correct":
                score = 1
            u = UserResult(user=request.user.username,
                           quiz_id=quiz_id, score=score)
            u.time = str(time)
            u.save()
        return JsonResponse({"qn_no": qn_no+1, "question": question_obj.question, "option1": question_obj.option1, "option2": question_obj.option2, "option3": question_obj.option3,
                             "option4": question_obj.option4, "explanation": question_obj.explanation, "answer": question_obj.answer, "quiz_id": quiz_id})


@login_required
def dashboard(request):
    quiz_ids = {
        quiz.quiz_id: quiz.score
        for quiz in UserResult.objects.filter(user=request.user.username)
    }
    quiz_scores = list(quiz_ids.values())
    quiz_names = [
        QuizAuthor.objects.get(id=int(ids)).quiz_name
        for ids in list(quiz_ids.keys())
    ]
    played_quizzes = dict(zip(quiz_names, quiz_scores))
    return render(
        request, "dashboard.html", {"played_quizzes": played_quizzes.items()}
    )

from django.shortcuts import redirect, render
from .models import Questions, QuizAuthor, UserResult

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


def quiz_list(request):
    return render(
        request, "quiz_list.html", {"quizzes_list": QuizAuthor.objects.all()}
    )


def delete_quiz(request, quiz_id):
    QuizAuthor.objects.get(id=quiz_id).delete()
    return redirect("/")


def student_quizzes(request):
    return render(
        request,
        "student_quizzes.html",
        {"quizzes": QuizAuthor.objects.all()},
    )


def play_quiz(request, quiz_id, qn_no):
    all_q = Questions.objects.filter(quiz_id=int(quiz_id))
    time = 0
    if request.method == "POST":
        qn_no = int(request.POST["qn_no"])
        answer_choosed = request.POST["result"]
        time = int(request.POST["time"])+time
        if qn_no in range(0, 10):
            question_obj = all_q[int(qn_no)]
            if UserResult.objects.filter(
                user=request.user.username, quiz_id=quiz_id
            ).exists():
                if answer_choosed == "correct":
                    u = UserResult.objects.get(
                        user=request.user.username, quiz_id=quiz_id
                    )
                    u.score = str(int(u.score) + 1)
                    u.save()
                    return render(
                        request,
                        "play_quiz.html",
                        {
                            "question_obj": question_obj,
                            "qn_no": int(qn_no)+1,
                            "quiz_id": quiz_id,
                        },
                    )
                else:
                    return render(
                        request,
                        "play_quiz.html",
                        {
                            "question_obj": question_obj,
                            "qn_no": int(qn_no)+1,
                            "quiz_id": quiz_id,
                        },
                    )
            else:
                if answer_choosed == "correct":
                    u = UserResult(
                        user=request.user.username, quiz_id=quiz_id, score=1
                    )
                    u.save()
                    return render(
                        request,
                        "play_quiz.html",
                        {
                            "question_obj": question_obj,
                            "qn_no": int(qn_no)+1,
                            "quiz_id": quiz_id,
                        },
                    )
                else:
                    u = UserResult(
                        user=request.user.username, quiz_id=quiz_id, score=0
                    )
                    u.save()
                    return render(
                        request,
                        "play_quiz.html",
                        {
                            "question_obj": question_obj,
                            "qn_no": int(qn_no)+1,
                            "quiz_id": quiz_id,
                        },
                    )
        else:
            if UserResult.objects.filter(
                user=request.user.username, quiz_id=quiz_id
            ).exists():
                u = UserResult.objects.get(
                    user=request.user.username, quiz_id=quiz_id
                )
                if answer_choosed == "correct":
                    u.score = str(int(u.score) + 1)
                    u.save()
                score = u.score
                return render(request, 'alert.html', {"message": "Your Score out of 10 is "+score, "url": "/quiz/quizzes/"})
            else:
                return render(request, 'alert.html', {"message": "Something Went Wrong", "url": "/quiz/quizzes/"})
    else:
        question_obj = all_q[0]
        if UserResult.objects.filter(
            user=request.user.username, quiz_id=quiz_id
        ).exists():
            u = UserResult.objects.get(
                user=request.user.username, quiz_id=quiz_id)
            u.score = "0"
            u.save()
            return render(
                request,
                "play_quiz.html",
                {
                    "question_obj": question_obj,
                    "qn_no": int(qn_no)+1,
                    "quiz_id": quiz_id,
                },
            )
        return render(
            request,
            "play_quiz.html",
            {"question_obj": question_obj, "qn_no": int(
                qn_no)+1, "quiz_id": quiz_id},
        )


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

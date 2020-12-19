import random
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def how_many_seconds_until_midnight():
    """Get the number of seconds until midnight."""
    tomorrow = datetime.now() + timedelta(1)
    midnight = datetime(
        year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=0, minute=0, second=0
    )
    return (midnight - datetime.now()).seconds


@csrf_exempt
def index(request):
    seconds_until_midnight = how_many_seconds_until_midnight()
    if not request.session.get("start_page"):
        request.session["start_page"] = True
        return render(request, "start.html", {},)
    if not request.session.get("question_number"):
        request.session["question_number"] = 0
    if not request.session.get("correct_aswers"):
        request.session["correct_aswers"] = 0
    request.session.set_expiry(seconds_until_midnight)
    if request.method == "POST":
        choice = int(request.POST["choice"])
        form_multiplication_result = int(request.POST["result"])
        if choice != form_multiplication_result:
            if request.session["question_number"] == 10:
                return render(
                    request,
                    "negative_limit_per_day.html",
                    {
                        "form_multiplication_result": form_multiplication_result,
                        "correct_aswers": request.session["correct_aswers"],
                    },
                )
            else:
                return render(
                    request,
                    "negative_answer.html",
                    {"form_multiplication_result": form_multiplication_result},
                )
        else:
            request.session["correct_aswers"] += 1
    first_number = random.randint(1, 10)
    second_number = random.randint(1, 10)
    multiplication_result = first_number * second_number
    random_answers = random.sample(range(1, 100), 3)
    random_insert_index = random.randint(0, 3)
    random_answers.insert(random_insert_index, multiplication_result)
    request.session["question_number"] += 1
    if request.session["question_number"] > 10:
        return render(
            request,
            "positive_limit_per_day.html",
            {"correct_aswers": request.session["correct_aswers"]},
        )
    return render(
        request,
        "index.html",
        {
            "first_number": first_number,
            "second_number": second_number,
            "first_question": random_answers[0],
            "second_question": random_answers[1],
            "third_question": random_answers[2],
            "fourth_question": random_answers[3],
            "multiplication_result": multiplication_result,
            "current_question_number": request.session["question_number"],
        },
    )


def server_time_view(request):
    return HttpResponse(datetime.now().strftime("%H:%M:%S"))

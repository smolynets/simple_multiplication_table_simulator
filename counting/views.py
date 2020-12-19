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


def get_spent_time(request):
    """
    Get difference bettwen current time and saved in session start time
    """
    start_time = datetime.strptime(request.session["start_time"], "%Y-%m-%d %H:%M:%S")
    now = datetime.now().replace(microsecond=0)
    time_delta = now - start_time
    return (
        time_delta.seconds // 3600,
        time_delta.seconds // 60 % 60,
        time_delta.seconds,
    )


@csrf_exempt
def index(request):
    seconds_until_midnight = how_many_seconds_until_midnight()
    request.session.set_expiry(seconds_until_midnight)
    if not request.session.get("start_page"):
        request.session["start_page"] = True
        return render(request, "start.html", {},)
    if not request.session.get("question_number"):
        request.session["question_number"] = 0
    if not request.session.get("correct_aswers"):
        request.session["correct_aswers"] = 0
    if request.method == "POST":
        choice = int(request.POST["choice"])
        form_multiplication_result = int(request.POST["result"])
        if choice != form_multiplication_result:
            if request.session["question_number"] == 10:
                hours, minutes, seconds = get_spent_time(request)
                return render(
                    request,
                    "negative_limit_per_day.html",
                    {
                        "form_multiplication_result": form_multiplication_result,
                        "correct_aswers": request.session["correct_aswers"],
                        "hours": hours,
                        "minutes": minutes,
                        "seconds": seconds,
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
    if request.session["question_number"] == 1:
        request.session["start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if request.session["question_number"] > 10:
        hours, minutes, seconds = get_spent_time(request)
        return render(
            request,
            "positive_limit_per_day.html",
            {
                "correct_aswers": request.session["correct_aswers"],
                "hours": hours,
                "minutes": minutes,
                "seconds": seconds,
            },
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

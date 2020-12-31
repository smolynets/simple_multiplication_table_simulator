import random
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from counting.models import FinishPerDay


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
    if request.session.get("start_time"):
        start_time = datetime.strptime(request.session["start_time"], "%Y-%m-%d %H:%M:%S")
        now = datetime.strptime(request.session["finish_time"], "%Y-%m-%d %H:%M:%S")
        time_delta = now - start_time
        return time_delta.seconds
    seconds = None
    return seconds


def get_correct_aswers_str(correct_aswers):
    """
    Different question words
    """
    if correct_aswers == 0 or correct_aswers >= 5:
        return f"{correct_aswers} питань"
    return f"{correct_aswers} питання"


def create_finish_per_day(score, finish_time, spended_time):
    """
    Create FinishPerDay when finish studing per day
    """
    if not FinishPerDay.objects.filter(finish_time=finish_time).exists():
        FinishPerDay.objects.create(
            finish_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            score=score,
            spended_time=spended_time,
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
        if request.session["question_number"] == 10 and not request.session.get("finish_time"):
            request.session["finish_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if choice != form_multiplication_result:
            if request.session["question_number"] == 10:
                seconds = get_spent_time(request)
                create_finish_per_day(
                    request.session["correct_aswers"], request.session.get("finish_time"), seconds
                )
                return render(
                    request,
                    "negative_limit_per_day.html",
                    {
                        "form_multiplication_result": form_multiplication_result,
                        "correct_aswers_str": get_correct_aswers_str(
                            request.session["correct_aswers"]
                        ),
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
            if request.session["question_number"] <= 10 and not request.session.get("finish_time"):
                request.session["correct_aswers"] += 1
            else:
                if request.session["question_number"] == 10 and not request.session.get(
                    "finish_last_question"
                ):
                    request.session["correct_aswers"] += 1
                    request.session["finish_last_question"] = True
                seconds = get_spent_time(request)
                create_finish_per_day(
                    request.session["correct_aswers"], request.session.get("finish_time"), seconds
                )
                return render(
                    request,
                    "positive_limit_per_day.html",
                    {
                        "correct_aswers_str": get_correct_aswers_str(
                            request.session["correct_aswers"]
                        ),
                        "seconds": seconds,
                    },
                )
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
        seconds = get_spent_time(request)
        return render(
            request,
            "limit_per_day.html",
            {
                "correct_aswers_str": get_correct_aswers_str(request.session["correct_aswers"]),
                "seconds": seconds,
            },
        )
    return render(
        request,
        "question_form.html",
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

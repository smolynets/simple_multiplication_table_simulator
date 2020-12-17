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
    if not request.session.get("aswers"):
        request.session["aswers"] = 0
        request.session.set_expiry(seconds_until_midnight)
    request.session["aswers"] += 1
    if request.session["aswers"] >= 10:
        return render(request, "limit_per_day.html", {},)
    if request.method == "POST":
        choice = int(request.POST["choice"])
        form_multiplication_result = int(request.POST["result"])
        if choice != form_multiplication_result:
            return render(request, "negative_answer.html", {})
    first_number = random.randint(1, 10)
    second_number = random.randint(1, 10)
    multiplication_result = first_number * second_number
    random_answers = random.sample(range(1, 100), 3)
    random_insert_index = random.randint(0, 3)
    random_answers.insert(random_insert_index, multiplication_result)
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
        },
    )


def server_time_view(request):
    return HttpResponse(datetime.now().strftime("%H:%M:%S"))

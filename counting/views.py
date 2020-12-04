import random

from django.shortcuts import render


def index(request):
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

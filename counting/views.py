from django.shortcuts import render


def index(request):
    if request.method == "POST":
        choice = request.POST["choice"]
    return render(request, "index.html", {"one": 2, "two": 4})

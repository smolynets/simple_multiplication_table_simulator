from django.shortcuts import render


def index(request):
    if request.method == "POST":
        choice = request.POST["choice"]
        import ipdb

        ipdb.set_trace()
    return render(request, "index.html", {"one": 2, "two": 4, "third": 5, "four": 7})

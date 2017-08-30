from django.shortcuts import render, redirect


def home(request):
    # if request.user.is_authenticated:
    #     return redirect("trip:list")
    return render(request, "home.html", {})

def apidoc(request):
    return render(request, "apidoc.html", {})

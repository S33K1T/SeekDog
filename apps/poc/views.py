from django.shortcuts import render

# Create your views here.


def poc(request):
    return render(request, "pages/poc/poc.html")

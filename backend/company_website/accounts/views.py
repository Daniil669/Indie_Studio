from django.http import HttpResponse

def account(request):
    return HttpResponse("Account page")

def logout(request):
    return HttpResponse("Logout page")

def login(request):
    return HttpResponse("Login page")

def signup(request):
    return HttpResponse("SignUpp page")

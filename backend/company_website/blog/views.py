from django.http import HttpResponse

def blog(request):
    return HttpResponse("Blog page")

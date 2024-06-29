from django.shortcuts import render

# Create your views here.


def bad_request(request, exception):
    return render(request, 'error_handling/400.html')

def permission_denied(request,exception):
    return render(request, 'error_handling/403.html')

def page_not_found(request,exception):
    return render(request, 'error_handling/404.html')

def server_error(request):
    return render(request, 'error_handling/500.html')
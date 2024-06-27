from django.shortcuts import render

# Create your views here.

def login(request):
    if 'email' and 'role' in request.session:
        pass
    return render(request, 'Log-In.html')
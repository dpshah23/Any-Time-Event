from django.shortcuts import render,redirect

# Create your views here.
def index(request):
    if 'email' and 'role' not in request.session:
        return redirect('auth/login')
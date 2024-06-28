from django.shortcuts import render,redirect,HttpResponse

# Create your views here.
def index(request):
    if 'email' and 'role' in request.session:
        email=request.session['email']
        role=request.session['role']
        if role=="volunteer":
                       
            return HttpResponse("Volunteer")
        elif role=="company":
            return HttpResponse("Company")
        else:
            redirect('/')
    return render(request,'home.html')
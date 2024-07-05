from django.shortcuts import render,redirect
from auth1.models import users,company,volunteer
from django.contrib import messages

# Create your views here.
def accept_user(request):
    return render(request, 'accept_user.html')

def pay(request):
    return render(request, 'pay.html')

def acceptyes(request,volemail):
    userchange=users.objects.get(email=volemail)
    userchange.is_active=True
    userchange.save()
    messages.error(request,"User Accepted")
    return redirect('admincustom/acceptusers')
    
    
def acceptno(request,volemail):
    userchange=users.objects.get(email=volemail)
    userchange.is_active=False
    userchange.save()
    
    if userchange.role=="volunteer":
        volunteer.delete(email=volemail)
        users.delete(email=volemail)
        
    else:
        company.delete(email=volemail)
        users.delete(email=volemail)
        
    messages.error(request,"User Rejected")
    return redirect("/admincustom/acceptusers")
    
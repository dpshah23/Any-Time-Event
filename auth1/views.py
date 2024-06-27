from django.shortcuts import render,redirect
from .models import users
from cryptography.fernet import Fernet
import base64
from django.contrib import messages


# Create your views here.
def decrypt_password(password,key):
    decoded_key = base64.b64decode(key)
    decoded_password = base64.b64decode(password)

    f = Fernet(decoded_key)
   
    decrypted_password = f.decrypt(decoded_password)
    
    return decrypted_password.decode()


def login(request):
    if 'email' and 'role' in request.session:
        pass
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            user=users.objects.all(email=email)
            decrypted_pass=decrypt_password(user.password,user.key)
            if user.email==email and decrypted_pass==password:
                request.session['email']=email
                request.session['role']=user.role

                if user.role=="volunteer":
                    return redirect('/volunteer')
                elif user.role=="company":
                    return redirect('/company')
                else:
                    redirect('/')

                

        except:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'Log-In.html')

    return render(request, 'Log-In.html')
from django.shortcuts import redirect, render
from userauths.form import UserRegisterForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User

def register_view(request):
    
    if request.method == "POST":
        form=UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user=form.save()
            username=form.cleaned_data.get("username")
            messages.success(request, f"heyy{username}, you account was create successfully.")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
            )
            login(request,new_user)
            return redirect("userauths:sign-in")
            
            
            
    else:
        form=UserRegisterForm()
        
    context={
        'form':form,
    }
    return render(request,"userauths/sign-up.html",context)

def login_view(request):
    
    if request.method == "POST":
        email = request.POST.get("contact-email")
        password = request.POST.get("contact-subject")
        
        try:
            user=User.objects.get(email=email)
            user = authenticate(request,email=email,password=password)
        
            if user is not None:
                login(request,user)
                messages.success(request,"You are logged in.")
                return redirect("core:index")
            
            else:
                messages.warning(request,"User Dose Not Exist, Create an account.")
            
        except:
            messages.warning(request,f"User with {email} dose not exist")
            

    return render(request,"userauths/sign-in.html")


def logout_view(request):
    logout(request)
    messages.success(request,"You logged out.")
    return redirect("userauths:sign-in")
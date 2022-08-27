from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout #giriş yapmak, kullanıcı veri kontrolü,çıkış yapmak kütüphaneleri
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            
            
            newUser = User(username = username,first_name = first_name,last_name=last_name,email=email)
            newUser.set_password(password)
            

            newUser.save()
            login(request,newUser)
            messages.info(request,"Başarıyla Kayıt Oldunuz...")

            return redirect("index")
    context = {
        "form" : form
    }
    return render(request, "register.html",context)

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username,password = password)

        if user is None:
            messages.info(request,"Kullanıcı Adı veya Parola Hatalı")
            return render(request,"login.html",context)
        
        messages.success(request, "Başarıyla Giriş Yapıldı...")
        login(request,user)
        return redirect("index")

    return render(request,"login.html",context)

    
def logoutUser(request):
    logout(request)
    messages.success(request, "Başarıyla Çıkış Yapıldı...")
    return redirect("index")




def profile(request):
    return render(request, "profile.html")
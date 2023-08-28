from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .EmailBackEnd import EmailBackEnd
from django.shortcuts import render
from django.contrib.auth import login, logout

# Create your views here.

def shwoDemoPage(request):
    return render(request, 'demo.html')

def ShowLoginPage(request):
    return render(request, 'login.html')

def doLoginPage(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowd</h2>")
    else:
        user = EmailBackEnd.authenticate(request,username= request.POST.get('email'),password= request.POST.get('password'))
        if user != None:
            login(request,user)
            if user.user_type == '1':
                return HttpResponseRedirect(reverse('admin_home'))
            elif user.user_type =='2':
                return HttpResponseRedirect(reverse('staff_home'))
            else:
                return HttpResponseRedirect(reverse('student_home'))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/showLogin")
        
def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("Email: "+str(request.user.email)+ "<br>" + "user type: "+str(request.user.user_type)) 
    else:
        return HttpResponseRedirect("/showLogin")

def LogoutUser(request):
    logout(request)
    return HttpResponseRedirect('/showLogin')
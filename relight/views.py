from django.shortcuts import render, loader, redirect
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.views import LogoutView 
from django.http import HttpResponse
from relight.models import UserInfo
from relight.forms.forms import Create_account_Form , LoginForm
from django.contrib.auth import authenticate, login
from django.views import View

# Create your views here.

def top(request):
   template = loader.get_template('relight/top.html')
   return HttpResponse(template.render(None, request))

def create_account(request):
   if request.method == 'GET':
      form = Create_account_Form()
   else:
      print(request.FILES)
      form = Create_account_Form(request.POST,request.FILES) 
      if form.is_valid():
         print('user_regist is_valid')
         form.save(request.POST,request.FILES)
         return redirect('/login/')
      else:
         print('user_regist false is_valid')
         
   template = loader.get_template('relight/create_account.html')
   context = {
      'form': form,
   }
   return HttpResponse(template.render(context, request))

def Login(request):
   if request.method == 'GET':
      form = LoginForm()
   else:
      form = LoginForm(data=request.POST) 
      print(form)
      print(request)
      print(request.POST)
      if form.is_valid():
         print('user_login is_valid')
         email = form.cleaned_data.get('email')
         print(email)
         user = UserInfo.objects.get(email=email)
         login(request, user)
         return redirect('/index/')
         
   template = loader.get_template('relight/login.html')
   context = {
      'form': form,
   }
   return HttpResponse(template.render(context, request))

class Logout(LoginRequiredMixin, LogoutView):
   template_name = 'relight/top.html'

def cus_profile(request):
   return render(request, 'relight/cus_profile.html',{})

def shop_profile(request):
   return render(request, 'relight/shop_profile.html',{})

def event_index(request):
   return render(request, 'relight/event_index.html',{})

def event_detail(request):
   return render(request, 'relight/event_detail.html',{})

def create_event(request):
   return render(request, 'relight/create_event.html',{})

def shop_video(request):
   return render(request, 'relight/shop_video.html',{})

def cus_video(request):
   return render(request, 'relight/cus_video.html',{})



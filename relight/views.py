from django.shortcuts import render, loader, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from relight.models import UserInfo
from relight.forms.forms import Create_account_Form
# from relight.forms.forms import Customer_SignUpForm ,  Shop_SignUpForm

# Create your views here.

def top(request):
   template = loader.get_template('relight/top.html')
   return HttpResponse(template.render(None, request))

def create_account(request):
   if request.method == 'GET':
      form = Create_account_Form()
   else:
      form = Create_account_Form(data=request.POST)
      if form.is_valid():
         print('user_regist is_valid')
         form.save(request.POST)
         return redirect('/login/')
      else:
         print('user_regist false is_valid')
         
   template = loader.get_template('relight/create_account.html')
   context = {
      'form': form,
   }
   return HttpResponse(template.render(context, request))


def login(request):
   return render(request, 'relight/login.html',{})

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



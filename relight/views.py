from django.shortcuts import render, loader, redirect
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.views import LogoutView 
from django.http import HttpResponse
from relight.models import UserInfo
from relight.forms.forms import Create_account_Form , LoginForm
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.decorators import login_required

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
         form.save()
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
      if form.is_valid():
         print('user_login is_valid')
         email = form.cleaned_data.get('email')
         user = UserInfo.objects.get(email=email)
         login(request, user)
         url = '/cus/profile/' + str(user.id)
         if user.s_or_c == "shop":
            url = '/shop/profile/' + str(user.id)   
         return redirect(url)
         
   template = loader.get_template('relight/login.html')
   context = {
      'form': form,
   }
   return HttpResponse(template.render(context, request))

class Logout(LoginRequiredMixin, LogoutView):
   template_name = 'relight/top.html'

@login_required
def cus_profile(request,cus_id):
   if request.method == 'GET':
      user = UserInfo.objects.get(id=shop_id)

   template = loader.get_template('relight/cus_profile.html')
   context = {
      'user': user,
   }
   return HttpResponse(template.render(context, request))

@login_required
def shop_profile(request,shop_id):
   if request.method == 'GET':
      user = UserInfo.objects.get(id=shop_id)

   template = loader.get_template('relight/shop_profile.html')
   context = {
      'user': user,
   }
   return HttpResponse(template.render(context, request))

@login_required
def event_index(request):
   return render(request, 'relight/event_index.html',{})

@login_required
def event_detail(request):
   return render(request, 'relight/event_detail.html',{})

@login_required
def create_event(request):
   return render(request, 'relight/create_event.html',{})

@login_required
def shop_video(request):
   return render(request, 'relight/shop_video.html',{})

@login_required
def cus_video(request):
   return render(request, 'relight/cus_video.html',{})



from django.shortcuts import render, loader, redirect
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.views import LogoutView 
from django.http import HttpResponse
from relight.models import UserInfo , Event
from relight.forms.forms import Create_account_Form , LoginForm , Create_Event_Form
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
         userid = form.cleaned_data.get('userid')
         user = UserInfo.objects.get(userid=userid)
         login(request, user)
         url = '/index/' + str(user.userid)
         if user.s_or_c == "shop":
            url = '/shop/profile/' + str(user.userid)   
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
      user = UserInfo.objects.get(userid=cus_id)

   template = loader.get_template('relight/cus_profile.html')
   context = {
      'user': user,
   }
   return HttpResponse(template.render(context, request))

@login_required
def shop_profile(request,shop_id):
   if request.method == 'GET':
      user = UserInfo.objects.get(userid=shop_id)

   template = loader.get_template('relight/shop_profile.html')
   context = {
      'user': user,
   }
   return HttpResponse(template.render(context, request))

@login_required
def event_index(request,user_id):
   events = Event.objects.all()
   user = UserInfo.objects.get(userid=user_id) 
   template = loader.get_template('relight/event_index.html')
   context = {
      'events': events,
      'user' : user,
   }
   return HttpResponse(template.render(context, request))

@login_required
def event_detail(request,event_title):
   if request.method == 'GET':
      event = Event.objects.get(title=event_title)
      user = UserInfo.objects.get(id=event.user.id)

   template = loader.get_template('relight/event_detail.html')
   context = {
      'user': user,
      'event' : event,
   }
   return HttpResponse(template.render(context, request))

@login_required
def create_event(request,shop_id):
   user = UserInfo.objects.get(userid=shop_id)
   if request.method == 'GET':
      form = Create_Event_Form()      
   else:
      form = Create_Event_Form(request.POST,request.FILES) 
      if form.is_valid():
         print('user_login is_valid')
         form.save(request.POST,request.FILES,user)
         ev_detail = '/event/' + request.POST["title"]
         return redirect(ev_detail)

   template = loader.get_template('relight/create_event.html')
   context = {
      'form': form,
      'user': user,
   }
   return HttpResponse(template.render(context, request))


@login_required
def video(request,user_id):
   user = UserInfo.objects.get(userid=user_id) 
   template = loader.get_template('relight/video.html')
   context = {
      'user' : user,
   }
   return HttpResponse(template.render(context, request))



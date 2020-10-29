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
         if user.s_or_c == "shop":
            return redirect('/profile')   
         return redirect('/index')
         
   template = loader.get_template('relight/login.html')
   context = {
      'form': form,
   }
   return HttpResponse(template.render(context, request))

class Logout(LoginRequiredMixin, LogoutView):
   template_name = 'relight/top.html'

@login_required
def profile(request):
   if request.method == 'GET':
      user = request.user
      events = Event.objects.filter(user_id=user.id)

   template = loader.get_template('relight/profile.html')
   context = {
      'user': user,
      'events' : events,
   }
   return HttpResponse(template.render(context, request))

@login_required
def event_index(request):
   events = Event.objects.all()
   user = request.user
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
      user = request.user
      auth_user = UserInfo.objects.get(id=event.user.id)

   template = loader.get_template('relight/event_detail.html')
   context = {
      'user': user,
      'event' : event,
      'auth_user' : auth_user,
   }
   return HttpResponse(template.render(context, request))

@login_required
def create_event(request):
   user = request.user
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
def shop_video(request,event_title):
   user = request.user
   event = Event.objects.get(title=event_title)
   template = loader.get_template('relight/shop_video.html')
   context = {
      'user' : user,
      'event' : event,
   }
   return HttpResponse(template.render(context, request))

@login_required
def cus_video(request,event_title):
   user = request.user
   event = Event.objects.get(title=event_title)
   template = loader.get_template('relight/cus_video.html')
   context = {
      'user' : user,
      'event' : event,
   }
   return HttpResponse(template.render(context, request))



from django.shortcuts import render, loader, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from relight.models import UserInfo, Shop_Profile, Cus_Profile, Event
from relight.forms.forms import Create_UserInfo_Form, Create_Cus_Form, LoginForm, Create_Shop_Form, Create_Event_Form
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.decorators import login_required

# Create your views here.


def top(request):
    template = loader.get_template('relight/top.html')
    return HttpResponse(template.render(None, request))


def create_account(request):
    if request.method == 'GET':
        form = Create_UserInfo_Form()
    else:
        print(request.FILES)
        form = Create_UserInfo_Form(request.POST, request.FILES)
        if form.is_valid():
            print('user_regist is_valid')
            form.save()
            s_or_c = form.cleaned_data.get('s_or_c')
            user_id = form.cleaned_data.get('userid')
            url = 'cus/create/' + user_id
            if (s_or_c == "shop"):
                url = 'shop/create/' + user_id
            return redirect(url)
        else:
            print('user_regist false is_valid')

    template = loader.get_template('relight/create_account.html')
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))


def create_customer(request, user_id):
    user = UserInfo.objects.get(userid=user_id)
    if request.method == 'GET':
        form = Create_Cus_Form()
    else:
        print(request.FILES, user_id)
        form = Create_Cus_Form(request.POST, request.FILES)
        if form.is_valid():
            print('user_regist is_valid')
            form.save(request.POST, request.FILES, user)
            return redirect('/login/')
        else:
            print('user_regist false is_valid')

    template = loader.get_template('relight/create_customer.html')
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))


def create_shop(request, user_id):
    user = UserInfo.objects.get(userid=user_id)
    if request.method == 'GET':
        form = Create_Shop_Form()
    else:
        print(request.FILES)
        form = Create_Shop_Form(request.POST, request.FILES)
        if form.is_valid():
            print('user_regist is_valid')
            form.save(request.POST, request.FILES, user)
            return redirect('/login/')
        else:
            print('user_regist false is_valid')

    template = loader.get_template('relight/create_shop.html')
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
            if (user.s_or_c == 'shop'):
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
        if (user.s_or_c == 'shop'):
            profile = Shop_Profile.objects.get(shop_id=user.id)
        if (user.s_or_c == 'cus'):
            profile = Cus_Profile.objects.get(cus_id=user.id)
        events = Event.objects.filter(user_id=user.id)

    template = loader.get_template('relight/profile.html')
    context = {
        'user': user,
        'events': events,
        'profile': profile,
    }
    return HttpResponse(template.render(context, request))


@login_required
def event_index(request):
    events = Event.objects.all()
    user = request.user
    if (user.s_or_c == 'shop'):
        profile = Shop_Profile.objects.get(shop_id=user.id)
    if (user.s_or_c == 'cus'):
        profile = Cus_Profile.objects.get(cus_id=user.id)
    template = loader.get_template('relight/event_index.html')
    context = {
        'profile': profile,
        'events': events,
        'user': user,
    }
    return HttpResponse(template.render(context, request))


@login_required
def event_detail(request, event_title):
    if request.method == 'GET':
        event = Event.objects.get(title=event_title)
        user = request.user
        if (user.s_or_c == 'shop'):
            profile = Shop_Profile.objects.get(shop_id=user.id)
        if (user.s_or_c == 'cus'):
            profile = Cus_Profile.objects.get(cus_id=user.id)
        auth_user = Shop_Profile.objects.get(shop_id=event.user.id)

    template = loader.get_template('relight/event_detail.html')
    context = {
        'user': user,
        'profile': profile,
        'event': event,
        'auth_user': auth_user,
    }
    return HttpResponse(template.render(context, request))


@login_required
def create_event(request):
    user = request.user
    if request.method == 'GET':
        form = Create_Event_Form()
    else:
        form = Create_Event_Form(request.POST, request.FILES)
        if form.is_valid():
            print('user_login is_valid')
            form.save(request.POST, request.FILES, user)
            ev_detail = '/event/' + request.POST["title"]
            return redirect(ev_detail)

    template = loader.get_template('relight/create_event.html')
    context = {
        'form': form,
        'user': user,
    }
    return HttpResponse(template.render(context, request))


@login_required
def shop_video(request, event_title):
    event = Event.objects.get(title=event_title)
    auth_user = Shop_Profile.objects.get(shop_id=event.user.id)
    template = loader.get_template('relight/shop_video.html')
    context = {
        'event': event,
        'auth_user': auth_user,
    }
    return HttpResponse(template.render(context, request))


@login_required
def cus_video(request, event_title):
    user = request.user
    event = Event.objects.get(title=event_title)
    auth_user = Shop_Profile.objects.get(shop_id=event.user.id)
    profile = Cus_Profile.objects.get(cus_id=user.id)
    template = loader.get_template('relight/cus_video.html')
    context = {
        'profile': profile,
        'event': event,
        'auth_user': auth_user,
    }
    return HttpResponse(template.render(context, request))


def privacy(request):
    template = loader.get_template('relight/privacy.html')
    return HttpResponse(template.render(None, request))


def about(request):
    template = loader.get_template('relight/about.html')
    return HttpResponse(template.render(None, request))

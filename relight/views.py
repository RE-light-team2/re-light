from django.shortcuts import render, loader, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from relight.models import UserInfo, Shop_Profile, Cus_Profile, Event
from relight.forms.forms import Create_UserInfo_Form, Create_Cus_Form, LoginForm, Create_Shop_Form, Create_Event_Form, Change_UserInfo_Form, Change_Cus_Form, Change_Shop_Form
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.decorators import login_required

# Create your views here.


def top(request):
    template = loader.get_template('relight/top.html')
    return HttpResponse(template.render(None, request))


def create_account(request):
    template = loader.get_template('relight/create_account.html')
    return HttpResponse(template.render(None, request))


def create_customer(request):
    if request.method == 'GET':
        form_cus = Create_Cus_Form()
        form_user = Create_UserInfo_Form()
    else:
        form_user = Create_UserInfo_Form(request.POST)
        user_id = request.POST["userid"]
        form_cus = Create_Cus_Form(request.POST, request.FILES)
        if form_user.is_valid():
            if form_cus.is_valid():
                print('user_regist is_valid')
                form_user.save(request.POST, "cus")
                form_cus.save(request.POST, request.FILES, user_id)
                return redirect('/login/')
        else:
            print('user_regist false is_valid')

    template = loader.get_template('relight/create_customer.html')
    context = {
        'form_cus': form_cus,
        'form_user': form_user,
    }
    return HttpResponse(template.render(context, request))


def create_shop(request):
    if request.method == 'GET':
        form_shop = Create_Shop_Form()
        form_user = Create_UserInfo_Form()
    else:
        form_user = Create_UserInfo_Form(request.POST)
        user_id = request.POST["userid"]
        form_shop = Create_Shop_Form(request.POST, request.FILES)
        if form_user.is_valid():
            if form_shop.is_valid():
                print('user_regist is_valid')
                form_user.save(request.POST, "shop")
                form_shop.save(request.POST, request.FILES, user_id)
                return redirect('/login/')
        else:
            print('user_regist false is_valid')

    template = loader.get_template('relight/create_shop.html')
    context = {
        'form_shop': form_shop,
        'form_user': form_user,
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
            return redirect('/event_index')

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
            profile = Shop_Profile.objects.get(shop=user.userid)
        if (user.s_or_c == 'cus'):
            profile = Cus_Profile.objects.get(cus=user.userid)
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
        profile = Shop_Profile.objects.get(shop=user.userid)
    if (user.s_or_c == 'cus'):
        profile = Cus_Profile.objects.get(cus=user.userid)
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
            profile = Shop_Profile.objects.get(shop=user.userid)
        if (user.s_or_c == 'cus'):
            profile = Cus_Profile.objects.get(cus=user.userid)
        auth_user = Shop_Profile.objects.get(shop=event.user.userid)

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
    auth_user = Shop_Profile.objects.get(shop=event.user.userid)
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
    auth_user = Shop_Profile.objects.get(shop=event.user.userid)
    profile = Cus_Profile.objects.get(cus=user.userid)
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


@login_required
def shop_index(request):
    shops = Shop_Profile.objects.all()
    user = request.user
    if (user.s_or_c == 'shop'):
        profile = Shop_Profile.objects.get(shop=user.userid)
    if (user.s_or_c == 'cus'):
        profile = Cus_Profile.objects.get(cus=user.userid)
    template = loader.get_template('relight/shop_index.html')
    context = {
        'profile': profile,
        'shops': shops,
        'user': user,
    }
    return HttpResponse(template.render(context, request))


@login_required
def shop_profile(request, shop_name):
    if request.method == 'GET':
        user = request.user
        shop_profile = Shop_Profile.objects.get(name=shop_name)
        shop = UserInfo.objects.get(userid=shop_profile.shop)
        if (user.s_or_c == 'shop'):
            profile = Shop_Profile.objects.get(shop=user.userid)
        if (user.s_or_c == 'cus'):
            profile = Cus_Profile.objects.get(cus=user.userid)
        events = Event.objects.filter(user_id=shop.id)

    template = loader.get_template('relight/shop_profile.html')
    context = {
        'user': user,
        'events': events,
        'profile': profile,
        'shop': shop,
        'shop_profile': shop_profile,
    }
    return HttpResponse(template.render(context, request))


def change_profile(request):
    user = request.user
    if user.s_or_c == "cus":
        profile = Cus_Profile.objects.get(cus=user.userid)
    else:
        profile = Shop_Profile.objects.get(shop=user.userid)

    if request.method == 'GET':
        initial_user = {
            'userid': user.userid,
            'email': user.email,
        }
        form_user = Change_UserInfo_Form(initial=initial_user)
        if user.s_or_c == "cus":
            initial_cus = {
                'name': profile.name,
                'gender': profile.gender,
                'self_introduction': profile.self_introduction,
                'cus': user.userid,
            }
            form_prof = Change_Cus_Form(initial=initial_cus)
        else:
            initial_shop = {
                'name': profile.name,
                'online_address': profile.online_address,
                'self_introduction': profile.self_introduction,
                'shop': user.userid,
            }
            form_prof = Change_Shop_Form(initial=initial_shop)

    else:
        form_user = Change_UserInfo_Form(request.POST, instance=user)
        user_id = request.POST["userid"]
        if user.s_or_c == "cus":
            form_prof = Change_Cus_Form(
                request.POST, request.FILES or None, instance=profile)
        else:
            form_prof = Change_Shop_Form(
                request.POST, request.FILES or None, instance=profile)
        print(request.POST)
        print(request.FILES or None)
        if form_prof.is_valid():
            print('user is_valid')
            if form_user.is_valid():
                print('user_regist is_valid')
                form_user.save(request.POST, user)
                form_prof.save(
                    request.POST, request.FILES or None, user_id, profile)
                login(request, user)
                return redirect('/profile')
        else:
            print('user_regist false is_valid')

    template = loader.get_template('relight/change_profile.html')
    context = {
        'form_prof': form_prof,
        'form_user': form_user,
        'user': user,
        'profile': profile,
    }
    return HttpResponse(template.render(context, request))

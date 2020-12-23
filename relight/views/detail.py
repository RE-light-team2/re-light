from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, loader, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from relight.models import UserInfo, Shop_Profile, Cus_Profile, Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


@login_required
def profile(request):
    if request.method == 'GET':
        user = request.user
        if (user.s_or_c == 'shop'):
            profile = Shop_Profile.objects.get(shop=user.id)
        if (user.s_or_c == 'cus'):
            profile = Cus_Profile.objects.get(cus=user.id)
        events = Event.objects.filter(user_id=user.id)

    template = loader.get_template('relight/profile.html')
    context = {
        'user': user,
        'events': events,
        'profile': profile,
    }
    return HttpResponse(template.render(context, request))


@login_required
def event_detail(request, event_title):
    if request.method == 'GET':
        event = Event.objects.get(title=event_title)
        user = request.user
        if (user.s_or_c == 'shop'):
            profile = Shop_Profile.objects.get(shop=user.id)
        if (user.s_or_c == 'cus'):
            profile = Cus_Profile.objects.get(cus=user.id)
        auth_user = Shop_Profile.objects.get(shop=event.user.id)

    template = loader.get_template('relight/event_detail.html')
    context = {
        'user': user,
        'profile': profile,
        'event': event,
        'auth_user': auth_user,
    }
    return HttpResponse(template.render(context, request))


@login_required
def shop_video(request, event_title):
    event = Event.objects.get(title=event_title)
    auth_user = Shop_Profile.objects.get(shop=event.user.id)
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
    auth_user = Shop_Profile.objects.get(shop=event.user.id)
    profile = Cus_Profile.objects.get(cus=user.id)
    template = loader.get_template('relight/cus_video.html')
    context = {
        'profile': profile,
        'event': event,
        'auth_user': auth_user,
    }
    return HttpResponse(template.render(context, request))


@login_required
def shop_profile(request, shop_name):
    if request.method == 'GET':
        user = request.user
        shop_profile = Shop_Profile.objects.get(name=shop_name)
        shop = UserInfo.objects.get(userid=shop_profile.shop)
        if (user.s_or_c == 'shop'):
            profile = Shop_Profile.objects.get(shop=user.id)
        if (user.s_or_c == 'cus'):
            profile = Cus_Profile.objects.get(cus=user.id)
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

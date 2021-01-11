from django.conf import settings
from django.shortcuts import render, loader, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from relight.models import UserInfo, Shop_Profile, Cus_Profile, Event
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from functools import reduce
from operator import and_
# Create your views here.


def top(request):
    template = loader.get_template('relight/top.html')
    return HttpResponse(template.render(None, request))


@login_required
def event_index(request):
    events = Event.objects.all()
    user = request.user
    if (user.s_or_c == 'shop'):
        profile = Shop_Profile.objects.get(shop=user.id)
    if (user.s_or_c == 'cus'):
        profile = Cus_Profile.objects.get(cus=user.id)
    template = loader.get_template('relight/event_index.html')
    context = {
        'profile': profile,
        'events': events,
        'user': user,
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
        profile = Shop_Profile.objects.get(shop=user.id)
    if (user.s_or_c == 'cus'):
        profile = Cus_Profile.objects.get(cus=user.id)
    template = loader.get_template('relight/shop_index.html')
    context = {
        'profile': profile,
        'shops': shops,
        'user': user,
    }
    return HttpResponse(template.render(context, request))


def event_searched(request):
    events = Event.objects.order_by('-id')
    keyword = request.GET.get('keyword')
    user = request.user
    if (user.s_or_c == 'shop'):
        profile = Shop_Profile.objects.get(shop=user.id)
    if (user.s_or_c == 'cus'):
        profile = Cus_Profile.objects.get(cus=user.id)

    if keyword:
        """ 除外リストを作成 """
        exclusion_list = set([' ', '　'])
        q_list = ''

        for i in keyword:
            """ 全角半角の空文字が含まれていたら無視 """
            if i in exclusion_list:
                pass
            else:
                q_list += i

        query = reduce(
            and_, [Q(title__icontains=q) | Q(detail__icontains=q)
                   for q in q_list]
        )
        events = events.filter(query)
        messages = ('「{}」の検索結果'.format(keyword))

    context = {
        'events': events,
        'user': user,
        'profile': profile,
        'messages': messages,
    }
    template = loader.get_template('relight/event_searched.html')
    return HttpResponse(template.render(context, request))


def shop_searched(request):
    shops = Shop_Profile.objects.order_by('-id')
    keyword = request.GET.get('keyword')
    user = request.user
    if (user.s_or_c == 'shop'):
        profile = Shop_Profile.objects.get(shop=user.id)
    if (user.s_or_c == 'cus'):
        profile = Cus_Profile.objects.get(cus=user.id)

    if keyword:
        """ 除外リストを作成 """
        exclusion_list = set([' ', '　'])
        q_list = ''

        for i in keyword:
            """ 全角半角の空文字が含まれていたら無視 """
            if i in exclusion_list:
                pass
            else:
                q_list += i

        query = reduce(
            and_, [Q(name__icontains=q) | Q(self_introduction__icontains=q)
                   for q in q_list]
        )
        shops = shops.filter(query)
        messages = ('「{}」の検索結果'.format(keyword))

    context = {
        'shops': shops,
        'user': user,
        'profile': profile,
        'messages': messages,
    }
    template = loader.get_template('relight/shop_searched.html')
    return HttpResponse(template.render(context, request))

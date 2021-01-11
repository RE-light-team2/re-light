from django.conf import settings
from django.shortcuts import render, loader, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from relight.models import UserInfo, Shop_Profile, Cus_Profile, Event
from relight.forms.create import Create_UserInfo_Form, Create_Cus_Form, Create_Shop_Form, Create_Event_Form
from django.views import View, generic
from django.core.signing import BadSignature, SignatureExpired, dumps, loads
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model


def create_account(request):
    template = loader.get_template('relight/create_account.html')
    return HttpResponse(template.render(None, request))


def create_customer(request):
    if request.method == 'GET':
        form_cus = Create_Cus_Form()
        form_user = Create_UserInfo_Form()
    else:
        form_user = Create_UserInfo_Form(request.POST)
        form_cus = Create_Cus_Form(request.POST, request.FILES or None)
        if form_user.is_valid():
            if form_cus.is_valid():
                print('user_regist is_valid')
                user = form_user.save(request.POST, "cus", commit=False)
                user.is_active = False
                user.save()
                prof = form_cus.save(
                    request.POST, request.FILES or None, user, commit=False)
                prof.save()
                current_site = get_current_site(request)
                domain = current_site.domain
                mail_context = {
                    'protocol': request.scheme,
                    'domain': domain,
                    'token': dumps(user.pk),
                    'prof': prof,
                }
                subject = "RE-light一般ユーザー登録のためのメール"
                message = render_to_string(
                    'relight/mail_template/message.txt', mail_context)
                user.email_user(subject, message)
                return redirect('/user_create/done')
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
        form_shop = Create_Shop_Form(request.POST, request.FILES)
        if form_user.is_valid():
            if form_shop.is_valid():
                user = form_user.save(request.POST, "shop", commit=False)
                user.is_active = False
                user.save()
                prof = form_shop.save(
                    request.POST, request.FILES, user, commit=False)
                prof.save()
                current_site = get_current_site(request)
                domain = current_site.domain
                mail_context = {
                    'protocol': request.scheme,
                    'domain': domain,
                    'token': dumps(user.pk),
                    'prof': prof,
                }
                subject = "RE-light企業ユーザー登録のためのメール"
                message = render_to_string(
                    'relight/mail_template/message.txt', mail_context)
                user.email_user(subject, message)
                return redirect('/user_create/done')
        else:
            print('user_regist false is_valid')

    template = loader.get_template('relight/create_shop.html')
    context = {
        'form_shop': form_shop,
        'form_user': form_user,
    }
    return HttpResponse(template.render(context, request))


@login_required
def create_event(request):
    user = request.user
    profile = Shop_Profile.objects.get(shop=user.id)
    if request.method == 'GET':
        form = Create_Event_Form()
    else:
        form = Create_Event_Form(request.POST, request.FILES)
        if form.is_valid():
            print('user_login is_valid')
            event_ins = form.save(
                request.POST, request.FILES, user, commit=False)
            event_ins.save()
            ev_detail = '/event/' + event_ins.title
            return redirect(ev_detail)

    template = loader.get_template('relight/create_event.html')
    context = {
        'form': form,
        'user': user,
        'profile': profile,
    }
    return HttpResponse(template.render(context, request))


def UserCreateDone(request):
    template = loader.get_template('relight/create_user_done.html')
    return HttpResponse(template.render(None, request))


def UserCreateComplete(request, token):
    """メール内URLアクセス後のユーザー本登録"""
    User = get_user_model()
    template = loader.get_template('relight/create_user_complete.html')
    timeout_seconds = getattr(
        settings, 'ACTIVATION_TIMEOUT_SECONDS', 60 * 60 * 24)  # デフォルトでは1日以内
    try:
        user_pk = loads(token, max_age=timeout_seconds)
        # 期限切れ
    except SignatureExpired:
        return HttpResponseBadRequest()

        # tokenが間違っている
    except BadSignature:
        return HttpResponseBadRequest()

        # tokenは問題なし
    else:
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return HttpResponseBadRequest()
        else:
            if not user.is_active:
                # 問題なければ本登録とする
                user.is_active = True
                user.save()
                return HttpResponse(template.render(None, request))
    return HttpResponseBadRequest()

from django.conf import settings
from django.shortcuts import render, loader, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from relight.models import UserInfo, Shop_Profile, Cus_Profile, Event
from relight.forms.forms import Create_UserInfo_Form, Create_Cus_Form, LoginForm, Create_Shop_Form, Create_Event_Form, Change_UserInfo_Form, Change_Cus_Form, Change_Shop_Form
from django.contrib.auth import authenticate, login
from django.views import View, generic
from django.core.signing import BadSignature, SignatureExpired, dumps, loads
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q
from functools import reduce
from operator import and_
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
        form_cus = Create_Cus_Form(request.POST, request.FILES)
        if form_user.is_valid():
            if form_cus.is_valid():
                print('user_regist is_valid')
                user = form_user.save(request.POST, "cus", commit=False)
                user.is_active = False
                user.save()
                prof = form_cus.save(
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
                subject = render_to_string(
                    'relight/mail_template/subject.txt', mail_context)
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
                subject = render_to_string(
                    'relight/mail_template/subject.txt', mail_context)
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


def Login(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            print('user_login is_valid')
            userid = form.cleaned_data.get('userid')
            password = form.cleaned_data.get('password')
            user = authenticate(userid=userid, password=password)
            if user is not None:
                if user.is_active:
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
            ev_detail = '/event/' + event_ins.title
            return redirect(ev_detail)

    template = loader.get_template('relight/create_event.html')
    context = {
        'form': form,
        'user': user,
        'profile': profile,
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


def change_profile(request):
    user = request.user
    if user.s_or_c == "cus":
        profile = Cus_Profile.objects.get(cus=user.id)
    else:
        profile = Shop_Profile.objects.get(shop=user.id)

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

        if user.s_or_c == "cus":
            form_prof = Change_Cus_Form(
                request.POST, request.FILES or None, instance=profile)
        else:
            form_prof = Change_Shop_Form(
                request.POST, request.FILES or None, instance=profile)
        if form_prof.is_valid():
            if form_user.is_valid():
                user_changed = form_user.save(request.POST, user, commit=False)
                user_changed.save()
                changed_prof = form_prof.save(
                    request.POST, request.FILES or None, user_changed, profile, commit=False)
                changed_prof.save()
                login(request, user_changed)
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
        print("Error1")
        return HttpResponseBadRequest()

        # tokenが間違っている
    except BadSignature:
        print("Error2")
        return HttpResponseBadRequest()

        # tokenは問題なし
    else:
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            print("Error3")
            return HttpResponseBadRequest()
        else:
            print("Error4")
            if not user.is_active:
                # 問題なければ本登録とする
                user.is_active = True
                user.save()
                return HttpResponse(template.render(None, request))
    print("Error5")
    return HttpResponseBadRequest()


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
    profile = Shop_Profile.objects.get(shop=user.id)

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

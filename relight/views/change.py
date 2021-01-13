from django.conf import settings
from django.shortcuts import render, loader, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from relight.models import UserInfo, Shop_Profile, Cus_Profile, Event
from relight.forms.change import Change_UserInfo_Form, Change_Cus_Form, Change_Shop_Form, Change_Event_Form
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
# Create your views here.


@login_required
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


@login_required
def change_event(request, event_title):
    user = request.user
    event = Event.objects.get(title=event_title)
    if user.s_or_c == "cus":
        profile = Cus_Profile.objects.get(cus=user.id)
    else:
        profile = Shop_Profile.objects.get(shop=user.id)

    if request.method == 'GET':
        initial_event = {
            'title': event_title,
            'detail': event.detail,
            'questionnaire_url': event.questionnaire_url,
        }
        form = Change_Event_Form(initial=initial_event)

    else:
        form = Change_Event_Form(request.POST, instance=event)

        if form.is_valid():
            event_changed = form.save(
                request.POST, request.FILES or None, event, commit=False)
            event_changed.save()
            url = '/event/'+event_changed.title
            return redirect(url)
        else:
            print('user_regist false is_valid')

    template = loader.get_template('relight/change_event.html')
    context = {
        'event': event,
        'form': form,
        'user': user,
        'profile': profile,
    }
    return HttpResponse(template.render(context, request))


def delete_event(request, event_title):
    user = request.user
    event = Event.objects.get(title=event_title)
    if user.s_or_c == "cus":
        profile = Cus_Profile.objects.get(cus=user.id)
    else:
        profile = Shop_Profile.objects.get(shop=user.id)

    if request.method == 'POST':
        print("post")
        if 'yes' in request.POST:
            print("post yes")
            event.delete()
        else:
            return redirect('/profile')
        return redirect('/profile')
    template = loader.get_template('relight/delete_event.html')
    context = {
        'event': event,
        'user': user,
        'profile': profile,
    }
    return HttpResponse(template.render(context, request))

from django.conf import settings
from django.shortcuts import render, loader, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponse
from relight.models import UserInfo
from relight.forms.auth import LoginForm
from django.contrib.auth import authenticate, login
from django.views import View, generic
from django.core.signing import BadSignature, SignatureExpired, dumps, loads
from django.template.loader import render_to_string
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def Login(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
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


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = UserInfo.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    email_template_name = "relight/mail_template/reset_message.txt"
                    subject = "RE-lightパスワードリセットのためのメール"
                    current_site = get_current_site(request)
                    domain = current_site.domain
                    c = {
                        "email": user.email,
                        'domain': domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': request.scheme,
                    }
                    message = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="relight/password_reset.html", context={"password_reset_form": password_reset_form})


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'relight/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    success_url = reverse_lazy('relight:password_reset_complete')
    template_name = 'relight/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'relight/password_reset_complete.html'

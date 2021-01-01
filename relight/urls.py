from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import index
from .views import auth
from .views import create
from .views import change
from .views import detail

app_name = "relight"

urlpatterns = [
    path('', index.top, name='top'),
    path('login/', auth.Login, name='login'),
    path('logout/', auth.Logout.as_view(), name='logout'),
    path('profile', detail.profile, name='profile'),
    path('privacy', index.privacy, name='privacy'),
    path('about', index.about, name='about'),
    path('cus_video/<str:event_title>', detail.cus_video, name='cus_video'),
    path('shop_video/<str:event_title>', detail.shop_video, name='shop_video'),
    path('ajax/<str:cus_name>', detail.ajax, name='ajax'),
    path('event_index', index.event_index, name='event_index'),
    path('shop_index', index.shop_index, name='shop_index'),
    path('shop_profile/<str:shop_name>',
         detail.shop_profile, name='shop_profile'),
    path('event/<str:event_title>', detail.event_detail, name='detail'),
    path('create_account', create.create_account, name='create_account'),
    path('cus/create', create.create_customer, name='create_customer'),
    path('shop/create', create.create_shop, name='create_shop'),
    path('user_create/done', create.UserCreateDone,
         name='user_create_done'),
    path('user_create/complete/<str:token>/', create.UserCreateComplete,
         name='user_create_complete'),
    path('change_profile', change.change_profile, name='change_profile'),
    path('create_event', create.create_event, name='create_event'),
    path('change_event/<str:event_title>',
         change.change_event, name='change_event'),
    path('delete_event/<str:event_title>',
         change.delete_event, name='delete_event'),
    path('event_searched', index.event_searched, name='event_searched'),
    path('shop_searched', index.shop_searched, name='shop_searched'),
    path('password_reset/', auth.password_reset_request,
         name='password_reset'),
    path('password_reset/done/', auth.PasswordResetDone.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth.PasswordResetConfirm.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth.PasswordResetComplete.as_view(),
         name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

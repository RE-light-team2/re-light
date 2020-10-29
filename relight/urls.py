from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .import views

urlpatterns = [
    path('', views.top, name='top'), 
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('profile', views.profile, name='profile'),
    path('cus_video/<str:event_title>', views.cus_video, name='cus_video'),
    path('shop_video/<str:event_title>', views.shop_video, name='shop_video'),
    path('index',views.event_index, name='index'),
    path('event/<str:event_title>',views.event_detail, name='detail'),
    path('create_account',views.create_account, name='create_account'),
    path('create_event',views.create_event, name='create_event'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
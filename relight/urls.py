from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .import views

urlpatterns = [
    path('', views.top, name='top'), 
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('shop/profile/<str:shop_id>', views.shop_profile, name='shop_profile'),
    path('video/<str:user_id>', views.video, name='video'),
    path('cus/profile/<str:cus_id>', views.cus_profile, name='cus_profile'),
    path('index/<str:user_id>',views.event_index, name='index'),
    path('event/<str:event_title>',views.event_detail, name='detail'),
    path('create_account',views.create_account, name='create_account'),
    path('create_event/<str:shop_id>',views.create_event, name='create_event'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
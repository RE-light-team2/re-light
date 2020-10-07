from django.urls import path
from .import views

urlpatterns = [
    path('', views.top, name='top'), 
    path('login/', views.login, name='login'),
    path('shop_profile/<int:shop_id>', views.shop_profile, name='shop_profile'),
    path('shop_video/<int:shop_id>', views.shop_video, name='shop_video'),
    path('cus_profile/<int:cus_id>', views.cus_profile, name='cus_login'),
    path('cus_video/<int:cus_id>', views.cus_video, name='cus_video'),
    path('index/',views.event_index, name='index'),
    path('index/<int:event_id>',views.event_detail, name='detail'),
    path('create_account',views.create_account, name='create_account'),
    path('create_event',views.create_event, name='create_event'),
]
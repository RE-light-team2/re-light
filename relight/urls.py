from django.urls import path
from .import views

app_name = 'relight'

urlpatterns = [
    path('', views.top, name='top'), 
    path('shop_login/', views.shop_login, name='shop_login'),
    path('shop_profile/<int:shop_id>', views.shop_profile, name='shop_profile'),
    path('shop_video/<int:shop_id>', views.shop_video, name='shop_video'),
    path('cus_login/', views.cus_login, name='cus_login'),
    path('cus_profile/<int:cus_id>', views.cus_profile, name='cus_login'),
    path('cus_video/<int:cus_id>', views.cus_video, name='cus_video'),
    path('index/',views.event_index, name='index'),
    path('index/<int:event_id>',views.event_detail, name='detail'),
    static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT),
]
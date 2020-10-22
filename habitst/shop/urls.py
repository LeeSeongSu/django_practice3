from django.conf.urls import url
from django.urls import path, include
from . import views

#지예가 추가한거
from django.contrib import admin
import shop.views
from django.conf import settings
from django.conf.urls.static import static
from shop import views as accounts_views
#from shop import views
from shop import views as accounts_views
app_name = 'shop'
urlpatterns = [
    url(r'^$', views.index, name='index', kwargs={'template_name': 'shop/item_list.html'}),
    url(r'^(?P<item_id>\d+)/order/new/$', views.order_new, name='order_new'),
    url(r'^(?P<item_id>\d+)/order/(?P<merchant_uid>[\da-f\-]{36})/pay/$', views.order_pay, name='order_pay'),
    path('meet_create', views.meet_create, name='meet_create'),
    path('withmepayment/<int:pk>', views.withmepayment, name='withmepayment'),
    url(r'^withmepayment(?P<item_id>\d+)/order/new/$', views.order_new, name='order_new'),
    url(r'^withmepayment(?P<item_id>\d+)/order/(?P<merchant_uid>[\da-f\-]{36})/pay/$', views.order_pay, name='order_pay'),
    #url(r'^shop/shop/withmepayment/(?P<item_id>\d+)/order/new/$', views.order_new, name='order_new'),
    #url(r'^shop/shop/withmepayment/(?P<item_id>\d+)/order/(?P<merchant_uid>[\da-f\-]{36})/pay/$', views.order_pay, name='order_pay'),
    #path(r'^(?P<pk>\d+)/', views.payment_detail, name='payment_detail'),
    url('withme2', views.withme2, name='withme2'),
    #url('withmepayment', views.withmepayment, name='withmepayment'),
   
]

"""habitst URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import appname.views
from django.conf import settings
from django.conf.urls.static import static
from appname import views as accounts_views
from django.conf.urls import url
from appname import views
from django.contrib.auth import views as auth_views
app_name = 'habitst'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', appname.views.main, name='main'),
    url(r'^core/', include('core.urls', namespace='core')),
    path('main2', appname.views.main2, name='main2'),
    path('create', appname.views.create, name='create'),
    path('update/<int:pk>', appname.views.update, name='update'),
    path('delete/<int:pk>', appname.views.delete, name='delete'),
    path('delete_comment/<int:pk>', appname.views.delete_comment, name='delete_comment'),
    path('delete_recom/<int:pk>', appname.views.delete_recom, name='delete_recom'),
    path('signin', appname.views.signin, name='signin'),
    path('signup', appname.views.signup, name='signup'),
    path('comment/<int:post_id>',appname.views.comment,name='comment'),
    path('create_recomment/<int:post_id>', appname.views.create_recomment , name='create_recomment'),
    path('hashtag/<str:hashtag_name>', appname.views.hashtag, name='hashtag'),
    path('like/<int:pk>',appname.views.like, name='like'),
    path('search', appname.views.search, name='search'),
    url('more/', appname.views.more, name='more'),
    path('category', appname.views.category, name='category'),
    path('habittest', appname.views.habittest, name='habittest'),
    path('myblog', appname.views.myblog, name='myblog'),
    path('mygroup', appname.views.mygroup, name='mygroup'),
    path('mypage', appname.views.mypage, name='mypage'),
    path('review', appname.views.review, name='review'),
    #path('search', appname.views.search, name='search'), #뷰스에 search가 두개가 있더라고요
    path('withme', appname.views.withme, name='withme'),
    path('accounts/', include('allauth.urls')),
    # path('accounts/', include('allauth.urls')),
    path('',include('django.contrib.auth.urls')),
    url(r'^shop/', include('shop.urls', namespace='shop')),
    url(r'^$', lambda request: redirect('shop:index'), name='root'),
    path('order/cancel/<str:imp_uid>', views.OrderCancel.as_view(), name='order_cancel'),
    url(r'^Test/', include('Test.urls')),
    # path('accounts/login/kakao/', appname.views.kakao_login, name='kakao_login'),
    # path('accounts/login/kakao/callback/',appname.views.kakao_callback, name='kakao_callback'),
    # path('/login/kakao',KakaoLoginView.as_view()),
    #카카오로그인
    path('postblog', appname.views.postblog, name='postblog'),
    path('postwithme', appname.views.postwithme, name='postwithme'),
    path('summernote/', include('django_summernote.urls')),
    path('new_post/', appname.views.new_post, name='new_post'),
    path('new_post/', appname.views.new_post, name='new_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

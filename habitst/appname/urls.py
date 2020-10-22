from django.contrib import admin
from django.urls import path, include
import appname.views
from django.conf import settings
from django.conf.urls.static import static
from appname import views as accounts_views
from django.conf.urls import url
from appname import views
from appname import views as accounts_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', appname.views.main, name='main'),
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
    path('category', appname.views.category, name='category'),
    path('habittest', appname.views.habittest, name='habittest'),
    path('myblog', appname.views.myblog, name='myblog'),
    path('mygroup', appname.views.mygroup, name='mygroup'),
    path('mypage', appname.views.mypage, name='mypage'),
    path('review', appname.views.review, name='review'),
    #path('search', appname.views.search, name='search'), #뷰스에 search가 두개가 있더라고요
    #path('withme/<int:pk>', appname.views.withme, name='withme'),
    #path('withmepayment', appname.views.withmepayment, name='withmepayment'),
    #path('member/<int:pk>',appname.views.member, name='member'),
 
    path('more', appname.views.more, name='more'),
    path('accounts/', include('allauth.urls')),
    # path('accounts/', include('allauth.urls')),
    path('',include('django.contrib.auth.urls')),
    
    #연결 url
    # url(r'^shop/', include('shop.urls', namespace='shop')),
    # url(r'^$', lambda request: redirect('shop:index'), name='root'),
    # url(r'^Test/', include('Test.urls')),
    
    path('order/cancel/<str:imp_uid>', views.OrderCancel.as_view(), name='order_cancel'),
    
    # path('accounts/login/kakao/', appname.views.kakao_login, name='kakao_login'),
    # path('accounts/login/kakao/callback/',appname.views.kakao_callback, name='kakao_callback'),
    # path('/login/kakao',KakaoLoginView.as_view()),
    
    #카카오로그인
    path('postblog', appname.views.postblog, name='postblog'),
    #path('postwithme', appname.views.postwithme, name='postwithme'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

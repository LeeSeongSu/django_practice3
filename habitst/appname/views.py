from django.shortcuts import render, redirect,get_object_or_404
from .models import Post,CustomUser, Hashtag, Comment, ReComment

from .forms import PostForm,SigninForm,UserForm,CommentForm, HashtagForm, ReCommentForm
from django.http import HttpResponseRedirect
# from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse

from .forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect 
import urllib 
from django.db.models import Count
from django.contrib.auth.models import User

############성수의 import
from shop.models import Order
from Test.models import Tester
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView
from django.contrib import messages
# Create your views here.



def new_post(request):
    form = PostForm()
    return render(request, 'new_post.html', {'form': form})





def main(request):
    sort = request.GET.get('sort','')
    if sort == 'likes':
        posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count','-id')
        users = CustomUser.objects.all()
        signin_form = SigninForm()
        comment_form = CommentForm()
        recomment_form = ReCommentForm()
        return render(request, 'appname/main.html', {'posts': posts,'comment_form': comment_form,'users':users,'signin_form':signin_form, 'recomment_form':recomment_form})
    else:
        posts = Post.objects.all().order_by('-id')
        users = CustomUser.objects.all()
        signin_form = SigninForm()
        comment_form = CommentForm()
        recomment_form = ReCommentForm()
        return render(request, 'appname/main.html', {'posts': posts,'comment_form': comment_form,'users':users,'signin_form':signin_form, 'recomment_form':recomment_form})

    # posts = Post.objects.all().order_by('-id')
    
def main2(request):
    return render(request, 'appname/main2.html')    
    
def create(request):
    if not request.user.is_active:
        signin_form = SigninForm()
        return render(request, 'appname/signin.html', {'signin_form': signin_form})


    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            
            hashtag_field = form.cleaned_data['hashtag_field']
            str_hashtags = hashtag_field.split('#')
            list_hashtags = list()    

            for hashtag in str_hashtags:
                if Hashtag.objects.filter(name=hashtag):
                    list_hashtags.append(Hashtag.objects.get(name=hashtag))
                else:
                    temp_hashtag = HashtagForm().save(commit=False)
                    temp_hashtag.name = hashtag
                    temp_hashtag.save()
                    list_hashtags.append(temp_hashtag)
                
            post.save()
            post.hashtags.add(*list_hashtags)

            return redirect('main')
    else:
        form = PostForm()
        return render(request, 'appname/create.html', {'form': form})

def read(request):
    return redirect('main')

def update(request, pk):   
    if not request.user.is_active:
        signin_form = SigninForm()
        return render(request, 'appname/signin.html', {'signin_form': signin_form})
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('main')
    else:
        form = PostForm(instance=post)
        return render(request,'appname/create.html',{'form':form})
    

def delete(request, pk):
    if not request.user.is_active:
        signin_form = SigninForm()
        return render(request, 'appname/signin.html', {'signin_form': signin_form})
    post = get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('main')

def delete_comment(request, pk):
    if not request.user.is_active:
        signin_form = SigninForm()
        return render(request, 'appname/signin.html', {'signin_form': signin_form})
    post = get_object_or_404(Comment, pk=pk)
    post.delete()
    return redirect('main')

def delete_recom(request, pk):
    if not request.user.is_active:
        signin_form = SigninForm()
        return render(request, 'appname/signin.html', {'signin_form': signin_form})
    post = get_object_or_404(ReComment, pk=pk)
    post.delete()
    return redirect('main')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)

        if user is not None:
            login(request,user)
            return redirect('main')
        else:
            return HttpResponse("로그인 실패. 다시 시도해보세요")
    else:
        signin_form = SigninForm()
        return render(request, 'appname/signin.html', {'signin_form': signin_form})

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            new_user = CustomUser.objects.create_user(username=form.cleaned_data['username'],
            email = form.cleaned_data['email'],
            password = form.cleaned_data['password'],
            nickname = form.cleaned_data['nickname'],
            phone_number = form.cleaned_data['phone_number'],
            profile_image = form.cleaned_data['profile_image'])
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('main')
        else:
            return HttpResponse("회원가입 실패!")
    else:
        form = UserForm()
        return render(request,'appname/signup.html',{'form':form})

def comment(request,post_id):
    if not request.user.is_active:
        return HttpResponse("Can't write a post without Sign In")
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.c_writer = request.user
            comment.post_id = post
            comment.text = form.cleaned_data['text']
            comment.save()
            return redirect('main')

def create_recomment(request, post_id):
    if not request.user.is_active:
        return HttpResponse("Can't write a post without Sign In")
    post = get_object_or_404(Comment, id=post_id)
    if request.method == "POST":    
        filled_form = ReCommentForm(request.POST)
        if filled_form.is_valid():
            comment = filled_form.save(commit=False)
            comment.rc_writer = request.user
            comment.post_id = post
            comment.text = filled_form.cleaned_data['text']
            filled_form.save()
            return redirect('main')

def hashtag(request, hashtag_name):
    hashtag=get_object_or_404(Hashtag, name=hashtag_name)
    #return render(request, 'insta/hashtag.html', {'hashtag': hashtag})
    # posts = Post.objects.all()
    sort = request.GET.get('sort','') #url의 쿼리스트링을 가져온다. 없는 경우 공백을 리턴한다

    if sort == 'likes':
        hashtags = Post.objects.all().annotate(likes=hashtags.like_count('likes')).order_by('-likes', '-id')
        return render(request, 'insta/hashtag.html', {'hashtags' : hashtags, 'hashtag': hashtag})
    else:
        hashtags = Post.objects.all().order_by('-id')
        return render(request, 'insta/hashtag.html', {'hashtags' : hashtags, 'hashtag': hashtag})

def like(request,pk):
    if not request.user.is_active:
        return HttpResponse('First SignIn please')

    post = get_object_or_404(Post,pk=pk)
    user = request.user

    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    return redirect('main')

   
    
def profile(request,user_id):
    
    if not request.user.is_active:
        signin_form = SigninForm()
        return render(request, 'appname/signin.html', {'signin_form': signin_form})

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)

        if user is not None:
            login(request,user)
            return redirect('main')
        else:
            return HttpResponse("로그인 실패. 다시 시도해보세요")
    else:
        posts = Post.objects.all()
        comment_form = CommentForm()
        return render(request, 'appname/profile.html', {'posts': posts,'comment_form': comment_form})
    
    
@login_required 
def profile_update(request):
    if request.method == 'GET':
        return render(request, 'appname/profile_update.html')

    elif request.method == 'POST':
        user = request.user
        email = request.POST.get('email')
        username = request.POST.get('username')
        new_user_pw = request.POST.get('new_user_pw')
        nickname = request.POST.get('nickname')

      
        user.email = email
        user.username = username
        user.nickname = nickname
        user.set_password(new_user_pw)

        user.save()


        return redirect('main')

def search(request):
    posts = Post.objects.all().order_by('-id')
    users = CustomUser.objects.all()
    q = request.POST.get('q', "") 

    if q:
        posts = posts.filter(writer__username__icontains=q)
        return render(request, 'appname/search.html', {'posts' : posts, 'q' : q, 'users' : users})
    
    else:
        return render(request, 'appname/search.html')

def category(request):
    return render(request, 'appname/category.html')

def habittest(request):
    return render(request, 'appname/habittest.html')

def myblog(request):
    return render(request, 'appname/myblog.html')

def mygroup(request):
    return render(request, 'appname/mygroup.html')

def mypage(request):
    order_list = Order.objects.filter(user=request.user)
    test_list = Tester.objects.filter(name=request.user).last()
    return render(request, 'appname/mypage.html', {
        'order_list': order_list,
        'test_list' : test_list,
    })

def review(request):
    return render(request, 'appname/review.html')

#def search(request):
    #return render(request, 'appname/search.html')

def withme(request):
    return render(request, 'appname/withme.html')

# code 요청
def kakao_login(request):
    app_rest_api_key = "38f54ea64798fa95b74475fabaa40cee"
    redirect_uri = "http://127.0.0.1:8000/accounts/login/kakao/callback/"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )
    
    
# access token 요청
def kakao_callback(request):                                                                  
    params = urllib.parse.urlencode(request.GET)                                      

    return redirect(f'http://127.0.0.1:8000/accounts/login/kakao/callback/?{params}')   

def main2(request):
    return render(request, 'appname/main2.html')


@method_decorator(login_required, name='dispatch')
class OrderCancel(RedirectView):
    url = 'mypage'

    def get(self, request, *args, **kwargs):
        queryset = Order.objects.get(imp_uid=self.kwargs.get('imp_uid'))
        try:

            if queryset.status == "cancelled":
                print("여기?")
                messages.error(self.request, '이미 주문을 취소하셨습니다.')
                print("취소가 이미됨")
                return redirect(self.url)

            elif queryset.status == "paid":
                messages.error(self.request, '거래가 완료된 상태입니다.')
                queryset.cancel()
                queryset.update()
                messages.info(self.request, '주문을 취소하셨습니다.')
                print("주문취소?")
                return redirect(self.url)

            queryset.cancel()
            messages.info(self.request, '주문을 취소하셨습니다.')
        except:
            messages.error(self.request, '유효하지 않은 상품입니다.')
            

        return redirect(self.url)

def more(request):
    # posts = Post.objects.get(pk=pk)
    # users = CustomUser.objects.all()
    # signin_form = SigninForm()
    comment_form = CommentForm()
    recomment_form = ReCommentForm()
    if 'id' in request.GET:
        post = get_object_or_404(Post,pk=request.GET.get('id'))
        return render(request, 'appname/more.html', {'post': post,'comment_form':comment_form,'recomment_form':recomment_form})
    return HttpResponseRedirect('appname/main/')

def postblog(request):
    return render(request, 'appname/postblog.html')

def postwithme(request):
    return render(request, 'appname/postwithme.html')

def search(request):
    posts = Post.objects.all().order_by('-id')
    users = CustomUser.objects.all()
    q = request.POST.get('q', "") 

    if q:
        posts = posts.filter(title__icontains=q)
        return render(request, 'appname/search.html', {'posts' : posts, 'q' : q, 'users' : users})
    
    else:
        return render(request, 'appname/search.html')


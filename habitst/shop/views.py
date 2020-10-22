from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Item, Order
from .forms import PayForm,ItemForm
from appname.forms import HashtagForm


#지예의 import
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
import urllib
from django.db.models import Count
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import RedirectView
from django.http import HttpResponseRedirect

class ItemListView(ListView):
    model = Item
    queryset = Item.objects.filter(is_public=True)

    def get_queryset(self):
        self.q = self.request.GET.get('q', '')
        qs = super().get_queryset()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ItemListView,self).get_context_data(**kwargs)
        context['q'] = self.q
        context['Order_list'] = Order.objects.all()
      
        return context
 

index = ItemListView.as_view()
# Create your views here.


@login_required
def order_new(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    order = Order.objects.create(user=request.user, item=item, name=item.name, amount=item.amount)
    return redirect('shop:order_pay', item_id, str(order.merchant_uid))


@login_required
def order_pay(request, item_id, merchant_uid):
    order = get_object_or_404(Order, user=request.user, merchant_uid=merchant_uid, status='ready')
    if request.method == 'POST':
        form = PayForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('mypage')
    else:
        form = PayForm(instance=order)
    return render(request, 'shop/pay_form.html', {
        'form': form,
    })

def meet_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.username = request.user           
            post.save()
            return redirect('./')
    else:
        form = ItemForm()
        return render(request, 'shop/meet_create.html', {'form': form})

def withme2(request):
    # posts=Item.objects.get(pk=pk)
    # context={
    #     'posts': posts
    # }
    # return render(request, 'shop/withme2.html', context)

    if 'id' in request.GET:
        posts = get_object_or_404(Item,pk=request.GET.get('id'))
        return render(request, 'shop/withme2.html', {'posts': posts})
    return HttpResponseRedirect('/shop/')
    #members = Item.objects.annotate(other_idd=Count('member'))
    #user=request.user
    #posts = Item.objects.filter(writer=user.pk) #withme 들어가지는 a태그는 href="/withme2/{{ user.pk }}"
    #return render(request, 'shop/withme2.html', {'posts':posts})

def withmepayment(request,pk):
    posts = Item.objects.get(pk=pk)
    user = request.user
    
    if not posts.member.filter(id=user.id).exists():
        posts.member.add(user)
    return render(request, 'shop/withmepayment.html', {'posts':posts})
    

def payment_detail(request, pk):
    post=Item.objects.get(pk=pk)
    context={
        'post': post
    }
    return render(request, 'shop/order_form.html', context)

"""
def postwithme(request):
    if not request.user.is_active:
        return HttpResponse("Can't write a post without Sign In")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user

            hashtag_field = form.cleaned_data['hashtag_field']
            str_hashtags = hashtag_field.split('#')
            list_hashtags = list()

            for hashtag in str_hashtags:
                hashtag = hashtag.strip()
                if Hashtag.objects.filter(name=hashtag):
                    list_hashtags.append(Hashtag.objects.get(name=hashtag))
                else:
                    temp_hashtag = HashtagForm().save(commit=False)
                    temp_hashtag.name = hashtag
                    temp_hashtag.save()
                    list_hashtags.append(temp_hashtag)

            post.save()
            post.hashtags.add(*list_hashtags)

            #form.save_m2m()
            return redirect('./')
    else:
        form = PostForm()
        return render(request, 'shop/postwithme.html', {'form': form})
"""

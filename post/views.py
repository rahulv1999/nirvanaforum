# from audioop import reverse
from multiprocessing import context
from unicodedata import category
from django.urls import reverse
from django.shortcuts import redirect, render,get_list_or_404, get_object_or_404
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from .models import Account, Post, Author, Category, PostLike, PostView, Images,Comment, homeData
from django.db.models import Q
from .forms import CommentForm,PostForm, UserCreateForm,ProfileUpdateForm
from PIL import Image
from forex_python.converter import CurrencyRates
import san
from datetime import date,datetime
import pytz
import json
from django.contrib.auth import get_user_model
# from StringIO import StringIO
User = get_user_model()
post_per_page = 10

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None 

def search(request):
    queryset = Post.objects.order_by('-timestamp')
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) 
        ).distinct()
    paginator = Paginator(queryset,post_per_page)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)

    except PageNotAnInteger :
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'querysetSearch' : paginated_queryset,
        'page_request_var' : page_request_var,
        'searchText' : query,
    }

    return render(request,'search_results.html',context)


def index(request):
    # # queryset = Post.objects.filter(featured=True)
    # queryset = Post.objects.order_by('-timestamp')[0:3]
    # context = {
    #     'object_list' : queryset
    # }
    return redirect("post-list")


def blog(request):
    post_list = Post.objects.filter(featured=True).order_by('-timestamp')
    paginator = Paginator(post_list,post_per_page)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    categories = Category.objects.all()
    homedata = homeData.objects.all().order_by("-timestamp")
    today = date.today().strftime("%B %d %Y")

    if len(homedata)==0:
        c = CurrencyRates()
        d = c.get_rates('USD')
        btc = san.get("ohlc/bitcoin").tail().iloc[4,0]
        eth = san.get("ohlc/ethereum").tail().iloc[4,0]
        
        homeData.objects.create(
            btc = btc,
            eth = eth,
            eur = d['EUR'],
            gbp = d['GBP']
        )
    else :
        if (datetime.now(pytz.UTC) - homedata[0].timestamp).total_seconds() > 60*60*24:
            c = CurrencyRates()
            d = c.get_rates('USD')
            btc = san.get("ohlc/bitcoin").tail().iloc[4,0]
            eth = san.get("ohlc/ethereum").tail().iloc[4,0]
            
            homeData.objects.create(
                btc = btc,
                eth = eth,
                eur = d['EUR'],
                gbp = d['GBP']
            )
        else :
            btc = json.dumps(float(homedata[0].btc)),
            eth = json.dumps(float(homedata[0].eth)),
            eur = json.dumps(float(homedata[0].eur)),
            gbp = json.dumps(float(homedata[0].gbp))


    currency = [eur[0],gbp[0],btc[0],eth[0],today]


    try:
        paginated_queryset = paginator.page(page)

    except PageNotAnInteger :
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'queryset' : paginated_queryset,
        'page_request_var' : page_request_var,
        'categories' : categories,
        'message' : 'Welcome to Nirvana Forum',
        'flag' : 1,
        'currency' : currency,
    }

    return render(request,'blog.html',context)


def post(request,id):
    post = get_list_or_404(Post, id=id)[0]
    form = CommentForm(request.POST or None)
    thumbnail = Images.objects.filter(post=post)

    if request.method == "POST" : 
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()

    context = {
        'post' : post,
        'form' : form,
        'queryset' : thumbnail,
    }

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)
    return render(request,'post.html',context)

def reply(request,id,post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    thumbnail = Images.objects.filter(post=post)

    if request.method == "POST" : 
        commentReply = request.POST.get(f'reply_{id}')
        print(commentReply)
        Comment.objects.create(
            user = request.user,
            content = commentReply,
            post = post,
            parent = Comment.objects.get(id=id)
        )
        return redirect("post-detail",id=post.id)
    context = {
        'post' : post,
        'form' : form,
        'queryset' : thumbnail,
    }

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)
    return render(request,'post.html',context) 

def post_cat(request,id):
    cat = get_object_or_404(Category,id=id)
    post_list = Post.objects.filter(categories=cat).order_by('-timestamp')
    paginator = Paginator(post_list,post_per_page)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)

    except PageNotAnInteger :
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'queryset' : paginated_queryset,
        'page_request_var' : page_request_var,
        'message' : cat.title,
        'flag' : 0,
    }
    return render(request,'blog.html',context)

def post_create(request):
    if not request.user.is_authenticated:
        return redirect("post-list")
    title = "Create"
    form = PostForm(request.POST or None)    
    author = get_author(request.user)
    
    if not author : 
        author = Author(user=request.user)
        author.save()

    if request.method == "POST":
        print(request.FILES,request)
        imageslist = request.FILES.getlist('imagesUpload')

        if form.is_valid():
            form.instance.author = author
            form.instance.featured = False
            form.save()
            for img in imageslist:
                Images.objects.create(thumbnail=img,post=form.instance)

            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        "form" : form,
        "title" : title,

    }
    return render(request,"post_create.html",context)


def post_update(request,id):
    title = "Update"
    post = get_object_or_404(Post,id=id)
    form = PostForm(request.POST or None, request.FILES or None,instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        # print(request,2,form)
        if form.is_valid():
            form.instance.author = author
            form.instance.feature = False
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        "form" : form,
        "title" : title
    }
    return render(request,"post_create.html",context)

def post_delete(request,id):
    post = get_object_or_404(Post,id=id)
    post.delete()
    return redirect(reverse("post-list"))



def register(request):
    form = UserCreateForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(reverse("post-list"))
    
    context = {
        'form' : form,
    }
    return render(request,'account/signup.html',context)


def profile_update(request,id):
    user  = get_object_or_404(User,id=id)
    account = get_object_or_404(Account,user = user)
    form = ProfileUpdateForm(request.POST or None, request.FILES or None,instance=account)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect(reverse("post-list"))
    
    context = {
        'form' : form,
    }
    return render(request,'profile_update.html',context)
        





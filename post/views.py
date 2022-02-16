# from audioop import reverse
from multiprocessing import context
from unicodedata import category
from django.urls import reverse
from django.shortcuts import redirect, render,get_list_or_404, get_object_or_404
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from .models import Post, Author, Category
from django.db.models import Q
from .forms import CommentForm,PostForm


def get_author(user):
    qs = Author.objects.filter(user=user)

    if qs.exists():
        return qs[0]
    return None 

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query) 
        ).distinct()

    context = {
        'querysetSearch' : queryset,
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
    post_list = Post.objects.order_by('-timestamp')
    paginator = Paginator(post_list,5)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    categories = Category.objects.all()
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
        'message' : 'Welcome to Blog Post',
        'flag' : 1,
    }

    return render(request,'blog.html',context)


def post(request,id):
    post = get_list_or_404(Post, id=id)[0]
    form = CommentForm(request.POST or None)
    
    if request.method == "POST" : 
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            
            form.save()
            return redirect("post-detail",id=post.id)
    context = {
        'post' : post,
        'form' : form
    }
    return render(request,'post.html',context)


def post_cat(request,id):
    cat = get_object_or_404(Category,id=id)
    post_list = get_list_or_404(Post.objects.order_by('-timestamp'), categories=cat)
    paginator = Paginator(post_list,3)
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
    form = PostForm(request.POST or None, request.FILES or None)
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






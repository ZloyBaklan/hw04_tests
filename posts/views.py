from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from yatube.settings import postsconstant

from .models import Group, Post, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, postsconstant)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'paginator': paginator,
        'page': page,
    }
    return render(request, "index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, postsconstant)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'group': group,
        'paginator': paginator,
        'page': page,
    }
    return render(
        request, "group.html", context
    )


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:index')
    return render(request, 'new.html', {'form': form})


def profile(request, username):
    author_posts = get_object_or_404(User, username=username)
    posts = author_posts.post_author.all()
    paginator = Paginator(posts, postsconstant)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'author_posts': author_posts,
        'paginator': paginator,
        'page': page,
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    author_one_post = get_object_or_404(User, username=username)
    post_V = author_one_post.post_author.all()
    post = get_object_or_404(Post, id=post_id, author=author_one_post)
    context = {
        'author_one_post': author_one_post,
        'post': post,
        'post_V': post_V,
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = Post.objects.get(id=post_id, author=request.user)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post', username=post.author, post_id=post.id)
    context = {
        'form': form,
        'author': author,
        'post': post
    }
    return render(request, 'new.html', context)

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Group, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
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
    paginator = Paginator(posts, 10)
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
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('posts:index'))
    return render(request, 'new.html', {'form': form})


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile).all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    count = Post.objects.filter(author=profile).count()
    context = {
        'profile': profile,
        'paginator': paginator,
        'page': page,
        'count': count,
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    profile_one_post = get_object_or_404(User, username=username)
    item = get_object_or_404(Post, id=post_id)
    postV = Post.objects.filter(
        author=profile_one_post
    ).filter(id=post_id).all()
    count = Post.objects.filter(author=profile_one_post).count()
    context = {
               'profile_one_post': profile_one_post,
               'item': item,
               'postV': postV,
               'count': count
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    point = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'GET':
        form = PostForm(instance=point)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=point)
        if form.is_valid():
            edit_point = form.save(commit=False)
            point.text = edit_point.text
            point.group = edit_point.group
            point.save()
        return redirect('posts:post', username=point.author, post_id=point.id)
    context = {
               'form': form,
               'author': author,
               'point': point
    }
    return render(request, 'new.html', context)

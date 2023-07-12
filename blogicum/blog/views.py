from django.utils import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404, render

from blog.models import Category, Post


def index(request):
    now = timezone.now()
    template = 'blog/index.html'
    posts = Post.objects.filter(
        category__is_published=True,
        is_published=True,
        pub_date__lt=now).order_by('-id')[:settings.POSTS_LIMIT]
    context = {'post_list': posts}

    return render(request, template, context)


def post_detail(request, post_id):
    now = timezone.now()
    posts = get_object_or_404(
        Post,
        id=post_id,
        is_published=True,
        pub_date__lt=now,
        category__is_published=True
    )
    template = 'blog/detail.html'
    context = {'post': posts}

    return render(request, template, context)


def category_posts(request, slug):
    now = timezone.now()
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=slug,
        is_published=True,
    )
    posts = category.posts.all().filter(pub_date__lt=now, is_published=True)
    context = {
        'category': category,
        'post_list': posts
    }

    return render(request, template, context)

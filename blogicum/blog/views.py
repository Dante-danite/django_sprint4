from django.utils import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from blog.models import Category, Post, Comment
from .forms import PostForm, UserForm, CommentForm


def index(request):
    template = 'blog/index.html'

    now = timezone.now()
    posts = Post.objects.filter(
        category__is_published=True,
        is_published=True,
        pub_date__lt=now).order_by('-pub_date')
    paginator = Paginator(posts, settings.POSTS_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}

    return render(request, template, context)


@login_required
def post_detail(request, pk):
    now = timezone.now()

    posts = Post.objects.filter(Q(is_published=True,
                                  category__is_published=True,
                                  pub_date__lt=now) | Q(author=request.user))

    post = get_object_or_404(posts, id=pk)

    comments = post.comments.all().order_by('created_at')
    form = CommentForm()
    template = 'blog/detail.html'
    context = {'post': post, 'form': form, 'comments': comments}

    return render(request, template, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user.get_username()
        return reverse('blog:profile', args=(username,))


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_id = kwargs['pk']
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', pk=self.post_id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', args=(self.post_id,))


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_id = kwargs['pk']
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', pk=self.post_id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:index')


def category_posts(request, slug):
    template = 'blog/category.html'

    now = timezone.now()
    category = get_object_or_404(Category, slug=slug, is_published=True)
    posts = category.posts.all().filter(
        pub_date__lt=now,
        is_published=True
        ).order_by('-pub_date')

    paginator = Paginator(posts, settings.POSTS_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj
    }

    return render(request, template, context)


def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    template = 'blog/profile.html'
    posts = Post.objects.filter(
        author__id=user.id).order_by('-pub_date')
    paginator = Paginator(posts, settings.POSTS_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'profile': user, 'page_obj': page_obj}

    return render(request, template, context)


@login_required
def edit_profile(request):
    template = 'blog/user.html'
    form = UserForm(request.POST or None, instance=request.user)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=post_id)


@login_required
def edit_comment(request, comment_id, post_id):
    instance = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    form = CommentForm(request.POST or None, instance=instance)
    if instance.author != request.user:
        return redirect('blog:post_detail', pk=post_id)
    context = {
        'form': form,
        'comment': instance
    }

    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', pk=post_id)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, comment_id, post_id):
    instance = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if instance.author != request.user:
        return redirect('blog:post_detail', pk=post_id)
    context = {'comment': instance}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', pk=post_id)
    return render(request, 'blog/comment.html', context)

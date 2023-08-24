from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path(
        'category/<slug:slug>/',
        views.category_posts,
        name='category_posts'
    ),

    path(
        'profile/<str:username>/',
        views.user_detail,
        name='profile'
    ),
    path(
        'edit_profile',
        views.edit_profile,
        name='edit_profile'
    ),
    path(
        '',
        views.index,
        name='index'
    ),
    path(
        'posts/<int:pk>/',
        views.post_detail,
        name='post_detail'
    ),
    path(
        'posts/create/',
        views.PostCreateView.as_view(),
        name='create_post'
    ),
    path(
        'posts/<int:pk>/edit/',
        views.PostEditView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:pk>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post'
    ),

    path(
        'posts/<int:post_id>/comment',
        views.add_comment,
        name='add_comment'
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>',
        views.edit_comment,
        name='edit_comment'
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>',
        views.delete_comment,
        name='delete_comment'
    )
]
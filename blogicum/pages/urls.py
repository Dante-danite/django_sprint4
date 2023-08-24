from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path("about/", views.AboutPage.as_view(), name='about'),
    path("rules/", views.RulesPage.as_view(), name='rules'),
    path("404/", views.NotFoundPage.as_view()),
    path("403csrf/", views.CsrfErrorPage.as_view()),
    path("500/", views.ServerErrorPage.as_view()),
]

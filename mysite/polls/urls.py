"""'include()'ed in mysite/urls.py"""
from django.urls import path
from . import views

# Namespace to differentiate URL names between apps in a Django project
# Templates refer to path names using app_name:path_name
app_name = "polls"

urlpatterns = [
    # path() function is passed four arguments, two required: route and view, and two
    # optional: kwargs, and name
    # - route: a string that contains a URL pattern
    # - view: when Django finds a matching pattern, it calls the specified view
    # function with an HttpRequest object as the first argument and any "captured"
    # values from the route as keyword arguments
    # - kwargs: arbitrary keyword arguments can be passed in a dictionary to the target
    # view
    # - name: naming your URL lets you refer to it unambiguously from elsewhere in
    # Django, especially from within templates
    # path("", views.index, name="index"),
    # Generic list view
    path("", views.IndexView.as_view(), name="index"),
    # path("<int:question_id>/", views.detail, name="detail"),
    # Generic detail view - expects the primary key value captured from the URL to be
    # called "pk", so we've changed question_id to pk.
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),  # Generic detail view
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]

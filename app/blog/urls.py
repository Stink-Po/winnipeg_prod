from django.urls import path
from .views import post_detail, post_list, create_post
from .feeds import LatestPostsFeed

app_name = "blog"

urlpatterns = [
    path("", post_list, name="post_list"),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path("<int:year>/<int:month>/<int:day>/<slug:post>/", post_detail, name="post_detail"),
    path("feed/", LatestPostsFeed(), name="post_feed"),
    path("new-post/", create_post, name="create_post"),
]

from django.urls import path
from . import views


urlpatterns = [

    # Home
    path("", views.home, name="home"),

    # Authentication
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Posts
    path("post/create/", views.create_post, name="create_post"),
    path("post/<int:post_id>/delete/", views.delete_post, name="delete_post"),

    # Comments
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),

    # Likes
    path("post/<int:post_id>/like/", views.like_post, name="like_post"),

    # Edit profile MUST come before username profile
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    # User profile
    path("profile/<str:username>/", views.profile_view, name="profile"),

    # Follow
    path("follow/<str:username>/", views.follow_user, name="follow_user"),

    # Search
    path("search/", views.search_users, name="search_users"),
]
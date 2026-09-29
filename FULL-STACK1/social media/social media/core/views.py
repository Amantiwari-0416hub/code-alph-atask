from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Profile, Post, Comment, Like, Follow
from .forms import RegisterForm, ProfileForm, PostForm


# -----------------------------
# HOME / FEED
# -----------------------------
@login_required
def home(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    posts = Post.objects.all().order_by("-created_at")

    return render(request, "index.html", {
        "page": "home",
        "posts": posts,
        "profile": profile,
    })


# -----------------------------
# REGISTER
# -----------------------------
def register_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # Securely save password
            user.set_password(
                form.cleaned_data["password"]
            )

            user.save()

            # Automatically create profile
            Profile.objects.create(user=user)

            messages.success(
                request,
                "Account created successfully. Please login."
            )

            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "index.html", {
        "page": "register",
        "form": form,
    })


# -----------------------------
# LOGIN
# -----------------------------
def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            Profile.objects.get_or_create(
                user=user
            )

            return redirect("home")

        else:
            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "index.html", {
        "page": "login",
    })


# -----------------------------
# LOGOUT
# -----------------------------
def logout_view(request):

    logout(request)

    return redirect("login")


# -----------------------------
# CREATE POST
# -----------------------------
@login_required
def create_post(request):

    if request.method == "POST":

        form = PostForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            post = form.save(commit=False)

            post.user = request.user

            post.save()

            messages.success(
                request,
                "Post created successfully."
            )

            return redirect("home")

    else:
        form = PostForm()

    return render(request, "index.html", {
        "page": "create_post",
        "form": form,
    })


# -----------------------------
# DELETE POST
# -----------------------------
@login_required
def delete_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user
    )

    if request.method == "POST":
        post.delete()

        messages.success(
            request,
            "Post deleted."
        )

    return redirect("home")


# -----------------------------
# ADD COMMENT
# -----------------------------
@login_required
def add_comment(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    if request.method == "POST":

        text = request.POST.get(
            "comment",
            ""
        ).strip()

        if text:

            Comment.objects.create(
                user=request.user,
                post=post,
                text=text
            )

    return redirect("home")


# -----------------------------
# LIKE / UNLIKE POST
# -----------------------------
@login_required
def like_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    like = Like.objects.filter(
        user=request.user,
        post=post
    ).first()

    # If already liked → unlike
    if like:
        like.delete()

    # Otherwise → like
    else:
        Like.objects.create(
            user=request.user,
            post=post
        )

    return redirect("home")


# -----------------------------
# USER PROFILE
# -----------------------------
@login_required
def profile_view(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    profile, created = Profile.objects.get_or_create(
        user=profile_user
    )

    posts = Post.objects.filter(
        user=profile_user
    ).order_by("-created_at")

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    return render(request, "index.html", {

        "page": "profile",

        "profile_user": profile_user,

        "profile": profile,

        "posts": posts,

        "followers_count": followers_count,

        "following_count": following_count,

        "is_following": is_following,
    })


# -----------------------------
# EDIT PROFILE
# -----------------------------
@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect(
                "profile",
                username=request.user.username
            )

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(request, "index.html", {

        "page": "edit_profile",

        "form": form,

        "profile": profile,
    })


# -----------------------------
# FOLLOW / UNFOLLOW
# -----------------------------
@login_required
def follow_user(request, username):

    user_to_follow = get_object_or_404(
        User,
        username=username
    )

    # User cannot follow himself
    if user_to_follow == request.user:

        messages.warning(
            request,
            "You cannot follow yourself."
        )

        return redirect(
            "profile",
            username=username
        )

    follow = Follow.objects.filter(
        follower=request.user,
        following=user_to_follow
    ).first()

    # Already following → unfollow
    if follow:

        follow.delete()

    # Not following → follow
    else:

        Follow.objects.create(
            follower=request.user,
            following=user_to_follow
        )

    return redirect(
        "profile",
        username=username
    )


# -----------------------------
# SEARCH USERS
# -----------------------------
@login_required
def search_users(request):

    query = request.GET.get(
        "q",
        ""
    ).strip()

    users = User.objects.none()

    if query:

        users = User.objects.filter(

            Q(username__icontains=query) |

            Q(first_name__icontains=query) |

            Q(last_name__icontains=query)

        ).exclude(
            id=request.user.id
        )

    return render(request, "index.html", {

        "page": "search",

        "users": users,

        "query": query,
    })
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import User, Post, Follow, Like

import json

# Busca todas as postagens ordenadas da mais recente para a mais antiga
def index(request):
    posts_list = Post.objects.all().order_by('-date')
    paginator = Paginator(posts_list, 10)

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    liked_posts_ids = []  # Valor padrão para usuários não autenticados
    if request.user.is_authenticated:
        liked_posts_ids = request.user.likes.values_list('id', flat=True)

    return render(request, "network/index.html", {
        "posts": posts,
        "liked_posts_ids": liked_posts_ids
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# Cria uma nova postagem se a requisição for do tipo POST
def newPost(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()

        return HttpResponseRedirect(reverse(index))

# Exibe o perfil de um usuário, incluindo seus posts, contagem de seguidores/seguidos e funcionalidade de seguir/deixar de seguir
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts_list = Post.objects.filter(user=profile_user).order_by('-date')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    followers_count = Follow.objects.filter(user=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(user=profile_user, follower=request.user).exists()

    # Seguir/Deixar de seguir
    if request.method == "POST" and request.user.is_authenticated and request.user != profile_user:
        if is_following:
            Follow.objects.filter(user=profile_user, follower=request.user).delete()
        else:
            Follow.objects.create(user=profile_user, follower=request.user)
        return redirect('profile', username=username)

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "posts": posts,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following
    })

# Exibe os posts dos usuários que o usuário atual está seguindo
@login_required
def following(request):
    following_users = [follow.user for follow in request.user.seguindo.all()]
    posts_list = Post.objects.filter(user__in=following_users).order_by('-date')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "posts": posts
    })

# Permite que um usuário autenticado edite um post via requisição POST com dados JSON.
@csrf_exempt
@login_required
def edit_post(request, post_id):
    if request.method == "POST":
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post não encontrado."}, status=404)
        if post.user != request.user:
            return JsonResponse({"error": "Permissão negada."}, status=403)
        data = json.loads(request.body)
        content = data.get("content", "")
        post.content = content
        post.save()
        return JsonResponse({"message": "Post atualizado com sucesso.", "content": post.content})
    return JsonResponse({"error": "Método não permitido."}, status=405)

# Permite que um usuário autenticado curta ou descurta um post via requisição POST com dados JSON.

@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    like_count = post.likes.count()
    return JsonResponse({"liked": liked, "like_count": like_count})


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import RegistroForm, PostForm, ComentarioForm
from .models import Post, Follow, Like, Hashtag
from django.contrib.auth.decorators import login_required

@login_required
def comentar_post(request, post_id):

    post = Post.objects.get(id=post_id)

    if request.method == 'POST':

        form = ComentarioForm(request.POST)

        if form.is_valid():

            comentario = form.save(commit=False)

            comentario.usuario = request.user
            comentario.post = post

            comentario.save()

    return redirect('inicio')

@login_required
def toggle_like(request, post_id):

    post = Post.objects.get(id=post_id)

    like, creado = Like.objects.get_or_create(
        usuario=request.user,
        post=post
    )

    if not creado:
        like.delete()

    return redirect('inicio')

@login_required
def inicio(request):

    siguiendo = Follow.objects.filter(
        seguidor=request.user
    ).values_list('seguido', flat=True)

    posts = Post.objects.filter(
        usuario__in=list(siguiendo) + [request.user.id]
    ).order_by('-fecha_creacion')

    return render(request, 'inicio.html', {
        'posts': posts
    })

def registro(request):

    if request.method == 'POST':

        form = RegistroForm(request.POST)

        if form.is_valid():

            user = form.save()
            login(request, user)

            return redirect('inicio')

    else:
        form = RegistroForm()

    return render(request, 'registro.html', {
        'form': form
    })

@login_required
def crear_post(request):

    if request.method == 'POST':

        form = PostForm(request.POST)

        if form.is_valid():

            post = form.save(commit=False)

            post.usuario = request.user

            post.save()

            hashtags = post.contenido.split()

            for palabra in hashtags:

                if palabra.startswith('#'):

                    nombre_hashtag = palabra[1:]

                    hashtag, creado = Hashtag.objects.get_or_create(
                        nombre=nombre_hashtag
                    )

                    hashtag.posts.add(post)

            return redirect('inicio')

    else:

        form = PostForm()

    return render(request, 'crear_post.html', {
        'form': form
    })

from django.contrib.auth.models import User

def perfil(request, username):
    usuario = User.objects.get(username=username)

    posts = Post.objects.filter(usuario=usuario).order_by('-fecha_creacion')

    ya_sigue = False

    if request.user.is_authenticated:
        ya_sigue = Follow.objects.filter(
            seguidor=request.user,
            seguido=usuario
        ).exists()

    return render(request, 'perfil.html', {
        'usuario_perfil': usuario,
        'posts': posts,
        'ya_sigue': ya_sigue
    })

from .models import Follow

@login_required
def seguir_usuario(request, username):

    usuario_a_seguir = User.objects.get(
        username=username
    )

    if request.user != usuario_a_seguir:

        Follow.objects.get_or_create(
            seguidor=request.user,
            seguido=usuario_a_seguir
        )

    return redirect('perfil', username=username)

@login_required
def dejar_de_seguir(request, username):
    usuario_a_dejar = User.objects.get(username=username)

    Follow.objects.filter(
        seguidor=request.user,
        seguido=usuario_a_dejar
    ).delete()

    return redirect('perfil', username=username)

def buscar(request):

    query = request.GET.get('q')

    usuarios = []

    if query:
        usuarios = User.objects.filter(
            username__icontains=query
        )

    return render(request, 'buscar.html', {
        'usuarios': usuarios,
        'query': query
    })

def ver_hashtag(request, nombre):

    hashtag = Hashtag.objects.get(nombre=nombre)

    posts = hashtag.posts.all().order_by('-fecha_creacion')

    return render(request, 'hashtag.html', {
        'hashtag': hashtag,
        'posts': posts
    })
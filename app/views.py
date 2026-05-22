from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import RegistroForm, PostForm
from .models import Post

def inicio(request):

    posts = Post.objects.all().order_by('-fecha_creacion')

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
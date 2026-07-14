from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comentario, Perfil
class PerfilForm(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = ["bio", "foto"]
class RegistroForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['contenido']

class ComentarioForm(forms.ModelForm):

    class Meta:
        model = Comentario
        fields = ['contenido']
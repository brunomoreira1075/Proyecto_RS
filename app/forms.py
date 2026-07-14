from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil, Post, Comentario
class EditarPerfilForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Nombre",
        max_length=150,
        required=False
    )

    last_name = forms.CharField(
        label="Apellido",
        max_length=150,
        required=False
    )

    class Meta:
        model = Perfil
        fields = ["foto", "bio"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["first_name"].initial = self.user.first_name
        self.fields["last_name"].initial = self.user.last_name

    def save(self, commit=True):
        perfil = super().save(commit=False)

        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]

        if commit:
            self.user.save()
            perfil.save()

        return perfil
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
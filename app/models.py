from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField(max_length=280)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username}: {self.contenido[:30]}'
    
class Perfil(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(blank=True)

    def __str__(self):
        return self.usuario.username
    
class Follow(models.Model):

    seguidor = models.ForeignKey(
        User,
        related_name='siguiendo',
        on_delete=models.CASCADE
    )

    seguido = models.ForeignKey(
        User,
        related_name='seguidores',
        on_delete=models.CASCADE
    )

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.seguidor} sigue a {self.seguido}'    

class Like(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'post')

    def __str__(self):
        return f'{self.usuario} le dio like a {self.post.id}'
    
class Comentario(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    contenido = models.TextField(max_length=200)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario}: {self.contenido[:20]}'
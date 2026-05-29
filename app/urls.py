from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.inicio, name='inicio'),

    path('registro/', views.registro, name='registro'),

    path('crear/', views.crear_post, name='crear_post'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    
    path('perfil/<str:username>/', views.perfil, name='perfil'),

    path(
    'seguir/<str:username>/',
    views.seguir_usuario,
    name='seguir_usuario'
    ),

    path('dejar/<str:username>/', views.dejar_de_seguir, name='dejar_de_seguir'),

    path('buscar/', views.buscar, name='buscar'),

    path(
    'like/<int:post_id>/',
    views.toggle_like,
    name='toggle_like'
    ),
    
    path(
    'comentario/<int:post_id>/',
    views.comentar_post,
    name='comentar_post'
    ),
]

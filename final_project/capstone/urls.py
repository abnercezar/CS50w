from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path("usuarios/", include('usuarios.urls')),
    path("produtos/", include('produtos.urls')),
    path("servicos/", include('servicos.urls')),
    path("entrada/", include('entrada.urls')),
    path("saida/", include('saida.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import CustomUser

# View para cadastro de usuários


@login_required
def cadastro_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = CustomerUserCreationForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})


@login_required
def lista_usuarios(request):
    usuarios = CustomUser.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

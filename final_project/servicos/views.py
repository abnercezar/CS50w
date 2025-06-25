from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Servico
from .forms import ServicoForm
from django.http import JsonResponse


def cadastro_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_servicos')
    else:
        form = ServicoForm()
    return render(request, 'servicos/cadastro_servico.html', {'form': form})


def lista_servicos(request):
    servicos = Servico.objects.all()
    paginator = Paginator(servicos, 15)  # 15 serviços por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'servicos/lista_servicos.html', {'page_obj': page_obj})


def editar_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            return redirect('lista_servicos')
    else:
        form = ServicoForm(instance=servico)
    return render(request, 'servicos/cadastro_servico.html', {'form': form})


def excluir_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    if request.method == 'POST':
        servico.delete()
        return redirect('lista_servicos')
    return render(request, 'servicos/confirmar_exclusao.html', {'servico': servico})


def obter_valor_servico(request, servico_id):
    try:
        servico = Servico.objects.get(id=servico_id)
        return JsonResponse({'valor': servico.valor})
    except Servico.DoesNotExist:
        return JsonResponse({'error': 'Serviço não encontrado'}, status=404)

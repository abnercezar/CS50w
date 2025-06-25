from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Entrada
from .forms import EntradaForm


def cadastro_entrada(request):
    if request.method == 'POST':
        form = EntradaForm(request.POST)
        if form.is_valid():
            quantidade = form.cleaned_data['quantidade']
            produto = form.cleaned_data['produto']
            servico = form.cleaned_data['servico']
            for _ in range(quantidade):
                Entrada.objects.create(produto=produto, servico=servico, quantidade=1)
            return redirect('lista_entradas')
    else:
        form = EntradaForm()
    return render(request, 'entrada/cadastro_entrada.html', {'form': form})


def lista_entradas(request):
    entradas_list = Entrada.objects.all()
    paginator = Paginator(entradas_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total_itens = entradas_list.count()
    return render(request, 'entrada/lista_entradas.html', {'page_obj': page_obj, 'total_itens': total_itens})


def editar_entrada(request, entrada_id):
    entrada = get_object_or_404(Entrada, id=entrada_id)
    if request.method == 'POST':
        form = EntradaForm(request.POST, instance=entrada)
        if form.is_valid():
            form.save()
            return redirect('lista_entradas')
    else:
        form = EntradaForm(instance=entrada)
    return render(request, 'entrada/cadastro_entrada.html', {'form': form})


def excluir_entrada(request, entrada_id):
    entrada = get_object_or_404(Entrada, id=entrada_id)
    if request.method == 'POST':
        entrada.delete()
        return redirect('lista_entradas')
    return render(request, 'entrada/confirmar_exclusao.html', {'entrada': entrada})


def salvar_entradas(request):
    if request.method == 'POST':
        for entrada in Entrada.objects.all():
            serie = request.POST.get(f'serie_{entrada.id}')
            if serie is not None:
                entrada.serie = serie
                entrada.save()
    return redirect('lista_entradas')


def excluir_selecionados(request):
    if request.method == 'POST':
        selecionados = request.POST.getlist('selecionados')
        Entrada.objects.filter(id__in=selecionados).delete()
    return redirect('lista_entradas')

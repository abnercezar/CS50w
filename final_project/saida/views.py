from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Saida
from .forms import SaidaForm
from produtos.models import Produto


def cadastro_saida(request):
    if request.method == 'POST':
        form = SaidaForm(request.POST)
        if form.is_valid():
            quantidade = form.cleaned_data['quantidade']
            produto = form.cleaned_data['produto']
            servico = form.cleaned_data['servico']
            valor_unitario = form.cleaned_data['valor_unitario']
            for _ in range(quantidade):
                Saida.objects.create(produto=produto, servico=servico, quantidade=1, valor_unitario=valor_unitario)
            return redirect('lista_saidas')
    else:
        form = SaidaForm()
    produtos = Produto.objects.all()
    return render(request, 'saida/cadastro_saida.html', {'form': form, 'produtos': produtos})


def lista_saidas(request):
    saidas_list = Saida.objects.all()
    paginator = Paginator(saidas_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total_itens = saidas_list.count()
    return render(request, 'saida/lista_saidas.html', {'page_obj': page_obj, 'total_itens': total_itens})


def editar_saida(request, saida_id):
    saida = get_object_or_404(Saida, id=saida_id)
    if request.method == 'POST':
        form = SaidaForm(request.POST, instance=saida)
        if form.is_valid():
            form.save()
            return redirect('lista_saidas')
    else:
        form = SaidaForm(instance=saida)
    return render(request, 'saida/cadastro_saida.html', {'form': form})


def excluir_saida(request, saida_id):
    saida = get_object_or_404(Saida, id=saida_id)
    if request.method == 'POST':
        saida.delete()
        return redirect('lista_saidas')
    return render(request, 'saida/confirmar_exclusao.html', {'saida': saida})


def excluir_selecionados(request):
    if request.method == 'POST':
        selecionados = request.POST.getlist('selecionados')
        Saida.objects.filter(id__in=selecionados).delete()
    return redirect('lista_saidas')


def salvar_saidas(request):
    if request.method == 'POST':
        for saida in Saida.objects.all():
            serie = request.POST.get(f'serie_{saida.id}')
            if serie is not None:
                saida.serie = serie
                saida.save()
    return redirect('lista_saidas')

from django.shortcuts import render
from entrada.models import Entrada
from saida.models import Saida
from django.db.models.functions import TruncMonth
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    entradas = (
        Entrada.objects
        .annotate(mes=TruncMonth('data_entrada'))
        .values('mes', 'produto', 'produto__produto', 'produto__versao')
        .annotate(total=Sum('quantidade'))
        .order_by('mes')
    )

    saidas = (
        Saida.objects
        .annotate(mes=TruncMonth('data_saida'))
        .values('mes', 'produto', 'produto__produto', 'produto__versao')
        .annotate(total=Sum('quantidade'))
        .order_by('mes')
    )

    meses = sorted(set([e['mes'] for e in entradas] + [s['mes'] for s in saidas if s['mes']]))
    labels = [m.strftime('%b/%Y') for m in meses]

    grupos = set()
    for e in entradas:
        grupos.add((e['produto__produto'], e['produto__versao']))
    for s in saidas:
        grupos.add((s['produto__produto'], s['produto__versao']))

    entradas_datasets = []
    saidas_datasets = []
    for produto, versao in grupos:
        entrada_data = []
        saida_data = []

        for mes in meses:
            entrada = next(
                (e['total'] for e in entradas if e['mes'] == mes and e['produto__produto'] == produto and e['produto__versao'] == versao),
                0
            )
            saida = next(
                (s['total'] for s in saidas if s['mes'] == mes and s['produto__produto'] == produto and s['produto__versao'] == versao),
                0
            )
            entrada_data.append(entrada)
            saida_data.append(saida)

        entradas_datasets.append({
            "label": f"{produto} v{versao}",
            "data": entrada_data,
            "backgroundColor": "rgba(54, 162, 235, 0.7)",
        })

        saidas_datasets.append({
            "label": f"{produto} v{versao}",
            "data": saida_data,
            "backgroundColor": "rgba(255, 99, 132, 0.7)",
        })

    total_entregue = Saida.objects.aggregate(total=Sum('quantidade'))['total'] or 0
    total_a_receber = Saida.objects.aggregate(
        total=Sum(ExpressionWrapper(F('quantidade') * F('valor_unitario'), output_field=FloatField()))
    )['total'] or 0

    return render(request, "dashboard/dashboard.html", {
        "labels": labels,
        "entradas_datasets": entradas_datasets,
        "saidas_datasets": saidas_datasets,
        "total_entregue": total_entregue,
        "total_a_receber": total_a_receber,
    })

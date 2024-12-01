import re
from django.shortcuts import render, redirect
import random
from django import forms
from markdown2 import Markdown
from . import util

# Função para converter conteúdo Markdown em HTML
def convert_md_to_html_simple(markdown_text):
    # Converter títulos
    markdown_text = re.sub(r'^(#{1,6})\s*(.+)$', lambda m: f'<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>', markdown_text, flags=re.MULTILINE)

    # Converter texto em negrito
    markdown_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', markdown_text)

    # Converter listas não ordenadas
    markdown_text = re.sub(r'^\*\s+(.+)$', r'<ul><li>\1</li></ul>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'(<ul>.*?</ul>)\s*<ul>', r'\1', markdown_text, flags=re.DOTALL)

    # Converter links
    markdown_text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', markdown_text)

    # Converter parágrafos
    markdown_text = re.sub(r'^(?!<h|<ul|<li|<a|<strong)(.+)$', r'<p>\1</p>', markdown_text, flags=re.MULTILINE)

    return markdown_text

# Atualizar a função convert_md_to_html para usar a conversão simples
def convert_md_to_html(title):
    content = util.get_entry(title)
    if content is None:
        return None
    return convert_md_to_html_simple(content)

# View para a página inicial
def index(request):

    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

# View para exibir uma entrada específica da enciclopédia
def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "A entrada solicitada não foi encontrada."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

# View para buscar entradas na enciclopédia
def search(request):
    query = request.GET.get('q', '')
    if query:
        entries = util.list_entries()
        results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "results": results,
            "query": query
        })
    else:
        return render(request, "encyclopedia/search.html", {
            "results": [],
            "query": query
        })

# View para criar uma nova entrada na enciclopédia
class NewPageForm(forms.Form):
        title = forms.CharField(label="Title")
        content = forms.CharField(widget=forms.Textarea, label="Content")

def create_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                return render(request, "encyclopedia/create_page.html", {
                    "form": form,
                    "error": "Já existe uma página com este título."
                    })
            else:
                util.save_entry(title, content)
                return redirect('entry', title=title)
    else:
        form = NewPageForm()
    return render(request, "encyclopedia/create_page.html", {
        "form": form
    })

# View para editar uma nova entrada na enciclopédia
class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")

def edit_page(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('entry', title=title)
    else:
        content = util.get_entry(title)
        if content is None:
            return render(request, "encyclopedia/error.html", {
                "message": "The requested page was not found."
            })
        form = EditPageForm(initial={'content': content})
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "form": form
    })

# View para redirecionar para uma entrada aleatória na enciclopédia
def random_page(request):
    entries = util.list_entries()
    if entries:
        random_entry = random.choice(entries)
        return redirect('entry', title=random_entry)
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Nenhuma entrada encontrada."
            })


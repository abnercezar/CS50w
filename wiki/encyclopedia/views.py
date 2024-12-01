from django.shortcuts import render, redirect
from django import forms
from markdown2 import Markdown
from . import util

# Função para converter conteúdo Markdown em HTML
def convert_md_to_html(title):
    content = util.get_entry(title)
    if content is None:
        return None
    return Markdown().convert(content)

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

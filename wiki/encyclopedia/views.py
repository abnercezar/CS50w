from django.shortcuts import render
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

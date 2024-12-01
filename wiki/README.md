# 📝 Wiki Encyclopedia - CS50W Project

Este projeto foi desenvolvido como parte do curso **CS50’s Web Programming with Python and JavaScript** da Universidade de Harvard. Trata-se de uma enciclopédia online que permite criar, editar, pesquisar e visualizar entradas em formato Markdown, além de fornecer funcionalidades interativas.

---

## 📋 Funcionalidades Principais

### 🌐 Página de Entrada
- **Descrição:** Permite visualizar o conteúdo de uma entrada específica.
- **Detalhes:**
  - Acesse `/wiki/<TITLE>` para visualizar o conteúdo da entrada `TITLE`.
  - Caso a entrada não exista, uma página de erro será exibida.
  - O conteúdo em Markdown é convertido para HTML.

---

### 📚 Página de Índice
- **Descrição:** Exibe uma lista de todas as entradas disponíveis.
- **Detalhes:**
  - A lista de entradas permite que o usuário clique em um título para navegar diretamente para a página correspondente.

---

### 🔍 Pesquisar
- **Descrição:** Busca por entradas existentes.
- **Detalhes:**
  - Caso o termo buscado corresponda exatamente ao título de uma entrada, o usuário será redirecionado para a página correspondente.
  - Caso contrário, uma lista com entradas relacionadas (substring do termo) será exibida.
  - Os resultados são clicáveis e levam diretamente à página da entrada.

---

### ✏️ Criar Nova Página
- **Descrição:** Permite adicionar uma nova entrada de enciclopédia.
- **Detalhes:**
  - O usuário fornece um título e conteúdo em Markdown.
  - Se uma entrada com o mesmo título já existir, uma mensagem de erro será exibida.
  - Entradas válidas são salvas e exibidas imediatamente.

---

### 🛠️ Editar Página
- **Descrição:** Permite editar uma entrada existente.
- **Detalhes:**
  - O conteúdo atual da entrada é exibido em um editor de texto.
  - Após salvar, as alterações são aplicadas à entrada original.

---

### 🎲 Página Aleatória
- **Descrição:** Redireciona o usuário para uma entrada aleatória da enciclopédia.

---

### 🔄 Conversão de Markdown para HTML
- **Descrição:** O conteúdo das entradas é escrito em Markdown e automaticamente convertido para HTML antes de ser exibido.
- **Desafio:** A conversão pode ser feita com a biblioteca `markdown2` ou manualmente usando expressões regulares.

---

## 🛠️ Estrutura do Projeto

```plaintext
wiki/
├── entries/                # Arquivos de entradas em formato Markdown (.md)
├── encyclopedia/
│   ├── templates/          # Templates HTML
│   │   ├── layout.html     # Layout base
│   │   ├── index.html      # Página de índice
│   │   ├── entry.html      # Página de entrada
│   │   ├── search.html     # Resultados de pesquisa
│   │   ├── new.html        # Página de criação de entrada
│   │   ├── edit.html       # Página de edição
│   ├── views.py            # Lógica das rotas
│   ├── urls.py             # Configuração das URLs
│   ├── util.py             # Funções auxiliares para gerenciar entradas
├── requirements.txt        # Dependências do projeto
├── manage.py               # Comando principal do Django
└── README.md               # Este arquivo!
```
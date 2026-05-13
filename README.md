# 📡 Tech & Insights — Newsletter Automatizada

Portal de curadoria semanal de notícias sobre **Inteligência Artificial**, **Controladoria**, **Finanças**, **Business Intelligence** e **Automação**.

Hospedado via **GitHub Pages** com geração automática de edições.

---

## 📁 Estrutura do Projeto

```
ControladorIA-News/
├── index.html              ← Página principal (lista edições)
├── template.html            ← Template para novas edições
├── .nojekyll                ← Desabilita Jekyll no GitHub Pages
├── css/
│   └── style.css            ← Design system completo
├── data/
│   ├── current_news.json    ← Conteúdo da próxima edição
│   └── editions.json        ← Registro de todas as edições
├── news/
│   └── 2026-05-07.html      ← Edições geradas (uma por semana)
├── scripts/
│   └── generate_news.py     ← Script de geração automática
├── assets/                  ← Imagens e recursos (futuro)
└── .github/
    └── workflows/
        └── main_workflow.yml ← Automação via GitHub Actions
```

---

## 🚀 Como Funciona

### Fluxo de Geração

1. Edite o arquivo `data/current_news.json` com o conteúdo da semana
2. Rode o script `python scripts/generate_news.py`
3. O script:
   - Lê o JSON com as notícias
   - Aplica no `template.html`
   - Gera um novo arquivo em `news/YYYY-MM-DD.html`
   - Atualiza `data/editions.json` (registro central)
4. O `index.html` carrega `editions.json` via JavaScript e exibe os cards

### Exemplo do JSON de Notícias

```json
{
    "id": "01",
    "date": "07 de Maio, 2026",
    "slug": "2026-05-07",
    "title": "A Nova Era da Controladoria",
    "summary": "Resumo breve da edição...",
    "hero_title": "Título do destaque principal",
    "hero_content": "Texto do destaque...",
    "news": [
        {
            "cat": "IA",
            "title": "Título da notícia",
            "desc": "Descrição da notícia...",
            "source_name": "TechCrunch",
            "source_url": "https://techcrunch.com"
        }
    ],
    "trends": [
        { "icon": "🤖", "title": "AI Agents", "desc": "Descrição da tendência..." }
    ],
    "tools": [
        { "icon": "⚡", "name": "Cursor AI", "desc": "Descrição...", "url": "https://cursor.sh" }
    ],
    "videos": [
        {
            "youtube_id": "ID_DO_VIDEO",
            "title": "Título do vídeo",
            "channel": "Nome do Canal",
            "desc": "Descrição breve"
        }
    ],
    "insights": [
        "Insight sobre finanças ou controladoria..."
    ]
}
```

---

## 💻 Rodar Localmente

### Gerar uma edição

```bash
python scripts/generate_news.py
```

### Visualizar o site

Abra o `index.html` em um browser. Para server local:

```bash
# Python
python -m http.server 8000

# Acesse http://localhost:8000
```

> **Nota:** O `index.html` usa `fetch()` para carregar `editions.json`, então precisa de um servidor HTTP (file:// bloqueia fetch por CORS).

---

## ⚙️ Automação com GitHub Actions

O workflow `main_workflow.yml` roda automaticamente toda **segunda-feira às 09:00 UTC**.

### O que o workflow faz:

1. ✅ Checkout do repositório
2. ✅ Instala Python 3.12
3. ✅ Roda `generate_news.py`
4. ✅ Faz commit e push das mudanças
5. ✅ Deploy automático no GitHub Pages

### Rodar manualmente:

1. Vá no GitHub → **Actions** → **Publicação Automática Newsletter**
2. Clique em **"Run workflow"**

---

## 🌐 Como Publicar no GitHub Pages

### Passo a passo:

1. Crie um repositório no GitHub (ex: `ControladorIA-News`)
2. Faça push do código:
   ```bash
   git init
   git add .
   git commit -m "🚀 Primeira versão do portal"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/ControladorIA-News.git
   git push -u origin main
   ```
3. No GitHub, vá em:
   - **Settings** → **Pages**
   - **Source**: selecione **"GitHub Actions"**
4. O workflow fará o deploy automaticamente

### URL do site:
```
https://SEU_USUARIO.github.io/ControladorIA-News/
```

---

## 📋 Categorias Suportadas

| Categoria      | Badge CSS                    | Cor      |
|----------------|------------------------------|----------|
| IA             | `category-tag--ia`           | 🟣 Roxo  |
| Tecnologia     | `category-tag--tecnologia`   | 🔵 Azul  |
| Finanças       | `category-tag--financas`     | 🟢 Verde |
| Controladoria  | `category-tag--controladoria`| 🟡 Âmbar |
| Mercado        | `category-tag--mercado`      | 🔴 Verm. |
| Automação      | `category-tag--automacao`    | 🩵 Cyan  |
| Dados          | `category-tag--dados`        | 🩷 Rosa  |
| Ferramentas    | `category-tag--ferramentas`  | 🟠 Laranja|

---

## 🔮 Roadmap Futuro

- [ ] Integrar API de notícias (NewsAPI, RSS feeds)
- [ ] Curadoria automática via OpenAI API
- [ ] Dark mode
- [ ] Sistema de tags e filtros
- [ ] RSS feed do portal
- [ ] Newsletter por email (Mailchimp / Resend)

---

## 📄 Licença

© 2026 Tech & Insights. Todos os direitos reservados.

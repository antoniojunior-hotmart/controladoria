#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║  Controlador.IA News — Gerador Automático de Newsletter               ║
║  ────────────────────────────────────────────────────    ║
║  Lê data/current_news.json → Gera HTML em news/        ║
║  Atualiza data/editions.json (registro central)         ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
from datetime import datetime

# ── Caminhos ────────────────────────────────────────────────
BASE_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE      = os.path.join(BASE_DIR, 'data', 'current_news.json')
EDITIONS_FILE  = os.path.join(BASE_DIR, 'data', 'editions.json')
TEMPLATE_FILE  = os.path.join(BASE_DIR, 'template.html')
NEWS_DIR       = os.path.join(BASE_DIR, 'news')


def load_json(path):
    """Carrega um arquivo JSON com encoding UTF-8."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    """Salva dados em JSON formatado."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_category_class(category):
    """Retorna a classe CSS correspondente à categoria."""
    mapping = {
        'ia':             'category-tag--ia',
        'inteligência artificial': 'category-tag--ia',
        'tecnologia':     'category-tag--tecnologia',
        'finanças':       'category-tag--financas',
        'financas':       'category-tag--financas',
        'controladoria':  'category-tag--controladoria',
        'mercado':        'category-tag--mercado',
        'automação':      'category-tag--automacao',
        'automacao':      'category-tag--automacao',
        'dados':          'category-tag--dados',
        'data':           'category-tag--dados',
        'ferramentas':    'category-tag--ferramentas',
    }
    return mapping.get(category.lower().strip(), 'category-tag--default')


def build_news_html(news_items):
    """Gera o HTML dos cards de notícia."""
    html = ''
    for item in news_items:
        cat = item.get('cat', 'Geral')
        cat_class = get_category_class(cat)
        source_name = item.get('source_name', '')
        source_url = item.get('source_url', '')

        source_link = ''
        if source_url and source_name:
            source_link = (
                f'<a href="{source_url}" target="_blank" '
                f'rel="noopener noreferrer" class="source-link">'
                f'Fonte: {source_name}</a>'
            )

        title = item.get('title') or item.get('headline') or item.get('titulo') or ''
        desc  = item.get('desc') or item.get('description') or item.get('descricao') or item.get('descri\u00e7\u00e3o') or ''
        html += f'''
            <article class="news-item">
                <span class="category-tag {cat_class}">{cat}</span>
                <h3>{title}</h3>
                <p>{desc}</p>
                {source_link}
            </article>'''
    return html


def build_trends_html(trends):
    """Gera o HTML da seção Tendências da Semana."""
    if not trends:
        return ''
    html = ''
    for trend in trends:
        t_title = trend.get('title') or trend.get('name') or trend.get('titulo') or ''
        t_desc  = trend.get('desc') or trend.get('description') or trend.get('descricao') or ''
        html += f'''
                <div class="trend-item">
                    <div class="trend-icon">{trend.get("icon", "📌")}</div>
                    <h4>{t_title}</h4>
                    <p>{t_desc}</p>
                </div>'''
    return html


def build_tools_html(tools):
    """Gera o HTML da seção Ferramentas em Alta."""
    if not tools:
        return ''
    html = ''
    for tool in tools:
        url = tool.get('url', '#')
        # Tolerante a variações de chave do agente: name / title / tool / ferramenta
        name = (
            tool.get('name') or
            tool.get('title') or
            tool.get('tool') or
            tool.get('ferramenta') or
            'Ferramenta'
        )
        # Tolerante a variações de descrição: desc / description / descricao / descricao
        desc = (
            tool.get('desc') or
            tool.get('description') or
            tool.get('descricao') or
            tool.get('descrição') or
            ''
        )
        html += f'''
                <a href="{url}" target="_blank" rel="noopener noreferrer" class="tool-card">
                    <div class="tool-icon">{tool.get("icon", "🔧")}</div>
                    <h4>{name}</h4>
                    <p>{desc}</p>
                    <span class="tool-link">Acessar ↗</span>
                </a>'''
    return html


def build_insights_html(insights):
    """Gera o HTML da seção Insights Financeiros."""
    if not insights:
        return ''
    html = ''
    for insight in insights:
        html += f'<div class="insight-item">{insight}</div>\n'
    return html


def build_videos_html(videos):
    """Gera o HTML da seção de Vídeos Recomendados do YouTube."""
    if not videos:
        return ''
    html = ''
    for video in videos:
        yt_id = video.get('youtube_id', '')
        thumbnail = f'https://img.youtube.com/vi/{yt_id}/mqdefault.jpg' if yt_id else ''
        url = f'https://www.youtube.com/watch?v={yt_id}' if yt_id else video.get('url', '#')
        v_title = video.get('title') or video.get('titulo') or ''
        v_desc  = video.get('desc') or video.get('description') or video.get('descricao') or ''
        html += f'''
                <a href="{url}" target="_blank" rel="noopener noreferrer" class="video-card">
                    {f'<img src="{thumbnail}" alt="{v_title}" class="video-thumb">' if thumbnail else ''}
                    <div class="video-info">
                        <h4>{v_title}</h4>
                        <p class="video-channel">{video.get("channel", "")}</p>
                        <p>{v_desc}</p>
                    </div>
                </a>'''
    return html


def get_next_id(editions_data):
    """Calcula o próximo ID baseado nas edições existentes."""
    editions = editions_data.get('editions', [])
    if not editions:
        return '01'
    max_id = max(int(e.get('id', '0')) for e in editions)
    return str(max_id + 1).zfill(2)


def is_duplicate(editions_data, slug):
    """Verifica se o slug já existe no registro de edições."""
    for edition in editions_data.get('editions', []):
        if edition.get('slug') == slug:
            return True
    return False


def generate_newsletter():
    """Fluxo principal de geração da newsletter."""

    # ── 1. Carregar dados ───────────────────────────────────
    if not os.path.exists(DATA_FILE):
        print('❌ Erro: Arquivo data/current_news.json não encontrado.')
        sys.exit(1)

    data = load_json(DATA_FILE)

    # ── 2. Carregar ou criar editions.json ──────────────────
    if os.path.exists(EDITIONS_FILE):
        editions_data = load_json(EDITIONS_FILE)
    else:
        editions_data = {'editions': []}

    # ── 3. Definir slug e verificar duplicata ───────────────
    slug = data.get('slug', datetime.now().strftime('%Y-%m-%d'))

    if is_duplicate(editions_data, slug):
        print(f'⚠️  Edição com slug "{slug}" já existe. Nenhuma ação tomada.')
        return

    # ── 4. Auto-incrementar ID se necessário ────────────────
    edition_id = data.get('id')
    if not edition_id or is_duplicate_id(editions_data, edition_id):
        edition_id = get_next_id(editions_data)
        data['id'] = edition_id

    # ── 5. Ler template e substituir variáveis ──────────────
    if not os.path.exists(TEMPLATE_FILE):
        print('❌ Erro: template.html não encontrado.')
        sys.exit(1)

    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    # Construir blocos de HTML
    news_html     = build_news_html(data.get('news', []))
    trends_html   = build_trends_html(data.get('trends', []))
    tools_html    = build_tools_html(data.get('tools', []))
    insights_html = build_insights_html(data.get('insights', []))
    videos_html   = build_videos_html(data.get('videos', []))

    # Substituições
    replacements = {
        '{{ID}}':                 data['id'],
        '{{DATE}}':               data.get('date', ''),
        '{{TITLE}}':              data.get('title', ''),
        '{{SUMMARY}}':            data.get('summary', data.get('title', '')),
        '{{HERO_TITLE}}':         data.get('hero_title', ''),
        '{{HERO_CONTENT}}':       data.get('hero_content', ''),
        '{{NEWS_ITEMS}}':         news_html,
        '{{TRENDS_ITEMS}}':       trends_html,
        '{{TOOLS_ITEMS}}':        tools_html,
        '{{VIDEOS_ITEMS}}':       videos_html,
        '{{FINANCIAL_INSIGHTS}}': insights_html,
    }

    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)

    # ── 6. Salvar HTML na pasta news/ ───────────────────────
    os.makedirs(NEWS_DIR, exist_ok=True)
    output_path = os.path.join(NEWS_DIR, f'{slug}.html')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'✅ Edição #{edition_id} salva: {output_path}')

    # ── 7. Atualizar editions.json ──────────────────────────
    edition_entry = {
        'id':      edition_id,
        'slug':    slug,
        'date':    data.get('date', ''),
        'title':   data.get('title', ''),
        'summary': data.get('summary', ''),
    }

    editions_data['editions'].append(edition_entry)
    save_json(EDITIONS_FILE, editions_data)
    print(f'✅ editions.json atualizado ({len(editions_data["editions"])} edições)')


def is_duplicate_id(editions_data, edition_id):
    """Verifica se o ID já existe."""
    for edition in editions_data.get('editions', []):
        if edition.get('id') == edition_id:
            return True
    return False


if __name__ == '__main__':
    generate_newsletter()
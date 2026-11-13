# -*- coding: utf-8 -*-
"""
Собирает весь сайт в один самодостаточный HTML-файл для публикации
как Артефакт: страницы, стили, скрипты, шрифты и фотографии внутри файла.

Отличия от настоящего сайта — только технические:
  · переходы между страницами через хеш-роутер, а не отдельные файлы
  · фотографии пережаты сильнее (артефакт должен быть компактным)
  · шрифты урезаны до символов, которые реально встречаются на сайте

Запуск из корня проекта:
    python3 site/_build/artifact.py
"""

import base64
import io
import json
import os
import re
import sys

from PIL import Image, ImageOps
from fontTools import subset

Image.MAX_IMAGE_PIXELS = None

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = os.path.join(ROOT, 'site')
OUT = os.path.join(ROOT, 'site', '_build', 'artifact.html')

PAGES = ['index', 'about', 'issues', 'archive', 'hero', 'become-hero',
         'become-participant', 'zines', 'partners', 'news', 'faq', 'contacts']
LONGREAD = 'notes/altay'

PHOTO_WIDTH = 1000          # артефакт грузится целиком, поэтому кадры мельче
PHOTO_QUALITY = 70


def read(*parts):
    return open(os.path.join(SITE, *parts), encoding='utf-8').read()


# ── 1. Тела страниц ────────────────────────────────────────────
def page_bodies():
    bodies = {}
    for name in PAGES + [LONGREAD]:
        html = read(f'{name}.html')
        body = re.search(r'<main id="main">(.*?)</main>', html, re.S).group(1)
        # лонгрид лежит на уровень глубже — выравниваем пути
        body = body.replace('href="../', 'href="').replace('src="../', 'src="')
        bodies[name + '.html'] = body
    return bodies


# ── 2. Фотографии ──────────────────────────────────────────────
def collect_slugs(bodies):
    slugs = set()
    blob = '\n'.join(bodies.values()) + read('js', 'data.js')
    for m in re.finditer(r'photo/([a-z0-9-]+)-(?:600|1200|2000)\.(?:webp|jpg)', blob):
        slugs.add(m.group(1))
    for m in re.finditer(r"(?:photo|cover):\s*'([^']+)'", read('js', 'data.js')):
        slugs.add(m.group(1))
    for m in re.finditer(r'gallery:\s*\[([^\]]*)\]', read('js', 'data.js')):
        slugs.update(re.findall(r"'([^']+)'", m.group(1)))
    return sorted(s for s in slugs if s and s != 'photo')


def encode_photos(slugs):
    out, total = {}, 0
    src_dir = os.path.join(SITE, 'assets', 'img', 'photo')
    for s in slugs:
        path = os.path.join(src_dir, f'{s}-2000.webp')
        if not os.path.exists(path):
            path = os.path.join(src_dir, f'{s}-1200.webp')
        if not os.path.exists(path):
            print(f'  нет файла для {s}')
            continue
        im = Image.open(path).convert('RGB')
        im.thumbnail((min(PHOTO_WIDTH, im.width), 10 ** 6), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, 'WEBP', quality=PHOTO_QUALITY, method=6)
        total += buf.tell()
        out[s] = 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()
    print(f'  фотографий: {len(out)}, {total / 1048576:.1f} МБ до base64')
    return out


# ── 3. Шрифты ──────────────────────────────────────────────────
FACES = [('rubik', 500), ('rubik', 700), ('rubik', 800),
         ('inter', 400), ('inter', 500), ('inter', 600)]


def used_chars(bodies):
    text = '\n'.join(bodies.values()) + read('js', 'data.js') + read('js', 'archive.js') \
        + read('js', 'hero.js') + read('js', 'issues.js') + read('js', 'forms.js') + read('js', 'map.js')
    text = re.sub(r'<[^>]+>', ' ', text)          # выкидываем теги, оставляем текст
    chars = set(text)
    chars |= set('0123456789 ' + '«»—–…·→×№₽%()[]{}:;,.!?"\'/\\@#&*+-=_')
    chars |= set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    chars |= set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
    chars |= set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return ''.join(sorted(c for c in chars if c.isprintable() and ord(c) > 31))


def encode_fonts(chars):
    css, total = [], 0
    fonts_dir = os.path.join(SITE, 'assets', 'fonts')
    for fam, weight in FACES:
        # склеиваем кириллицу и латиницу в один урезанный файл
        merged = None
        for sub in ('cyrillic', 'latin'):
            p = os.path.join(fonts_dir, f'{fam}-{weight}-{sub}.woff2')
            if not os.path.exists(p):
                continue
            opts = subset.Options(flavor='woff2', layout_features=['*'],
                                  notdef_outline=True, desubroutinize=True)
            font = subset.load_font(p, opts)
            subsetter = subset.Subsetter(options=opts)
            subsetter.populate(text=chars)
            subsetter.subset(font)
            buf = io.BytesIO()
            subset.save_font(font, buf, opts)
            font.close()
            data = buf.getvalue()
            # кириллический файл — основной, латинский добавляем отдельным @font-face
            name = f'{fam}-{weight}-{sub}'
            total += len(data)
            b64 = base64.b64encode(data).decode()
            css.append(f"@font-face{{font-family:'{fam.capitalize()}';font-style:normal;"
                       f"font-weight:{weight};font-display:swap;"
                       f"src:url(data:font/woff2;base64,{b64}) format('woff2');"
                       + ("unicode-range:U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116;"
                          if sub == 'cyrillic' else
                          "unicode-range:U+0000-00FF,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212;")
                       + "}")
            merged = name
    print(f'  шрифты: {len(css)} начертаний, {total / 1024:.0f} КБ до base64')
    return '\n'.join(css)


# ── 4. Скрипты ─────────────────────────────────────────────────
def bundle_js():
    order = ['russia', 'data', 'ui', 'map', 'archive', 'hero', 'issues', 'forms']
    parts = []
    for name in order:
        src = read('js', f'{name}.js')
        src = re.sub(r'^\s*import .*?;\s*$', '', src, flags=re.M)      # модулей больше нет
        src = re.sub(r'^export (const|function|async function)', r'\1', src, flags=re.M)
        parts.append(f'/* ── {name}.js ── */\n{src}')
    js = '\n\n'.join(parts)

    # ROOT берём из data-атрибута — в артефакте он всегда пустой
    js = js.replace("const ROOT = document.documentElement.dataset.root || '';",
                    "const ROOT = '';")

    # виртуальный адрес вместо настоящего location.search
    js = js.replace('new URLSearchParams(location.search)', 'new URLSearchParams(VQ)')
    js = js.replace("history.replaceState(null, '', url);", 'VQ = q.toString();')
    js = js.replace("const url = q.toString() ? `?${q}` : location.pathname;", '')

    # переходы внутри артефакта — через роутер, а не перезагрузкой
    js = js.replace('location.href = `${ROOT}archive.html?region=${slug}`;',
                    "go('archive.html?region=' + slug);")

    # фотографии лежат в объекте PHOTOS, а не файлами
    js = re.sub(
        r'function photo\(slug, alt, opts = \{\}\) \{.*?\n\}',
        '''function photo(slug, alt, opts = {}) {
  const { eager = false, cls = '' } = opts;
  const src = PHOTOS[slug];
  if (!src) return `<div class="ph__empty-inner">${esc(alt || 'Фото появится после экспедиции')}</div>`;
  return `<img src="${src}" alt="${esc(alt)}" class="${cls}"
     loading="${eager ? 'eager' : 'lazy'}" decoding="async">`;
}''', js, flags=re.S)
    return js


ROUTER = '''
/* ── Роутер артефакта ──────────────────────────────────────────
   В настоящем сайте это 13 отдельных HTML-файлов. Здесь всё лежит
   в одном файле, поэтому переходы подменяют содержимое <main>.   */
let VQ = '';

function currentRoute() {
  const h = decodeURIComponent(location.hash.replace(/^#\\/?/, '')) || 'index.html';
  const [path, query = ''] = h.split('?');
  return { path: PAGES[path] ? path : 'index.html', query };
}

function render() {
  const { path, query } = currentRoute();
  VQ = query;
  const main = document.getElementById('main');
  main.innerHTML = PAGES[path];

  document.querySelectorAll('.nav__link').forEach(a => {
    const target = a.dataset.to;
    a.toggleAttribute('aria-current', target === path
      || (path === 'hero.html' && target === 'archive.html')
      || (path === 'notes/altay.html' && target === 'archive.html'));
    if (a.hasAttribute('aria-current')) a.setAttribute('aria-current', 'page');
  });

  initReveal();
  initMap();
  initIssues();
  initArchive();
  initHero();
  initForms();

  document.title = (TITLES[path] || 'ДРУГ') + ' — ДРУГ';
}

function go(to) {
  location.hash = '/' + to;
  if (currentRoute().path + (currentRoute().query ? '?' + currentRoute().query : '') !== to) render();
}

document.addEventListener('click', (e) => {
  const a = e.target.closest('a[href]');
  if (!a) return;
  const href = a.getAttribute('href');
  if (!href || /^(https?:|mailto:|tel:|#)/.test(href)) return;
  e.preventDefault();
  go(href.replace(/^\\.\\//, ''));
  scrollTo({ top: 0, behavior: 'instant' });
});

addEventListener('hashchange', () => { render(); scrollTo({ top: 0, behavior: 'instant' }); });

initHeader();
initYear();
render();
'''


def main():
    print('Собираю артефакт:')
    bodies = page_bodies()
    print(f'  страниц: {len(bodies)}')

    photos = encode_photos(collect_slugs(bodies))
    fonts_css = encode_fonts(used_chars(bodies))

    # в разметке заменяем <picture> на одну картинку с data-URI
    def swap_picture(m):
        block = m.group(0)
        slug = re.search(r'photo/([a-z0-9-]+)-\d+\.', block)
        alt = re.search(r'alt="([^"]*)"', block)
        if not slug or slug.group(1) not in photos:
            return block
        eager = 'fetchpriority' in block or 'loading="eager"' in block
        return (f'<img src="{photos[slug.group(1)]}" alt="{alt.group(1) if alt else ""}" '
                f'loading="{"eager" if eager else "lazy"}" decoding="async">')

    for k in bodies:
        bodies[k] = re.sub(r'<picture>.*?</picture>', swap_picture, bodies[k], flags=re.S)

    css = '\n'.join(read('css', f) for f in
                    ('tokens.css', 'base.css', 'components.css', 'pages.css'))
    # логотип тоже внутрь файла
    logo = base64.b64encode(open(os.path.join(SITE, 'assets', 'img', 'logo.png'), 'rb').read()).decode()
    logo_uri = f'data:image/png;base64,{logo}'

    titles = {'index.html': 'Живые истории российских территорий', 'about.html': 'О проекте',
              'issues.html': 'Цифровые выпуски', 'archive.html': 'Медиаархив',
              'hero.html': 'Досье героя', 'become-hero.html': 'Рассказать свою историю',
              'become-participant.html': 'Поехать в экспедицию', 'zines.html': 'Печатные издания',
              'partners.html': 'Сотрудничество', 'news.html': 'Новости экспедиции',
              'faq.html': 'Вопрос-ответ', 'contacts.html': 'Контакты',
              'notes/altay.html': 'Путевые заметки. Алтай'}

    nav = [('about.html', 'О проекте'), ('issues.html', 'Выпуски'), ('archive.html', 'Архив'),
           ('zines.html', 'Зины'), ('partners.html', 'Сотрудничество'),
           ('faq.html', 'Вопросы'), ('contacts.html', 'Контакты')]
    nav_html = '\n        '.join(
        f'<a href="{h}" class="nav__link" data-to="{h}">{t}</a>' for h, t in nav)

    footer = re.search(r'<footer class="footer">.*?</footer>',
                       read('index.html'), re.S).group(0)
    footer = footer.replace('src="assets/img/logo.png"', f'src="{logo_uri}"')

    html = f'''<title>ДРУГ — живые истории российских территорий</title>
<style>
{fonts_css}

{css}

/* Артефакт — одна страница, поэтому фотографии вставлены напрямую,
   без <picture>; правила заполнения контейнера остаются теми же. */
.ph > img {{ width: 100%; height: 100%; object-fit: cover; }}
</style>

<a class="skip-link" href="#main">Перейти к содержимому</a>

<header class="header">
  <div class="container header__inner">
    <a href="index.html" class="logo" aria-label="ДРУГ — на главную">
      <img src="{logo_uri}" alt="ДРУГ" width="544" height="218">
    </a>
    <nav class="nav" id="nav" aria-label="Основная навигация">
        {nav_html}
    </nav>
    <a href="become-hero.html" class="btn btn--primary header__cta">Рассказать свою историю</a>
    <button class="burger" id="burger" aria-label="Меню" aria-expanded="false" aria-controls="nav">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<main id="main"></main>

{footer}

<script>
const PHOTOS = {json.dumps(photos, ensure_ascii=False)};
const PAGES = {json.dumps(bodies, ensure_ascii=False)};
const TITLES = {json.dumps(titles, ensure_ascii=False)};

{bundle_js()}

{ROUTER}
</script>
'''

    open(OUT, 'w', encoding='utf-8').write(html)
    print(f'\nГотово: {OUT}')
    print(f'Размер: {len(html.encode()) / 1048576:.1f} МБ')


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""
Общая оболочка страниц сайта «ДРУГ»: <head>, шапка, футер.

Страницы собираются один раз скриптом build.py и дальше живут как
обычные HTML-файлы — их можно править руками. Скрипт нужен, только
если захотите поменять шапку или футер сразу на всех страницах.
"""

# Все модули сайта. Порядок не важен: браузер тянет их параллельно.
MODULES = ('main', 'ui', 'map', 'russia', 'data', 'archive', 'hero', 'issues', 'forms', 'lightbox')

NAV = [
    ('about.html',      'О проекте'),
    ('issues.html',     'Выпуски'),
    ('archive.html',    'Архив'),
    ('expedition.html', 'Экспедиции'),
    ('zines.html',      'Зины'),
    ('partners.html',   'Сотрудничество'),
    ('faq.html',        'Вопросы'),
    ('contacts.html',   'Контакты'),
]

# Боевой адрес сайта. Нужен для og:image и canonical: краулеры Telegram,
# ВКонтакте и поисковиков не разрешают относительные пути, и без домена
# превью расшаренной ссылки собирается пустым.
# При переезде на свой домен поменять здесь и пересобрать страницы.
SITE_URL = 'https://softeners.github.io/friend/site/'

# Адрес приёмника заявок (Formspree, getform, свой обработчик).
# Пока пусто, формы НЕ показывают «заявка принята»: человек видит честный
# экран с текстом своей заявки и адресами, куда её прислать. Как только
# строка заполнена и страницы пересобраны — формы отправляют по-настоящему.
FORM_ENDPOINT = ''

# TODO: заказчик просил сменить почту, новый адрес пока не назван.
# Поменять здесь и в js/data.js — больше нигде не встречается.
EMAIL = 'sycheva.alina.2000@bk.ru'
PHONE = '+7&nbsp;961&nbsp;879&#8209;55&#8209;42'   # неразрывный: номер не должен ломаться переносом
PHONE_HREF = '+79618795542'

TELEGRAM = 'https://t.me/tvoi_friend_media'
VK = 'https://vk.ru/tvoi_friend_media'

AUTHOR = 'Сычева Алина Артемовна'
AUTHOR_TG = 'https://t.me/Alina_Teplo'


def header(active, root=''):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ''
        links.append(f'<a href="{root}{href}" class="nav__link"{cur}>{label}</a>')
    nav = '\n        '.join(links)
    return f'''<a class="skip-link" href="#main">Перейти к содержимому</a>

<header class="header">
  <div class="container header__inner">
    <a href="{root}index.html" class="logo" aria-label="ДРУГ — на главную">
      <img src="{root}assets/img/logo.png" alt="ДРУГ" width="544" height="218">
    </a>

    <nav class="nav" id="nav" aria-label="Основная навигация">
        {nav}
    </nav>

    <a href="{root}become-hero.html" class="btn btn--primary header__cta">Рассказать историю</a>

    <button type="button" class="burger" id="burger" aria-label="Меню" aria-expanded="false" aria-controls="nav">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>'''


def footer(root=''):
    return f'''<footer class="footer">
  <div class="container">
    <div class="footer__top">
      <div class="footer__col">
        <a href="{root}index.html" class="logo logo--lg" aria-label="ДРУГ — на главную">
          <img src="{root}assets/img/logo.png" alt="ДРУГ" width="544" height="218">
        </a>
        <p class="footer__about">
          Исследуем страну через призму восприятия её жителей.
        </p>
      </div>

      <div class="footer__col">
        <span class="footer__head">Написать</span>
        <a class="footer__contact footer__link" href="mailto:{EMAIL}">{EMAIL}</a>
        <a class="footer__contact footer__link" href="tel:{PHONE_HREF}">{PHONE}</a>
      </div>

      <div class="footer__col">
        <span class="footer__head">Читать</span>
        <a class="footer__link" href="{TELEGRAM}" target="_blank" rel="noopener">Telegram-канал</a>
        <a class="footer__link" href="{VK}" target="_blank" rel="noopener">Сообщество ВКонтакте</a>
        <a class="footer__link" href="{root}issues.html">Цифровые выпуски</a>
        <a class="footer__link" href="{root}archive.html">Медиаархив</a>
        <a class="footer__link" href="{root}news.html">Ход проекта</a>
      </div>

      <div class="footer__col">
        <span class="footer__head">Участвовать</span>
        <a class="footer__link" href="{root}become-hero.html">Стать героем</a>
        <a class="footer__link" href="{root}expedition.html">Поехать в экспедицию</a>
        <a class="footer__link" href="{root}become-participant.html">Заявка в экспедицию</a>
        <a class="footer__link" href="{root}zines.html">Заказать зин</a>
        <a class="footer__link" href="{root}partners.html">Сотрудничество</a>
      </div>
    </div>

    <div class="footer__bottom">
      <span>© <span data-year>2026</span> Проект «ДРУГ». Автор
        <a class="footer__link" href="{AUTHOR_TG}" target="_blank" rel="noopener">{AUTHOR}</a></span>
      <span class="footer__legal">
        <a class="footer__link" href="{root}faq.html">Вопрос-ответ</a>
        <a class="footer__link" href="{root}privacy.html">Обработка персональных данных</a>
      </span>
    </div>
  </div>
</footer>'''


def card_preload(cover, root=''):
    """Предзагрузка обложки первой карточки.

    Сетку рисует скрипт, поэтому браузер узнаёт о картинке только после
    того, как модули отработали, и самый крупный элемент экрана появляется
    почти на секунду позже, чем мог бы. imagesrcset и imagesizes обязаны
    совпадать с тем, что потом выдаст photo() в js/ui.js, иначе браузер
    скачает файл дважды."""
    if not cover:
        return ''
    p = f'{root}assets/img/photo/{cover}'
    return (f'  <link rel="preload" as="image" type="image/webp" fetchpriority="high"\n'
            f'        imagesrcset="{p}-600.webp 600w, {p}-1200.webp 1200w"\n'
            f'        imagesizes="(max-width: 860px) 90vw, 30vw">\n')


def page(*, title, description, body, active='', root='', slug='',
         needs_js=False, noindex=False, preload='',
         og_image='assets/img/photo/sunset-ridge-1200.jpg'):
    """Оболочка страницы.

    slug — путь страницы от корня сайта ('index.html', 'notes/altay.html').
    Из него собираются canonical и og:url. Абсолютные, а не относительные:
    относительный og:image краулеры Telegram и ВКонтакте не разрешают,
    и превью расшаренной ссылки приходит пустым.
    """
    canonical = SITE_URL + ('' if slug == 'index.html' else slug)
    endpoint = f' data-form-endpoint="{FORM_ENDPOINT}"' if FORM_ENDPOINT else ''
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ''
    noscript = NOSCRIPT.format(root=root) if needs_js else ''
    modulepreload = '\n'.join(
        f'  <link rel="modulepreload" href="{root}js/{m}.js">' for m in MODULES)
    return f'''<!DOCTYPE html>
<html lang="ru" data-root="{root}"{endpoint}>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#2C2C2C">{robots}

  <link rel="canonical" href="{canonical}">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="ДРУГ">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{SITE_URL}{og_image}">
  <meta property="og:image:alt" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:locale" content="ru_RU">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" href="{root}assets/img/favicon.png" type="image/png" sizes="192x192">
  <link rel="apple-touch-icon" href="{root}assets/img/favicon.png">
  <link rel="preload" href="{root}assets/fonts/rubik-800-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{root}assets/fonts/inter-400-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{root}css/fonts.css">
  <link rel="stylesheet" href="{root}css/tokens.css">
  <link rel="stylesheet" href="{root}css/base.css">
  <link rel="stylesheet" href="{root}css/components.css">
  <link rel="stylesheet" href="{root}css/pages.css">

{preload}  <!-- Модули грузятся водопадом: main.js → его импорты → их импорты.
       На медленном канале это три круга по 150 мс, и сетка выпусков
       дорисовывается через три секунды после первой отрисовки, сдвигая
       всё, что ниже. modulepreload запускает загрузку всех сразу. -->
{modulepreload}

  <!-- Помечаем страницу как «скрипты работают». Без этого класса стили
       не прячут блоки перед анимацией, и сайт читается даже без JS. -->
  <script>document.documentElement.classList.add('js')</script>
</head>
<body>

{header(active, root)}

<main id="main">
{noscript}
{body}
</main>

{footer(root)}

<script type="module" src="{root}js/main.js"></script>
</body>
</html>
'''


# Карта, сетка выпусков, архив и каталог зинов рисуются из js/data.js.
# Если скрипт не загрузился, эти разделы остаются пустыми, и человек
# не понимает, сломан сайт или там правда ничего нет.
NOSCRIPT = '''<noscript>
  <p class="notice notice--noscript">
    Часть разделов собирается скриптом, а он сейчас отключён — карта, сетка выпусков
    и архив останутся пустыми. Читать проект это не мешает:
    <a href="{root}notes/altay.html">путевые заметки с Алтая</a> открываются как обычная страница,
    а заявку можно прислать письмом на <a href="mailto:''' + EMAIL + '''">''' + EMAIL + '''</a>.
  </p>
</noscript>'''


def tg_block(note='Короткие заметки прямо с маршрута. Кого встретили, что снимаем сегодня, где застряли.',
             root=''):
    """Блок «следить за экспедицией». Стоит на десяти страницах, поэтому
    именно здесь живёт единственная ссылка на «Ход проекта» из тела сайта:
    страница есть, а войти на неё раньше было неоткуда."""
    return f'''<div class="tg reveal">
  <div class="tg__text">
    <p class="tg__title">Следить за экспедицией</p>
    <p class="tg__note">{note}</p>
  </div>
  <div class="tg__actions">
    <a class="btn btn--ghost" href="{TELEGRAM}" target="_blank" rel="noopener">Подписаться в Telegram</a>
    <a class="btn btn--ghost" href="{root}news.html">Ход проекта</a>
  </div>
</div>'''


def head_block(label, num, title=None, lead=None):
    """Шапка секции: ДРУГ ◆ РАЗДЕЛ слева, полевая нумерация справа.

    Заголовок и подводка живут в отдельной обёртке .section__intro —
    расстояния между ними задаёт gap, а не margin у каждого элемента.
    """
    h = f'''<div class="section__head">
    <span class="eyebrow">ДРУГ <span class="eyebrow__rest">{label}</span></span>
    <span class="section__num">{num}</span>
  </div>'''
    if not (title or lead):
        return h

    inner = ''
    if title:
        inner += f'\n    <h2 class="h2">{title}</h2>'
    if lead:
        inner += f'\n    <p class="lead">{lead}</p>'
    return h + f'\n\n  <div class="section__intro">{inner}\n  </div>'

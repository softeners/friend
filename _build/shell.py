# -*- coding: utf-8 -*-
"""
Общая оболочка страниц сайта «ДРУГ»: <head>, шапка, футер.

Страницы собираются один раз скриптом build.py и дальше живут как
обычные HTML-файлы — их можно править руками. Скрипт нужен, только
если захотите поменять шапку или футер сразу на всех страницах.
"""

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

# TODO: заказчик просил сменить почту, новый адрес пока не назван.
# Поменять здесь, в js/data.js и в js/forms.js — больше нигде не встречается.
EMAIL = 'sycheva.alina.2000@bk.ru'
PHONE = '+7 961 879-55-42'
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

    <button class="burger" id="burger" aria-label="Меню" aria-expanded="false" aria-controls="nav">
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
      </div>

      <div class="footer__col">
        <span class="footer__head">Участвовать</span>
        <a class="footer__link" href="{root}become-hero.html">Стать героем</a>
        <a class="footer__link" href="{root}expedition.html">Поехать в экспедицию</a>
        <a class="footer__link" href="{root}zines.html">Заказать зин</a>
        <a class="footer__link" href="{root}partners.html">Сотрудничество</a>
      </div>
    </div>

    <div class="footer__bottom">
      <span>© <span data-year>2026</span> Проект «ДРУГ». Автор
        <a class="footer__link" href="{AUTHOR_TG}" target="_blank" rel="noopener">{AUTHOR}</a></span>
      <a class="footer__link" href="{root}faq.html">Вопрос-ответ</a>
    </div>
  </div>
</footer>'''


def page(*, title, description, body, active='', root='', og_image='assets/img/photo/sunset-ridge-1200.jpg'):
    return f'''<!DOCTYPE html>
<html lang="ru" data-root="{root}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#2C2C2C">

  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{root}{og_image}">
  <meta property="og:locale" content="ru_RU">

  <link rel="icon" href="{root}assets/img/logo.png" type="image/png">
  <link rel="preload" href="{root}assets/fonts/rubik-800-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{root}assets/fonts/inter-400-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{root}css/fonts.css">
  <link rel="stylesheet" href="{root}css/tokens.css">
  <link rel="stylesheet" href="{root}css/base.css">
  <link rel="stylesheet" href="{root}css/components.css">
  <link rel="stylesheet" href="{root}css/pages.css">

  <!-- Помечаем страницу как «скрипты работают». Без этого класса стили
       не прячут блоки перед анимацией, и сайт читается даже без JS. -->
  <script>document.documentElement.classList.add('js')</script>
</head>
<body>

{header(active, root)}

<main id="main">
{body}
</main>

{footer(root)}

<script type="module" src="{root}js/main.js"></script>
</body>
</html>
'''


def tg_block(note='Короткие заметки прямо с маршрута. Кого встретили, что снимаем сегодня, где застряли.'):
    return f'''<div class="tg reveal">
  <div class="tg__text">
    <p class="tg__title">Следить за экспедицией</p>
    <p class="tg__note">{note}</p>
  </div>
  <a class="btn btn--ghost" href="{TELEGRAM}" target="_blank" rel="noopener">Подписаться в Telegram</a>
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

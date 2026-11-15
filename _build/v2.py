# -*- coding: utf-8 -*-
"""
Сборка сайта «Друг» по аудиту от 15 ноября 2026.

Запуск:  python3 _build/v2.py   (из корня сайта)

Шапка, подвал, плашка cookies и все страницы с текстами собираются здесь.
Старые скрипты (build.py и pages_*.py) больше не используются.
"""
import os, json, html

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
V = '20261115v2'
EMAIL = 'tvoi.friend.media@yandex.ru'
TG = 'https://t.me/tvoi_friend_media'
VK = 'https://vk.ru/tvoi_friend_media'
SITE = 'https://tvoifriend.ru/'
OG = 'assets/img/og-sysert.jpg'

e = html.escape


# ─────────────────────────────── общий каркас ───────────────────────────────
def head(title, desc, root='', og_img=OG, og_type='website'):
    return f'''<!DOCTYPE html>
<html lang="ru" data-root="{root}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="theme-color" content="#2C2C2C">

  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="«Друг»">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:image" content="{SITE}{og_img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="ru_RU">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}{og_img}">

  <link rel="icon" href="{root}assets/img/logo.png" type="image/png">
  <link rel="preload" href="{root}assets/fonts/rubik-800-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{root}assets/fonts/inter-400-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{root}css/fonts.css">
  <link rel="stylesheet" href="{root}css/tokens.css">
  <link rel="stylesheet" href="{root}css/base.css">
  <link rel="stylesheet" href="{root}css/components.css?v={V}">
  <link rel="stylesheet" href="{root}css/pages.css?v={V}">
  <link rel="stylesheet" href="{root}css/v2.css?v={V}">
  <script>document.documentElement.classList.add('js')</script>
</head>
<body>

<a class="skip-link" href="#main">Перейти к содержимому</a>
'''


NAV = [('archive.html', 'Истории'), ('participate.html', 'Участвовать'), ('about.html', 'О проекте')]


def header(root='', active=''):
    links = '\n'.join(
        f'        <a href="{root}{h}" class="nav__link"{" aria-current=\"page\"" if h == active else ""}>{t}</a>'
        for h, t in NAV)
    return f'''
<header class="header">
  <div class="container header__inner">
    <a href="{root}index.html" class="logo" aria-label="«Друг» — на главную">
      <img src="{root}assets/img/logo.png" alt="Друг" width="544" height="218">
    </a>

    <nav class="nav" id="nav" aria-label="Основная навигация">
{links}
        <a href="{root}become-hero.html" class="nav__link nav__link--cta">Рассказать о человеке</a>
    </nav>

    <a href="{root}become-hero.html" class="btn btn--primary header__cta">Рассказать о человеке</a>

    <button class="burger" id="burger" aria-label="Меню" aria-expanded="false" aria-controls="nav">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
'''


def partners_strip(root=''):
    return f'''<div class="partners" data-partners>
        <a class="partners__item" href="https://www.fondpotanin.ru/" target="_blank" rel="noopener">Благотворительный фонд Владимира Потанина</a>
        <span class="partners__item">Сысертский завод-музей</span>
        <span class="partners__item">«Кот Шредингера»</span>
        <span class="partners__item">Госкомитет Республики Башкортостан по молодежной политике и Республиканский молодежный психологический центр</span>
        <span class="partners__item partners__item--caps">АНО «ПОЛЕТ»</span>
      </div>'''


def footer(root=''):
    L = lambda h, t: f'<a class="footer__link" href="{root}{h}">{t}</a>'
    return f'''
<footer class="footer">
  <div class="container">
    <div class="footer__top">
      <div class="footer__col footer__col--wide">
        <a href="{root}index.html" class="logo logo--lg" aria-label="«Друг» — на главную">
          <img src="{root}assets/img/logo.png" alt="Друг" width="544" height="218">
        </a>
        <p class="footer__about">«Друг». Медиа о людях из небольших городов России</p>
        <p class="footer__support">Проект реализуется при поддержке Благотворительного фонда Владимира Потанина</p>
      </div>

      <div class="footer__col">
        <span class="footer__head">Разделы</span>
        {L('archive.html', 'Истории')}
        {L('participate.html', 'Участвовать')}
        {L('about.html', 'О проекте')}
      </div>

      <div class="footer__col">
        <span class="footer__head">Еще</span>
        {L('partners.html', 'Партнерам')}
        {L('faq.html', 'Вопросы')}
        {L('contacts.html', 'Контакты')}
      </div>
    </div>

    <div class="footer__partners">
      {partners_strip(root)}
    </div>

    <div class="footer__bottom">
      <span>{L('privacy.html', 'Политика обработки данных')}. {L('privacy.html#consent', 'Согласие на обработку данных')}. © 2026 «Друг»</span>
    </div>
  </div>
</footer>

<div class="cookies" data-cookies hidden>
  <p class="cookies__text">Мы считаем посещения через Яндекс Метрику, чтобы понимать, какие истории вы читаете. Подробности в <a href="{root}privacy.html">политике</a>.</p>
  <button type="button" class="btn btn--paper cookies__ok" data-cookies-ok>Хорошо</button>
</div>

<script type="module" src="{root}js/main.js?v={V}"></script>
</body>
</html>
'''


def page(title, desc, body, root='', active='', og_img=OG, og_type='website'):
    return head(title, desc, root, og_img, og_type) + header(root, active) + \
        '\n<main id="main">\n' + body + '\n</main>\n' + footer(root)


def section_head(rest, num=None):
    n = f'<span class="section__num">{num}</span>' if num else ''
    return f'''<div class="section__head">
        <span class="eyebrow">ДРУГ <span class="eyebrow__rest">{rest}</span></span>
        {n}
      </div>'''


def pagehead(rest, title, lead='', extra=''):
    lead_html = f'<p class="lead pagehead__lead">{lead}</p>' if lead else ''
    return f'''
  <section class="section pagehead">
    <div class="container">
      <span class="eyebrow">ДРУГ <span class="eyebrow__rest">{rest}</span></span>
      <h1 class="h1 pagehead__title">{title}</h1>
      {lead_html}
      {extra}
    </div>
  </section>
'''


def pic(slug, alt, sizes='100vw', eager=False, big=False):
    p = f'assets/img/photo/{slug}'
    srcset = f'{p}-600.webp 600w, {p}-1200.webp 1200w' + (f', {p}-2000.webp 2000w' if big else '')
    ld = 'eager" fetchpriority="high' if eager else 'lazy'
    return f'''<picture>
            <source type="image/webp" srcset="{srcset}" sizes="{sizes}">
            <img src="{p}-1200.jpg" alt="{e(alt)}" loading="{ld}" decoding="async">
          </picture>'''


# ─────────────────────────────── поля форм ───────────────────────────────
def field(id, label, kind='text', required=True, placeholder='', note='', rows=5, maxlength=None,
          extra=''):
    req = ' <span class="field__req" aria-hidden="true">*</span>' if required else \
        ' <span class="field__opt">(необязательно)</span>'
    desc = (f'{id}-note ' if note else '') + f'{id}-err'
    r = ' required' if required else ''
    ph = f' placeholder="{e(placeholder)}"' if placeholder else ''
    ml = f' maxlength="{maxlength}"' if maxlength else ''
    if kind == 'textarea':
        ctl = (f'<textarea class="textarea" id="{id}" name="{id}" rows="{rows}" data-label="это поле"{r}{ml}'
               f' aria-describedby="{desc}"{extra}></textarea>')
        if maxlength:
            ctl += f'\n      <p class="field__count" data-count-for="{id}" aria-hidden="true">0 / {maxlength}</p>'
    elif kind == 'select':
        ctl = f'<select class="select" id="{id}" name="{id}" data-label="это поле"{r} aria-describedby="{desc}">{extra}</select>'
    else:
        ctl = (f'<input class="input" type="{kind}" id="{id}" name="{id}" data-label="это поле"{r}{ph}{ml}'
               f' aria-describedby="{desc}"{extra}>')
    n = f'\n      <p class="field__note" id="{id}-note">{note}</p>' if note else ''
    return f'''<div class="field">
      <label class="field__label" for="{id}">{label}{req}</label>
      {ctl}{n}
      <p class="field__error" id="{id}-err" role="alert"></p>
    </div>'''


def check(id, text, err='Без этого согласия мы не сможем принять заявку'):
    return f'''<div class="field">
        <label class="check">
          <input type="checkbox" name="{id}" id="{id}" required data-error-required="{e(err)}" aria-describedby="{id}-err">
          <span>{text}</span>
        </label>
        <p class="field__error" id="{id}-err" role="alert"></p>
      </div>'''


CONSENT = check('consent', 'Я соглашаюсь на обработку моих персональных данных. '
                '<a href="privacy.html" target="_blank" rel="noopener">Политика обработки данных</a>')


# ─────────────────────────────── ГЛАВНАЯ ───────────────────────────────
def index():
    body = f'''
  <section class="hero hero--home">
      <div class="hero__frame">
        <div class="hero__media">
          {pic('sysert-f3272', 'Цех Сысертского фарфорового завода, под потолком висят фарфоровые голуби', '(max-width: 1360px) 100vw, 1360px', eager=True, big=True)}
        </div>

        <div class="hero__content">
          <span class="hero__margin">медиа о людях</span>
          <h1 class="hero__heading">
            <span class="hero__mark" role="img" aria-label="Друг"></span>
            <span class="hero__title">Раскрываем регионы через истории местных жителей</span>
          </h1>

          <p class="hero__lead">Приезжаем в небольшие города и записываем людей, которые там живут и работают. А вы в путешествиях обретаете друга, который из первых уст поделиться своим сокровенным.</p>

          <div class="hero__actions">
            <a class="btn btn--primary btn--lg" href="archive.html">Читать истории</a>
            <a class="hero__link" href="become-hero.html">Рассказать историю <span aria-hidden="true">→</span></a>
          </div>
        </div>

        <figure class="hero__quote">
          <blockquote>«Все наши стены, все-все родное»</blockquote>
          <figcaption>Зинаида Мотавкина, электрообмотчица, Сысерть</figcaption>
        </figure>
      </div>
  </section>

  <section class="section" id="about">
    <div class="container">
      {section_head('Зачем')}
      <div class="grid grid--sidebar">
        <div class="prose">
          <h2 class="h2">Изучаем регионы через людей</h2>
          <p class="lead">О регионах привыкли рассказывать цифрами: экономика, население, список предприятий. Мы идем к людям. Отливщица, печник и обмотчица знают о своем городе то, чего нет в справочниках. Их истории мы считаем культурным наследием, которое создается прямо сейчас, и собираем из них журналы и маршруты по городам.</p>
        </div>
        <div class="ph ph--4x3">{pic('sysert-f3244', 'Расписной фарфор Сысертского завода', '(max-width: 860px) 92vw, 38vw')}</div>
      </div>
    </div>
  </section>

  <section class="section section--deep" id="issue">
    <div class="container">
      {section_head('Новый выпуск')}
      <div class="latest reveal">
        <a class="ph ph--4x3 latest__ph" href="sysert.html">
          {pic('sysert-e4322', 'Корпус электротехнического завода в Сысерти', '(max-width: 860px) 92vw, 50vw', big=True)}
        </a>
        <div class="latest__body">
          <p class="latest__num">Выпуск 01</p>
          <h2 class="h2">Сысерть</h2>
          <p class="text text--measure">Город заводов. На одном обжигали глину, на другом плавили метал. Мы собрали зин, который ближе познакомит с территорией через их истории.</p>
          <div class="btn-row">
            <a class="btn btn--primary btn--lg" href="sysert.html">Открыть выпуск</a>
            <a class="btn btn--ghost btn--lg" href="zines/sysert/">Листать журнал</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="route">
    <div class="container">
      {section_head('Маршрут')}
      <div class="section__intro"><h2 class="h2">Где мы сейчас</h2></div>
      <ol class="stops">
        <li class="stop stop--done">
          <span class="stop__dot" aria-hidden="true"></span>
          <h3 class="stop__name">Сысерть</h3>
          <p class="stop__text">Записали героев, журнал готов.</p>
        </li>
        <li class="stop">
          <span class="stop__dot" aria-hidden="true"></span>
          <h3 class="stop__name">Шерегеш</h3>
          <p class="stop__text">Едем в январе или феврале. Знаете, кого там записать? <a href="become-hero.html">Напишите нам.</a></p>
        </li>
        <li class="stop">
          <span class="stop__dot" aria-hidden="true"></span>
          <h3 class="stop__name">Алтай</h3>
          <p class="stop__text">Едем весной. Знаете, кого там записать? <a href="become-hero.html">Напишите нам.</a></p>
        </li>
        <li class="stop stop--next">
          <span class="stop__dot" aria-hidden="true"></span>
          <h3 class="stop__name">Дальше</h3>
          <p class="stop__text">Следующий город выберем вместе с вами.</p>
        </li>
      </ol>
    </div>
  </section>

  <section class="section section--deep" id="join">
    <div class="container">
      {section_head('Участие')}
      <div class="section__intro"><h2 class="h2">Как стать частью «Друга»</h2></div>
      <div class="grid grid--2">
        <article class="card card--big reveal">
          <h3 class="card__title">Есть что рассказать?</h3>
          <p class="card__text">Известным быть не нужно. Напишите пару слов о себе или о человеке, которого стоит записать.</p>
          <a class="btn btn--primary" href="become-hero.html">Рассказать о человеке</a>
        </article>
        <article class="card card--big reveal">
          <h3 class="card__title">Хотите записать человека из своего города?</h3>
          <p class="card__text">Мы дадим вопросы, подскажем, как снимать, и отредактируем материал вместе с вами. Он выйдет на сайте с вашим авторством.</p>
          <a class="btn btn--ghost" href="become-participant.html">Стать соавтором</a>
        </article>
      </div>
    </div>
  </section>

  <section class="section" id="partners">
    <div class="container">
      {section_head('Партнеры')}
      <div class="section__intro"><h2 class="h2">С нами</h2></div>
      {partners_strip()}

      <div class="tg reveal">
        <div class="tg__text">
          <p class="tg__title">Пишем с дороги</p>
          <p class="tg__note">Заметки из поездок, новые герои и анонсы выпусков. Здесь же можно заказать печатный журнал, просто напишите нам.</p>
        </div>
        <div class="btn-row">
          <a class="btn btn--ghost" href="{TG}" target="_blank" rel="noopener">Telegram</a>
          <a class="btn btn--ghost" href="{VK}" target="_blank" rel="noopener">ВКонтакте</a>
        </div>
      </div>
    </div>
  </section>
'''
    return page('«Друг». Раскрываем регионы через истории местных жителей',
                'Мы приезжаем в небольшие города и записываем людей, которые там живут и работают. '
                'А вы в путешествиях обретаете друга, который из первых уст поделиться своим сокровенным.',
                body)


# ─────────────────────────────── ИСТОРИИ ───────────────────────────────
def archive():
    body = pagehead('Истории', 'Истории',
                    'Здесь все наши записи: выпуски по городам, герои, фото, видео и отрывки интервью. '
                    'Выберите место или найдите историю по ключевому слову.') + '''
  <section class="section section--flush">
    <div class="container">
      <div class="search">
        <label class="visually-hidden" for="q">Поиск по историям</label>
        <input class="input search__input" type="search" id="q" data-search placeholder="Например, завод или фарфор" autocomplete="off">
      </div>
      <div class="archive__filters" data-filters></div>
      <p class="archive__count" data-archive-count aria-live="polite"></p>
      <div data-archive class="archive__grid"></div>

      <div class="soon">
        <h2 class="h3">Будущие выпуски</h2>
        <ul class="soon__list">
          <li><b>Шерегеш.</b> Скоро, собираем героев.</li>
          <li><b>Алтай.</b> Скоро.</li>
        </ul>
      </div>

      <p class="archive__foot">Хотите использовать наши материалы в учебе или исследовании? <a href="contacts.html">Напишите нам</a>, подскажем, как сослаться.</p>
    </div>
  </section>
'''
    return page('Истории. «Друг»', 'Изучить город перед путешествием: герои, фото, видео и отрывки интервью.',
                body, active='archive.html')


# ─────────────────────────────── ВЫПУСК «СЫСЕРТЬ» ───────────────────────────────
def sysert(heroes):
    cards = '\n'.join(f'''        <a class="card hero-card" href="hero.html?slug={h['slug']}">
          <span class="hero-card__role">{e(h['role'])}</span>
          <h3 class="card__title">{e(h['name'])}</h3>
          <p class="card__text">«{e(h['quotes'][0][:150].rsplit(' ', 1)[0] if len(h['quotes'][0]) > 150 else h['quotes'][0])}{'…' if len(h['quotes'][0]) > 150 else ''}»</p>
        </a>''' for h in heroes)
    body = f'''
  <section class="hero hero--home hero--page hero--issue">
    <div class="hero__frame">
      <div class="hero__media">
        {pic('sysert-e4322', 'Корпус электротехнического завода в Сысерти', '(max-width: 1360px) 100vw, 1360px', eager=True, big=True)}
      </div>
      <div class="hero__content">
        <span class="eyebrow hero__eyebrow">ДРУГ <span class="eyebrow__rest">Выпуск 01</span></span>
        <h1 class="hero__title">Сысерть</h1>
      </div>
      <div class="hero__aside">
        <p class="hero__lead">Сысерть выросла вокруг заводов. Сначала здесь плавили железо, потом создавали фарфор и электромоторы. Мы записали живописцев, отливщиц, печника, обмотчиц и снабженца. Они рассказали про цеха, праздники, девяностые и про то, что осталось от заводов сегодня.</p>
        <a class="btn btn--primary btn--lg" href="zines/sysert/">Листать журнал</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      {section_head('Герои выпуска')}
      <div class="section__intro"><h2 class="h2">Герои выпуска</h2></div>
      <div class="grid grid--3 hero-grid">
{cards}
      </div>
    </div>
  </section>

  <section class="section section--deep">
    <div class="container">
      {section_head('Кто делал выпуск')}
      <div class="grid grid--sidebar">
        <div class="prose">
          <h2 class="h2">Кто делал выпуск</h2>
          <dl class="credits">
            <div><dt>Автор проекта и редактор</dt><dd>Алина Сычева</dd></div>
            <div><dt>Дизайн</dt><dd>Роман Ракчеев, Дарья Щуцкая</dd></div>
            <div><dt>Фото</dt><dd>Софья Брянцева</dd></div>
            <div><dt>Архивные материалы</dt><dd>ООО «Фарфор Сысерти», АНО «Железный», АНО «Полет»</dd></div>
            <div><dt>Краевед, экскурсовод и просто хороший человек</dt><dd>Александр Савичев</dd></div>
          </dl>
        </div>
        <div class="paper paper--right">
          <span class="paper__label">Журнал</span>
          <p>Печатный журнал про Сысерть можно заказать в нашем <a href="{TG}" target="_blank" rel="noopener">Telegram</a> или <a href="{VK}" target="_blank" rel="noopener">ВКонтакте</a>.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      {section_head('Еще из этого места')}
      <div class="section__intro"><h2 class="h2">Еще из этого места</h2></div>
      <div class="grid grid--3">
        <a class="card material-card" href="zines/sysert/">
          <div class="ph ph--4x3 ph--zoom material-card__ph">{pic('sysert-f3272', 'Журнал «Друг. Сысерть»', '(max-width: 860px) 90vw, 30vw')}</div>
          <span class="material-card__kind">Журнал</span>
          <h3 class="card__title">Журнал «Друг. Сысерть»</h3>
          <p class="card__text">Листайте журнал онлайн.</p>
        </a>
        <a class="card material-card" href="archive.html?region=sysert">
          <div class="ph ph--4x3 ph--zoom material-card__ph">{pic('sysert-f3244', 'Расписной фарфор Сысерти', '(max-width: 860px) 90vw, 30vw')}</div>
          <span class="material-card__kind">Истории</span>
          <h3 class="card__title">Все истории Сысерти</h3>
          <p class="card__text">Герои, фото и отрывки интервью.</p>
        </a>
      </div>
    </div>
  </section>

  <section class="section section--deep">
    <div class="container">
      {section_head('Поделиться')}
      <div class="share" data-share>
        <a class="btn btn--ghost" href="https://t.me/share/url?url={SITE}sysert.html" target="_blank" rel="noopener">Поделиться в Telegram</a>
        <a class="btn btn--ghost" href="https://vk.com/share.php?url={SITE}sysert.html" target="_blank" rel="noopener">Поделиться ВКонтакте</a>
        <button type="button" class="btn btn--ghost" data-copy-link>Скопировать ссылку</button>
      </div>
      <p class="archive__foot">Печатный журнал про Сысерть можно заказать в нашем <a href="{TG}" target="_blank" rel="noopener">Telegram</a> или <a href="{VK}" target="_blank" rel="noopener">ВКонтакте</a>.</p>
    </div>
  </section>
'''
    return page('Сысерть. Выпуск «Друг»',
                'Истории людей, которые работали на фарфоровом и электротехническом заводах Сысерти.',
                body, og_type='article')


# ─────────────────────────────── ГЕРОЙ ───────────────────────────────
def hero():
    body = '''
  <section class="section pagehead pagehead--doc">
    <div class="container" data-hero></div>
  </section>
'''
    return page('Герой выпуска. «Друг»',
                'Истории людей, которые работали на фарфоровом и электротехническом заводах Сысерти.',
                body, og_type='article')


# ─────────────────────────────── УЧАСТВОВАТЬ ───────────────────────────────
def participate():
    body = pagehead('Участвовать', 'Как стать частью «Друга»') + '''
  <section class="section section--flush">
    <div class="container">
      <div class="grid grid--3">
        <a class="card card--big card--link" href="become-hero.html">
          <span class="card__num">01</span>
          <h2 class="card__title">Рассказать о себе</h2>
          <p class="card__text">Напишите, где живете и чем занимаетесь.</p>
          <span class="card__more">Заполнить форму →</span>
        </a>
        <a class="card card--big card--link" href="become-hero.html?mode=other">
          <span class="card__num">02</span>
          <h2 class="card__title">Посоветовать героя</h2>
          <p class="card__text">Знаете человека, которого стоит записать? Расскажите о нем.</p>
          <span class="card__more">Заполнить форму →</span>
        </a>
        <a class="card card--big card--link card--accent" href="become-participant.html">
          <span class="card__num">03</span>
          <h2 class="card__title">Стать соавтором</h2>
          <p class="card__text">Запишите человека из своего города, мы поможем.</p>
          <span class="card__more">Подать заявку →</span>
        </a>
      </div>
    </div>
  </section>
'''
    return page('Исследуйте свой регион с  проектом «Друг»',
                'Расскажите свою историю жизни, посоветуйте героя  вашего города',
                body, active='participate.html')


# ─────────────────────────────── ГЕРОЯМ (форма) ───────────────────────────────
def become_hero():
    self_fields = '\n'.join([
        field('name', 'Как вас зовут'),
        field('place', 'Где вы живете', placeholder='Город или поселок'),
        field('work', 'Чем вы занимаетесь (пары предложений хватит)', 'textarea', rows=4, maxlength=1500),
        field('contact', 'Как с вами связаться: телефон, почта или ник в Telegram'),
    ])
    other_fields = '\n'.join([
        field('o_name', 'Как вас зовут'),
        field('o_contact', 'Как с вами связаться'),
        field('o_hero', 'Кого советуете и где он живет'),
        field('o_why', 'Чем он интересен', 'textarea', rows=4, maxlength=1500),
        field('o_knows', 'Он знает, что вы его советуете?', 'select',
              extra='<option value="" disabled selected>Выберите</option><option>Да</option><option>Нет</option><option>Скажу позже</option>'),
        '<p class="form__hint">Контакты героя пока не присылайте. Сначала спросите его самого.</p>',
    ])
    body = pagehead('Героям', 'Знаете человека, которого стоит записать?',
                    'Это можете быть вы сами, ваша бабушка или мастер с соседней улицы. '
                    'Соцсети и опыт интервью не нужны.') + f'''
  <section class="section section--flush">
    <div class="container">
      <div class="grid grid--sidebar">
        <div>
          <form class="form" data-form="hero" data-subject="Заявка героя с сайта «Друг»" novalidate>
            <div class="form__section form__section--first">
              <div class="switch" role="radiogroup" aria-label="О ком заявка">
                <label class="switch__opt"><input type="radio" name="mode" value="self" data-mode-switch checked><span>Я рассказываю о себе</span></label>
                <label class="switch__opt"><input type="radio" name="mode" value="other" data-mode-switch><span>Я советую другого человека</span></label>
              </div>
            </div>

            <div class="form__section" data-mode="self">
              <div class="form__grid">
{self_fields}
              </div>
            </div>

            <div class="form__section" data-mode="other" hidden>
              <div class="form__grid">
{other_fields}
              </div>
            </div>

            <div class="form__section">
              {CONSENT}
            </div>

            <div class="form__foot">
              <button class="btn btn--primary btn--lg" type="submit" data-submit>Отправить</button>
              <p class="form__status" data-status role="status" aria-live="polite"></p>
            </div>
            <p class="form__hint">Перед съемкой мы попросим героя подписать согласие на публикацию. Его текст можно прочитать заранее.</p>
          </form>

          <div class="sent" data-sent="hero">
            <div class="paper paper--wide">
              <span class="paper__label">Заявка у нас</span>
              <p class="paper__title">Спасибо!</p>
              <p>Мы получили заявку и ответим в течение недели. Если ответа нет, напишите нам в <a href="{TG}" target="_blank" rel="noopener">Telegram</a> или <a href="{VK}" target="_blank" rel="noopener">ВКонтакте</a>, письма иногда теряются.</p>
            </div>
          </div>
        </div>

        <aside class="aside">
          <div class="card">
            <h2 class="card__title">Что будет дальше</h2>
            <ol class="numlist">
              <li>Вы заполняете форму, это пять минут.</li>
              <li>Мы отвечаем в течение недели и договариваемся о звонке.</li>
              <li>Приезжаем сами или находим соавтора в вашем городе.</li>
              <li>Перед публикацией показываем вам текст и фотографии.</li>
            </ol>
          </div>
          <div class="card">
            <h2 class="card__title">Что получает герой</h2>
            <ul class="list">
              <li>Все фотографии со съемки и запись интервью.</li>
              <li>Печатный журнал со своей историей.</li>
              <li>Право прочитать текст до публикации и попросить правки.</li>
              <li>Право в любой момент попросить убрать материал с сайта.</li>
            </ul>
          </div>
          <div class="paper paper--right">
            <span class="paper__label">Про деньги</span>
            <p>Участие бесплатное. Гонорар за интервью мы не платим.</p>
          </div>
        </aside>
      </div>
    </div>
  </section>
'''
    return page('Расскажите историю своей жизни проекту «Друг»',
                '«Друг» изучает регионы России через людей. Расскажите о себе или о человеке из вашего города, '
                'чью историю стоит сохранить. Известным быть не нужно.',
                body, active='participate.html')


# ─────────────────────────────── СОАВТОРАМ (форма) ───────────────────────────────
def become_participant():
    who = ''.join(f'<option>{x}</option>' for x in [
        'студент бакалавриата', 'студент магистратуры', 'журналист', 'фотограф или видеограф',
        'житель или активист', 'другое'])
    fields1 = '\n'.join([
        field('name', 'Фамилия и имя'),
        '<div class="form__row">',
        field('age', 'Возраст', 'number', extra=' min="12" max="99" data-age'),
        field('city', 'Город'),
        '</div>',
        field('who', 'Кто вы', 'select', extra='<option value="" disabled selected>Выберите</option>' + who),
        field('study', 'Где учитесь или работаете', required=False),
    ])
    fields2 = '\n'.join([
        field('why', 'Кого хотите записать и почему', 'textarea', rows=7, maxlength=1500),
        field('links', 'Ссылка на работы или соцсети', required=False),
        '<div class="form__row">',
        field('email', 'Почта', 'email', placeholder='you@example.ru'),
        field('phone', 'Telegram или телефон', 'tel', placeholder='@nickname или +7 900 000-00-00'),
        '</div>',
    ])
    guardian = '\n'.join([
        field('guardian_name', 'Имя родителя или опекуна'),
        field('guardian_contact', 'Как с ним связаться'),
    ])
    body = pagehead('Соавторам', 'Запишите человека из своего города',
                    'Вы встречаетесь с героем у себя в городе. Мы даем вопросы, памятку по съемке '
                    'и редактируем материал вместе с вами.') + f'''
  <section class="section section--flush">
    <div class="container">
      <div class="grid grid--sidebar">
        <div>
          <form class="form" data-form="participant" data-subject="Заявка соавтора с сайта «Друг»" novalidate>
            <div class="form__section form__section--first">
              <div class="form__grid">
{fields1}
              </div>
            </div>

            <div class="form__section">
              <div class="guardian">
                <p class="form__legend">Вам еще нет 18?</p>
                <p class="form__hint">Тогда нужно согласие родителя или опекуна. Укажите его имя и как с ним связаться. Мы поговорим с ним до начала работы.</p>
                <div class="form__grid">
{guardian}
                </div>
              </div>
            </div>

            <div class="form__section">
              <div class="form__grid">
{fields2}
              </div>
            </div>

            <div class="form__section">
              {CONSENT}
              {check('terms', 'Я прочитал условия для соавторов и принимаю их', 'Без согласия с условиями мы не сможем принять заявку')}
            </div>

            <div class="form__foot">
              <button class="btn btn--primary btn--lg" type="submit" data-submit>Отправить заявку</button>
              <p class="form__status" data-status role="status" aria-live="polite"></p>
            </div>
          </form>

          <div class="sent" data-sent="participant">
            <div class="paper paper--wide">
              <span class="paper__label">Заявка у нас</span>
              <p class="paper__title">Заявка у нас!</p>
              <p>Ответим в течение недели и предложим время для созвона.</p>
            </div>
          </div>
        </div>

        <aside class="aside">
          <div class="card">
            <h2 class="card__title">Кого мы ищем</h2>
            <p class="card__text">Студентов бакалавриата и магистратуры, журналистов, фотографов, видеографов, активистов и жителей, которым интересен свой город. Журналистское образование не нужно.</p>
          </div>
          <div class="card">
            <h2 class="card__title">Как это устроено</h2>
            <ol class="numlist">
              <li>Вы присылаете заявку и пишете, кого хотите записать.</li>
              <li>Мы созваниваемся, обсуждаем героя, даем вопросы и памятку.</li>
              <li>Вы записываете разговор и делаете фото.</li>
              <li>Вместе редактируем, герой подписывает согласие.</li>
              <li>Материал выходит на сайте с вашим именем.</li>
            </ol>
          </div>
          <div class="card">
            <h2 class="card__title">Что вы получите</h2>
            <p class="card__text">Публикацию с вашим именем и страницу автора со всеми работами. Кейс для портфолио. Лучшие материалы попадут в печатный журнал. Место в «Друг.Клубе», где знакомятся авторы и герои. Самых активных авторов позовем в команду.</p>
          </div>
          <div class="paper paper--right" id="terms-info">
            <span class="paper__label">Важно знать заранее</span>
            <p>Это добровольное соавторство. Мы не платим гонорар и не оплачиваем дорогу и жилье. Вы работаете в своем городе и в удобное вам время. Материал остается вашим, а нам вы разрешаете публиковать его на сайте, в журнале и в соцсетях с вашим именем. Подробности в условиях для соавторов.</p>
          </div>
        </aside>
      </div>
    </div>
  </section>
'''
    return page('Станьте соавтором «Друга»: запишите историю жителя своего города',
                'Истории обычных людей тоже наследие города. Запишите человека, который живет рядом с вами, '
                'а мы поможем с вопросами, съемкой и редактурой. Материал выйдет с вашим именем.',
                body, active='participate.html')


# ─────────────────────────────── О ПРОЕКТЕ ───────────────────────────────
def about():
    team = [('Алина Сычева', 'автор проекта'), ('Георгий Шарипов', 'технический директор'),
            ('Виолетта Шкуропатская', 'контент-маркетолог'), ('Роман Ракчеев', 'дизайнер'),
            ('Дарья Щуцкая', 'дизайнер')]
    team_html = '\n'.join(f'''        <div class="person">
          <div class="person__photo" aria-hidden="true">{n.split()[0][0]}{n.split()[1][0]}</div>
          <p class="person__name">{n}</p>
          <p class="person__role">{r}</p>
        </div>''' for n, r in team)
    steps = ['Ищем героев. Нам пишут сами люди, их внуки, соседи и краеведы.',
             'Приезжаем туда, где человек живет и работает.',
             'Слушаем и почти не перебиваем.',
             'Собираем выпуск на сайте и печатный журнал. Герой видит текст до публикации.',
             'Знакомим героев и авторов из разных городов между собой.']
    body = pagehead('О проекте', 'Медиа, которое ведет себя как друг',
                    'Друг знакомит тебя со своими людьми, водит по любимым местам и рассказывает, '
                    'как здесь все устроено. Так мы и рассказываем о городах.') + f'''
  <section class="section section--flush">
    <div class="container">
      <div class="grid grid--sidebar">
        <div class="prose">
          <h2 class="h2">Зачем мы это делаем</h2>
          <p class="lead">О небольших городах обычно пишут коротко: достопримечательности, население, сколько ехать до областного центра. В Сысерти мы услышали другое. Живописец спустя годы узнает свои сервизы в чужих домах. Печник каждый Новый год играл Деда Мороза для заводских детей. Обмотчицы носили работу домой и гнули детали всей семьей. Если такие истории не записать, они уйдут вместе с людьми.</p>
        </div>
        <div class="ph ph--3x4">{pic('sysert-f3267', 'Живописец за работой на фарфоровом заводе', '(max-width: 860px) 92vw, 38vw')}</div>
      </div>
    </div>
  </section>

  <section class="section section--deep">
    <div class="container">
      {section_head('Как мы работаем')}
      <div class="section__intro"><h2 class="h2">Как мы работаем</h2></div>
      <ol class="steps steps--big">
        {''.join(f'<li>{s}</li>' for s in steps)}
      </ol>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="grid grid--2">
        <div class="prose">
          <h2 class="h2">Во что мы верим</h2>
          <p class="text">Мы оставляем прямую речь: интонация и любимые словечки тоже часть истории. Герой сам решает, что о нем публиковать, и может передумать. Журнал печатаем на бумаге, чтобы его можно было подарить и увезти с собой.</p>
        </div>
        <div class="prose">
          <h2 class="h2">Что уже сделано</h2>
          <p class="text">Мы записали героев Сысерти и выпустили про нее <a href="zines/sysert/">журнал</a>. Собрали методику, по которой интервью может провести человек без журналистского образования.</p>
          <h2 class="h2">Что дальше</h2>
          <p class="text">Выпуски про Шерегеш и Алтай, на сайте и на бумаге. «Друг.Клуб», где герои и авторы знакомятся друг с другом. Открытый архив всех записей.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--deep">
    <div class="container">
      {section_head('Команда')}
      <div class="section__intro"><h2 class="h2">Команда</h2></div>
      <div class="team">
{team_html}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      {section_head('Нас поддерживают')}
      <div class="section__intro">
        <h2 class="h2">Нас поддерживают</h2>
        <p class="lead">Проект реализуется при поддержке Благотворительного фонда Владимира Потанина. Ниже логотипы партнеров.</p>
      </div>
      {partners_strip()}
    </div>
  </section>
'''
    return page('О проекте «Друг»: изучаем регионы России через истории людей',
                'Мы записываем жителей небольших городов и собираем из их историй журналы и маршруты. '
                'Так сохраняется культурное наследие, которое создается прямо сейчас.',
                body, active='about.html')


# ─────────────────────────────── ПАРТНЕРАМ ───────────────────────────────
def partners():
    body = pagehead('Партнерам', 'Сделаем выпуск вместе',
                    'Мы работаем с музеями, университетами, фондами и предприятиями. Выпуск про Сысерть '
                    'мы делали вместе с заводом «Фарфор Сысерти» и музеем на электротехническом заводе '
                    'и АНО «ПОЛЕТ».') + f'''
  <section class="section section--flush">
    <div class="container">
      <div class="grid grid--sidebar">
        <div>
          <h2 class="h2">Что можем сделать</h2>
          <div class="grid grid--2">
            <article class="card"><h3 class="card__title">Выпуск о вашем городе или поселке</h3></article>
            <article class="card"><h3 class="card__title">Истории людей вашего музея или предприятия</h3></article>
            <article class="card"><h3 class="card__title">Совместный проект со студентами или волонтерами</h3><p class="card__text">Они записывают героев, мы помогаем и редактируем.</p></article>
            <article class="card"><h3 class="card__title">Выставку или презентацию выпуска у вас</h3></article>
          </div>
        </div>
        <aside class="aside">
          <div class="paper paper--right">
            <span class="paper__label">Как начать</span>
            <p>Напишите на <a href="mailto:{EMAIL}">{EMAIL}</a>, что за место и чего хочется. Ответим в течение недели.</p>
          </div>
        </aside>
      </div>
    </div>
  </section>

  <section class="section section--deep">
    <div class="container">
      {section_head('С нами')}
      {partners_strip()}
    </div>
  </section>
'''
    return page('Партнерам: выпуск «Друга» о вашем городе, музее или предприятии',
                'Расскажем о вашей территории через людей, которые там живут и работают: интервью, фото, '
                'видео и печатный журнал. Работаем с музеями, вузами, фондами и предприятиями.', body)


# ─────────────────────────────── ВОПРОСЫ ───────────────────────────────
FAQ = [
    ('Что такое «Друг»?', 'Медиа о людях из небольших российских городов. Мы приезжаем, записываем их рассказы и собираем из них выпуск о городе. Мы изучаем как судьбы людей переплетаются с территорией и раскрываем регион именно через эти истории.'),
    ('Как стать героем, если я не публичный человек?', 'Публичность не нужна. Заполните <a href="become-hero.html">короткую форму</a> и расскажите своими словами, чем занимаетесь.'),
    ('Это платно? Герой что-то получает?', 'Участие бесплатное, гонорар мы не платим. Герой получает все фото со съемки, запись интервью.'),
    ('Можно посмотреть текст до публикации?', 'Да. Мы всегда показываем герою текст и фото перед выходом и правим неточности.'),
    ('А если я передумаю?', 'Напишите нам, и мы уберем материал с сайта. Уже напечатанные журналы забрать не получится, об этом мы предупреждаем заранее.'),
    ('Почему вы приезжаете, а не созваниваетесь?', 'По видеосвязи человек говорит иначе. Нам важно видеть, где он живет, где работал и как создает свои вещи, чем и где вдохновляется, как выглядит его рабочий процесс и детали жизни.'),
    ('Где вы сейчас работаете?', 'Выпуск про Сысерть готов. Дальше Шерегеш и Алтай. Следующие места выбираем вместе с читателями.'),
    ('Кто может стать соавтором?', 'Студенты бакалавриата и магистратуры, журналисты, фотографы, видеографы, активисты и жители, которым интересен свой город. Вопросы и памятку мы дадим.'),
    ('Вы оплачиваете соавторам дорогу?', 'Нет. Соавторы записывают героев в своем городе. Взамен публикация с именем и кейс в портфолио, лучшие работы выходят в печатном журнале. А лучшие команды из регионов будут приглашены на стажироку и могут попасть в постоянную команду медиа, создавая заказные выпуски.'),
    ('Как купить печатный журнал?', f'Напишите нам в <a href="{TG}" target="_blank" rel="noopener">Telegram</a> или <a href="{VK}" target="_blank" rel="noopener">ВКонтакте</a>. Журнал про Сысерть можно сначала <a href="zines/sysert/">полистать на сайте</a>.'),
    ('Можно использовать ваши материалы?', 'Для учебы и исследований можно, напишите нам, подскажем, как сослаться. Для публикации в других медиа или для использования материалов в коммерческих целях нужно наше разрешение и согласие героя.'),
]


def faq():
    items = '\n'.join(f'''        <details class="faq__item">
          <summary class="faq__q">{q}<span class="faq__sign" aria-hidden="true"></span></summary>
          <div class="faq__a"><p class="text">{a}</p></div>
        </details>''' for q, a in FAQ)
    body = pagehead('Вопросы', 'Что обычно спрашивают') + f'''
  <section class="section section--flush">
    <div class="container">
      <div class="faq">
{items}
      </div>
      <div class="tg reveal">
        <div class="tg__text">
          <p class="tg__title">Не нашли ответа?</p>
          <p class="tg__note">Напишите нам. Ответим и добавим вопрос сюда</p>
        </div>
        <a class="btn btn--ghost" href="mailto:{EMAIL}">Написать на почту</a>
      </div>
    </div>
  </section>
'''
    return page('Вопросы о проекте «Друг»: как стать героем или соавтором',
                'Кого мы записываем, что получает герой, можно ли передумать и как заказать журнал. '
                'Ответы на частые вопросы о проекте «Друг».', body)


# ─────────────────────────────── КОНТАКТЫ ───────────────────────────────
def contacts():
    body = pagehead('Контакты', 'Напишите нам', 'Отвечаем в течение недели. Быстрее всего в Telegram.') + f'''
  <section class="section section--flush">
    <div class="container">
      <div class="contact-grid">
        <a class="contact-card" href="mailto:{EMAIL}">
          <span class="contact-card__kind">Почта</span>
          <span class="contact-card__value">{EMAIL}</span>
        </a>
        <a class="contact-card" href="{TG}" target="_blank" rel="noopener">
          <span class="contact-card__kind">Telegram</span>
          <span class="contact-card__value">t.me/tvoi_friend_media</span>
        </a>
        <a class="contact-card" href="{VK}" target="_blank" rel="noopener">
          <span class="contact-card__kind">ВКонтакте</span>
          <span class="contact-card__value">vk.ru/tvoi_friend_media</span>
        </a>
        <a class="contact-card contact-card--accent" href="become-hero.html">
          <span class="contact-card__value">Хотите рассказать о себе или посоветовать героя?</span>
          <span class="contact-card__note">Рассказать о человеке →</span>
        </a>
        <a class="contact-card contact-card--accent" href="become-participant.html">
          <span class="contact-card__value">Хотите записать человека из своего города?</span>
          <span class="contact-card__note">Стать соавтором →</span>
        </a>
        <a class="contact-card contact-card--accent" href="partners.html">
          <span class="contact-card__value">Хотите сделать выпуск вместе?</span>
          <span class="contact-card__note">Партнерам →</span>
        </a>
      </div>
      <p class="fine">Оператор персональных данных Сычева Алина Артемовна</p>
    </div>
  </section>
'''
    return page('Контакты проекта «Друг»: почта, Telegram и ВКонтакте',
                'Напишите, если хотите рассказать историю, записать жителя своего города или сделать выпуск '
                '«Друга» вместе. Отвечаем в течение недели.', body)


# ─────────────────────────────── 404 ───────────────────────────────
def notfound():
    body = pagehead('404', 'Такой страницы нет', 'Возможно, мы ее переименовали или убрали.',
                    '<div class="pagehead__actions"><a class="btn btn--primary btn--lg" href="index.html">На главную</a>'
                    '<a class="btn btn--ghost btn--lg" href="archive.html">Читать истории</a></div>')
    # 404 открывается по любому адресу: <base> ставит пути от корня сайта
    txt = page('Такой страницы нет. «Друг»', 'Такой страницы нет. Возможно, мы ее переименовали или убрали.', body)
    return txt.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n  <script>document.write(\'<base href="\'+(location.pathname.indexOf(\'/friend/\')===0?\'/friend/\':\'/\')+\'">\')</script>', 1)


# ─────────────────────────────── ЖУРНАЛ ───────────────────────────────
def journal():
    R = '../../'
    data = json.loads(open(os.path.join(ROOT, '_build', 'zinetext.json'), encoding='utf-8').read())
    junk = {'Друг · Сысерть', 'tvoifriend.ru', 'ДРУГ', 'Друг'}
    parts = []
    for num, name, lines in data:
        ls = [l for l in lines if l not in junk and not l.isdigit() and len(l) > 2]
        if not ls:
            continue
        ps = '\n'.join(f'          <p>{e(l)}</p>' for l in ls)
        parts.append(f'''        <section class="zine-text__part">
          <h3 class="h3">{e(name)}</h3>
{ps}
        </section>''')
    text = '\n'.join(parts)
    body = pagehead('Журнал', 'Выпуск 01. Сысерть',
                    'Листайте журнал онлайн. Фарфоровый и электротехнический заводы Сысерти в рассказах людей, '
                    'которые там работали. Город, каким его помнят местные.') + f'''
  <section class="section section--flush">
    <div class="container">
      <div class="book" data-book>
        <iframe class="book__frame" src="book.html?v={V}" title="Журнал «Друг. Сысерть»" allow="fullscreen" allowfullscreen></iframe>
      </div>
      <div class="book__tools">
        <p class="book__hint"><span class="hint-mouse">Листайте стрелками или тяните лист за угол. Колесико меняет масштаб, двойной клик приближает.</span><span class="hint-touch">Листайте пальцем. Чтобы приблизить, раздвиньте два пальца.</span></p>
        <a class="btn btn--ghost" href="book.html" target="_blank" rel="noopener">На весь экран ↗</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="grid grid--2">
        <article class="card card--big">
          <h2 class="card__title">Хотите держать журнал в руках?</h2>
          <p class="card__text">Напишите нам, и мы расскажем, как его получить.</p>
          <a class="btn btn--primary" href="{TG}" target="_blank" rel="noopener">Заказать печатный журнал</a>
        </article>
        <article class="card card--big">
          <h2 class="card__title">Знаете человека, которого стоит записать?</h2>
          <a class="btn btn--ghost" href="{R}become-hero.html">Рассказать о человеке</a>
        </article>
      </div>
    </div>
  </section>

  <section class="section section--deep">
    <div class="container">
      <details class="zine-text">
        <summary class="zine-text__sum"><span class="h2">Текст журнала</span><span class="zine-text__note">Все развороты обычным текстом. Подробнее о героях в <a href="{R}sysert.html">выпуске «Сысерть»</a>.</span></summary>
        <div class="zine-text__body">
{text}
        </div>
      </details>
    </div>
  </section>
'''
    return page('Журнал «Друг», выпуск 01: Сысерть в историях ее жителей',
                'Листайте журнал онлайн. Фарфоровый и электротехнический заводы Сысерти в рассказах людей, '
                'которые там работали. Город, каким его помнят местные.', body, root=R, og_type='article')


def redirect(to, title):
    return f'''<!DOCTYPE html>
<html lang="ru"><head><meta charset="UTF-8"><title>{title}</title>
<meta http-equiv="refresh" content="0; url={to}"><link rel="canonical" href="{to}">
<meta name="robots" content="noindex"></head>
<body><p><a href="{to}">{title}</a></p><script>location.replace('{to}'+location.hash)</script></body></html>
'''


def wrap_existing(src, title, desc):
    """Старые страницы (политика, статья из админки): берём их <main> и ставим новый каркас."""
    body = open(os.path.join(ROOT, '_build', src), encoding='utf-8').read().strip()
    body = body.replace('<span class="legal__num">4</span>', '<span class="legal__num" id="consent">4</span>')
    body = body.replace('Медиаархив', 'Истории').replace('Вернуться в архив', 'Вернуться к историям')
    out = page(title, desc, '')
    a, b = out.index('<main id="main">'), out.index('</main>') + 7
    return out[:a] + body + out[b:]


def main():
    hero_data = json.loads(open(os.path.join(ROOT, '_build', 'heroes.json'), encoding='utf-8').read())
    files = {
        'index.html': index(),
        'archive.html': archive(),
        'sysert.html': sysert(hero_data),
        'hero.html': hero(),
        'participate.html': participate(),
        'become-hero.html': become_hero(),
        'become-participant.html': become_participant(),
        'about.html': about(),
        'partners.html': partners(),
        'faq.html': faq(),
        'contacts.html': contacts(),
        '404.html': notfound(),
        'zines/sysert/index.html': journal(),
        'zines.html': redirect('zines/sysert/', 'Журнал «Друг. Сысерть»'),
        'news.html': redirect('archive.html', 'Истории'),
        'issues.html': redirect('archive.html', 'Истории'),
        'privacy.html': wrap_existing('privacy_src.html', 'Политика обработки данных. «Друг»',
                                      'Политика обработки персональных данных проекта «Друг»: какие данные мы собираем '
                                      'через формы на сайте, зачем, сколько храним и как их удалить.'),
        'article.html': wrap_existing('article_src.html', 'История. «Друг»', 'История проекта «Друг».'),
    }
    for name, txt in files.items():
        with open(os.path.join(ROOT, name), 'w', encoding='utf-8') as f:
            f.write(txt)
        print(f'  {name:26s} {len(txt) / 1024:6.1f} KB')


if __name__ == '__main__':
    main()

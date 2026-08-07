# -*- coding: utf-8 -*-
"""
Главная, О проекте, Выпуски, Медиаархив, Досье героя.

Все формулировки взяты из документа о проекте (концепция, философия,
ценностное предложение, логика проекта). Ничего не додумано.
"""

from shell import page, tg_block, head_block

PHOTO = 'assets/img/photo'


def img(root, slug, alt, sizes='100vw', eager=False, big=False):
    p = f'{root}{PHOTO}/{slug}'
    srcset = (f'{p}-600.webp 600w, {p}-1200.webp 1200w, {p}-2000.webp 2000w' if big
              else f'{p}-600.webp 600w, {p}-1200.webp 1200w')
    load = 'eager" fetchpriority="high' if eager else 'lazy'
    return (f'<picture>\n'
            f'      <source type="image/webp" srcset="{srcset}" sizes="{sizes}">\n'
            f'      <img src="{p}-1200.jpg" alt="{alt}" loading="{load}" decoding="async">\n'
            f'    </picture>')


# ═══════════════════════════════════════════════════════════════
# 1. ГЛАВНАЯ
# ═══════════════════════════════════════════════════════════════
INDEX = page(
    title='ДРУГ — живые истории российских территорий',
    description='Культурно-медийный проект «Друг» знакомит со страной через доверие к человеку. '
                'Экспедиции в шесть регионов, доверительные интервью, документальная съёмка, '
                'цифровые выпуски и печатный зин.',
    active='index.html',
    body=f'''
  <!-- ── Первый экран ── -->
  <section class="hero">
    <div class="hero__media">
      {img('', 'sunset-ridge', 'Закат над хребтом в Республике Алтай', sizes='100vw', eager=True, big=True)}
    </div>

    <div class="container hero__inner">
      <span class="eyebrow">ДРУГ <span class="eyebrow__rest">культурно-медийный проект</span></span>

      <h1 class="hero__title">Знакомим со страной через доверие к человеку</h1>

      <p class="hero__lead">
        Экспедиции в шесть регионов России, доверительные интервью и документальная съёмка.
        Мы сохраняем живые истории, сказания и легенды и превращаем их в общее культурное наследие.
      </p>

      <div class="hero__foot">
        <div class="hero__actions">
          <a class="btn btn--primary btn--lg" href="become-hero.html">Рассказать свою историю</a>
          <a class="btn btn--outline btn--lg" href="issues.html">Читать выпуски</a>
        </div>

        <div class="paper paper--right">
          <span class="paper__label">Коротко о нас</span>
          <p>Мы делаем так, чтобы медиа было как друг. Знакомим с отдалёнными уголками России
             через крафтовые материалы «из уст в уста» и собираем сеть социальных связей.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ── Идея ── -->
  <section class="section">
    <div class="container">
      {head_block('Идея', '01 / 05')}

      <div class="grid grid--sidebar">
        <div class="prose">
          <h2 class="h2">Человек, а не список объектов</h2>
          <p class="lead">
            «Друг» — культурно-медийный проект, который показывает Россию не через перечень
            достопримечательностей, а через человека: мастера, учителя, художника, хранителя,
            предпринимателя.
          </p>
          <p class="text">
            Смысл места появляется тогда, когда конкретный человек рассказывает о своей малой
            родине и любимых местах. Объясняет, почему остался или переехал, каким был его путь
            и как на него повлияла среда.
          </p>
          <p class="text">
            Мы записываем интервью от первого лица. Доверие и полное погружение рождаются
            из личной речи с её интонацией, из деталей рассказчика и его обстановки.
            Пересказ и редакционные колонки это теряют.
          </p>
        </div>

        <figure class="ph ph--3x4">
          {img('', 'altay-16', 'Всадник на летнем выпасе, Республика Алтай',
               sizes='(max-width: 860px) 92vw, 38vw')}
        </figure>
      </div>
    </div>
  </section>

  <!-- ── Карта ── -->
  <section class="section section--deep">
    <div class="container">
      {head_block('География', '02 / 05', 'Шесть регионов',
                  'Новосибирская область, Республика Алтай, Шерегеш, Бурятия, Якутия и Приморье. '
                  'По каждому региону выйдет отдельный выпуск.')}

      <div class="grid grid--sidebar map-layout">
        <div class="map" data-map data-map-mode="link"></div>
        <ul class="region-list" data-map-list></ul>
      </div>
    </div>
  </section>

  <!-- ── Последний выпуск ── -->
  <section class="section">
    <div class="container">
      {head_block('Журнал', '03 / 05')}
      <div class="latest reveal" data-latest-issue></div>
    </div>
  </section>

  <!-- ── Два способа участвовать ── -->
  <section class="section section--deep" id="join">
    <div class="container">
      {head_block('Участие', '04 / 05', 'Два способа стать частью проекта')}

      <article class="invite reveal">
        <div class="ph ph--4x3 invite__media">
          {img('', 'altay-11', 'Житель Республики Алтай на лесной дороге',
               sizes='(max-width: 860px) 92vw, 46vw')}
        </div>

        <div class="invite__body">
          <span class="invite__kind">Героям</span>
          <h3 class="h2 invite__title">Расскажите свою историю</h3>
          <p class="text">
            Мы приезжаем к тем, кто своим делом меняет жизнь небольшой территории. Публичность
            и опыт интервью не нужны, важно само дело и ваша готовность о нём говорить.
          </p>
          <ul class="list">
            <li>Видимость и признание вклада</li>
            <li>Возможность поделиться видением мира и своей историей</li>
            <li>Связь с другими героями проекта из разных регионов</li>
            <li>Продвижение вашего дела и возможные коллаборации</li>
            <li>Печатный зин с вашей историей и материалы съёмки</li>
          </ul>
          <a class="btn btn--primary btn--lg" href="become-hero.html">Рассказать свою историю</a>
        </div>
      </article>

      <article class="invite invite--flip reveal">
        <div class="ph ph--4x3 invite__media">
          {img('', 'altay-2', 'Дорога между сёлами во время экспедиции',
               sizes='(max-width: 860px) 92vw, 46vw')}
        </div>

        <div class="invite__body">
          <span class="invite__kind">Молодым авторам</span>
          <h3 class="h2 invite__title">Поехать в экспедицию</h3>
          <p class="text">
            Участники экспедиций обучатся методам интервьюирования, видеосъёмке и основам
            документальной фотографии. Познакомятся с людьми из интересующей их области,
            увидят пути развития в своём регионе.
          </p>
          <p class="invite__note">
            В экспедицию по региону едут те, кто в этом регионе живёт. Перед поездкой участники
            проходят обучение методике с наставником.
          </p>
          <a class="btn btn--paper btn--lg" href="expedition.html">Узнать об экспедициях</a>
        </div>
      </article>
    </div>
  </section>

  <!-- ── Вопросы и Telegram ── -->
  <section class="section">
    <div class="container">
      {head_block('Вопросы', '05 / 05', 'Что спрашивают чаще всего')}

      <div class="faq">
        <details class="faq__item">
          <summary class="faq__q">Герой что-то платит или получает?<span class="faq__sign" aria-hidden="true"></span></summary>
          <div class="faq__a"><p class="text">Участие бесплатное, гонорар за интервью мы не платим.
            Герой получает видимость и признание вклада, связь с другими участниками проекта,
            все фотографии съёмки и печатный зин со своей историей.</p></div>
        </details>
        <details class="faq__item">
          <summary class="faq__q">Почему обязательно нужна экспедиция?<span class="faq__sign" aria-hidden="true"></span></summary>
          <div class="faq__a"><p class="text">Доверие невозможно собрать дистанционно. Мы не приглашаем
            героя в студию, а приезжаем к нему в среду. Это метод включённого наблюдения, который
            даёт контекст, невозможный при удалённой работе.</p></div>
        </details>
        <details class="faq__item">
          <summary class="faq__q">Кто может поехать в экспедицию?<span class="faq__sign" aria-hidden="true"></span></summary>
          <div class="faq__a"><p class="text">Молодые авторы, которые живут в одном из шести регионов
            маршрута. Журналистское образование не требуется: методика построена так, чтобы
            качественное интервью мог провести любой подготовленный человек.</p></div>
        </details>
      </div>

      <div class="section__foot">
        <a class="btn btn--ghost" href="faq.html">Все вопросы и ответы</a>
      </div>

      {tg_block()}
    </div>
  </section>
''')


# ═══════════════════════════════════════════════════════════════
# 2. О ПРОЕКТЕ
# ═══════════════════════════════════════════════════════════════
ABOUT = page(
    title='О проекте — ДРУГ',
    description='Идея, философия и миссия проекта «Друг». Почему восприятие места идёт через '
                'человека, зачем нужны экспедиции и что даёт печатный артефакт.',
    active='about.html',
    body=f'''
  <section class="section pagehead">
    <div class="container">
      <span class="eyebrow">ДРУГ <span class="eyebrow__rest">О проекте</span></span>
      <h1 class="h1 pagehead__title">Медиа как друг</h1>
      <p class="lead pagehead__lead">
        Проект «Друг» знакомит людей с людьми. Он прививает путь путешественника, а не туриста,
        и знакомит с отдалёнными уголками России через крафтовые материалы «из уст в уста».
      </p>
    </div>
  </section>

  <section class="section section--flush">
    <div class="container">
      <figure class="ph ph--16x9">
        {img('', 'mountain-range', 'Горная гряда в Республике Алтай', sizes='100vw', big=True)}
      </figure>
    </div>
  </section>

  <section class="section">
    <div class="container">
      {head_block('Миссия', '01 / 04', 'Зачем всё это',
                  'Проект собирает сеть связей между людьми, даёт инструмент знакомства '
                  'с регионом через подлинное общение и формирует новый взгляд на путешествия.')}

      <div class="grid grid--sidebar">
        <div class="prose">
          <p class="lead">
            Проект создан для людей, которые каждый день делают выбор в пользу своего дома
            и находят вдохновение на созидание и развитие своего дела и региона.
          </p>
          <p class="text">
            Мы создаём культурное медиа нового типа, которое показывает Россию через живые
            человеческие истории и формирует глубокую эмоциональную связь человека и территории.
          </p>
        </div>

        <div class="paper paper--right paper--mid">
          <span class="paper__label">Наши ценности</span>
          <ul class="list">
            <li>Доверие важнее охвата.</li>
            <li>Человек первичен, а место поддерживает человека.</li>
            <li>Физическое имеет значение: уход в цифру уводит фокус от материального мира
                и от контакта человека с человеком.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--deep">
    <div class="container">
      {head_block('Философия', '02 / 04', 'Почему именно так')}

      <div class="grid grid--3">
        <article class="card">
          <h3 class="card__title">Восприятие места через человека</h3>
          <p class="card__text">
            Смысл места появляется, когда конкретный человек рассказывает о своей малой родине
            и любимых местах, объясняет, почему остался или переехал, и как на него повлияла среда.
          </p>
        </article>

        <article class="card">
          <h3 class="card__title">Интервью от первого лица</h3>
          <p class="card__text">
            Доверие и полное погружение рождаются через личную речь с интонацией, детали
            рассказчика и его обстановки. Пересказ и редакционные колонки теряют это.
          </p>
        </article>

        <article class="card card--accent">
          <h3 class="card__title">Экспедиции</h3>
          <p class="card__text">
            Доверие невозможно собрать дистанционно. В атмосферу, пантомимику рассказчика,
            его традиции, кухню и быт нельзя погрузиться удалённо.
          </p>
        </article>

        <article class="card">
          <h3 class="card__title">Журнал, цифровой и печатный</h3>
          <p class="card__text">
            История требует композиции. Лента даёт только фрагменты, а печатный артефакт
            становится материальным доказательством важности истории.
          </p>
        </article>

        <article class="card">
          <h3 class="card__title">Документальная фотография</h3>
          <p class="card__text">
            Постановка возвращает в туристическую оптику. Живые кадры позволяют заглянуть
            внутрь сцены и увидеть человека таким, какой он есть.
          </p>
        </article>

        <article class="card">
          <h3 class="card__title">Материалы делает молодёжь</h3>
          <p class="card__text">
            В экспедицию по региону едут те, кто в нём живёт. Работая над выпуском, молодые
            авторы находят в своём регионе новые связи и возможности.
          </p>
        </article>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      {head_block('Методика', '03 / 04', 'В чём новизна',
                  'Глубокие интервью и личные истории используют многие. Но эти практики остаются '
                  'авторскими, не систематизированы и не могут быть переданы другим.')}

      <div class="grid grid--sidebar">
        <ul class="list list--loose">
          <li>Мы не создаём ещё одно успешное шоу, а разрабатываем алгоритм: гайд, чек-листы
              и банк вопросов. По нему качественное интервью может провести
              человек без журналистского образования.</li>
          <li>Фокус на методе, а не на личности интервьюера. В центре внимания герой и его история,
              а не автор и его интерпретации услышанного.</li>
          <li>Экспедиция — обязательное условие. Мы приезжаем к герою в его среду, а не приглашаем
              в студию. Это метод включённого наблюдения.</li>
          <li>Мы фиксируем не только сам материал, но и метод работы с героем. Метод становится
              основой для обучения, поэтому проект тиражируем и не зависит от одной команды.</li>
        </ul>

        <div class="paper paper--right">
          <span class="paper__label">Результат первого этапа</span>
          <p>Методика в виде гайда, чек-листов и банка вопросов. Шесть цифровых выпусков,
             пилотный зин, медиаархив с открытой и внутренней частями и этот сайт-платформа.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--deep">
    <div class="container">
      {head_block('Экосистема', '04 / 04', 'Четыре части проекта',
                  'Сейчас работает первая часть. Остальные вырастают из неё по мере того, '
                  'как накапливается материал и появляется аудитория.')}

      <div class="eco">
        <article class="card card--accent eco__step">
          <span class="eco__now">этап 1</span>
          <h3 class="card__title">Друг.Медиа</h3>
          <p class="card__text">Экспедиции, выпуски, зин и записанная методика работы с героем.</p>
        </article>
        <article class="card eco__step">
          <span class="eco__now">этап 2</span>
          <h3 class="card__title">Друг.Академия</h3>
          <p class="card__text">Обучение методике. Курс из шести модулей и практика с наставником.</p>
        </article>
        <article class="card eco__step">
          <span class="eco__now">этап 3</span>
          <h3 class="card__title">Друг.Клуб</h3>
          <p class="card__text">Сообщество: лекции, разборы выпусков, показы и встречи с героями.</p>
        </article>
        <article class="card eco__step">
          <span class="eco__now">долгосрочно</span>
          <h3 class="card__title">Друг.Архив</h3>
          <p class="card__text">Культурный архив живых историй российских территорий.</p>
        </article>
      </div>

      {tg_block()}
    </div>
  </section>
''')


# ═══════════════════════════════════════════════════════════════
# 3. ВЫПУСКИ
# ═══════════════════════════════════════════════════════════════
ISSUES = page(
    title='Цифровые выпуски — ДРУГ',
    description='Шесть цифровых выпусков журнала, по одному на регион. Каждый выпуск собран '
                'как номер журнала с композицией, а не как лента постов.',
    active='issues.html',
    body=f'''
  <section class="section pagehead">
    <div class="container">
      <span class="eyebrow">ДРУГ <span class="eyebrow__rest">Журнал</span></span>
      <h1 class="h1 pagehead__title">Цифровые выпуски</h1>
      <p class="lead pagehead__lead">
        Шесть выпусков, по одному на регион. Такое количество выбрано не случайно: оно позволяет
        доказать, что методика воспроизводима в разных культурных контекстах.
      </p>
      <p class="lead pagehead__lead">
        История требует композиции, поэтому каждый выпуск собран как номер журнала,
        который читают от начала до конца.
      </p>
    </div>
  </section>

  <section class="section section--flush">
    <div class="container">
      <div class="grid grid--3" data-issues></div>

      {tg_block('О выходе нового выпуска мы сообщаем в Telegram-канале.')}
    </div>
  </section>
''')


# ═══════════════════════════════════════════════════════════════
# 4. МЕДИААРХИВ
# ═══════════════════════════════════════════════════════════════
ARCHIVE = page(
    title='Медиаархив — ДРУГ',
    description='Открытая часть медиаархива проекта: видео-интервью, статьи, фотографии '
                'и подкасты по регионам и героям.',
    active='archive.html',
    body=f'''
  <section class="section pagehead">
    <div class="container">
      <span class="eyebrow">ДРУГ <span class="eyebrow__rest">Медиаархив</span></span>
      <h1 class="h1 pagehead__title">Открытая часть архива</h1>
      <p class="lead pagehead__lead">
        Открытая часть архива собрана здесь: путевые заметки, материалы о территориях
        и досье героев. Выберите регион на карте или отфильтруйте по типу и формату.
      </p>
    </div>
  </section>

  <section class="section section--flush">
    <div class="container">
      <div class="grid grid--sidebar map-layout">
        <div class="map" data-map data-map-mode="filter"></div>
        <ul class="region-list" data-map-list></ul>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section__head">
        <span class="eyebrow">ДРУГ <span class="eyebrow__rest">Материалы</span></span>
        <span class="section__num" data-archive-count></span>
      </div>

      <div class="archive__filters" data-filters></div>

      <div class="archive__grid" data-archive></div>

      {tg_block('Архив пополняется после каждой экспедиции. Анонсы выходят в канале.')}
    </div>
  </section>
''')


# ═══════════════════════════════════════════════════════════════
# 5. ДОСЬЕ ГЕРОЯ
# ═══════════════════════════════════════════════════════════════
HERO = page(
    title='Досье героя — ДРУГ',
    description='Материалы одного героя проекта: фотографии с экспедиции, фрагменты интервью '
                'и ссылка на выпуск журнала.',
    active='archive.html',
    body='''
  <section class="section pagehead pagehead--doc">
    <div class="container" data-hero></div>
  </section>

  <section class="section section--flush">
    <div class="container">
      ''' + tg_block() + '''
    </div>
  </section>
''')

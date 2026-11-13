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


# Простые геометрические иконки шагов маршрута «Как работает Друг».
# Не набор из внешней библиотеки: те же четыре штриха, что и в остальной
# графике сайта (скрепка, галочка чекбокса) — inline SVG, stroke=currentColor.
ICON_FIND = ('<svg viewBox="0 0 28 28" fill="none" stroke="currentColor" stroke-width="1.6" '
             'stroke-linecap="round"><circle cx="12" cy="12" r="7.5"/><path d="M17.5 17.5L23 23"/></svg>')
ICON_VISIT = ('<svg viewBox="0 0 28 28" fill="none" stroke="currentColor" stroke-width="1.6" '
              'stroke-linecap="round"><path d="M4 20Q10 8 14 14T24 8" stroke-dasharray=".5 4.2"/>'
              '<circle cx="24" cy="8" r="2.2" fill="currentColor" stroke="none"/></svg>')
ICON_TELL = ('<svg viewBox="0 0 28 28" fill="none" stroke="currentColor" stroke-width="1.6" '
             'stroke-linecap="round" stroke-linejoin="round">'
             '<path d="M14 9c-2.2-1.6-5.2-2-9-1.6v13.2c3.8-.4 6.8 0 9 1.6 2.2-1.6 5.2-2 9-1.6V7.4c-3.8-.4-6.8 0-9 1.6Z"/>'
             '<path d="M14 9v13.2"/></svg>')
ICON_LINK = ('<svg viewBox="0 0 28 28" fill="none" stroke="currentColor" stroke-width="1.6">'
             '<circle cx="10.5" cy="14" r="6"/><circle cx="18.5" cy="14" r="6"/></svg>')


# ═══════════════════════════════════════════════════════════════
# 1. ГЛАВНАЯ
# ═══════════════════════════════════════════════════════════════
INDEX = page(
    title='ДРУГ — медиа о людях, которые делают российские регионы особенными',
    description='Культурно-медийный проект «Друг» показывает Россию через людей: мастеров, '
                'художников, предпринимателей, хранителей традиций. Экспедиции по регионам, '
                'документальные интервью, цифровые выпуски и печатный зин.',
    active='index.html',
    body=f'''
  <!-- ── Первый экран ── -->
  <section class="hero hero--cinematic">
    <div class="hero__media">
      {img('', 'sunset-ridge', 'Закат над хребтом в Республике Алтай', sizes='100vw', eager=True, big=True)}
    </div>

    <div class="container hero__inner">
      <span class="eyebrow">ДРУГ <span class="eyebrow__rest">культурно-медийный проект</span></span>

      <h1 class="hero__title">Медиа о&nbsp;людях, которые делают<br>российские регионы особенными</h1>

      <p class="hero__lead">
        Мы отправляемся в&nbsp;экспедиции по&nbsp;России, записываем документальные интервью
        с&nbsp;местными жителями и&nbsp;превращаем их истории в&nbsp;цифровые выпуски,
        фотографии и&nbsp;печатные издания.
      </p>

      <p class="hero__accent">
        Главная идея проекта — показать Россию через людей, а&nbsp;не через список
        достопримечательностей.
      </p>

      <div class="hero__actions">
        <a class="btn btn--primary btn--lg" href="issues.html">Читать выпуски</a>
        <a class="btn btn--outline btn--lg" href="become-hero.html">Рассказать историю</a>
      </div>
    </div>
  </section>

  <!-- ── Как работает «Друг» ── -->
  <section class="section" id="how">
    <div class="container">
      {head_block('Как это устроено', '01 / 09', 'Как работает «Друг»')}

      <div class="route">
        <div class="route__item reveal">
          <span class="route__node" aria-hidden="true">{ICON_FIND}</span>
          <div class="route__body">
            <span class="route__num">01</span>
            <h3 class="route__title">Находим героев</h3>
            <p class="route__text">Мастеров, художников, предпринимателей, хранителей традиций,
              исследователей и&nbsp;других людей, связанных с&nbsp;жизнью территории.</p>
          </div>
        </div>

        <div class="route__item reveal">
          <span class="route__node" aria-hidden="true">{ICON_VISIT}</span>
          <div class="route__body">
            <span class="route__num">02</span>
            <h3 class="route__title">Приезжаем к&nbsp;ним</h3>
            <p class="route__text">Проводим интервью в&nbsp;их реальной среде и&nbsp;снимаем
              документальные фотографии и&nbsp;видео.</p>
          </div>
        </div>

        <div class="route__item reveal">
          <span class="route__node" aria-hidden="true">{ICON_TELL}</span>
          <div class="route__body">
            <span class="route__num">03</span>
            <h3 class="route__title">Рассказываем их истории</h3>
            <p class="route__text">Создаём цифровые выпуски, публикации и&nbsp;печатные зины.</p>
          </div>
        </div>

        <div class="route__item reveal">
          <span class="route__node" aria-hidden="true">{ICON_LINK}</span>
          <div class="route__body">
            <span class="route__num">04</span>
            <h3 class="route__title">Соединяем людей</h3>
            <p class="route__text">Помогаем героям становиться видимыми за&nbsp;пределами своего
              региона и&nbsp;создаём связи между участниками проекта.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ── Кого мы показываем ── -->
  <section class="section section--deep">
    <div class="container">
      {head_block('Люди', '02 / 09', 'Людей, через которых можно узнать место',
                  'Мы рассказываем о&nbsp;людях, которые своим делом формируют жизнь территории: '
                  'мастерах, художниках, предпринимателях, учителях, исследователях, хранителях '
                  'традиций и&nbsp;создателях локальных инициатив.')}

      <div class="category-grid">
        <div class="ph ph--4x3 ph--empty"><span>Мастера</span></div>
        <div class="ph ph--4x3 ph--empty"><span>Художники</span></div>
        <div class="ph ph--4x3 ph--empty"><span>Предприниматели</span></div>
        <div class="ph ph--4x3 ph--empty"><span>Хранители традиций</span></div>
        <div class="ph ph--4x3 ph--empty"><span>Исследователи</span></div>
        <div class="ph ph--4x3 ph--empty"><span>Создатели локальных инициатив</span></div>
      </div>

      <div class="section__foot">
        <a class="btn btn--primary btn--lg" href="become-hero.html">Рассказать историю</a>
      </div>
    </div>
  </section>

  <!-- ── Герой получает медиаподдержку ── -->
  <section class="section" id="support">
    <div class="container">
      {head_block('Героям', '03 / 09', 'Герой получает медиаподдержку',
                  'Участие в&nbsp;проекте бесплатно. Мы создаём материалы о&nbsp;человеке '
                  'и&nbsp;его деле и&nbsp;передаём герою готовые фотографии и&nbsp;другие '
                  'материалы.')}

      <div class="grid grid--3">
        <article class="card">
          <h3 class="card__title">История на платформе</h3>
          <p class="card__text">Публикация истории героя на&nbsp;сайте проекта.</p>
        </article>
        <article class="card">
          <h3 class="card__title">Профессиональные фотографии</h3>
          <p class="card__text">Фотографии героя, его работы и&nbsp;среды, в&nbsp;которой
            он&nbsp;живёт и&nbsp;работает.</p>
        </article>
        <article class="card">
          <h3 class="card__title">Публикация материалов о вас и вашем деле</h3>
          <p class="card__text">В&nbsp;социальных сетях проекта и&nbsp;на&nbsp;партнёрских
            площадках.</p>
        </article>
        <article class="card">
          <h3 class="card__title">Внимание к своему делу</h3>
          <p class="card__text">Рассказ о&nbsp;мастерской, продукте, инициативе, услуге
            или&nbsp;другом деле героя аудитории проекта.</p>
        </article>
        <article class="card">
          <h3 class="card__title">Участие в печатных выпусках</h3>
          <p class="card__text">История героя может войти в&nbsp;тематический выпуск проекта
            и&nbsp;печатный зин.</p>
        </article>
        <article class="card card--accent">
          <h3 class="card__title">Новые знакомства и коллаборации</h3>
          <p class="card__text">Возможность познакомиться с&nbsp;другими героями, авторами
            и&nbsp;партнёрами проекта.</p>
        </article>
      </div>

      <div class="paper paper--wide">
        <span class="paper__label">Важно</span>
        <p>Мы не&nbsp;берём с&nbsp;героев плату за&nbsp;участие и&nbsp;не&nbsp;получаем процент
           от&nbsp;их продаж, заказов или&nbsp;других результатов публикации.</p>
      </div>
    </div>
  </section>

  <!-- ── Почему это важно ── -->
  <section class="section section--deep">
    <div class="container">
      {head_block('Смысл', '04 / 09')}

      <div class="grid grid--sidebar">
        <div class="prose">
          <h2 class="h2">Почему это важно</h2>
          <p class="lead">
            О&nbsp;регионе часто рассказывают через места: что посмотреть, куда сходить
            и&nbsp;где остановиться. «Друг» смотрит на&nbsp;территорию иначе — через людей,
            которые в&nbsp;ней живут, работают и&nbsp;создают что-то важное для&nbsp;себя
            и&nbsp;окружающих.
          </p>
          <p class="text">
            Мы делаем эти истории доступными тем, кто живёт далеко от&nbsp;героя, и&nbsp;создаём
            возможность для&nbsp;новых знакомств, поездок и&nbsp;сотрудничества.
          </p>
        </div>

        <div class="quote-block">
          <p class="quote-block__lines">
            История мастера помогает узнать о&nbsp;ремесле.<br>
            История художника — увидеть локальную культуру.<br>
            История предпринимателя — понять, как устроена жизнь территории.<br>
            История хранителя традиции — сохранить знание, которое может исчезнуть.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- ── Карта ── -->
  <section class="section" id="expeditions">
    <div class="container">
      {head_block('География', '05 / 09', 'Экспедиции',
                  'В 2026–2027 годах «Друг» отправляется в&nbsp;разные регионы России, '
                  'чтобы собрать истории людей и&nbsp;локальных сообществ.')}

      <div class="grid grid--sidebar map-layout">
        <div class="map" data-map data-map-mode="link"></div>
        <ul class="region-list" data-map-list></ul>
      </div>

      <p class="section__note">География будет расширяться.</p>
    </div>
  </section>

  <!-- ── Последний выпуск ── -->
  <section class="section section--deep">
    <div class="container">
      {head_block('Журнал', '06 / 09')}
      <div class="latest reveal" data-latest-issue></div>
    </div>
  </section>

  <!-- ── Два способа участвовать ── -->
  <section class="section" id="join">
    <div class="container">
      {head_block('Участие', '07 / 09', 'Два способа стать частью проекта')}

      <article class="invite reveal">
        <div class="ph ph--4x3 invite__media">
          {img('', 'altay-11', 'Житель Республики Алтай на лесной дороге',
               sizes='(max-width: 860px) 92vw, 46vw')}
        </div>

        <div class="invite__body">
          <span class="invite__kind">Героям</span>
          <h3 class="h2 invite__title">Расскажите свою историю</h3>
          <p class="text">
            Мы рассказываем о&nbsp;людях, которые своим делом формируют жизнь территории.
            Публичность и&nbsp;опыт интервью не&nbsp;нужны, важно само дело и&nbsp;ваша
            готовность о&nbsp;нём говорить.
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

  <!-- ── Что остаётся после экспедиции ── -->
  <section class="section section--deep">
    <div class="container">
      {head_block('Итог', '08 / 09', 'Что остаётся после экспедиции')}

      <div class="grid grid--5">
        <article class="card">
          <h3 class="card__title">Истории</h3>
          <p class="card__text">Документальные интервью с&nbsp;жителями региона.</p>
        </article>
        <article class="card">
          <h3 class="card__title">Фотографии</h3>
          <p class="card__text">Документальная съёмка людей и&nbsp;среды.</p>
        </article>
        <article class="card">
          <h3 class="card__title">Видео</h3>
          <p class="card__text">Короткие документальные материалы.</p>
        </article>
        <article class="card">
          <h3 class="card__title">Цифровой выпуск</h3>
          <p class="card__text">Собранные и&nbsp;отредактированные истории региона.</p>
        </article>
        <article class="card card--accent">
          <h3 class="card__title">Печатный зин</h3>
          <p class="card__text">Материальное издание с&nbsp;историями героев.</p>
        </article>
      </div>
    </div>
  </section>

  <!-- ── Вопросы и Telegram ── -->
  <section class="section">
    <div class="container">
      {head_block('Вопросы', '09 / 09', 'Что спрашивают чаще всего')}

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
          <div class="faq__a"><p class="text">Молодые авторы, которые живут в одном из семи регионов
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
          <p>Методика в виде гайда, чек-листов и банка вопросов. Семь цифровых выпусков,
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
    description='Семь цифровых выпусков журнала, по одному на регион. Каждый выпуск собран '
                'как номер журнала с композицией, а не как лента постов.',
    active='issues.html',
    body=f'''
  <section class="section pagehead">
    <div class="container">
      <span class="eyebrow">ДРУГ <span class="eyebrow__rest">Журнал</span></span>
      <h1 class="h1 pagehead__title">Цифровые выпуски</h1>
      <p class="lead pagehead__lead">
        Семь выпусков, по одному на регион. Такое количество выбрано не случайно: оно позволяет
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

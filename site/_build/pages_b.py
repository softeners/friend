# -*- coding: utf-8 -*-
"""
Экспедиции, формы, издания, сотрудничество, ход проекта, вопросы, контакты.

Содержание разделов взято из документа о проекте: логика проекта,
структура курса, механика доступа, устойчивость и монетизация.
"""

from shell import page, tg_block, head_block, EMAIL, PHONE, PHONE_HREF, TELEGRAM, VK

PHOTO = 'assets/img/photo'


def img(slug, alt, sizes='100vw', big=False):
    p = f'{PHOTO}/{slug}'
    srcset = (f'{p}-600.webp 600w, {p}-1200.webp 1200w, {p}-2000.webp 2000w' if big
              else f'{p}-600.webp 600w, {p}-1200.webp 1200w')
    return (f'<picture>\n'
            f'      <source type="image/webp" srcset="{srcset}" sizes="{sizes}">\n'
            f'      <img src="{p}-1200.jpg" alt="{alt}" loading="lazy" decoding="async">\n'
            f'    </picture>')


CONSENT_TEXT = (
    'Мы используем их только для связи по вашей заявке, никому не передаём и удаляем '
    'по первой просьбе. Подробности в '
    '<a href="privacy.html" target="_blank" rel="noopener">политике обработки '
    'персональных данных</a>.'
)


def field(name, label, *, kind='text', required=True, placeholder='', note='',
          rows=0, options=None, minlength=0, maxlength=0, extra=''):
    req = ' required' if required else ''
    star = (' <span class="field__req" aria-hidden="true">*</span>' if required
            else ' <span class="field__opt">по желанию</span>')
    ml = f' minlength="{minlength}"' if minlength else ''
    mx = f' maxlength="{maxlength}"' if maxlength else ''
    ph = f' placeholder="{placeholder}"' if placeholder else ''
    note_html = f'\n      <p class="field__note" id="{name}-note">{note}</p>' if note else ''
    described = f' aria-describedby="{name}-note {name}-err"' if note else f' aria-describedby="{name}-err"'
    counter = (f'\n      <p class="field__count" data-count-for="{name}" aria-hidden="true">'
               f'0 / {maxlength}</p>') if (maxlength and rows) else ''

    if rows:
        control = (f'<textarea class="textarea" id="{name}" name="{name}" rows="{rows}"'
                   f' data-label="это поле"{req}{ml}{mx}{ph}{described}{extra}></textarea>')
    elif options:
        opts = ''.join(f'\n        <option value="{o}">{o}</option>' for o in options)
        control = (f'<select class="select" id="{name}" name="{name}" data-label="это поле"'
                   f'{req}{described}{extra}>{opts}\n      </select>')
    else:
        control = (f'<input class="input" type="{kind}" id="{name}" name="{name}"'
                   f' data-label="это поле"{req}{ml}{mx}{ph}{described}{extra}>')

    return f'''<div class="field">
      <label class="field__label" for="{name}">{label}{star}</label>
      {control}{note_html}{counter}
      <p class="field__error" id="{name}-err" role="alert"></p>
    </div>'''


def consent_block():
    return f'''<div class="form__section">
              <div class="field">
                <label class="check">
                  <input type="checkbox" name="consent" id="consent" required
                         data-error-required="Без этого согласия мы не сможем принять заявку"
                         aria-describedby="consent-err">
                  <span>Согласен на обработку персональных данных. {CONSENT_TEXT}</span>
                </label>
                <p class="field__error" id="consent-err" role="alert"></p>
              </div>
            </div>'''


def sent_screen(form_id, title, lines):
    body = ''.join(f'\n      <p>{l}</p>' for l in lines)
    return f'''<div class="sent" data-sent="{form_id}">
    <div class="paper paper--wide">
      <span class="paper__label">Заявка принята</span>
      <p class="paper__title">{title}</p>{body}
    </div>
  </div>'''


# ═══════════════════════════════════════════════════════════════
# 1. ЭКСПЕДИЦИИ
# ═══════════════════════════════════════════════════════════════
EXPEDITION = page(
    title='Экспедиции — ДРУГ',
    description='Как попасть в экспедицию проекта «Друг»: заявка, отбор, курс из шести модулей '
                'с наставником, финальная работа и поездка в составе команды.',
    active='expedition.html',
    body=f'''
  <section class="section pagehead">
    <div class="container">
      <span class="eyebrow">ДРУГ <span class="eyebrow__rest">Экспедиции</span></span>
      <h1 class="h1 pagehead__title">Поехать в экспедицию</h1>
      <p class="lead pagehead__lead">
        Методика проекта построена так, чтобы качественное интервью мог провести человек
        без журналистского образования. Мы обучаем ей молодых авторов, а затем едем
        вместе с ними в регионы.
      </p>
      <div class="pagehead__actions">
        <a class="btn btn--paper btn--lg" href="become-participant.html">Подать заявку</a>
        <a class="btn btn--ghost btn--lg" href="#course">Программа курса</a>
      </div>
    </div>
  </section>

  <section class="section section--flush">
    <div class="container">
      <figure class="ph ph--16x9">
        {img('altay-38', 'Дорога вдоль реки в Республике Алтай', sizes='100vw', big=True)}
      </figure>
    </div>
  </section>

  <!-- ── Путь участника: настоящая последовательность, поэтому нумеруем ── -->
  <section class="section">
    <div class="container">
      {head_block('Путь', '01 / 04', 'Как проходит участие')}

      <ol class="steps">
        <li class="steps__item">
          <span class="steps__num">1</span>
          <h3 class="steps__title">Заявка</h3>
          <p class="steps__text">
            Вы заполняете анкету и рассказываете о себе, своём регионе и о том, каких героев
            видите в будущем выпуске.
          </p>
        </li>
        <li class="steps__item">
          <span class="steps__num">2</span>
          <h3 class="steps__title">Отбор</h3>
          <p class="steps__text">
            Мы читаем заявки и приглашаем на короткий разговор. Готовиться к нему не нужно,
            портфолио тоже не требуется.
          </p>
        </li>
        <li class="steps__item">
          <span class="steps__num">3</span>
          <h3 class="steps__title">Курс с наставником</h3>
          <p class="steps__text">
            Шесть модулей и финальная работа: интервью с героем или обработка материалов.
            Наставники — опытные авторы «Друг.Медиа».
          </p>
        </li>
        <li class="steps__item">
          <span class="steps__num">4</span>
          <h3 class="steps__title">Экспедиция</h3>
          <p class="steps__text">
            После защиты работы вы получаете доступ к экспедиции в команде проекта
            и вступаете в сообщество авторов.
          </p>
        </li>
      </ol>
    </div>
  </section>

  <!-- ── Курс ── -->
  <section class="section section--deep" id="course">
    <div class="container">
      {head_block('Программа', '02 / 04', 'Шесть модулей курса',
                  'Содержание курса — это методика, по которой работает редакция. '
                  'Всё изучается с нуля, предварительной подготовки не требуется.')}

      <div class="grid grid--3">
        <article class="card">
          <span class="card__num">01</span>
          <h3 class="card__title">Исследование территории</h3>
          <p class="card__text">
            Как изучить регион до поездки и найти в нём людей, о которых стоит рассказать.
          </p>
        </article>
        <article class="card">
          <span class="card__num">02</span>
          <h3 class="card__title">Подготовка экспедиции</h3>
          <p class="card__text">
            Маршрут, договорённости с героями, распределение ролей в команде и план съёмочного дня.
          </p>
        </article>
        <article class="card">
          <span class="card__num">03</span>
          <h3 class="card__title">Доверительное интервью</h3>
          <p class="card__text">
            Банк вопросов и сценарий разговора. Как построить беседу так, чтобы человек
            рассказывал, а не отвечал.
          </p>
        </article>
        <article class="card">
          <span class="card__num">04</span>
          <h3 class="card__title">Документирование</h3>
          <p class="card__text">
            Документальная фотография и видео по методике проекта, без постановки
            и туристической оптики.
          </p>
        </article>
        <article class="card">
          <span class="card__num">05</span>
          <h3 class="card__title">Редактура и архивирование</h3>
          <p class="card__text">
            Как собрать материал в историю с композицией и подготовить его для медиаархива.
          </p>
        </article>
        <article class="card card--accent">
          <span class="card__num">06</span>
          <h3 class="card__title">Публичное представление</h3>
          <p class="card__text">
            Как показать готовый материал аудитории и рассказать о герое на встрече или показе.
          </p>
        </article>
      </div>
    </div>
  </section>

  <!-- ── Кого приглашаем ── -->
  <section class="section">
    <div class="container">
      {head_block('Участники', '03 / 04')}

      <div class="grid grid--sidebar">
        <div class="prose">
          <h2 class="h2">Кого мы приглашаем</h2>
          <p class="lead">
            Молодых авторов, которые живут в одном из шести регионов маршрута и хотят
            развивать свой путь в регионе.
          </p>
          <p class="text">
            Журналистское образование не требуется. Методика проекта позволяет провести
            качественное интервью и создать достоверный материал без специальной подготовки.
            Опыт съёмки желателен, но не обязателен.
          </p>
          <p class="text">
            Организацию экспедиции берёт на себя проект. От участника нужны время
            и готовность работать в поле вместе с командой.
          </p>
        </div>

        <div class="paper paper--right">
          <span class="paper__label">Шесть регионов маршрута</span>
          <p>Новосибирская область, Республика Алтай, Шерегеш, Республика Бурятия,
             Республика Саха (Якутия), Приморский край.</p>
          <p>Если вы живёте в другом регионе, заявку всё равно можно отправить.
             География проекта будет расширяться.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ── Что даёт участие ── -->
  <section class="section section--deep">
    <div class="container">
      {head_block('Результат', '04 / 04', 'Что даёт участие')}

      <div class="grid grid--4">
        <article class="card">
          <h3 class="card__title">Метод</h3>
          <p class="card__text">
            Не посещение музея, а способ глубокого знакомства с человеком в интересующей вас сфере.
          </p>
        </article>
        <article class="card">
          <h3 class="card__title">Контакты</h3>
          <p class="card__text">
            Прямые знакомства с людьми, которые делают своё дело в вашем регионе.
          </p>
        </article>
        <article class="card">
          <h3 class="card__title">Взгляд на регион</h3>
          <p class="card__text">
            Понимание путей развития в регионе и слабых мест интересующей вас индустрии.
          </p>
        </article>
        <article class="card card--accent">
          <h3 class="card__title">Публикация</h3>
          <p class="card__text">
            Собранный вами материал выходит в цифровом выпуске и в печатном зине.
          </p>
        </article>
      </div>

      <div class="cta">
        <div class="cta__body">
          <h2 class="h2">Набор откроется 09.2027</h2>
          <p class="text">
            Сейчас мы формируем банк участников на следующий год. Если вы обучаетесь
            на 1–3 курсе бакалавриата или 1 курсе магистратуры — вы можете податься
            на участие в экспедиции. Финалистам будет доступен курс с сопровождением
            наставников. Итоги отбора будут доступны 05.2027.
          </p>
        </div>
        <a class="btn btn--paper btn--lg" href="become-participant.html">Подать заявку</a>
      </div>

      {tg_block('О новых наборах мы сообщаем в Telegram-канале.')}
    </div>
  </section>
''')


# ═══════════════════════════════════════════════════════════════
# 2. СТАТЬ ГЕРОЕМ
# ═══════════════════════════════════════════════════════════════
BECOME_HERO = page(
    title='Рассказать свою историю — ДРУГ',
    description='Форма заявки для героев проекта «Друг». Расскажите, чем занимаетесь '
                'и что делаете для места, где живёте.',
    active='become-hero.html',
    body=f'''
  <section class="section pagehead">
    <div class="container">
      <span class="eyebrow">ДРУГ <span class="eyebrow__rest">Стать героем</span></span>
      <h1 class="h1 pagehead__title">Расскажите свою историю</h1>
      <p class="lead pagehead__lead">
        Публичность не нужна, соцсети не обязательны, опыт интервью не важен.
        Важно то, что вы делаете для места, где живёте. Заполнение занимает около десяти минут.
      </p>
    </div>
  </section>

  <section class="section section--flush">
    <div class="container">
      <div class="grid grid--sidebar">
        <div>
          <form class="form" data-form="hero" data-subject="Заявка героя с сайта «ДРУГ»" novalidate>

            <div class="form__section form__section--first">
              <p class="form__legend">Кто вы и откуда</p>
              <div class="form__grid">
                <div class="form__row">
                  {field('name', 'Как вас зовут', placeholder='Имя и фамилия')}
                  {field('place', 'Регион, город или село', placeholder='Республика Алтай, село Онгудай')}
                </div>
              </div>
            </div>

            <div class="form__section">
              <p class="form__legend">О вашем деле</p>
              <p class="form__hint">
                Пишите обычными словами, как рассказали бы знакомому. Литературную форму
                мы придадим сами на этапе редактуры.
              </p>
              <div class="form__grid">
                {field('work', 'Чем вы занимаетесь и что делаете для своего места', rows=6, minlength=60,
                       placeholder='Например, держу мастерскую, где учу подростков работать с деревом')}
                {field('why', 'Почему считаете, что эту историю стоит рассказать', rows=5, minlength=40,
                       note='Нам важна личная причина, а не перечень достижений.')}
                {field('links', 'Ссылки на соцсети, сайт, портфолио', required=False,
                       placeholder='Через запятую')}
              </div>
            </div>

            <div class="form__section">
              <p class="form__legend">Фотографии</p>
              <p class="form__hint">
                От одной до трёх: вы за работой, ваше место, результат. Подойдут снимки с телефона,
                профессиональную съёмку мы проведём сами во время экспедиции.
              </p>

              <div class="field">
                <div class="upload" data-upload>
                  <input type="file" id="photos" name="photos" accept="image/jpeg,image/png,image/webp,image/heic" multiple>
                  <label class="upload__cta" for="photos">Выбрать файлы</label>
                  <span class="upload__note">или перетащите сюда. До трёх файлов, каждый до 10 МБ</span>
                  <div class="upload__list"></div>
                </div>
                <p class="field__error" role="alert"></p>
              </div>

              <div class="form__grid form__grid--after">
                {field('photo_link', 'Или ссылка на облако с фотографиями', required=False,
                       placeholder='Яндекс.Диск, Google Диск, альбом ВКонтакте',
                       note='Подойдёт, если файлы слишком тяжёлые для загрузки.')}
              </div>
            </div>

            <div class="form__section">
              <p class="form__legend">Как с вами связаться</p>
              <div class="form__grid">
                <div class="form__row">
                  {field('email', 'Почта', kind='email', placeholder='you@example.ru')}
                  {field('phone', 'Телефон или Telegram', kind='tel', placeholder='+7 900 000-00-00 или @nickname')}
                </div>
              </div>
            </div>

            {consent_block()}

            <div class="form__foot">
              <button class="btn btn--primary btn--lg" type="submit" data-submit>Отправить заявку</button>
              <p class="form__status" data-status role="status" aria-live="polite"></p>
            </div>
          </form>

          {sent_screen('hero', 'Мы получили вашу историю',
            ['Редакция разбирает заявки раз в неделю и отвечает в течение десяти рабочих дней на почту или в Telegram.',
             'Если история войдёт в ближайший маршрут, мы согласуем дату и приедем к вам. Съёмка занимает один день, интервью около трёх часов.',
             'Если по географии в этот раз не совпадёт, заявка останется в базе. Мы возвращаемся в регионы.',
             f'Если что-то изменилось или хотите дополнить заявку, напишите на <a href="mailto:{EMAIL}">{EMAIL}</a>.'])}
        </div>

        <aside class="aside">
          <div class="paper paper--right">
            <span class="paper__label">Как проходит съёмка</span>
            <p>Мы не приглашаем героя в студию, а приезжаем к нему в его среду. Готовиться
               и заучивать ответы не нужно: мы задаём вопросы, вы рассказываете.</p>
          </div>

          <div class="card">
            <h2 class="card__title">Участие бесплатное</h2>
            <p class="card__text">
              Герой ничего не платит и не получает гонорар. После публикации мы передаём все
              фотографии в высоком разрешении и присылаем печатный зин с вашей историей.
            </p>
          </div>

          <div class="card">
            <h2 class="card__title">Что это даёт</h2>
            <ul class="list list--sm">
              <li>Видимость и признание вклада в жизнь своего места</li>
              <li>Связь с другими героями проекта</li>
              <li>Продвижение вашего дела и услуг</li>
              <li>Возможные коллаборации: мастер-классы, совместные события</li>
            </ul>
          </div>
        </aside>
      </div>
    </div>
  </section>
''')


# ═══════════════════════════════════════════════════════════════
# 3. ЗАЯВКА УЧАСТНИКА ЭКСПЕДИЦИИ
# ═══════════════════════════════════════════════════════════════
STATUS_OPTIONS = [
    'Школьник или школьница',
    'Обучаюсь в профессиональном учреждении',
    'Обучаюсь в высшем учебном заведении',
    'Аспирантура',
    'Завершил обучение в этом году',
]

BECOME_PARTICIPANT = page(
    title='Заявка в экспедицию — ДРУГ',
    description='Анкета участника экспедиции проекта «Друг» для молодых авторов '
                'из шести регионов маршрута.',
    active='expedition.html',
    body=f'''
  <section class="section pagehead">
    <div class="container">
      <span class="eyebrow">ДРУГ <span class="eyebrow__rest">Заявка в экспедицию</span></span>
      <h1 class="h1 pagehead__title">Расскажите о себе</h1>
      <p class="lead pagehead__lead">
        Мы смотрим не на готовые работы, а на то, как вы думаете и как разговариваете с людьми.
        Три развёрнутых вопроса в конце анкеты важнее всего остального.
      </p>
      <p class="pagehead__back">
        Ещё не читали, как устроено участие? <a href="expedition.html">Начните отсюда</a>.
      </p>
    </div>
  </section>

  <section class="section section--flush">
    <div class="container">
      <div class="grid grid--sidebar">
        <div>
          <form class="form" data-form="participant" data-subject="Заявка в экспедицию с сайта «ДРУГ»" novalidate>

            <div class="form__section form__section--first">
              <p class="form__legend">Кто вы</p>
              <div class="form__grid">
                {field('name', 'Фамилия, имя и отчество', placeholder='Полностью')}
                <div class="form__row">
                  {field('email', 'Почта', kind='email', placeholder='you@example.ru')}
                  {field('social', 'Ссылка на соцсети', kind='url',
                         placeholder='vk.com/… или t.me/…',
                         note='Подойдёт любая страница, по которой можно составить о вас представление.')}
                </div>
                {field('age', 'Сколько вам лет', kind='number', placeholder='18',
                       extra=' min="14" max="35" data-age',
                       note='Если вам ещё нет восемнадцати, ниже появится блок для согласия законного представителя.')}
              </div>
            </div>

            <div class="form__section">
              <p class="form__legend">Где вы учитесь</p>
              <div class="form__grid">
                {field('status', 'Статус участника', options=STATUS_OPTIONS)}
                {field('school', 'Учебное заведение', placeholder='Полное название',
                       note='Школа, колледж, техникум или вуз.')}
                {field('speciality', 'Наименование специальности', placeholder='Например, прикладная информатика')}
              </div>
            </div>

            <div class="form__section">
              <p class="form__legend">Регион проживания</p>
              <p class="form__hint">
                В экспедицию по региону едут те, кто в этом регионе живёт. Так работает наш метод:
                своих героев участники находят через личные связи.
              </p>
              <div class="form__grid">
                <div class="field">
                  <label class="field__label" for="region">Регион проживания <span class="field__req" aria-hidden="true">*</span></label>
                  <select class="select" id="region" name="region" required data-label="регион"
                          data-region-select aria-describedby="region-note region-err"></select>
                  <p class="field__note" id="region-note">
                    Если вы живёте в другом регионе, выберите «Другой регион» и всё равно отправьте
                    заявку. География проекта будет расширяться.
                  </p>
                  <p class="field__error" id="region-err" role="alert"></p>
                </div>
              </div>
            </div>

            <div class="form__section">
              <p class="form__legend">Три вопроса</p>
              <p class="form__hint">
                Отвечайте своими словами. Нам важно понять, как вы думаете, поэтому текст,
                написанный нейросетью, здесь не поможет.
              </p>
              <div class="form__grid">
                {field('why', 'Почему вы хотите участвовать в экспедиции', rows=8,
                       minlength=100, maxlength=3000)}
                {field('experience', 'Был ли у вас опыт видеосъёмок, фотосъёмок, сбора интервью',
                       rows=5, minlength=20, maxlength=1000,
                       note='Опыт не обязателен. Если его нет, так и напишите.')}
                {field('heroes', 'Каких героев своего региона вы видите в этом выпуске',
                       rows=5, minlength=40, maxlength=1000,
                       note='Можно назвать конкретных людей или описать тип истории, который вам интересен.')}
              </div>
            </div>

            <div class="form__section">
              <div class="guardian">
                <p class="form__legend">Согласие законного представителя</p>
                <p class="form__hint">
                  Вам ещё нет восемнадцати лет, поэтому заявку должен подтвердить родитель
                  или опекун. Это значит, что взрослый знает о заявке, согласен на обработку
                  ваших персональных данных и на участие в поездке. Перед экспедицией
                  мы свяжемся с ним отдельно.
                </p>
                <div class="form__grid">
                  {field('guardian_name', 'ФИО родителя или опекуна', placeholder='Полностью')}
                  {field('guardian_contact', 'Его телефон или почта', placeholder='+7 900 000-00-00')}
                  <div class="field">
                    <label class="check">
                      <input type="checkbox" name="guardian_consent" id="guardian_consent" required
                             data-error-required="Без согласия законного представителя заявку от несовершеннолетнего принять нельзя"
                             aria-describedby="guardian_consent-err">
                      <span>Родитель или опекун знает о заявке и даёт согласие на обработку
                            персональных данных несовершеннолетнего и на его участие в проекте.</span>
                    </label>
                    <p class="field__error" id="guardian_consent-err" role="alert"></p>
                  </div>
                </div>
              </div>
            </div>

            {consent_block()}

            <div class="form__foot">
              <button class="btn btn--paper btn--lg" type="submit" data-submit>Отправить заявку</button>
              <p class="form__status" data-status role="status" aria-live="polite"></p>
            </div>
          </form>

          {sent_screen('participant', 'Заявка принята',
            ['Мы читаем анкеты в течение двух недель и отвечаем каждому, даже если в этот набор пригласить не получится.',
             'Следующий шаг — короткий разговор в Telegram или по видеосвязи. Готовиться к нему не нужно.',
             'Затем начинается курс с наставником и финальная работа, после защиты которой вы получаете доступ к экспедиции.',
             'Если вам ещё нет восемнадцати, до поездки мы свяжемся с вашим родителем или опекуном.'])}
        </div>

        <aside class="aside">
          <div class="paper paper--right">
            <span class="paper__label">Что мы оцениваем</span>
            <p>Не харизму и не портфолио. Нам важно, умеете ли вы слушать человека
               и интересно ли вам то, чем он занимается.</p>
          </div>

          <div class="card">
            <h2 class="card__title">Только шесть регионов</h2>
            <p class="card__text">
              Новосибирская область, Республика Алтай, Шерегеш, Бурятия, Якутия
              и Приморский край. В экспедицию едут те, кто здесь живёт.
            </p>
          </div>

          <div class="card">
            <h2 class="card__title">Организацию берёт на себя проект</h2>
            <p class="card__text">
              От участника нужны время и готовность работать в поле вместе с командой.
            </p>
          </div>
        </aside>
      </div>
    </div>
  </section>
''')


# ═══════════════════════════════════════════════════════════════
# 4. ПЕЧАТНЫЕ ИЗДАНИЯ
# ═══════════════════════════════════════════════════════════════
ZINES = page(
    title='Печатные издания — ДРУГ',
    description='Пилотный зин проекта «Друг» — компиляция материалов шести регионов. '
                'Печатный артефакт, который работает и на героя, и на аудиторию.',
    active='zines.html',
    body=f'''
  <section class="section pagehead">
    <div class="container">
      <span class="eyebrow">ДРУГ <span class="eyebrow__rest">Печатные издания</span></span>
      <h1 class="h1 pagehead__title">Зин</h1>
      <p class="lead pagehead__lead">
        Зин — это друг, который приглашает тебя в гости и из первых уст рассказывает о регионе.
      </p>
      <p class="lead pagehead__lead">
        Цифровые материалы масштабируемы, но полный уход в цифру уводит фокус от материального
        мира и от контакта человека с человеком. Поэтому бумага для нас принципиальна.
      </p>
    </div>
  </section>

  <section class="section section--flush">
    <div class="container">
      <div class="grid grid--2" data-zines></div>
    </div>
  </section>

  <section class="section section--deep" id="order">
    <div class="container">
      {head_block('Заказ', '01 / 01', 'Оформить заказ',
                  'Заполните форму, и мы покажем реквизиты для оплаты. После поступления оплаты '
                  'отправляем заказ в течение трёх рабочих дней.')}

      <div class="grid grid--sidebar">
        <div>
          <form class="form" data-form="order" data-subject="Заказ зина с сайта «ДРУГ»" novalidate>

            <div class="form__section form__section--first">
              <div class="form__grid">
                <div class="field">
                  <label class="field__label" for="zine">Что заказываете <span class="field__req" aria-hidden="true">*</span></label>
                  <select class="select" id="zine" name="zine" required data-label="издание"
                          data-zine-select aria-describedby="zine-err"></select>
                  <p class="field__error" id="zine-err" role="alert"></p>
                </div>

                <div class="form__row">
                  {field('qty', 'Количество экземпляров', kind='number', extra=' min="1" max="20" value="1"')}
                  {field('name', 'Имя и фамилия', placeholder='Для получения на почте')}
                </div>

                {field('address', 'Адрес доставки', rows=3,
                       placeholder='Индекс, город, улица, дом, квартира',
                       note='Отправляем Почтой России и СДЭК. По Сибири доставка обычно занимает от трёх до семи дней, в европейскую часть до двух недель.')}

                <div class="form__row">
                  {field('email', 'Почта', kind='email', placeholder='you@example.ru')}
                  {field('phone', 'Телефон', kind='tel', placeholder='+7 900 000-00-00',
                         note='Нужен службе доставки.')}
                </div>

                {field('comment', 'Комментарий к заказу', rows=3, required=False,
                       placeholder='Например, подписать зин или отправить в пункт выдачи')}
              </div>
            </div>

            {consent_block()}

            <div class="form__foot">
              <button class="btn btn--primary btn--lg" type="submit" data-submit>Оформить заказ</button>
              <p class="form__status" data-status role="status" aria-live="polite"></p>
            </div>
          </form>

          <div class="sent" data-sent="order">
            <div class="paper paper--wide">
              <span class="paper__label">Заказ принят</span>
              <p class="paper__title">Осталось оплатить</p>
              <p>Переведите сумму заказа по реквизитам ниже и укажите в комментарии к переводу
                 свою фамилию, чтобы мы могли сопоставить платёж с заказом.</p>
              <p><strong>Перевод по номеру телефона</strong><br>
                 {PHONE}, Сычева Алина Артемовна</p>
              <p>
                 <!-- TODO: заменить на ссылку оплаты, когда будет подключена платёжная система -->
                 Как только оплата поступит, мы напишем на указанную почту и отправим заказ
                 в течение трёх рабочих дней. Трек-номер придёт туда же.</p>
              <p>Если что-то пошло не так, напишите на
                 <a href="mailto:{EMAIL}">{EMAIL}</a>, и мы разберёмся.</p>
            </div>
          </div>
        </div>

        <aside class="aside">
          <div class="paper paper--right">
            <span class="paper__label">Почему бумага</span>
            <p>История требует композиции. Лента даёт только фрагменты, а печатный артефакт
               становится материальным доказательством важности истории.</p>
          </div>

          <div class="card">
            <h2 class="card__title">Оплата и доставка</h2>
            <ul class="list list--sm">
              <li>Оплата переводом по номеру телефона, реквизиты показываем после оформления</li>
              <li>Отправка в течение трёх рабочих дней после поступления оплаты</li>
              <li>Почта России и СДЭК, трек-номер присылаем на почту</li>
              <li>Если издание закончилось, мы сообщим об этом и вернём деньги</li>
            </ul>
          </div>
        </aside>
      </div>
    </div>
  </section>
''')


# ═══════════════════════════════════════════════════════════════
# 5. СОТРУДНИЧЕСТВО
# ═══════════════════════════════════════════════════════════════
SUBJ_NKO = 'Сотрудничество%3A%20институция%20или%20фонд'
SUBJ_BIZ = 'Сотрудничество%3A%20бизнес'

PARTNERS = page(
    title='Сотрудничество — ДРУГ',
    description='Партнёрство с проектом «Друг» для институций и фондов и отдельно для бизнеса '
                'в регионах: совместные события, доступ к архиву, спецвыпуски, лицензирование съёмки.',
    active='partners.html',
    body=f'''
  <section class="section pagehead">
    <div class="container">
      <span class="eyebrow">ДРУГ <span class="eyebrow__rest">Сотрудничество</span></span>
      <h1 class="h1 pagehead__title">С кем мы работаем</h1>
      <p class="lead pagehead__lead">
        Институциям и бизнесу мы предлагаем разное, поэтому разделили страницу на две части.
        Выберите подходящий случай, там же есть кнопка написать нам с готовой темой письма.
      </p>
    </div>
  </section>

  <section class="section section--flush">
    <div class="container">
      <div class="grid grid--2">
        <article class="card">
          <div class="offer">
            <span class="offer__kind">Институции, фонды, музеи, библиотеки</span>
            <h2 class="h3">Культурным организациям</h2>
            <p class="card__text">
              Проект мягко скрепляет образ регионов и общероссийскую идентичность через живое
              культурное наследие. Совместная работа может выглядеть так:
            </p>
            <ul class="list list--sm">
              <li>Публичные события: показы, разборы выпусков, встречи с героями</li>
              <li>Доступ к медиаархиву для образовательных программ</li>
              <li>Партнёрство по конкретному региону и помощь в поиске героев</li>
              <li>Совместная подача на гранты и программы поддержки</li>
            </ul>
            <a class="btn btn--primary" href="mailto:{EMAIL}?subject={SUBJ_NKO}">Написать о партнёрстве</a>
          </div>
        </article>

        <article class="card card--accent">
          <div class="offer">
            <span class="offer__kind">Туроператоры и локальный бизнес</span>
            <h2 class="h3">Бизнесу в регионах</h2>
            <p class="card__text">
              Мы работаем с теми, кто связан с территорией. Возможные форматы:
            </p>
            <ul class="list list--sm">
              <li>Спецвыпуски о регионе или направлении по редакционному стандарту проекта</li>
              <li>Лицензирование фотографий и видео из архива для промоматериалов</li>
              <li>Брендированное партнёрство с упоминанием в выпуске, канале и на сайте</li>
              <li>Софинансирование регионального зина</li>
            </ul>
            <a class="btn btn--paper" href="mailto:{EMAIL}?subject={SUBJ_BIZ}">Обсудить условия</a>
          </div>
        </article>
      </div>
    </div>
  </section>

  <section class="section section--deep">
    <div class="container">
      {head_block('Правила', '01 / 01', 'О чём мы договариваемся сразу')}

      <div class="grid grid--sidebar">
        <ul class="list list--loose">
          <li>Партнёрство не влияет на содержание историй. Редакционные решения остаются за редакцией.</li>
          <li>Спецвыпуск маркируется как партнёрский, чтобы читатель видел, кто его поддержал.</li>
          <li>Лицензия на фотографии и видео оформляется письменно, со сроком, перечнем площадок
              и территорией использования.</li>
          <li>Материалы с героями используются только с их согласия, независимо от договорённостей
              с партнёром.</li>
        </ul>

        <div class="paper paper--right">
          <span class="paper__label">Как ускорить ответ</span>
          <p>Напишите сразу, какой регион вам интересен и в каком формате вы видите сотрудничество.
             Мы отвечаем в течение недели и предлагаем короткий созвон.</p>
        </div>
      </div>
    </div>
  </section>
''')


# ═══════════════════════════════════════════════════════════════
# 6. ХОД ПРОЕКТА
# ═══════════════════════════════════════════════════════════════
NEWS = page(
    title='Ход проекта — ДРУГ',
    description='На каком этапе находится проект «Друг» и что уже сделано.',
    active='',
    body=f'''
  <section class="section pagehead">
    <div class="container">
      <span class="eyebrow">ДРУГ <span class="eyebrow__rest">Ход проекта</span></span>
      <h1 class="h1 pagehead__title">На каком мы этапе</h1>
      <p class="lead pagehead__lead">
        Проект находится на стадии реализации первого этапа. Здесь мы отмечаем ключевые шаги,
        а подробности и кадры с маршрута публикуем в Telegram-канале.
      </p>
    </div>
  </section>

  <section class="section section--flush">
    <div class="container">
      <div class="news">
        <article class="news__item">
          <div class="news__date">Подготовка</div>
          <div class="news__body">
            <h2 class="news__title">Разработаны концепция и методика</h2>
            <p class="text">
              Готовы полная концепция проекта, методика работы с героем, бюджет и календарный
              план. Проведён анализ аналогов, в том числе проектов, которые работали в этой нише
              и прекратили существование.
            </p>
          </div>
        </article>

        <article class="news__item">
          <div class="news__date">Первый этап</div>
          <div class="news__body">
            <h2 class="news__title">Экспедиции в шесть регионов</h2>
            <p class="text">
              Основная экспедиционная цепочка проходит через Новосибирскую область,
              Республику Алтай, Бурятию, Якутию и Приморский край. Отдельным зимним выездом
              запланирован Шерегеш.
            </p>
          </div>
        </article>

        <article class="news__item">
          <div class="news__date">Итог первого этапа</div>
          <div class="news__body">
            <h2 class="news__title">Шесть выпусков, зин и архив</h2>
            <p class="text">
              К концу этапа будут готовы методика в виде гайда, чек-листов и банка
              вопросов, шесть цифровых выпусков, пилотный зин, медиаархив и этот
              сайт-платформа.
            </p>
          </div>
        </article>
      </div>

      <!-- TODO: новые записи добавлять сверху таким же блоком .news__item -->

      {tg_block('Обновления с маршрута выходят в канале в тот же день.')}
    </div>
  </section>
''')


# ═══════════════════════════════════════════════════════════════
# 7. ВОПРОС-ОТВЕТ
# ═══════════════════════════════════════════════════════════════
def faq_page():
    from faq_data import FAQ_ITEMS
    items = ''.join(f'''
        <details class="faq__item">
          <summary class="faq__q">{q}<span class="faq__sign" aria-hidden="true"></span></summary>
          <div class="faq__a"><p class="text">{a}</p></div>
        </details>''' for q, a in FAQ_ITEMS)

    return page(
        title='Вопрос-ответ — ДРУГ',
        description='Как стать героем проекта «Друг», что получает герой, как попасть '
                    'в экспедицию, как заказать зин и на каких условиях доступен архив.',
        active='faq.html',
        body=f'''
  <section class="section pagehead">
    <div class="container">
      <span class="eyebrow">ДРУГ <span class="eyebrow__rest">Вопрос-ответ</span></span>
      <h1 class="h1 pagehead__title">Что обычно спрашивают</h1>
      <p class="lead pagehead__lead">
        Мы собрали вопросы, которые лучше закрыть заранее. Если вашего здесь нет,
        напишите на <a href="mailto:{EMAIL}" class="accent">{EMAIL}</a>. Мы ответим
        и дополним эту страницу.
      </p>
    </div>
  </section>

  <section class="section section--flush">
    <div class="container">
      <div class="faq">{items}
      </div>

      {tg_block()}
    </div>
  </section>
''')


# ═══════════════════════════════════════════════════════════════
# 8. КОНТАКТЫ
# ═══════════════════════════════════════════════════════════════
CONTACTS = page(
    title='Контакты — ДРУГ',
    description=f'Связаться с проектом «Друг». Почта {EMAIL}, телефон {PHONE}, '
                f'Telegram-канал и сообщество ВКонтакте.',
    active='contacts.html',
    body=f'''
  <section class="section pagehead">
    <div class="container">
      <span class="eyebrow">ДРУГ <span class="eyebrow__rest">Контакты</span></span>
      <h1 class="h1 pagehead__title">Связаться с нами</h1>
      <p class="lead pagehead__lead">Мы отвечаем в течение недели. Быстрее всего в Telegram.</p>
    </div>
  </section>

  <section class="section section--flush">
    <div class="container">
      <div class="contact-grid">
        <a class="contact-card" href="mailto:{EMAIL}">
          <span class="contact-card__kind">Почта</span>
          <span class="contact-card__value">{EMAIL}</span>
          <span class="contact-card__note">Заявки, партнёрство и запросы на материалы архива</span>
        </a>

        <a class="contact-card" href="{TELEGRAM}" target="_blank" rel="noopener">
          <span class="contact-card__kind">Telegram</span>
          <span class="contact-card__value">Канал проекта</span>
          <span class="contact-card__note">Обновления с маршрута и анонсы выпусков</span>
        </a>

        <a class="contact-card" href="{VK}" target="_blank" rel="noopener">
          <span class="contact-card__kind">ВКонтакте</span>
          <span class="contact-card__value">Сообщество</span>
          <span class="contact-card__note">То же самое для тех, кому удобнее эта площадка</span>
        </a>

        <a class="contact-card" href="tel:{PHONE_HREF}">
          <span class="contact-card__kind">Телефон</span>
          <span class="contact-card__value">{PHONE}</span>
          <span class="contact-card__note">Сычева Алина Артемовна, руководитель проекта</span>
        </a>

        <a class="contact-card contact-card--accent" href="become-hero.html">
          <span class="contact-card__kind">Хотите стать героем</span>
          <span class="contact-card__value">Рассказать свою историю</span>
          <span class="contact-card__note">Форма занимает около десяти минут</span>
        </a>

        <a class="contact-card contact-card--accent" href="expedition.html">
          <span class="contact-card__kind">Хотите в экспедицию</span>
          <span class="contact-card__value">Поехать с нами</span>
          <span class="contact-card__note">Для молодых авторов из шести регионов маршрута</span>
        </a>
      </div>
    </div>
  </section>
''')

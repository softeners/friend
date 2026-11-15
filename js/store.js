/* ═══════════════════════════════════════════════════════════
   ДРУГ — хранилище заявок и статей (демо-версия)

   Сервера пока нет: всё лежит в localStorage этого браузера.
   Позже этот файл заменяется на запросы к Directus (Timeweb) —
   остальной код сайта и админки работает только через функции
   ниже и ничего не знает о том, где лежат данные. Поэтому все
   функции асинхронные, как будут асинхронными запросы к серверу.

   Заявка:  { id, createdAt, status: 'new' | 'approved',
              name, place, work, why, links, photos: [src],
              photo_link, email, phone, age, guardian_name, guardian_contact }
   Статья:  { id, status: 'draft' | 'published', createdAt, updatedAt,
              title, cover, lead, region, type, formats: [],
              date: 'ГГГГ-ММ-ДД', blocks: [блок] }
   Блок:    { t: 'p', text } | { t: 'h', text } | { t: 'quote', text, author }
            | { t: 'photo', src, caption }

   Картинки (src, cover) — либо data:-строка (загружено в браузере),
   либо путь от корня сайта, например 'zines/sysert/pages/cover.webp'.
   ═══════════════════════════════════════════════════════════ */

const KEY = 'drug.demo.v2';

/* ── Демо-данные ───────────────────────────────────────────── */
function daysAgo(n, h = 12) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  d.setHours(h, 20, 0, 0);
  return d.toISOString();
}

function demoData() {
  return {
    requests: [
      {
        id: 'demo-r1', status: 'new', createdAt: daysAgo(1, 18),
        name: 'Мария Колесникова',
        place: 'Республика Алтай, село Чемал',
        work: 'Держу маленькую войлочную мастерскую. Валяем из шерсти местных овец ковры, '
          + 'тапочки и игрушки, по выходным учу детей из села. Шерсть беру у соседей-скотоводов, '
          + 'краски делаем сами из трав и коры.',
        why: 'Шерсть у нас раньше просто выбрасывали. Хочу показать, что ремесло может кормить '
          + 'семью и держать молодых в селе.',
        links: 'vk.com/chemal_voilok, t.me/chemal_voilok',
        photos: ['assets/img/photo/altay-55-600.webp', 'assets/img/photo/altay-37-600.webp'],
        photo_link: 'https://disk.yandex.ru/d/demo-chemal',
        email: 'maria.voilok@example.ru',
        phone: '+7 913 000-12-34'
      },
      {
        id: 'demo-r2', status: 'new', createdAt: daysAgo(3, 10),
        name: 'Арсений Чалчиков',
        place: 'Республика Алтай, Онгудай',
        work: 'Восстанавливаю старые мотоциклы и учу этому подростков из Онгудая. '
          + 'В гараже собираем «Уралы» и «Восходы» из того, что находим по дворам.',
        why: 'Ребятам здесь некуда пойти после школы. Гараж стал местом, где они '
          + 'чувствуют себя нужными.',
        links: '',
        photos: ['assets/img/photo/altay-11-600.webp'],
        photo_link: '',
        email: 'arseniy.garage@example.ru',
        phone: '@ongudai_garage'
      },
      {
        id: 'demo-r3', status: 'approved', createdAt: daysAgo(9, 14),
        name: 'Людмила Деменьшина',
        place: 'Свердловская область, Сысерть',
        work: 'Сорок лет работаю отливщицей на Сысертском фарфоровом заводе. '
          + 'Пришла в 1979 году, видела цеха, где работало восемьсот человек.',
        why: 'Завод — это дом родной. Хочется, чтобы люди знали, какой он был, '
          + 'пока ещё живы те, кто помнит.',
        links: '',
        photos: ['zines/sysert/pages/s03_R.webp'],
        photo_link: '',
        email: 'demenshina@example.ru',
        phone: '+7 922 000-56-78'
      }
    ],
    articles: [
      {
        id: 'demo-sysert', status: 'published',
        createdAt: daysAgo(20), updatedAt: daysAgo(20),
        title: 'Сысерть. Город двух заводов',
        cover: 'zines/sysert/pages/cover.webp',
        lead: 'Фарфоровый и железоделательный: как два завода собрали город вокруг себя '
          + 'и что от них осталось. Прогулка по Сысерти с местными.',
        region: 'sysert',
        type: 'text',
        formats: ['photo'],
        date: '2026-05-15',
        blocks: [
          { t: 'p', text: 'Фарфоровый завод — это сердце города. Его гордость и боль. '
            + 'Когда-то в этих цехах кипела жизнь: триста художников расписывали сервизы и статуэтки. '
            + 'Сейчас на заводе работает около пятидесяти человек.' },
          { t: 'quote', text: 'На этом заводе в самые лучшие годы работало от 700 до 800 человек.',
            author: 'Андрей Бородулин, потомок основателей завода' },
          { t: 'photo', src: 'zines/sysert/pages/s03_L.webp', caption: 'Цех Сысертского фарфорового завода' },
          { t: 'h', text: 'Дом' },
          { t: 'p', text: 'Людмила Деменьшина пришла на завод отливщицей в 1979 году '
            + 'и осталась на всю жизнь.' },
          { t: 'quote', text: 'Это как дом родной. Дом родной, мне кажется, на втором месте, '
            + 'а это на первом месте.', author: 'Людмила Деменьшина, отливщица' },
          { t: 'h', text: 'Работа' },
          { t: 'p', text: 'Глина проходила через снабженца, лаборанта, технолога, модельщика, '
            + 'скульптора, литейщика, отливщика, глазуровщицу, живописца, художника, '
            + 'обжигальщика и контролёра ОТК, чтобы стать сервизом.' },
          { t: 'photo', src: 'zines/sysert/pages/s03_R.webp', caption: 'Разворот зина «Друг. Сысерть»' }
        ]
      }
    ]
  };
}

/* ── Чтение и запись ───────────────────────────────────────── */
function load() {
  let db = null;
  try { db = JSON.parse(localStorage.getItem(KEY)); } catch { db = null; }
  if (!db || !Array.isArray(db.requests) || !Array.isArray(db.articles)) {
    db = demoData();
    save(db);
  }
  return db;
}

function save(db) {
  try {
    localStorage.setItem(KEY, JSON.stringify(db));
  } catch (err) {
    // Чаще всего — кончилось место: в браузере на сайт около 5 МБ.
    const e = new Error('В браузере закончилось место для демо-данных. '
      + 'Удалите несколько заявок или статей с фотографиями, или сбросьте демо-данные.');
    e.code = 'quota';
    throw e;
  }
}

const uid = (p) => `${p}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`;
const clone = (x) => JSON.parse(JSON.stringify(x));

/* ── Заявки ────────────────────────────────────────────────── */
export async function getRequests() {
  return clone(load().requests).sort((a, b) => b.createdAt.localeCompare(a.createdAt));
}

export async function addRequest(data) {
  const db = load();
  const req = { ...clone(data), id: uid('r'), status: 'new', createdAt: data.createdAt || new Date().toISOString() };
  db.requests.push(req);
  save(db);
  return clone(req);
}

export async function updateRequest(id, patch) {
  const db = load();
  const req = db.requests.find(r => r.id === id);
  if (!req) throw new Error('Заявка не найдена');
  Object.assign(req, clone(patch), { id });
  save(db);
  return clone(req);
}

export async function deleteRequest(id) {
  const db = load();
  db.requests = db.requests.filter(r => r.id !== id);
  save(db);
}

/* ── Статьи ────────────────────────────────────────────────── */
/** Все статьи (для админки). Для читателей: getArticles({ published: true }). */
export async function getArticles({ published = false } = {}) {
  const list = clone(load().articles);
  return (published ? list.filter(a => a.status === 'published') : list)
    .sort((a, b) => (b.date || '').localeCompare(a.date || '') || b.updatedAt.localeCompare(a.updatedAt));
}

export async function getArticle(id) {
  const a = load().articles.find(x => x.id === id);
  return a ? clone(a) : null;
}

/** Создаёт статью без id или обновляет существующую. Возвращает сохранённую. */
export async function saveArticle(article) {
  const db = load();
  const now = new Date().toISOString();
  const data = clone(article);
  let saved;
  if (data.id && db.articles.some(a => a.id === data.id)) {
    const i = db.articles.findIndex(a => a.id === data.id);
    saved = { ...db.articles[i], ...data, updatedAt: now };
    db.articles[i] = saved;
  } else {
    saved = { status: 'draft', ...data, id: uid('a'), createdAt: now, updatedAt: now };
    db.articles.push(saved);
  }
  save(db);
  return clone(saved);
}

export async function deleteArticle(id) {
  const db = load();
  db.articles = db.articles.filter(a => a.id !== id);
  save(db);
}

/** Стирает всё и возвращает демо-заявки и демо-статью. */
export async function resetDemo() {
  save(demoData());
}

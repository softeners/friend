/* ═══════════════════════════════════════════════════════════
   ДРУГ — общие утилиты интерфейса
   ═══════════════════════════════════════════════════════════ */

/** Базовый путь до корня сайта: страницы в issues/ лежат на уровень глубже. */
export const ROOT = document.documentElement.dataset.root || '';

/** Экранирование текста перед вставкой в разметку. */
export function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, c => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
}

/**
 * Разметка <picture> с webp и запасным jpeg.
 * slug — имя файла без размера, из site/assets/img/photo/
 * Если slug пустой — вернёт заглушку с подписью.
 */
export function photo(slug, alt, opts = {}) {
  const { sizes = '100vw', eager = false, cls = '', big = false } = opts;
  if (!slug) {
    return `<div class="ph__empty-inner">${esc(alt || 'Фото появится после экспедиции')}</div>`;
  }
  const p = `${ROOT}assets/img/photo/${slug}`;
  const srcset = big
    ? `${p}-600.webp 600w, ${p}-1200.webp 1200w, ${p}-2000.webp 2000w`
    : `${p}-600.webp 600w, ${p}-1200.webp 1200w`;
  return `<picture>
      <source type="image/webp" srcset="${srcset}" sizes="${sizes}">
      <img src="${p}-1200.jpg" alt="${esc(alt)}" class="${cls}"
           loading="${eager ? 'eager' : 'lazy'}" decoding="async"
           ${eager ? 'fetchpriority="high"' : ''}>
    </picture>`;
}

/**
 * Адрес картинки из хранилища (js/store.js): data:-строку и внешнюю ссылку
 * оставляем как есть, путь от корня сайта дополняем ROOT.
 */
export function imgSrc(src) {
  if (!src) return '';
  return /^(data:|blob:|https?:)/.test(src) ? src : ROOT + src;
}

const MONTHS = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
  'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь'];

/** 'ГГГГ-ММ-ДД' → 'май 2026', как в карточках архива. */
export function monthYear(iso) {
  const m = /^(\d{4})-(\d{2})/.exec(iso || '');
  return m ? `${MONTHS[Number(m[2]) - 1]} ${m[1]}` : '';
}

/** 'май 2026' или 'ГГГГ-ММ-ДД' → число для сортировки по дате. */
export function dateKey(s) {
  const iso = /^(\d{4})-(\d{2})(?:-(\d{2}))?/.exec(s || '');
  if (iso) return Number(iso[1]) * 10000 + Number(iso[2]) * 100 + Number(iso[3] || 1);
  const ru = /^([а-яё]+)\s+(\d{4})$/i.exec((s || '').trim());
  if (ru) {
    const mi = MONTHS.indexOf(ru[1].toLowerCase());
    if (mi >= 0) return Number(ru[2]) * 10000 + (mi + 1) * 100 + 1;
  }
  return 0;
}

/* ── Сжатие фото для демо-хранилища (js/store.js) ─────────────
   Длинная сторона до 1200px, JPEG — чтобы данные влезали в localStorage.
   Файл, который браузер не умеет открыть (например, HEIC), пропускаем. */
export async function compressImage(file, max = 1200) {
  const url = URL.createObjectURL(file);
  try {
    const img = await new Promise((res, rej) => {
      const i = new Image(); i.onload = () => res(i); i.onerror = rej; i.src = url;
    });
    const k = Math.min(1, max / Math.max(img.naturalWidth, img.naturalHeight));
    const c = document.createElement('canvas');
    c.width = Math.round(img.naturalWidth * k);
    c.height = Math.round(img.naturalHeight * k);
    c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
    return c.toDataURL('image/jpeg', 0.82);
  } catch {
    console.warn(`[ДРУГ] Не удалось открыть «${file.name}», фото пропущено`);
    return null;
  } finally {
    URL.revokeObjectURL(url);
  }
}

/** Значение query-параметра. */
export function param(name) {
  return new URLSearchParams(location.search).get(name);
}

/**
 * Плавное появление блоков при скролле.
 * Вызывается повторно после того, как модули дорисовали разметку:
 * блоки, добавленные позже, иначе так и остались бы прозрачными.
 */
export function initReveal() {
  const items = document.querySelectorAll('.reveal:not(.is-visible)');
  if (!items.length) return;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced || !('IntersectionObserver' in window)) {
    items.forEach(el => el.classList.add('is-visible'));
    return;
  }

  // Срабатываем с запасом до края экрана, чтобы блок успел проявиться
  // к тому моменту, когда человек до него доскроллит.
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.classList.add('is-visible');
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px 12% 0px' });

  items.forEach(el => io.observe(el));
  startSafetyNet();
}

/**
 * Страховка на случай, если наблюдатель почему-то не сработал:
 * при быстрой прокрутке, в необычном браузере, в фоновой вкладке.
 * Ничего видимого на экране не должно остаться прозрачным.
 */
let safetyOn = false;

function startSafetyNet() {
  if (safetyOn) return;
  safetyOn = true;

  const sweep = () => {
    const hidden = document.querySelectorAll('.reveal:not(.is-visible)');
    if (!hidden.length) {
      removeEventListener('scroll', onScroll);
      safetyOn = false;
      return;
    }
    hidden.forEach(el => {
      if (el.getBoundingClientRect().top < innerHeight * 1.15) el.classList.add('is-visible');
    });
  };

  let waiting = false;
  const onScroll = () => {
    if (waiting) return;
    waiting = true;
    setTimeout(() => { waiting = false; sweep(); }, 400);
  };

  setTimeout(sweep, 1200);
  addEventListener('scroll', onScroll, { passive: true });
}

/** Шапка: фон при скролле, бургер, закрытие по Esc и по клику вне. */
export function initHeader() {
  const header = document.querySelector('.header');
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('.nav');

  if (header) {
    const onScroll = () => header.classList.toggle('is-scrolled', scrollY > 20);
    onScroll();
    addEventListener('scroll', onScroll, { passive: true });
  }

  if (!burger || !nav) return;

  const close = () => {
    nav.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
  };

  burger.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', String(open));
  });

  addEventListener('keydown', (e) => {
    if (e.key !== 'Escape' || !nav.classList.contains('is-open')) return;
    close();
    burger.focus();
  });

  nav.addEventListener('click', (e) => { if (e.target.closest('a')) close(); });

  document.addEventListener('click', (e) => {
    if (!nav.classList.contains('is-open')) return;
    if (e.target.closest('.nav') || e.target.closest('.burger')) return;
    close();
  });
}

/** Текущий год в футере. */
export function initYear() {
  document.querySelectorAll('[data-year]').forEach(el => {
    el.textContent = new Date().getFullYear();
  });
}

/** Плашка cookies: показываем, пока человек не нажал «Хорошо». */
export function initCookies() {
  const bar = document.querySelector('[data-cookies]');
  if (!bar) return;
  let seen = false;
  try { seen = localStorage.getItem('drug.cookies') === 'ok'; } catch {}
  if (seen) return;
  bar.hidden = false;
  bar.querySelector('[data-cookies-ok]')?.addEventListener('click', () => {
    try { localStorage.setItem('drug.cookies', 'ok'); } catch {}
    bar.hidden = true;
  });
}

/** Кнопка «Скопировать ссылку». */
export function initCopyLink() {
  document.querySelectorAll('[data-copy-link]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const label = btn.textContent;
      try { await navigator.clipboard.writeText(location.href.split('#')[0]); btn.textContent = 'Ссылка скопирована'; }
      catch { btn.textContent = location.href; }
      setTimeout(() => { btn.textContent = label; }, 2500);
    });
  });
}

export function initCommon() {
  initHeader();
  initReveal();
  initYear();
  initCookies();
  initCopyLink();
}

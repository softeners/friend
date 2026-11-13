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

export function initCommon() {
  initHeader();
  initReveal();
  initYear();
}

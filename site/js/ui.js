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

/** Элементы, до которых можно дотабаться, внутри контейнера. */
function focusable(el) {
  return [...el.querySelectorAll('a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])')]
    .filter(e => e.offsetParent !== null || e === document.activeElement);
}

/**
 * Замыкает Tab внутри контейнера, пока он открыт.
 * Возвращает функцию, которая снимает замок.
 */
export function trapFocus(container) {
  const onKey = (e) => {
    if (e.key !== 'Tab') return;
    const items = focusable(container);
    if (!items.length) return;
    const first = items[0];
    const last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  };
  container.addEventListener('keydown', onKey);
  return () => container.removeEventListener('keydown', onKey);
}

/** Шапка: фон при скролле, бургер, закрытие по Esc и по клику вне.
 *
 *  Мобильное меню в разметке стоит ПЕРЕД бургером, поэтому само по себе
 *  оно не получает фокус при открытии, а Tab с бургера уходит в контент
 *  под меню. Поэтому фокус переносим руками, замыкаем его внутри меню,
 *  блокируем прокрутку фона и возвращаем фокус на бургер при закрытии.
 */
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

  let untrap = null;

  const open = () => {
    nav.classList.add('is-open');
    burger.setAttribute('aria-expanded', 'true');
    document.documentElement.classList.add('menu-open');
    untrap = trapFocus(nav);
    const first = focusable(nav)[0];
    if (first) first.focus();
  };

  const close = ({ restoreFocus = true } = {}) => {
    if (!nav.classList.contains('is-open')) return;
    nav.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
    document.documentElement.classList.remove('menu-open');
    if (untrap) { untrap(); untrap = null; }
    if (restoreFocus) burger.focus();
  };

  burger.addEventListener('click', () => {
    if (nav.classList.contains('is-open')) close();
    else open();
  });

  addEventListener('keydown', (e) => {
    if (e.key === 'Escape') close();
  });

  // Переход по ссылке уводит со страницы: возвращать фокус на бургер незачем
  nav.addEventListener('click', (e) => { if (e.target.closest('a')) close({ restoreFocus: false }); });

  document.addEventListener('click', (e) => {
    if (e.target.closest('.nav') || e.target.closest('.burger')) return;
    close({ restoreFocus: false });
  });

  // Меню живёт только на узких экранах. Если окно растянули при открытом
  // меню, оно должно закрыться, иначе замок фокуса останется висеть.
  const wide = matchMedia('(min-width: 961px)');
  const onWide = () => { if (wide.matches) close({ restoreFocus: false }); };
  wide.addEventListener ? wide.addEventListener('change', onWide) : wide.addListener(onWide);
}

/** Текущий год в футере. */
export function initYear() {
  document.querySelectorAll('[data-year]').forEach(el => {
    el.textContent = new Date().getFullYear();
  });
}

export function initCommon() {
  initHeader();
  initYear();
  // initReveal здесь не зовём: main.js вызывает его один раз после того,
  // как модули дорисовали разметку. Два вызова заводили два наблюдателя
  // на одних и тех же узлах.
}

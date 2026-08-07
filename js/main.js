/* ══════════════════════════════════════════════════════════
   ДРУГ — скрипты лендинга
   Без зависимостей. Каждый модуль работает автономно.
   ══════════════════════════════════════════════════════════ */

(() => {
  'use strict';

  const $  = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  /* ── 1. Шапка: фон при скролле ──────────────────────────── */
  const header = $('#header');
  const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 40);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ── 2. Мобильное меню ──────────────────────────────────── */
  const burger = $('#burger');
  const nav = $('#nav');

  burger?.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    burger.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open));
  });

  $$('.nav__link').forEach(link => link.addEventListener('click', () => {
    nav.classList.remove('is-open');
    burger.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
  }));

  /* ── 3. Подсветка активного пункта меню ─────────────────── */
  const sections = $$('main section[id], footer[id]');
  const navLinks = new Map($$('.nav__link').map(l => [l.getAttribute('href').slice(1), l]));

  const spy = new IntersectionObserver(entries => {
    entries.forEach(e => {
      const link = navLinks.get(e.target.id);
      if (link && e.isIntersecting) {
        navLinks.forEach(l => l.classList.remove('is-active'));
        link.classList.add('is-active');
      }
    });
  }, { rootMargin: '-45% 0px -50% 0px' });

  sections.forEach(s => spy.observe(s));

  /* ── 4. Появление блоков при скролле ────────────────────── */
  const revealTargets = $$('.section, .card, .person, .stat, .figure, .roadmap__step, .budget');
  revealTargets.forEach(el => el.classList.add('reveal'));

  const revealer = new IntersectionObserver((entries, obs) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.classList.add('is-visible');
      obs.unobserve(e.target);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

  revealTargets.forEach(el => revealer.observe(el));

  /* ── 5. Табы ────────────────────────────────────────────── */
  $$('[data-tabs]').forEach(root => {
    const btns = $$('.tabs__btn', root);
    const panels = $$('.tabs__panel', root);

    btns.forEach(btn => btn.addEventListener('click', () => {
      btns.forEach(b => b.classList.remove('is-active'));
      panels.forEach(p => p.classList.remove('is-active'));
      btn.classList.add('is-active');
      $('#' + btn.dataset.tab, root)?.classList.add('is-active');
    }));
  });

  /* ── 6. Аккордеон ───────────────────────────────────────── */
  $$('[data-accordion]').forEach(root => {
    const items = $$('.accordion__item', root);

    items.forEach(item => {
      $('.accordion__head', item).addEventListener('click', () => {
        const open = item.classList.contains('is-open');
        items.forEach(i => i.classList.remove('is-open'));   // убрать для мультиоткрытия
        if (!open) item.classList.add('is-open');
      });
    });
  });

  /* ── 7. Регионы: смена изображения ──────────────────────── */
  $$('[data-regions]').forEach(root => {
    const items = $$('.regions__item', root);
    const img = $('#regionImage');
    const caption = $('.figure__caption');

    items.forEach(item => item.addEventListener('mouseenter', () => {
      items.forEach(i => i.classList.remove('is-active'));
      item.classList.add('is-active');
      if (img && item.dataset.img) img.src = item.dataset.img;
      if (caption) caption.textContent = item.textContent.trim();
    }));
  });

  /* ── 8. Чипы аудитории ──────────────────────────────────── */
  $$('.chips').forEach(group => {
    const chips = $$('.chip', group);
    chips.forEach(chip => chip.addEventListener('click', () => {
      chips.forEach(c => c.classList.remove('is-active'));
      chip.classList.add('is-active');
    }));
  });

  /* ── 9. Счётчики цифр ───────────────────────────────────── */
  const counters = $$('[data-count]');

  const animateCount = el => {
    const target = Number(el.dataset.count);
    const duration = 1400;
    const start = performance.now();

    const tick = now => {
      const p = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased).toLocaleString('ru-RU');
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };

  const countObserver = new IntersectionObserver((entries, obs) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      animateCount(e.target);
      obs.unobserve(e.target);
    });
  }, { threshold: 0.5 });

  counters.forEach(el => countObserver.observe(el));

  /* ── 10. Плавный скролл с учётом шапки ──────────────────── */
  $$('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
      const id = link.getAttribute('href');
      if (id === '#' || id.length < 2) return;
      const target = $(id);
      if (!target) return;

      e.preventDefault();
      const top = target.getBoundingClientRect().top + window.scrollY - header.offsetHeight;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });

  /* ── 11. Год в футере ───────────────────────────────────── */
  const year = $('#year');
  if (year) year.textContent = new Date().getFullYear();

})();

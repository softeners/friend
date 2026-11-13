/* ═══════════════════════════════════════════════════════════
   ДРУГ — просмотр фото лонгрида на весь экран.
   Работает по data-slug на <picture>, который проставляет notes.py.
   ═══════════════════════════════════════════════════════════ */

import { photo } from './ui.js';

export function initLightbox() {
  const root = document.querySelector('.longread');
  if (!root) return;

  const overlay = document.createElement('div');
  overlay.className = 'lightbox';
  overlay.innerHTML = `
    <button class="lightbox__close" type="button" aria-label="Закрыть">&times;</button>
    <div class="lightbox__frame"></div>
  `;
  document.body.appendChild(overlay);

  const frame = overlay.querySelector('.lightbox__frame');
  const closeBtn = overlay.querySelector('.lightbox__close');
  let lastFocus = null;

  function open(slug, alt) {
    frame.innerHTML = photo(slug, alt, { sizes: '92vw', big: true, eager: true });
    overlay.classList.add('is-open');
    document.documentElement.classList.add('lightbox-open');
    lastFocus = document.activeElement;
    closeBtn.focus();
  }

  function close() {
    overlay.classList.remove('is-open');
    document.documentElement.classList.remove('lightbox-open');
    frame.innerHTML = '';
    lastFocus?.focus();
  }

  root.addEventListener('click', (e) => {
    const picture = e.target.closest('picture[data-slug]');
    if (!picture) return;
    open(picture.dataset.slug, picture.querySelector('img')?.alt || '');
  });

  closeBtn.addEventListener('click', close);
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) close();
  });
  addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && overlay.classList.contains('is-open')) close();
  });
}

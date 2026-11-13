/* ═══════════════════════════════════════════════════════════
   ДРУГ — досье героя (hero.html?slug=...)
   ═══════════════════════════════════════════════════════════ */

import { heroes, regions, issues, roleLabels } from './data.js';
import { photo, esc, param, ROOT } from './ui.js';

export function initHero() {
  const root = document.querySelector('[data-hero]');
  if (!root) return;

  const h = heroes.find(x => x.slug === param('slug')) || heroes[0];
  if (!h) return;

  const region = regions.find(r => r.slug === h.region);
  const issue = issues.find(i => i.slug === h.issue);
  document.title = `${h.name} — медиаархив «ДРУГ»`;

  const quoteBlock = h.quote
    ? `<blockquote class="quote-block reveal">
         <p class="quote">«${esc(h.quote)}»</p>
         <span class="quote__author">${esc(h.name)}, ${esc(region ? region.short : '')}</span>
       </blockquote>`
    : `<div class="paper paper--wide reveal">
         <span class="paper__label">Расшифровка</span>
         <p>Интервью записано, расшифровка в работе. Прямая речь появится здесь после того,
            как герой прочитает текст и подтвердит факты.</p>
       </div>`;

  const gallery = (h.gallery || []).map((slug, i) => `
    <figure class="gallery__item ${i === 0 ? 'gallery__item--wide' : ''}">
      <div class="ph ${i === 0 ? 'ph--16x9' : 'ph--4x3'}">
        ${photo(slug, `${h.name}, кадр ${i + 1}`, { sizes: '(max-width: 860px) 92vw, 45vw', big: i === 0 })}
      </div>
    </figure>`).join('');

  root.innerHTML = `
    <nav class="crumbs" aria-label="Хлебные крошки">
      <a href="${ROOT}archive.html">Медиаархив</a>
      <span aria-hidden="true">/</span>
      <a href="${ROOT}archive.html?region=${h.region}">${esc(region ? region.short : '')}</a>
    </nav>

    <header class="hero-doc__head">
      <div>
        <span class="eyebrow">ДРУГ <span class="eyebrow__rest">Досье</span></span>
        <h1 class="h1 hero-doc__name">${esc(h.name)}</h1>
        <p class="lead">${esc(h.lead)}</p>
        <dl class="meta">
          <div class="meta__item"><dt>Роль</dt><dd>${esc(roleLabels[h.role] || h.role)}</dd></div>
          <div class="meta__item"><dt>Регион</dt><dd>${esc(region ? region.name : '—')}</dd></div>
          <div class="meta__item"><dt>Место</dt><dd>${esc(h.place)}</dd></div>
          <div class="meta__item"><dt>Съёмка</dt><dd>${esc(region ? region.period : '—')}</dd></div>
        </dl>
      </div>
      <div class="ph ph--3x4 hero-doc__portrait">
        ${photo(h.photo, h.name, { sizes: '(max-width: 860px) 92vw, 38vw', eager: true, big: true })}
      </div>
    </header>

    ${quoteBlock}

    <section class="hero-doc__media">
      <h2 class="h2">Материалы</h2>
      <div class="media-slots">
        <div class="media-slot">
          <span class="media-slot__kind">Видео-интервью</span>
          <p class="media-slot__note">${h.formats.includes('video')
            ? 'Фрагмент интервью.' : 'Появится после монтажа выпуска.'}</p>
        </div>
        <div class="media-slot">
          <span class="media-slot__kind">Аудиофрагмент</span>
          <p class="media-slot__note">${h.formats.includes('audio')
            ? 'Запись разговора.' : 'Появится вместе с расшифровкой.'}</p>
        </div>
        <div class="media-slot is-filled">
          <span class="media-slot__kind">Фотографии</span>
          <p class="media-slot__note">${(h.gallery || []).length} кадра с экспедиции</p>
        </div>
      </div>
      <div class="gallery">${gallery}</div>
    </section>

    ${issue && issue.published ? `
      <a class="tg reveal" href="${ROOT}${issue.url}">
        <div class="tg__text">
          <p class="tg__title">Выпуск № ${esc(issue.number)}. ${esc(issue.title)}</p>
          <p class="tg__note">Полная история, в которой участвует герой</p>
        </div>
        <span class="btn btn--ghost">Читать выпуск</span>
      </a>` : ''}`;

}

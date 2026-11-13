/* ═══════════════════════════════════════════════════════════
   ДРУГ — карта экспедиций
   Один компонент на главную и на медиаархив.
   Разметка: <div class="map" data-map data-map-mode="link|filter"></div>
   ═══════════════════════════════════════════════════════════ */

import { regions } from './data.js';
import { RUSSIA_PATH, RUSSIA_VIEWBOX } from './russia.js';
import { esc, ROOT } from './ui.js';

const VB = RUSSIA_VIEWBOX.split(' ').map(Number);   // [0,0,1000,460]

function statusLabel(status) {
  return status === 'done' ? 'пройдено' : status === 'in-progress' ? 'в работе' : 'запланирована';
}

export function initMap() {
  const roots = document.querySelectorAll('[data-map]');
  if (!roots.length) return;

  roots.forEach(root => {
    const mode = root.dataset.mapMode || 'link';

    const pins = regions.map(r => {
      const left = ((r.x - VB[0]) / VB[2] * 100).toFixed(3);
      const top = ((r.y - VB[1]) / VB[3] * 100).toFixed(3);
      const cls = r.status === 'done' ? 'is-done' : r.status === 'in-progress' ? 'is-progress' : 'is-planned';
      const statusText = r.status === 'done' ? 'Экспедиция пройдена'
        : r.status === 'in-progress' ? 'Экспедиция в работе' : 'Экспедиция запланирована';
      const label = `${r.name}. ${statusText}, ${r.period}`;
      return `<button type="button"
          class="map__pin ${cls}"
          style="left:${left}%; top:${top}%"
          data-region="${r.slug}"
          aria-label="${esc(label)}">
          <span class="map__dot" aria-hidden="true"></span>
          <span class="map__tip" role="presentation">
            <span class="map__tip-name">${esc(r.name)}</span>
            <span class="map__tip-line">${esc(r.about)}</span>
            <span class="map__tip-meta">${statusLabel(r.status)} · ${esc(r.period)}</span>
          </span>
        </button>`;
    }).join('');

    root.innerHTML = `
      <div class="map__canvas">
        <svg class="map__svg" viewBox="${RUSSIA_VIEWBOX}" role="img"
             aria-label="Карта России с отметками регионов проекта" focusable="false">
          <path d="${RUSSIA_PATH}" class="map__land"/>
        </svg>
        ${pins}
      </div>
      <ul class="map__legend">
        <li><span class="map__key is-done" aria-hidden="true"></span>экспедиция пройдена</li>
        <li><span class="map__key is-progress" aria-hidden="true"></span>в работе</li>
        <li><span class="map__key is-planned" aria-hidden="true"></span>экспедиция впереди</li>
      </ul>`;

    // Дублируем точки списком: карта не должна быть единственным способом навигации
    const list = root.parentElement.querySelector('[data-map-list]');
    if (list) {
      list.innerHTML = regions.map(r => `
        <li>
          <a class="region-row" href="${ROOT}archive.html?region=${r.slug}">
            <span class="region-row__name">${esc(r.name)}</span>
            <span class="region-row__about">${esc(r.about)}</span>
            <span class="tag ${r.status === 'done' ? 'tag--done' : r.status === 'in-progress' ? 'tag--progress' : 'tag--planned'}">
              ${r.status === 'done' ? 'пройдено' : r.status === 'in-progress' ? 'в работе' : r.period}
            </span>
          </a>
        </li>`).join('');
    }

    root.addEventListener('click', (e) => {
      const pin = e.target.closest('.map__pin');
      if (!pin) return;
      const slug = pin.dataset.region;
      if (mode === 'filter') {
        root.dispatchEvent(new CustomEvent('map:select', { detail: slug, bubbles: true }));
      } else {
        location.href = `${ROOT}archive.html?region=${slug}`;
      }
    });
  });
}

/** Подсветить активный регион (используется архивом). */
export function setActiveRegion(slug) {
  document.querySelectorAll('.map__pin').forEach(p => {
    p.classList.toggle('is-active', p.dataset.region === slug);
  });
}

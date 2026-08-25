/* ═══════════════════════════════════════════════════════════
   ДРУГ — карта экспедиций
   Один компонент на главную и на медиаархив.
   Разметка: <div class="map" data-map data-map-mode="link|filter"></div>

   Три сибирских региона лежат почти в одной точке. Настоящее место
   помечаем маленьким кружком прямо на карте, а нажимаемый пин
   отводим в сторону и соединяем выноской — иначе Шерегеш накрывает
   Алтай целиком и по Алтаю нельзя попасть ни мышью, ни пальцем.
   ═══════════════════════════════════════════════════════════ */

import { regions } from './data.js';
import { RUSSIA_PATH, RUSSIA_VIEWBOX } from './russia.js';
import { esc, ROOT } from './ui.js';

const VB = RUSSIA_VIEWBOX.split(' ').map(Number);   // [0,0,1000,460]

/* Ниже этой ширины карта слишком мелкая, чтобы держать пальцевые цели:
   на 390 px между соседними точками остаётся 15 px. Пины становятся
   разметкой, а выбирают регион в списке под картой. */
const NARROW = '(max-width: 640px)';

const pct = (v, off, size) => ((v - off) / size * 100).toFixed(3);

export function initMap() {
  const roots = document.querySelectorAll('[data-map]');
  if (!roots.length) return;

  roots.forEach(root => {
    const mode = root.dataset.mapMode || 'link';

    const leaders = regions
      .filter(r => r.lx != null && r.ly != null)
      .map(r => `<line class="map__lead" x1="${r.x}" y1="${r.y}" x2="${r.lx}" y2="${r.ly}"/>
                 <circle class="map__anchor" cx="${r.x}" cy="${r.y}" r="3.4"/>`)
      .join('');

    const pins = regions.map(r => {
      const left = pct(r.lx != null ? r.lx : r.x, VB[0], VB[2]);
      const top = pct(r.ly != null ? r.ly : r.y, VB[1], VB[3]);
      const done = r.status === 'done';
      const label = `${r.name}. ${done ? 'Экспедиция пройдена' : 'Экспедиция запланирована'}, ${r.period}`;
      // В режиме фильтра пин — переключатель, и это должно быть слышно,
      // а не только видно по подсветке.
      const pressed = mode === 'filter' ? ' aria-pressed="false"' : '';
      return `<button type="button"
          class="map__pin ${done ? 'is-done' : 'is-planned'}"
          style="left:${left}%; top:${top}%"
          data-region="${esc(r.slug)}"${pressed}
          aria-label="${esc(label)}">
          <span class="map__dot" aria-hidden="true"></span>
          <span class="map__tip" role="presentation">
            <span class="map__tip-name">${esc(r.name)}</span>
            <span class="map__tip-line">${esc(r.about)}</span>
            <span class="map__tip-meta">${done ? 'пройдено' : 'запланирована'} · ${esc(r.period)}</span>
          </span>
        </button>`;
    }).join('');

    root.innerHTML = `
      <div class="map__canvas">
        <svg class="map__svg" viewBox="${RUSSIA_VIEWBOX}" role="img"
             aria-label="Карта России с отметками регионов проекта" focusable="false">
          <path d="${RUSSIA_PATH}" class="map__land"/>
          ${leaders}
        </svg>
        ${pins}
      </div>
      <p class="map__hint">Карта показывает маршрут. Регион выбирайте в списке ниже.</p>
      <ul class="map__legend">
        <li><span class="map__key is-done" aria-hidden="true"></span>экспедиция пройдена</li>
        <li><span class="map__key is-planned" aria-hidden="true"></span>экспедиция впереди</li>
      </ul>`;

    // Дублируем точки списком: карта не должна быть единственным способом навигации
    const list = root.parentElement.querySelector('[data-map-list]');
    if (list) {
      list.innerHTML = regions.map(r => `
        <li>
          <a class="region-row" href="${ROOT}archive.html?region=${encodeURIComponent(r.slug)}"
             data-region-row="${esc(r.slug)}">
            <span class="region-row__name">${esc(r.name)}</span>
            <span class="region-row__about">${esc(r.about)}</span>
            <span class="tag ${r.status === 'done' ? 'tag--done' : 'tag--planned'}">
              ${r.status === 'done' ? 'пройдено' : r.period}
            </span>
          </a>
        </li>`).join('');

      // В архиве список — такой же фильтр, как карта: перезагружать страницу
      // ради смены одного параметра незачем. Ссылка остаётся рабочей ссылкой:
      // её можно открыть в новой вкладке и поделиться ею.
      if (mode === 'filter') {
        list.addEventListener('click', (e) => {
          const row = e.target.closest('[data-region-row]');
          if (!row || e.metaKey || e.ctrlKey || e.shiftKey || e.button > 0) return;
          e.preventDefault();
          root.dispatchEvent(new CustomEvent('map:select', { detail: row.dataset.regionRow, bubbles: true }));
        });
      }
    }

    root.addEventListener('click', (e) => {
      const pin = e.target.closest('.map__pin');
      if (!pin || pin.disabled) return;
      const slug = pin.dataset.region;
      if (mode === 'filter') {
        root.dispatchEvent(new CustomEvent('map:select', { detail: slug, bubbles: true }));
      } else {
        location.href = `${ROOT}archive.html?region=${encodeURIComponent(slug)}`;
      }
    });

    syncTargets(root);
  });

  const mq = matchMedia(NARROW);
  const resync = () => document.querySelectorAll('[data-map]').forEach(syncTargets);
  mq.addEventListener ? mq.addEventListener('change', resync) : mq.addListener(resync);
}

/** На узком экране пины — разметка: ни мышью, ни табом, ни голосом. */
function syncTargets(root) {
  const off = matchMedia(NARROW).matches;
  root.querySelectorAll('.map__pin').forEach(p => {
    p.disabled = off;
    p.setAttribute('aria-hidden', String(off));
    if (off) p.setAttribute('tabindex', '-1');
    else p.removeAttribute('tabindex');
  });
}

/** Подсветить активный регион (используется архивом). */
export function setActiveRegion(slug) {
  document.querySelectorAll('.map__pin').forEach(p => {
    const on = p.dataset.region === slug;
    p.classList.toggle('is-active', on);
    if (p.hasAttribute('aria-pressed')) p.setAttribute('aria-pressed', String(on));
  });
  document.querySelectorAll('[data-region-row]').forEach(row => {
    const on = row.dataset.regionRow === slug;
    row.classList.toggle('is-active', on);
    if (on) row.setAttribute('aria-current', 'true');
    else row.removeAttribute('aria-current');
  });
}

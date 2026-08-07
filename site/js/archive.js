/* ═══════════════════════════════════════════════════════════
   ДРУГ — медиаархив: карта → регион, плашки типа и формата
   Состояние живёт в query-строке, чтобы ссылкой можно было делиться.
   ═══════════════════════════════════════════════════════════ */

import { materials, regions, typeLabels, formatLabels } from './data.js';
import { photo, esc, ROOT } from './ui.js';
import { setActiveRegion } from './map.js';

const state = { region: '', type: '', format: '' };

function readUrl() {
  const q = new URLSearchParams(location.search);
  state.region = q.get('region') || '';
  state.type = q.get('type') || '';
  state.format = q.get('format') || '';
}

function writeUrl() {
  const q = new URLSearchParams();
  Object.entries(state).forEach(([k, v]) => { if (v) q.set(k, v); });
  const url = q.toString() ? `?${q}` : location.pathname;
  history.replaceState(null, '', url);
}

function match(m) {
  return (!state.region || m.region === state.region)
    && (!state.type || m.type === state.type)
    && (!state.format || m.formats.includes(state.format));
}

function card(m) {
  const region = regions.find(r => r.slug === m.region);
  return `<a class="card material-card" href="${ROOT}${m.url}">
      <div class="ph ph--4x3 ph--zoom material-card__ph">
        ${photo(m.cover, m.title, { sizes: '(max-width: 860px) 90vw, 30vw' })}
      </div>
      <span class="material-card__kind">${esc(typeLabels[m.type] || m.type)}</span>
      <h2 class="card__title">${esc(m.title)}</h2>
      <p class="card__text">${esc(m.lead)}</p>
      <p class="material-card__meta">${esc(region ? region.short : '')} · ${esc(m.date)}</p>
    </a>`;
}

function emptyState() {
  // Героев в открытой части архива пока нет: об этом говорим прямо
  // и сразу даём тем, кто себя узнал, способ попасть в проект.
  if (state.type === 'heroes') {
    return `<div class="empty">
        <p class="empty__title">Первые герои появятся здесь после экспедиций</p>
        <p class="empty__text">Мы приезжаем к людям в их среду, поэтому досье героев выходят
          вместе с выпуском региона. Если вы знаете такого человека или сами им являетесь —
          расскажите.</p>
        <a class="btn btn--primary" href="${ROOT}become-hero.html">Рассказать историю</a>
      </div>`;
  }

  const r = regions.find(x => x.slug === state.region);
  if (r && r.status === 'planned') {
    return `<div class="empty">
        <p class="empty__title">${esc(r.name)} — экспедиция впереди</p>
        <p class="empty__text">${esc(r.lead)} Съёмка намечена на ${esc(r.period)}. Вернёмся, и материалы появятся здесь.</p>
        <a class="btn btn--primary" href="${ROOT}become-hero.html">Предложить героя из этого региона</a>
      </div>`;
  }

  return `<div class="empty">
      <p class="empty__title">Под такие условия ничего не нашлось</p>
      <p class="empty__text">Снимите один из фильтров, например оставьте только регион. Архив пополняется после каждой поездки.</p>
      <button type="button" class="btn btn--ghost" data-reset>Снять все фильтры</button>
    </div>`;
}

function chipRow(key, items, allLabel) {
  const btn = (val, label) =>
    `<button type="button" class="chip" data-filter="${key}" data-value="${esc(val)}"
       aria-pressed="${state[key] === val}">${esc(label)}</button>`;
  return btn('', allLabel) + items.map(([v, l]) => btn(v, l)).join('');
}

function renderFilters() {
  const box = document.querySelector('[data-filters]');
  if (!box) return;

  box.innerHTML = `
    <div class="filter">
      <span class="filter__label" id="f-region">Регион</span>
      <div class="chips" role="group" aria-labelledby="f-region">
        ${chipRow('region', regions.map(r => [r.slug, r.short]), 'Все регионы')}
      </div>
    </div>
    <div class="filter">
      <span class="filter__label" id="f-type">Тип материала</span>
      <div class="chips" role="group" aria-labelledby="f-type">
        ${chipRow('type', Object.entries(typeLabels), 'Любой')}
      </div>
    </div>
    <div class="filter">
      <span class="filter__label" id="f-format">Формат материала</span>
      <div class="chips" role="group" aria-labelledby="f-format">
        ${chipRow('format', Object.entries(formatLabels), 'Любой')}
      </div>
    </div>`;
}

function render() {
  renderFilters();
  setActiveRegion(state.region);

  const grid = document.querySelector('[data-archive]');
  const count = document.querySelector('[data-archive-count]');
  if (!grid) return;

  const found = materials.filter(match);
  grid.className = found.length ? 'grid grid--3 archive__grid' : 'archive__grid';
  grid.innerHTML = found.length ? found.map(card).join('') : emptyState();

  if (count) {
    const n = found.length;
    const word = n % 10 === 1 && n % 100 !== 11 ? 'материал'
      : [2, 3, 4].includes(n % 10) && ![12, 13, 14].includes(n % 100) ? 'материала' : 'материалов';
    count.textContent = n ? `${n} ${word}` : 'пока пусто';
  }
}

export function initArchive() {
  if (!document.querySelector('[data-archive]')) return;
  readUrl();
  render();

  document.addEventListener('click', (e) => {
    const chip = e.target.closest('[data-filter]');
    if (chip) {
      const key = chip.dataset.filter;
      state[key] = state[key] === chip.dataset.value ? '' : chip.dataset.value;
      writeUrl();
      render();
      return;
    }
    if (e.target.closest('[data-reset]')) {
      state.region = state.type = state.format = '';
      writeUrl();
      render();
    }
  });

  // клик по пину карты фильтрует, а не уводит со страницы
  document.addEventListener('map:select', (e) => {
    state.region = state.region === e.detail ? '' : e.detail;
    writeUrl();
    render();
    document.querySelector('[data-archive]')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
}

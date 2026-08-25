/* ═══════════════════════════════════════════════════════════
   ДРУГ — медиаархив: карта → регион, плашки типа и формата
   Состояние живёт в query-строке, чтобы ссылкой можно было делиться.
   ═══════════════════════════════════════════════════════════ */

import { materials, regions, typeLabels, formatLabels } from './data.js';
import { photo, esc, ROOT } from './ui.js';
import { setActiveRegion } from './map.js';

const state = { region: '', type: '', format: '' };
// Что пришло в адресе, но такого значения не существует. Держим отдельно,
// чтобы объяснить человеку, а не показывать безликое «ничего не нашлось».
const unknown = { region: '', type: '', format: '' };

const known = {
  region: () => regions.map(r => r.slug),
  type: () => Object.keys(typeLabels),
  format: () => Object.keys(formatLabels),
};

function readUrl() {
  const q = new URLSearchParams(location.search);
  Object.keys(state).forEach(k => {
    const v = q.get(k) || '';
    const ok = !v || known[k]().includes(v);
    state[k] = ok ? v : '';
    unknown[k] = ok ? '' : v;
  });
}

function writeUrl(push) {
  const q = new URLSearchParams();
  Object.entries(state).forEach(([k, v]) => { if (v) q.set(k, v); });
  const url = q.toString() ? `?${q}` : location.pathname;
  // pushState, а не replaceState: человек накликал три фильтра — «Назад»
  // должен снимать последний, а не выбрасывать со страницы целиком.
  if (push) history.pushState({ ...state }, '', url);
  else history.replaceState({ ...state }, '', url);
}

function match(m) {
  return (!state.region || m.region === state.region)
    && (!state.type || m.type === state.type)
    && (!state.format || (m.formats || []).includes(state.format));
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

/** Заметка о том, что в ссылке было значение, которого не существует.
 *  Показываем её независимо от того, нашлись материалы или нет: после
 *  очистки битого фильтра архив выдаёт полный список, и без объяснения
 *  человек решит, что открыл не ту ссылку. */
function renderNotice() {
  const grid = document.querySelector('[data-archive]');
  if (!grid) return;
  const prev = document.querySelector('[data-archive-notice]');
  if (prev) prev.remove();

  const bad = Object.entries(unknown).filter(([, v]) => v);
  if (!bad.length) return;

  const what = { region: 'региону', type: 'типу материалов', format: 'формату' };
  const list = bad.map(([k, v]) => `${what[k]} «${esc(v)}»`).join(' и ');
  const box = document.createElement('p');
  box.className = 'notice';
  box.setAttribute('data-archive-notice', '');
  box.setAttribute('role', 'status');
  box.innerHTML = `В ссылке был фильтр по ${list} — такого у нас нет. Показываем архив целиком.`;
  grid.parentNode.insertBefore(box, grid);
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
       aria-pressed="false">${esc(label)}</button>`;
  return btn('', allLabel) + items.map(([v, l]) => btn(v, l)).join('');
}

/** Плашки рисуются один раз. Перерисовка на каждый клик сбрасывала фокус
 *  на <body>: человек на клавиатуре после каждого фильтра начинал табаться
 *  заново с самого верха страницы. */
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

/** Переставляем только состояние — сами кнопки остаются теми же узлами,
 *  поэтому фокус на нажатой плашке никуда не девается. */
function syncFilters() {
  document.querySelectorAll('[data-filter]').forEach(btn => {
    btn.setAttribute('aria-pressed', String(state[btn.dataset.filter] === btn.dataset.value));
  });
}

function render() {
  syncFilters();
  renderNotice();
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

function apply(changes, { push = true } = {}) {
  Object.assign(state, changes);
  Object.keys(unknown).forEach(k => { unknown[k] = ''; });
  writeUrl(push);
  render();
}

export function initArchive() {
  if (!document.querySelector('[data-archive]')) return;
  readUrl();
  renderFilters();
  render();
  writeUrl(false);   // мусорные параметры вычищаем из адреса сразу

  document.addEventListener('click', (e) => {
    const chip = e.target.closest('[data-filter]');
    if (chip) {
      const key = chip.dataset.filter;
      apply({ [key]: state[key] === chip.dataset.value ? '' : chip.dataset.value });
      return;
    }
    if (e.target.closest('[data-reset]')) apply({ region: '', type: '', format: '' });
  });

  // клик по пину карты или по строке региона фильтрует, а не уводит со страницы
  document.addEventListener('map:select', (e) => {
    apply({ region: state.region === e.detail ? '' : e.detail });
    document.querySelector('[data-archive]')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  // «Назад» и «Вперёд» откатывают фильтры, а не уводят со страницы
  addEventListener('popstate', () => {
    readUrl();
    render();
  });
}

/* ═══════════════════════════════════════════════════════════
   ДРУГ — раздел «Истории»: поиск и фильтры Место, Тип, Тема, Год.
   Состояние живёт в query-строке, чтобы ссылкой можно было делиться.
   ═══════════════════════════════════════════════════════════ */

import { materials, heroes, regions, typeLabels, topicLabels } from './data.js';
import { photo, esc, ROOT, imgSrc } from './ui.js';
import { getArticles } from './store.js';

const state = { q: '', region: '', type: '', topic: '', year: '' };

/* Все истории: материалы из data.js, герои выпусков и статьи из админки. */
let all = [];

function heroMaterial(h) {
  return {
    slug: 'hero-' + h.slug,
    type: 'text',
    region: h.region,
    topics: h.topics || [],
    year: '2026',
    title: h.name,
    lead: h.lead,
    search: (h.quotes || []).join(' '),
    cover: h.photo,
    url: `hero.html?slug=${encodeURIComponent(h.slug)}`
  };
}

async function collect() {
  let articles = [];
  try { articles = await getArticles({ published: true }); } catch (err) { console.error(err); }
  const fromStore = articles.map(a => ({
    slug: a.id,
    type: typeLabels[a.type] ? a.type : 'text',
    region: a.region,
    topics: a.topics || [],
    year: (a.date || '').slice(0, 4),
    title: a.title,
    lead: a.lead,
    search: (a.blocks || []).map(b => b.text || '').join(' '),
    coverSrc: imgSrc(a.cover),
    url: `article.html?id=${encodeURIComponent(a.id)}`
  }));
  return [...materials, ...heroes.map(heroMaterial), ...fromStore];
}

function readUrl() {
  const q = new URLSearchParams(location.search);
  Object.keys(state).forEach(k => { state[k] = q.get(k) || ''; });
}

function writeUrl() {
  const q = new URLSearchParams();
  Object.entries(state).forEach(([k, v]) => { if (v) q.set(k, v); });
  history.replaceState(null, '', q.toString() ? `?${q}` : location.pathname);
}

const norm = s => String(s || '').toLowerCase().replace(/ё/g, 'е');

function match(m) {
  if (state.region && m.region !== state.region) return false;
  if (state.type && m.type !== state.type) return false;
  if (state.topic && !(m.topics || []).includes(state.topic)) return false;
  if (state.year && m.year !== state.year) return false;
  if (state.q) {
    const hay = norm([m.title, m.lead, m.search, (m.topics || []).join(' ')].join(' '));
    return norm(state.q).split(/\s+/).filter(Boolean).every(w => hay.includes(w));
  }
  return true;
}

function card(m) {
  const region = regions.find(r => r.slug === m.region);
  return `<a class="card material-card" href="${ROOT}${m.url}">
      <div class="ph ph--4x3 ph--zoom material-card__ph">
        ${m.coverSrc
          ? `<img src="${esc(m.coverSrc)}" alt="${esc(m.title)}" loading="lazy" decoding="async">`
          : photo(m.cover, m.title, { sizes: '(max-width: 860px) 90vw, 30vw' })}
      </div>
      <span class="material-card__kind">${esc(typeLabels[m.type] || m.type)}</span>
      <h2 class="card__title">${esc(m.title)}</h2>
      <p class="card__text">${esc(m.lead)}</p>
      <p class="material-card__meta">${esc(region ? region.short : '')}${m.year ? ' · ' + esc(m.year) : ''}</p>
    </a>`;
}

function emptyState() {
  return `<div class="empty">
      <p class="empty__title">Ничего не нашли</p>
      <p class="empty__text">Уберите один фильтр или попробуйте другое слово.</p>
      <button type="button" class="btn btn--ghost" data-reset>Показать все</button>
    </div>`;
}

function chipRow(key, items) {
  return items.map(([v, l]) =>
    `<button type="button" class="chip" data-filter="${key}" data-value="${esc(v)}"
       aria-pressed="${state[key] === v}">${esc(l)}</button>`).join('');
}

function renderFilters() {
  const box = document.querySelector('[data-filters]');
  if (!box) return;
  const years = [...new Set(all.map(m => m.year).filter(Boolean))].sort().reverse();
  const any = Object.entries(state).some(([k, v]) => k !== 'q' && v);
  box.innerHTML = `
    <div class="filter">
      <span class="filter__label" id="f-region">Место</span>
      <div class="chips" role="group" aria-labelledby="f-region">${chipRow('region', regions.map(r => [r.slug, r.short]))}</div>
    </div>
    <div class="filter">
      <span class="filter__label" id="f-type">Тип</span>
      <div class="chips" role="group" aria-labelledby="f-type">${chipRow('type', Object.entries(typeLabels))}</div>
    </div>
    <div class="filter">
      <span class="filter__label" id="f-topic">Тема</span>
      <div class="chips" role="group" aria-labelledby="f-topic">${chipRow('topic', Object.entries(topicLabels))}</div>
    </div>
    <div class="filter">
      <span class="filter__label" id="f-year">Год</span>
      <div class="chips" role="group" aria-labelledby="f-year">${chipRow('year', years.map(y => [y, y]))}</div>
    </div>
    ${any || state.q ? '<button type="button" class="btn btn--ghost" data-reset>Показать все</button>' : ''}`;
}

function render() {
  renderFilters();
  const grid = document.querySelector('[data-archive]');
  const count = document.querySelector('[data-archive-count]');
  if (!grid) return;
  const found = all.filter(match);
  grid.className = found.length ? 'grid grid--3 archive__grid' : 'archive__grid';
  grid.innerHTML = found.length ? found.map(card).join('') : emptyState();
  if (count) {
    const n = found.length;
    const word = n % 10 === 1 && n % 100 !== 11 ? 'история'
      : [2, 3, 4].includes(n % 10) && ![12, 13, 14].includes(n % 100) ? 'истории' : 'историй';
    count.textContent = n ? `${n} ${word}` : '';
  }
}

export async function initArchive() {
  if (!document.querySelector('[data-archive]')) return;
  readUrl();
  all = [...materials, ...heroes.map(heroMaterial)];
  const input = document.querySelector('[data-search]');
  if (input) input.value = state.q;
  render();
  all = await collect();
  render();

  input?.addEventListener('input', () => {
    state.q = input.value.trim();
    writeUrl();
    render();
  });

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
      Object.keys(state).forEach(k => { state[k] = ''; });
      if (input) input.value = '';
      writeUrl();
      render();
    }
  });
}

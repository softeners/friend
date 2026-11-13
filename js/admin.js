/* ═══════════════════════════════════════════════════════════
   ДРУГ — админка (демо-версия)
   Заявки героев и статьи медиаархива. Все данные — только через
   js/store.js; при переезде на Directus этот файл не меняется.
   ═══════════════════════════════════════════════════════════ */

import { regions, typeLabels, formatLabels } from './data.js';
import { esc, imgSrc, monthYear, compressImage, ROOT } from './ui.js';
import { initLightbox } from './lightbox.js';
import {
  getRequests, updateRequest, deleteRequest,
  getArticles, getArticle, saveArticle, deleteArticle, resetDemo
} from './store.js';

const PASSWORD = 'drug2026';
const AUTH_KEY = 'drug.admin';

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

const ui = { tab: 'requests', sub: 'new', reqId: null, editing: null };

/* ── Форматирование ────────────────────────────────────────── */
function fmtDate(iso) {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '';
  return d.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
    + ', ' + d.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
}
function firstWords(text, n = 14) {
  const w = String(text || '').trim().split(/\s+/);
  return w.slice(0, n).join(' ') + (w.length > n ? '…' : '');
}
function linkify(raw) {
  // «Ссылки на соцсети» — через запятую или пробел; каждую делаем ссылкой.
  return String(raw || '').split(/[,\s]+/).filter(Boolean).map(s => {
    const href = /^https?:\/\//i.test(s) ? s : /^[\w.-]+\.[a-z]{2,}(\/|$)/i.test(s) ? `https://${s}` : null;
    return href ? `<a href="${esc(href)}" target="_blank" rel="noopener">${esc(s)}</a>` : esc(s);
  }).join(', ');
}
function contactLink(raw) {
  const v = String(raw || '').trim();
  if (!v) return '';
  if (/^@?[a-z0-9_]{4,}$/i.test(v) && /[a-z_]/i.test(v)) {
    const nick = v.replace(/^@/, '');
    return `<a href="https://t.me/${esc(nick)}" target="_blank" rel="noopener">@${esc(nick)}</a> · Telegram`;
  }
  if (/t\.me\//i.test(v)) return linkify(v);
  const digits = v.replace(/[^\d+]/g, '');
  return digits.replace(/\D/g, '').length >= 10 ? `<a href="tel:${esc(digits)}">${esc(v)}</a>` : esc(v);
}
function setStatus(el, text, kind = '') {
  if (!el) return;
  el.textContent = text;
  el.className = `admin-status${kind ? ` is-${kind}` : ''}`;
}

/* ── Вход ──────────────────────────────────────────────────── */
function isAuthed() {
  try { return sessionStorage.getItem(AUTH_KEY) === '1'; } catch { return false; }
}
function showApp() {
  $('[data-login]').hidden = isAuthed();
  $('[data-app]').hidden = !isAuthed();
  $('[data-logout]').hidden = !isAuthed();
  if (isAuthed()) renderTab();
  else $('#pass')?.focus();
}
function initLogin() {
  $('[data-login-form]').addEventListener('submit', (e) => {
    e.preventDefault();
    const input = $('#pass');
    if (input.value === PASSWORD) {
      try { sessionStorage.setItem(AUTH_KEY, '1'); } catch { /* приватный режим */ }
      input.value = '';
      $('#pass-err').textContent = '';
      input.removeAttribute('aria-invalid');
      showApp();
    } else {
      $('#pass-err').textContent = 'Пароль не подошёл';
      input.setAttribute('aria-invalid', 'true');
      input.select();
    }
  });
  $('[data-logout]').addEventListener('click', () => {
    try { sessionStorage.removeItem(AUTH_KEY); } catch { /* ignore */ }
    ui.editing = null;
    showApp();
  });
}

/* ── Вкладки ───────────────────────────────────────────────── */
function renderTab() {
  $$('[data-tab]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.tab === ui.tab)));
  $$('[data-view]').forEach(v => { v.hidden = v.dataset.view !== ui.tab; });
  if (ui.tab === 'requests') renderRequests();
  else if (ui.editing) renderEditor();
  else renderArticles();
}

/* ── Заявки ────────────────────────────────────────────────── */
async function renderRequests() {
  const all = await getRequests();
  const counts = { new: 0, approved: 0 };
  all.forEach(r => { counts[r.status === 'approved' ? 'approved' : 'new']++; });
  $$('[data-count]').forEach(el => { el.textContent = counts[el.dataset.count]; });
  $$('[data-sub]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.sub === ui.sub)));

  const list = all.filter(r => (r.status === 'approved' ? 'approved' : 'new') === ui.sub);
  if (ui.reqId && !list.some(r => r.id === ui.reqId)) ui.reqId = null;

  $('[data-req-list]').innerHTML = list.length
    ? list.map(r => `
        <button type="button" class="admin-row" data-req="${esc(r.id)}" aria-current="${r.id === ui.reqId}">
          <span class="admin-row__top">
            <span class="admin-row__name">${esc(r.name || 'Без имени')}</span>
            <span class="admin-row__date">${esc(new Date(r.createdAt).toLocaleDateString('ru-RU'))}</span>
          </span>
          <span class="admin-row__text">${esc(firstWords(r.work))}</span>
        </button>`).join('')
    : `<p class="admin-empty">${ui.sub === 'new' ? 'Новых заявок нет' : 'Подтверждённых заявок пока нет'}</p>`;

  $('[data-split]').classList.toggle('is-detail', !!ui.reqId);
  renderRequestDetail(list.find(r => r.id === ui.reqId));
}

function renderRequestDetail(r) {
  const box = $('[data-req-detail]');
  if (!r) {
    box.innerHTML = `<p class="admin-empty">Выберите заявку слева, чтобы прочитать её целиком</p>`;
    return;
  }
  const row = (label, html) => html ? `<div><dt>${label}</dt><dd>${html}</dd></div>` : '';
  const photos = (r.photos || []).map((src, i) =>
    `<img src="${esc(imgSrc(src))}" alt="Фото ${i + 1} из заявки: ${esc(r.name)}" data-zoom loading="lazy">`).join('');
  const link = r.photo_link
    ? `<a href="${esc(/^https?:/i.test(r.photo_link) ? r.photo_link : 'https://' + r.photo_link)}" target="_blank" rel="noopener">${esc(r.photo_link)}</a>`
    : '';

  box.innerHTML = `
    <button type="button" class="btn btn--ghost admin-detail__back" data-req-back>← Все заявки</button>
    <div class="admin-detail__head">
      <span class="tag ${r.status === 'approved' ? 'tag--done' : 'tag--planned'}" style="align-self:flex-start">${r.status === 'approved' ? 'Подтверждена' : 'Новая'}</span>
      <h2 class="h3">${esc(r.name || 'Без имени')}</h2>
      <p class="admin-row__date">Отправлена ${esc(fmtDate(r.createdAt))}</p>
    </div>
    <dl class="admin-fields">
      ${row('Регион, город или село', esc(r.place))}
      ${row('Чем занимается и что делает для своего места', esc(r.work))}
      ${row('Почему стоит рассказать', esc(r.why))}
      ${row('Ссылки', linkify(r.links))}
      ${photos ? `<div><dt>Фото · ${r.photos.length}</dt><dd><div class="admin-photos">${photos}</div></dd></div>` : ''}
      ${row('Ссылка на облако', link)}
      ${row('Почта', r.email ? `<a href="mailto:${esc(r.email)}">${esc(r.email)}</a>` : '')}
      ${row('Телефон или Telegram', contactLink(r.phone))}
    </dl>
    <div class="admin-actions">
      ${r.status !== 'approved' ? `<button type="button" class="btn btn--primary" data-req-approve>Подтвердить</button>` : ''}
      <button type="button" class="btn btn--ghost" data-req-delete>Удалить</button>
    </div>`;
}

function initRequests() {
  $('[data-view="requests"]').addEventListener('click', async (e) => {
    const sub = e.target.closest('[data-sub]');
    if (sub) { ui.sub = sub.dataset.sub; ui.reqId = null; renderRequests(); return; }

    const row = e.target.closest('[data-req]');
    if (row) {
      ui.reqId = row.dataset.req;
      await renderRequests();
      if (matchMedia('(max-width: 860px)').matches) $('[data-req-detail]').scrollIntoView({ block: 'start' });
      return;
    }
    if (e.target.closest('[data-req-back]')) { ui.reqId = null; renderRequests(); return; }

    if (e.target.closest('[data-req-approve]')) {
      await updateRequest(ui.reqId, { status: 'approved' });
      ui.reqId = null;
      renderRequests();
      return;
    }
    if (e.target.closest('[data-req-delete]')) {
      if (!confirm('Удалить заявку? Вернуть её будет нельзя.')) return;
      await deleteRequest(ui.reqId);
      ui.reqId = null;
      renderRequests();
    }
  });
}

/* ── Статьи: список ────────────────────────────────────────── */
async function renderArticles() {
  $('[data-art-list-view]').hidden = false;
  $('[data-art-editor]').hidden = true;
  const list = await getArticles();
  $('[data-art-list]').innerHTML = list.length
    ? list.map(a => `
        <button type="button" class="card admin-article" data-art="${esc(a.id)}">
          <div class="ph ph--4x3">
            ${a.cover ? `<img src="${esc(imgSrc(a.cover))}" alt="" loading="lazy">` : '<div class="ph__empty-inner">Без обложки</div>'}
          </div>
          <span class="admin-article__body">
            <span class="card__title">${esc(a.title || 'Без заголовка')}</span>
            <span class="admin-article__meta">
              <span>${esc(monthYear(a.date) || 'без даты')}</span>
              <span class="tag ${a.status === 'published' ? 'tag--done' : 'tag--planned'}">${a.status === 'published' ? 'Опубликовано' : 'Черновик'}</span>
            </span>
          </span>
        </button>`).join('')
    : `<p class="admin-empty">Статей пока нет. Нажмите «Новая статья».</p>`;
}

/* ── Статьи: редактор ──────────────────────────────────────── */
const BLOCKS = {
  p: { label: 'Абзац', add: '+ Абзац' },
  h: { label: 'Подзаголовок', add: '+ Подзаголовок' },
  quote: { label: 'Цитата', add: '+ Цитата' },
  photo: { label: 'Фото', add: '+ Фото' }
};

function emptyArticle() {
  return {
    title: '', cover: '', lead: '', region: '', type: '', formats: [],
    date: new Date().toISOString().slice(0, 10), status: 'draft',
    blocks: [{ t: 'p', text: '' }]
  };
}

function options(entries, value, placeholder) {
  return `<option value="">${placeholder}</option>`
    + entries.map(([v, l]) => `<option value="${esc(v)}"${v === value ? ' selected' : ''}>${esc(l)}</option>`).join('');
}

function blockHtml(b, i, n) {
  const bar = `
    <div class="block__bar">
      <span class="filter__label block__kind">${BLOCKS[b.t].label}</span>
      <button type="button" class="block__btn" data-move="-1" data-i="${i}" ${i === 0 ? 'disabled' : ''} aria-label="Поднять блок">↑</button>
      <button type="button" class="block__btn" data-move="1" data-i="${i}" ${i === n - 1 ? 'disabled' : ''} aria-label="Опустить блок">↓</button>
      <button type="button" class="block__btn" data-remove="${i}" aria-label="Удалить блок">×</button>
    </div>`;
  let body = '';
  if (b.t === 'p') {
    body = `<textarea class="textarea" rows="5" data-b="${i}" data-k="text" placeholder="Текст абзаца. Пустая строка — новый абзац.">${esc(b.text)}</textarea>`;
  } else if (b.t === 'h') {
    body = `<input class="input" data-b="${i}" data-k="text" value="${esc(b.text)}" placeholder="Подзаголовок">`;
  } else if (b.t === 'quote') {
    body = `<textarea class="textarea" rows="3" data-b="${i}" data-k="text" placeholder="Текст цитаты">${esc(b.text)}</textarea>
      <input class="input" data-b="${i}" data-k="author" value="${esc(b.author)}" placeholder="Подпись: кто это сказал">`;
  } else {
    body = `<div class="block__photo">
        <div class="ph ph--4x3">${b.src ? `<img src="${esc(imgSrc(b.src))}" alt="" data-zoom>` : '<div class="ph__empty-inner">Фото не выбрано</div>'}</div>
        <label class="btn btn--ghost admin-filebtn">${b.src ? 'Заменить фото' : 'Выбрать фото'}
          <input type="file" accept="image/*" data-b-file="${i}"></label>
      </div>
      <input class="input" data-b="${i}" data-k="caption" value="${esc(b.caption)}" placeholder="Подпись к фото">`;
  }
  return `<div class="card block">${bar}${body}</div>`;
}

function renderBlocks() {
  const a = ui.editing;
  $('[data-blocks]').innerHTML = a.blocks.map((b, i) => blockHtml(b, i, a.blocks.length)).join('')
    || '<p class="admin-empty">Блоков пока нет. Добавьте первый кнопкой «+».</p>';
}

function renderEditor() {
  const a = ui.editing;
  $('[data-art-list-view]').hidden = true;
  const box = $('[data-art-editor]');
  box.hidden = false;
  const published = a.status === 'published';

  box.innerHTML = `
    <form class="admin-editor" data-editor novalidate>
      <div class="admin-editor__head">
        <button type="button" class="btn btn--ghost" data-ed-back>← Все статьи</button>
        <span class="tag ${published ? 'tag--done' : 'tag--planned'}">${published ? 'Опубликовано' : 'Черновик'}</span>
      </div>
      <h1 class="h2">${a.id ? 'Редактирование статьи' : 'Новая статья'}</h1>

      <div class="field">
        <label class="field__label" for="ed-title">Заголовок <span class="field__req" aria-hidden="true">*</span></label>
        <input class="input" id="ed-title" data-f="title" value="${esc(a.title)}" required>
      </div>

      <div class="field">
        <span class="field__label">Обложка</span>
        <div class="admin-cover">
          <div class="ph ph--4x3">${a.cover ? `<img src="${esc(imgSrc(a.cover))}" alt="" data-zoom>` : '<div class="ph__empty-inner">Нет обложки</div>'}</div>
          <label class="btn btn--ghost admin-filebtn">${a.cover ? 'Заменить обложку' : 'Загрузить обложку'}
            <input type="file" accept="image/*" data-cover-file></label>
        </div>
      </div>

      <div class="field">
        <label class="field__label" for="ed-lead">Короткое описание <span class="field__opt">для карточки в архиве</span></label>
        <textarea class="textarea" id="ed-lead" rows="3" data-f="lead">${esc(a.lead)}</textarea>
      </div>

      <div class="admin-grid2">
        <div class="field">
          <label class="field__label" for="ed-region">Регион <span class="field__req" aria-hidden="true">*</span></label>
          <select class="select" id="ed-region" data-f="region">${options(regions.map(r => [r.slug, r.name]), a.region, 'Выберите регион')}</select>
        </div>
        <div class="field">
          <label class="field__label" for="ed-type">Тип материала <span class="field__req" aria-hidden="true">*</span></label>
          <select class="select" id="ed-type" data-f="type">${options(Object.entries(typeLabels), a.type, 'Выберите тип')}</select>
        </div>
        <div class="field">
          <span class="field__label" id="ed-formats">Формат <span class="field__opt">можно не выбирать</span></span>
          <div class="chips" role="group" aria-labelledby="ed-formats">
            ${Object.entries(formatLabels).map(([v, l]) =>
              `<button type="button" class="chip" data-format="${v}" aria-pressed="${a.formats.includes(v)}">${esc(l)}</button>`).join('')}
          </div>
        </div>
        <div class="field">
          <label class="field__label" for="ed-date">Дата <span class="field__req" aria-hidden="true">*</span></label>
          <input class="input" type="date" id="ed-date" data-f="date" value="${esc(a.date)}">
        </div>
      </div>

      <div class="field">
        <span class="field__label">Текст</span>
        <div class="blocks" data-blocks></div>
        <div class="blocks__add">
          <button type="button" class="btn btn--ghost" data-add-toggle aria-expanded="false" aria-label="Добавить блок">+</button>
          <span class="chips" data-add-menu hidden>
            ${Object.entries(BLOCKS).map(([t, b]) => `<button type="button" class="chip" data-add="${t}">${b.add}</button>`).join('')}
          </span>
        </div>
      </div>

      <div class="admin-actions">
        <button type="button" class="btn btn--ghost" data-ed-save>${published ? 'Сохранить изменения' : 'Сохранить черновик'}</button>
        ${published
          ? `<button type="button" class="btn btn--ghost" data-ed-unpublish>Снять с публикации</button>
             <a class="btn btn--ghost" href="${ROOT}article.html?id=${encodeURIComponent(a.id)}" target="_blank" rel="noopener">Открыть на сайте ↗</a>`
          : `<button type="button" class="btn btn--primary" data-ed-publish>Опубликовать</button>`}
        ${a.id ? `<button type="button" class="btn btn--ghost" data-ed-delete>Удалить</button>` : ''}
      </div>
      <p class="admin-status" data-ed-status role="status" aria-live="polite"></p>
    </form>`;
  renderBlocks();
}

function validateForPublish(a) {
  const miss = [];
  if (!a.title.trim()) miss.push('заголовок');
  if (!a.region) miss.push('регион');
  if (!a.type) miss.push('тип материала');
  if (!a.date) miss.push('дату');
  return miss;
}

async function persist(status) {
  const a = ui.editing;
  const st = $('[data-ed-status]');
  if (!a.title.trim()) { setStatus(st, 'Без заголовка статью не сохранить', 'error'); $('#ed-title').focus(); return; }
  if (status === 'published') {
    const miss = validateForPublish(a);
    if (miss.length) { setStatus(st, `Чтобы опубликовать, заполните: ${miss.join(', ')}`, 'error'); return; }
  }
  try {
    ui.editing = await saveArticle({ ...a, status });
    renderEditor();
    setStatus($('[data-ed-status]'), status === 'published'
      ? (a.status === 'published' ? 'Изменения сохранены и уже видны в архиве' : 'Опубликовано: статья появилась в архиве')
      : a.status === 'published' ? 'Снято с публикации, статья сохранена как черновик' : 'Черновик сохранён', 'ok');
  } catch (err) {
    setStatus(st, err.message, 'error');
  }
}

function initArticles() {
  const view = $('[data-view="articles"]');

  view.addEventListener('click', async (e) => {
    if (e.target.closest('[data-art-new]')) { ui.editing = emptyArticle(); renderEditor(); $('#ed-title').focus(); return; }
    const card = e.target.closest('[data-art]');
    if (card) { ui.editing = await getArticle(card.dataset.art); renderEditor(); scrollTo(0, 0); return; }
    if (!ui.editing) return;
    const a = ui.editing;

    if (e.target.closest('[data-ed-back]')) { ui.editing = null; renderArticles(); return; }

    const fmt = e.target.closest('[data-format]');
    if (fmt) {
      const v = fmt.dataset.format;
      a.formats = a.formats.includes(v) ? a.formats.filter(x => x !== v) : [...a.formats, v];
      fmt.setAttribute('aria-pressed', String(a.formats.includes(v)));
      return;
    }

    if (e.target.closest('[data-add-toggle]')) {
      const menu = $('[data-add-menu]'); menu.hidden = !menu.hidden;
      e.target.closest('[data-add-toggle]').setAttribute('aria-expanded', String(!menu.hidden));
      return;
    }
    const add = e.target.closest('[data-add]');
    if (add) {
      const t = add.dataset.add;
      a.blocks.push(t === 'quote' ? { t, text: '', author: '' } : t === 'photo' ? { t, src: '', caption: '' } : { t, text: '' });
      $('[data-add-menu]').hidden = true;
      $('[data-add-toggle]').setAttribute('aria-expanded', 'false');
      renderBlocks();
      $$('.block', $('[data-blocks]')).at(-1)?.querySelector('textarea, input:not([type="file"])')?.focus();
      return;
    }
    const mv = e.target.closest('[data-move]');
    if (mv) {
      const i = Number(mv.dataset.i), j = i + Number(mv.dataset.move);
      if (j < 0 || j >= a.blocks.length) return;
      [a.blocks[i], a.blocks[j]] = [a.blocks[j], a.blocks[i]];
      renderBlocks();
      $(`[data-move="${mv.dataset.move}"][data-i="${j}"]`)?.focus();
      return;
    }
    const rm = e.target.closest('[data-remove]');
    if (rm) {
      const b = a.blocks[Number(rm.dataset.remove)];
      const filled = b.text || b.src || b.author || b.caption;
      if (filled && !confirm('Удалить этот блок?')) return;
      a.blocks.splice(Number(rm.dataset.remove), 1);
      renderBlocks();
      return;
    }

    if (e.target.closest('[data-ed-save]')) { persist(a.status === 'published' ? 'published' : 'draft'); return; }
    if (e.target.closest('[data-ed-publish]')) { persist('published'); return; }
    if (e.target.closest('[data-ed-unpublish]')) { persist('draft'); return; }
    if (e.target.closest('[data-ed-delete]')) {
      if (!confirm(`Удалить статью «${a.title || 'без заголовка'}»? Вернуть её будет нельзя.`)) return;
      await deleteArticle(a.id);
      ui.editing = null;
      renderArticles();
    }
  });

  view.addEventListener('input', (e) => {
    const a = ui.editing;
    if (!a) return;
    const f = e.target.dataset.f;
    if (f) { a[f] = e.target.value; return; }
    const bi = e.target.dataset.b;
    if (bi !== undefined) a.blocks[Number(bi)][e.target.dataset.k] = e.target.value;
  });
  view.addEventListener('change', async (e) => {
    const a = ui.editing;
    if (!a || e.target.type !== 'file' || !e.target.files[0]) return;
    const st = $('[data-ed-status]');
    setStatus(st, 'Сжимаем фото…');
    const src = await compressImage(e.target.files[0]);
    if (!src) { setStatus(st, 'Этот файл не открывается как картинка. Подойдёт JPG, PNG или WEBP', 'error'); return; }
    if (e.target.hasAttribute('data-cover-file')) {
      a.cover = src;
      const box = e.target.closest('.admin-cover');
      box.querySelector('.ph').innerHTML = `<img src="${src}" alt="" data-zoom>`;
      e.target.parentElement.firstChild.textContent = 'Заменить обложку';
    } else {
      a.blocks[Number(e.target.dataset.bFile)].src = src;
      renderBlocks();
    }
    setStatus(st, 'Фото добавлено. Не забудьте сохранить статью');
  });
}

/* ── Сброс демо-данных ─────────────────────────────────────── */
function initReset() {
  $('[data-reset-demo]').addEventListener('click', async () => {
    if (!confirm('Стереть все заявки и статьи и вернуть демо-данные?')) return;
    await resetDemo();
    Object.assign(ui, { sub: 'new', reqId: null, editing: null });
    renderTab();
  });
}

/* ── Старт ─────────────────────────────────────────────────── */
$$('[data-tab]').forEach(b => b.addEventListener('click', () => {
  ui.tab = b.dataset.tab;
  if (ui.tab === 'articles') ui.editing = null;
  renderTab();
}));
initLogin();
initRequests();
initArticles();
initReset();
initLightbox();
showApp();

/* ═══════════════════════════════════════════════════════════
   ДРУГ — страница статьи article.html?id=...
   Статьи пишутся в админке и лежат в js/store.js. Оформление
   повторяет путевые заметки (notes/altay.html): обложка на первом
   экране, метка типа, заголовок, описание, регион и дата, лонгрид.
   ═══════════════════════════════════════════════════════════ */

import { regions, typeLabels, formatLabels } from './data.js';
import { esc, param, imgSrc, monthYear } from './ui.js';
import { getArticle } from './store.js';

/** Абзацы внутри одного текстового блока — по пустой строке. */
function splitParas(text) {
  return String(text || '').split(/\n\s*\n/).map(t => t.trim()).filter(Boolean);
}

/*
 * Разметка блоков — та же, что в путевых заметках (notes/altay.html):
 *   подзаголовок  <span class="longread__part longread__part--mid">…</span>
 *                 (первый блок статьи — без --mid, как «Дорога» в начале заметок)
 *   вводный абзац <p class="longread__lead">…</p>  — первый абзац статьи
 *   абзац         <p>…</p>
 *   цитата        <blockquote><p class="verse">…</p><p class="verse__author">…</p></blockquote>
 *   фото          <figure class=""><div class="ph ph--4x3"><img></div><figcaption>…</figcaption></figure>
 * Все блоки стоят в .longread__col — одной колонке шириной с абзац.
 */
export function blockHtml(b, i = 1, ctx = { leadDone: true }) {
  switch (b.t) {
    case 'h':
      return b.text
        ? `<span class="longread__part${i === 0 ? '' : ' longread__part--mid'}">${esc(b.text)}</span>`
        : '';
    case 'quote':
      return b.text ? `<blockquote>
        <p class="verse">${esc(b.text)}</p>
        ${b.author ? `<p class="verse__author">${esc(b.author)}</p>` : ''}
      </blockquote>` : '';
    case 'photo':
      return b.src ? `<figure class="">
        <div class="ph ph--4x3">
          <img src="${esc(imgSrc(b.src))}" alt="${esc(b.caption || '')}" loading="lazy" decoding="async" data-zoom>
        </div>
        ${b.caption ? `<figcaption>${esc(b.caption)}</figcaption>` : ''}
      </figure>` : '';
    default:
      return splitParas(b.text).map(t => {
        const lead = !ctx.leadDone;
        ctx.leadDone = true;
        return `<p${lead ? ' class="longread__lead"' : ''}>${esc(t).replace(/\n/g, '<br>')}</p>`;
      }).join('\n');
  }
}

export async function initArticle() {
  const root = document.querySelector('[data-article]');
  if (!root) return;

  const a = await getArticle(param('id') || '');
  // Черновик читателю не показываем; админке для предпросмотра — можно (?preview=1).
  if (!a || (a.status !== 'published' && param('preview') !== '1')) {
    root.querySelector('[data-article-empty]').hidden = false;
    return;
  }

  const region = regions.find(r => r.slug === a.region);
  const kind = typeLabels[a.type] || '';
  const formats = (a.formats || []).map(f => formatLabels[f]).filter(Boolean).join(', ');
  document.title = `${a.title} — ДРУГ`;
  document.querySelector('meta[name="description"]')?.setAttribute('content', a.lead || '');

  root.querySelector('[data-article-body]').innerHTML = `
    <section class="hero">
      ${a.cover ? `<div class="hero__media">
        <img src="${esc(imgSrc(a.cover))}" alt="" loading="eager" fetchpriority="high" decoding="async">
      </div>` : ''}
      <div class="container hero__inner">
        <span class="eyebrow">ДРУГ <span class="eyebrow__rest">${esc(kind)}</span></span>
        <h1 class="hero__title">${esc(a.title)}</h1>
        ${a.lead ? `<p class="hero__lead">${esc(a.lead)}</p>` : ''}
        <dl class="meta">
          ${region ? `<div class="meta__item"><dt>Регион</dt><dd>${esc(region.name)}</dd></div>` : ''}
          ${a.date ? `<div class="meta__item"><dt>Дата</dt><dd>${esc(monthYear(a.date))}</dd></div>` : ''}
          ${formats ? `<div class="meta__item"><dt>Формат</dt><dd>${esc(formats)}</dd></div>` : ''}
        </dl>
      </div>
    </section>

    <article class="section longread">
      <div class="container">
        <div class="longread__col">
          ${(() => { const ctx = { leadDone: false }; return (a.blocks || []).map((b, i) => blockHtml(b, i, ctx)).join('\n'); })()}
          <p class="section__foot"><a class="btn btn--ghost" href="archive.html${region ? `?region=${region.slug}` : ''}">Ещё материалы${region ? ` · ${esc(region.short)}` : ''}</a></p>
        </div>
      </div>
    </article>`;
}

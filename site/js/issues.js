/* ═══════════════════════════════════════════════════════════
   ДРУГ — сетка выпусков журнала и каталог зинов
   ═══════════════════════════════════════════════════════════ */

import { issues, regions, zines } from './data.js';
import { photo, esc, ROOT } from './ui.js';

function issueCard(issue, opts = {}) {
  const region = regions.find(r => r.slug === issue.region);
  const tag = issue.published
    ? '<span class="tag tag--done">выпуск вышел</span>'
    : issue.status === 'in-progress'
      ? '<span class="tag tag--planned">выпуск в разработке</span>'
      : `<span class="tag tag--planned">${esc(issue.date)}</span>`;

  const inner = `
    <div class="ph ph--3x4 ph--zoom issue-card__ph">
      ${issue.cover
        ? photo(issue.cover, `Обложка выпуска № ${issue.number}: ${issue.title}`,
            { sizes: '(max-width: 860px) 90vw, 30vw', eager: !!opts.eager })
        : `<span class="ph--empty-label">Обложка появится<br>после экспедиции</span>`}
      <span class="issue-card__num">№&nbsp;${esc(issue.number)}</span>
    </div>
    <div class="issue-card__body">
      ${tag}
      <h2 class="card__title">${esc(issue.title)}</h2>
      <p class="issue-card__sub">${esc(issue.subtitle)}</p>
      <p class="card__text">${esc(issue.lead)}</p>
      <p class="issue-card__meta">${esc(region ? region.name : '')} · ${esc(issue.date)}</p>
    </div>`;

  return issue.published
    ? `<a class="card issue-card" href="${ROOT}${issue.url}">${inner}</a>`
    : `<article class="card issue-card is-soon" aria-label="${esc(issue.title)} — выпуск готовится">${inner}</article>`;
}

function zineCard(z) {
  return `<article class="card zine-card${z.available ? '' : ' is-soon'}">
      <div class="ph ph--3x4 zine-card__ph">
        ${photo(z.cover, `Обложка: ${z.title}`, { sizes: '(max-width: 860px) 90vw, 30vw' })}
      </div>
      <h2 class="card__title">${esc(z.title)}</h2>
      <p class="card__text">${esc(z.about)}</p>
      <dl class="zine-card__specs">
        <div><dt>Внутри</dt><dd>${esc(z.inside)}</dd></div>
        <div><dt>Формат</dt><dd>${esc(z.format)}</dd></div>
        <div><dt>Объём</dt><dd>${esc(z.pages)} страниц</dd></div>
      </dl>
      <div class="zine-card__foot">
        ${z.available
          ? `<span class="zine-card__price">${z.price.toLocaleString('ru-RU')} ₽</span>
             <a class="btn btn--primary" href="${ROOT}zines.html?zine=${z.slug}#order">Заказать</a>`
          : `<span class="tag tag--planned">выйдет при софинансировании</span>
             <a class="btn btn--ghost" href="${ROOT}partners.html">Условия партнёрства</a>`}
      </div>
    </article>`;
}

export function initIssues() {
  const grid = document.querySelector('[data-issues]');
  if (grid) {
    const limit = Number(grid.dataset.limit || 0);
    const list = limit ? issues.slice(0, limit) : issues;
    grid.innerHTML = list.map((i, n) => issueCard(i, { eager: n === 0 })).join('');
  }

  // Блок «последний выпуск» на главной
  const latest = document.querySelector('[data-latest-issue]');
  if (latest) {
    const issue = issues.find(i => i.published) || issues[0];
    const region = regions.find(r => r.slug === issue.region);
    latest.innerHTML = `
      <div class="ph ph--4x3 latest__ph">
        ${photo(issue.cover, `Обложка выпуска № ${issue.number}: ${issue.title}`,
          { sizes: '(max-width: 860px) 92vw, 50vw', big: true })}
      </div>
      <div class="latest__body">
        <span class="eyebrow">ДРУГ <span class="eyebrow__rest">Последний выпуск</span></span>
        <p class="latest__num">Выпуск № ${esc(issue.number)}</p>
        <h2 class="h2">${esc(issue.title)}</h2>
        <p class="latest__sub">${esc(issue.subtitle)}</p>
        <p class="text text--measure">${esc(issue.lead)}</p>
        <p class="latest__meta">${esc(region ? region.name : '')} · ${esc(issue.date)}</p>
        ${issue.published
          ? `<a class="btn btn--ghost btn--lg" href="${ROOT}${issue.url}">Читать выпуск</a>`
          : issue.status === 'in-progress'
            ? `<span class="tag tag--planned">Выпуск в разработке</span>`
            : `<span class="tag tag--planned">Выйдет ${esc(issue.date)}</span>`}
      </div>`;
  }

  const zineGrid = document.querySelector('[data-zines]');
  if (zineGrid) zineGrid.innerHTML = zines.map(zineCard).join('');

  initOrder();
}

/** Форма заказа: выбор издания по ссылке и видимая сумма.
 *
 *  Варианты в <select> впечатывает сборщик (см. _build/site_data.py),
 *  чтобы форму можно было отправить и без скрипта. Здесь — только то,
 *  что без скрипта невозможно: подстановка по ссылке и подсчёт итога.
 */
function initOrder() {
  const select = document.querySelector('[data-zine-select]');
  if (!select) return;

  const forSale = zines.filter(z => z.available);
  if (!select.options.length) {
    select.innerHTML = forSale.map(z =>
      `<option value="${esc(z.title)}" data-price="${z.price}">${esc(z.title)}, ${z.price.toLocaleString('ru-RU')} ₽</option>`).join('');
  }

  const want = new URLSearchParams(location.search).get('zine');
  const found = forSale.find(z => z.slug === want);
  if (found) select.value = found.title;

  const total = document.querySelector('[data-order-total]');
  const qty = document.getElementById('qty');
  if (!total || !qty) return;

  // Человек выбирает количество до двадцати штук и до этого места
  // нигде не видел, во сколько ему обойдётся заказ.
  const draw = () => {
    const price = Number(select.selectedOptions[0]?.dataset.price || 0);
    const n = Number(qty.value);
    if (!price || !Number.isInteger(n) || n < 1) { total.textContent = ''; return; }
    const money = (v) => v.toLocaleString('ru-RU');
    total.innerHTML = n === 1
      ? `К оплате <b>${money(price)} ₽</b> плюс доставка.`
      : `${money(price)} ₽ × ${n} шт. — к оплате <b>${money(price * n)} ₽</b> плюс доставка.`;
  };

  select.addEventListener('change', draw);
  qty.addEventListener('input', draw);
  draw();
}

/** Издание, которого нет в продаже, приходило по ссылке молча подменённым.
 *  Здесь ничего не подменяем: если slug не найден, остаётся первый вариант,
 *  а человек видит это в поле — оно заполнено и подписано. */

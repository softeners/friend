/* ═══════════════════════════════════════════════════════════
   ДРУГ — страница героя (hero.html?slug=...)
   ═══════════════════════════════════════════════════════════ */

import { heroes, regions, issues } from './data.js';
import { photo, esc, param, ROOT } from './ui.js';

export function initHero() {
  const root = document.querySelector('[data-hero]');
  if (!root) return;

  const h = heroes.find(x => x.slug === param('slug')) || heroes[0];
  if (!h) return;

  const region = regions.find(r => r.slug === h.region);
  const issue = issues.find(i => i.slug === h.issue);
  document.title = `${h.name}. Выпуск «${region ? region.short : ''}». «Друг»`;
  document.querySelector('meta[name="description"]')?.setAttribute('content', `${h.name}, ${h.role}. ${h.lead}`);

  const plant = h.plant === 'electro' ? 'Электротехнический завод' : 'Фарфоровый завод';
  const quotes = (h.quotes || []).map(q => `
      <blockquote class="quote-block reveal">
        <p class="quote">«${esc(q)}»</p>
        <span class="quote__author">${esc(h.name)}</span>
      </blockquote>`).join('');

  const others = heroes.filter(x => x.issue === h.issue && x.slug !== h.slug && x.plant === h.plant).slice(0, 3);

  root.innerHTML = `
    <nav class="crumbs" aria-label="Хлебные крошки">
      <a href="${ROOT}archive.html">Истории</a>
      <span aria-hidden="true">/</span>
      ${issue && issue.published ? `<a href="${ROOT}${issue.url}">Выпуск «${esc(issue.title)}»</a>` : esc(region ? region.short : '')}
    </nav>

    <header class="hero-doc__head">
      <div>
        <span class="eyebrow">ДРУГ <span class="eyebrow__rest">Герой выпуска</span></span>
        <h1 class="h1 hero-doc__name">${esc(h.name)}</h1>
        <p class="lead">${esc(h.lead)}</p>
        <dl class="meta">
          <div class="meta__item"><dt>Где живет</dt><dd>${esc(h.place)}</dd></div>
          <div class="meta__item"><dt>Чем занимается</dt><dd>${esc(h.role)}</dd></div>
          <div class="meta__item"><dt>Где работал</dt><dd>${esc(plant)}</dd></div>
        </dl>
      </div>
      <figure class="hero-doc__portrait">
        <div class="ph ph--3x4">
          ${photo(h.photo, h.portrait ? h.name : `${plant}, Сысерть`, { sizes: '(max-width: 860px) 92vw, 38vw', eager: true, big: true })}
        </div>
        ${h.portrait ? '' : `<figcaption class="ph__caption">${esc(plant)}. Фото из выпуска</figcaption>`}
      </figure>
    </header>

    <section class="hero-doc__quotes" aria-label="Истории с участием героя">
      <h2 class="h2">Истории с участием героя</h2>
      ${quotes}
    </section>

    <section class="hero-doc__more">
      <h2 class="h2">Все материалы</h2>
      <div class="btn-row">
        ${issue && issue.published ? `<a class="btn btn--primary" href="${ROOT}${issue.url}">Выпуск «${esc(issue.title)}»</a>` : ''}
        <a class="btn btn--ghost" href="${ROOT}zines/sysert/">Листать журнал</a>
      </div>
      ${others.length ? `<div class="grid grid--3 hero-grid" style="margin-top:var(--s-5)">
        ${others.map(o => `<a class="card hero-card" href="${ROOT}hero.html?slug=${o.slug}">
          <span class="hero-card__role">${esc(o.role)}</span>
          <h3 class="card__title">${esc(o.name)}</h3></a>`).join('')}
      </div>` : ''}
    </section>

    <p class="hero-doc__note">Интервью опубликовано с согласия героя. Если нужно что-то поправить, <a href="${ROOT}contacts.html">напишите нам</a>.</p>`;
}

/* ═══════════════════════════════════════════════════════════
   ДРУГ — формы: валидация, отправка, состояния

   ┌─────────────────────────────────────────────────────────┐
   │  КУДА ПРИХОДЯТ ЗАЯВКИ                                   │
   │                                                         │
   │  Заведите форму на formspree.io (или getform.io),       │
   │  скопируйте её адрес и вставьте ниже:                   │
   │                                                         │
   │    const FORM_ENDPOINT = 'https://formspree.io/f/xxxx'; │
   │                                                         │
   │  Пока стоит null — формы работают в демо-режиме:        │
   │  проверяют поля, показывают экран «принято»,            │
   │  но никуда не отправляют (payload видно в консоли).     │
   │                                                         │
   │  Загрузка файлов у Formspree работает на платном        │
   │  тарифе. На бесплатном фотографии придут ссылкой —      │
   │  поле «ссылка на облако» есть в форме героя.            │
   └─────────────────────────────────────────────────────────┘
   ═══════════════════════════════════════════════════════════ */

import { regions } from './data.js';

const FORM_ENDPOINT = null;

const MAX_FILES = 3;
const MAX_SIZE = 10 * 1024 * 1024;          // 10 МБ на файл
const OK_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/heic'];

/* ── Проверки одного поля ──────────────────────────────────── */
function fieldError(el) {
  const v = (el.value || '').trim();
  const label = el.dataset.label || 'это поле';

  if (el.type === 'checkbox') {
    return el.required && !el.checked ? el.dataset.errorRequired || 'Без этого согласия заявку принять нельзя' : '';
  }
  if (el.required && !v) return `Заполните ${label}`;
  if (!v) return '';

  if (el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) {
    return 'Проверьте адрес, похоже, тут опечатка';
  }
  if (el.type === 'tel' && v.replace(/\D/g, '').length < 10) {
    return 'Телефон коротковат, нужно десять или одиннадцать цифр';
  }
  if (el.type === 'number') {
    const n = Number(v);
    const min = el.min !== '' ? Number(el.min) : -Infinity;
    const max = el.max !== '' ? Number(el.max) : Infinity;
    if (Number.isNaN(n)) return 'Сюда нужно число';
    if (n < min || n > max) return `Подходит число от ${el.min} до ${el.max}`;
  }
  if (el.minLength > 0 && v.length < el.minLength) {
    return `Пока коротковато. Нужно хотя бы ${el.minLength} символов, сейчас ${v.length}`;
  }
  return '';
}

function showError(el, msg) {
  // .check вложен в .field, поэтому ищем именно .field — блок ошибки лежит там
  const box = (el.closest('.field') || el.closest('.check'))?.querySelector('.field__error');
  if (box) box.textContent = msg;
  if (msg) el.setAttribute('aria-invalid', 'true');
  else el.removeAttribute('aria-invalid');
  return !msg;
}

function validateField(el) {
  return showError(el, fieldError(el));
}

/** Поля внутри выключенного блока (согласие представителя) не проверяем. */
function activeFields(form) {
  return [...form.querySelectorAll('input, textarea, select')].filter(el => {
    if (el.type === 'file' || el.type === 'hidden' || el.disabled) return false;
    const guardian = el.closest('.guardian');
    return !guardian || guardian.classList.contains('is-open');
  });
}

/* ── Загрузка фотографий ───────────────────────────────────── */
function initUpload(form) {
  const box = form.querySelector('[data-upload]');
  if (!box) return null;

  const input = box.querySelector('input[type="file"]');
  const list = box.querySelector('.upload__list');
  const err = box.parentElement.querySelector('.field__error');
  let files = [];

  const draw = () => {
    list.innerHTML = files.map((f, i) => `
      <span class="upload__file">
        ${f.name.replace(/[<>&]/g, '')} · ${(f.size / 1048576).toFixed(1)} МБ
        <button type="button" class="upload__remove" data-i="${i}"
                aria-label="Убрать файл ${f.name.replace(/["<>&]/g, '')}">×</button>
      </span>`).join('');
  };

  const add = (incoming) => {
    const problems = [];
    for (const f of incoming) {
      if (files.length >= MAX_FILES) { problems.push(`Больше ${MAX_FILES} фото не нужно, выберите самые важные`); break; }
      if (!OK_TYPES.includes(f.type)) { problems.push(`«${f.name}» не похож на картинку. Подойдёт JPG, PNG, WEBP или HEIC`); continue; }
      if (f.size > MAX_SIZE) { problems.push(`«${f.name}» весит ${(f.size / 1048576).toFixed(1)} МБ, а больше десяти нельзя`); continue; }
      files.push(f);
    }
    err.textContent = problems[0] || '';
    draw();
  };

  input.addEventListener('change', () => { add([...input.files]); input.value = ''; });

  list.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-i]');
    if (!btn) return;
    files.splice(Number(btn.dataset.i), 1);
    err.textContent = '';
    draw();
  });

  ['dragenter', 'dragover'].forEach(t => box.addEventListener(t, (e) => {
    e.preventDefault(); box.classList.add('is-over');
  }));
  ['dragleave', 'drop'].forEach(t => box.addEventListener(t, () => box.classList.remove('is-over')));
  box.addEventListener('drop', (e) => { e.preventDefault(); add([...e.dataTransfer.files]); });

  return () => files;
}

/* ── Список регионов в форме заявки ────────────────────────
   Берём из data.js, чтобы список нигде не расходился.        */
function initRegionSelect(form) {
  const sel = form.querySelector('[data-region-select]');
  if (!sel) return;
  sel.innerHTML = '<option value="" disabled selected>Выберите регион</option>'
    + regions.map(r => `<option value="${r.name}">${r.name}</option>`).join('')
    + '<option value="Другой регион">Другой регион</option>';
}

/* ── Счётчик символов у длинных ответов ────────────────────── */
function initCounters(form) {
  form.querySelectorAll('[data-count-for]').forEach(out => {
    const el = form.querySelector('#' + out.dataset.countFor);
    if (!el) return;
    const max = Number(el.getAttribute('maxlength')) || 0;
    const draw = () => {
      const n = el.value.length;
      out.textContent = `${n} / ${max}`;
      out.classList.toggle('is-full', max && n >= max);
    };
    el.addEventListener('input', draw);
    draw();
  });
}

/* ── Блок согласия законного представителя ─────────────────── */
function initGuardian(form) {
  const age = form.querySelector('[data-age]');
  const block = form.querySelector('.guardian');
  if (!age || !block) return;

  const sync = () => {
    const n = Number(age.value);
    const minor = age.value !== '' && n > 0 && n < 18;
    block.classList.toggle('is-open', minor);
    block.querySelectorAll('input, textarea').forEach(el => {
      el.disabled = !minor;
      if (!minor) { el.removeAttribute('aria-invalid'); showError(el, ''); }
    });
  };

  age.addEventListener('input', sync);
  age.addEventListener('change', sync);
  sync();
}

/* ── Отправка ──────────────────────────────────────────────── */
async function send(form, getFiles) {
  const data = new FormData(form);
  data.delete('photos');
  (getFiles ? getFiles() : []).forEach((f, i) => data.append(`photo_${i + 1}`, f, f.name));
  data.append('_subject', form.dataset.subject || 'Заявка с сайта «ДРУГ»');

  if (!FORM_ENDPOINT) {
    console.info('[ДРУГ] Демо-режим: FORM_ENDPOINT не задан. Заявка не отправлена.',
      Object.fromEntries([...data.entries()].map(([k, v]) => [k, v instanceof File ? `файл ${v.name}` : v])));
    await new Promise(r => setTimeout(r, 600));
    return;
  }

  const res = await fetch(FORM_ENDPOINT, { method: 'POST', body: data, headers: { Accept: 'application/json' } });
  if (!res.ok) throw new Error(`Сервер ответил ${res.status}`);
}

/* ── Сборка ────────────────────────────────────────────────── */
export function initForms() {
  document.querySelectorAll('form[data-form]').forEach(form => {
    const getFiles = initUpload(form);
    initRegionSelect(form);
    initCounters(form);
    initGuardian(form);

    const btn = form.querySelector('[data-submit]');
    const status = form.querySelector('[data-status]');
    const sent = document.querySelector(`[data-sent="${form.dataset.form}"]`);
    const btnLabel = btn ? btn.textContent : '';

    form.addEventListener('blur', (e) => {
      if (e.target.matches('input, textarea, select')) validateField(e.target);
    }, true);

    form.addEventListener('input', (e) => {
      // ошибку убираем сразу, как только человек начал исправлять
      if (e.target.hasAttribute('aria-invalid')) validateField(e.target);
    });

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      status.className = 'form__status';
      status.textContent = '';

      const fields = activeFields(form);
      const bad = fields.filter(el => !validateField(el));

      if (bad.length) {
        status.className = 'form__status form__status--error';
        status.textContent = bad.length === 1
          ? 'Одно поле осталось незаполненным, оно подсвечено выше.'
          : `Осталось поправить ${bad.length} полей, они подсвечены выше.`;
        bad[0].focus();
        bad[0].scrollIntoView({ block: 'center', behavior: 'smooth' });
        return;
      }

      btn.disabled = true;
      btn.textContent = 'Отправляем…';
      status.textContent = '';

      try {
        await send(form, getFiles);
        form.classList.add('is-sent');
        sent?.classList.add('is-open');
        sent?.setAttribute('tabindex', '-1');
        sent?.focus();
        sent?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } catch (err) {
        btn.disabled = false;
        btn.textContent = btnLabel;
        status.className = 'form__status form__status--error';
        status.textContent = 'Заявка не ушла, похоже, пропала связь. Попробуйте ещё раз через минуту. '
          + 'Если не получится, напишите нам на почту sycheva.alina.2000@bk.ru';
        console.error(err);
      }
    });
  });
}

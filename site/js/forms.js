/* ═══════════════════════════════════════════════════════════
   ДРУГ — формы: валидация, отправка, состояния

   ┌─────────────────────────────────────────────────────────┐
   │  КУДА ПРИХОДЯТ ЗАЯВКИ                                   │
   │                                                         │
   │  Заведите форму на приёмнике заявок, скопируйте её      │
   │  адрес и впишите его в _build/shell.py:                 │
   │                                                         │
   │    FORM_ENDPOINT = 'https://…/f/xxxx'                   │
   │                                                         │
   │  и пересоберите страницы (python3 _build/build.py).     │
   │  Адрес попадает в <html data-form-endpoint> и его       │
   │  подхватывает этот файл.                                │
   │                                                         │
   │  Пока адрес пуст, формы НЕ показывают «заявка принята». │
   │  Вместо этого человек видит честный экран: форма ещё    │
   │  не подключена, вот собранный текст заявки, вот кнопка  │
   │  скопировать и адрес, куда его отправить. Так заявка    │
   │  не пропадает и никто не уходит с ложным ожиданием      │
   │  ответа в течение десяти рабочих дней.                  │
   └─────────────────────────────────────────────────────────┘
   ═══════════════════════════════════════════════════════════ */

import { regions, contacts } from './data.js';

/* Адрес приёмника заявок. Основной источник — _build/shell.py.
   Строку ниже можно заполнить напрямую, если собирать страницы неудобно. */
const FORM_ENDPOINT = document.documentElement.dataset.formEndpoint || null;

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

  // Браузер сам обнуляет значение числового поля, если туда ввели буквы.
  // Без этой ветки человек написал «двадцать» и получил «Заполните это поле».
  if (el.validity && el.validity.badInput) {
    return el.type === 'number' ? 'Сюда нужно число, цифрами' : 'Проверьте, что здесь написано';
  }

  if (el.required && !v) return `Заполните ${label}`;
  if (!v) return '';

  if (el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) {
    return 'Проверьте адрес, похоже, тут опечатка';
  }
  if (el.type === 'tel' && v.replace(/\D/g, '').length < 10) {
    return 'Телефон коротковат, нужно десять или одиннадцать цифр';
  }
  // Ссылку принимаем и голым доменом, и как @ник: в форме прямо так и просят
  if (el.type === 'url' && !/^(@[\w.]{3,}|(https?:\/\/)?[\w-]+(\.[\w-]+)+(\/\S*)?)$/i.test(v)) {
    return 'Похоже, это не ссылка. Подойдёт vk.com/…, t.me/… или @ник';
  }
  if (el.type === 'number') {
    const n = Number(v);
    const min = el.min !== '' ? Number(el.min) : -Infinity;
    const max = el.max !== '' ? Number(el.max) : Infinity;
    if (Number.isNaN(n)) return 'Сюда нужно число';
    if (n < min || n > max) return `Подходит число от ${el.min} до ${el.max}`;
    // Шаг 1 означает штуки. Заказ на 2,5 экземпляра исполнить нельзя.
    if ((el.step === '' || el.step === '1') && !Number.isInteger(n)) return 'Нужно целое число';
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

  const clean = (s) => String(s).replace(/[<>&"]/g, '');

  const draw = () => {
    list.innerHTML = files.map((f, i) => `
      <span class="upload__file">
        ${clean(f.name)} · ${(f.size / 1048576).toFixed(1)} МБ
        <button type="button" class="upload__remove" data-i="${i}"
                aria-label="Убрать файл ${clean(f.name)}">×</button>
      </span>`).join('');
  };

  const same = (a, b) => a.name === b.name && a.size === b.size && a.lastModified === b.lastModified;

  const add = (incoming) => {
    // Показываем ВСЕ причины, а не первую: человек выбрал шесть файлов,
    // три отвалились, и одно сообщение не объясняет, какие именно и почему.
    const problems = [];
    let overflow = 0;
    for (const f of incoming) {
      if (files.length >= MAX_FILES) { overflow++; continue; }
      if (files.some(x => same(x, f))) { problems.push(`«${clean(f.name)}» уже в списке`); continue; }
      if (!OK_TYPES.includes(f.type)) { problems.push(`«${clean(f.name)}» не похож на картинку. Подойдёт JPG, PNG, WEBP или HEIC`); continue; }
      if (f.size > MAX_SIZE) { problems.push(`«${clean(f.name)}» весит ${(f.size / 1048576).toFixed(1)} МБ, а больше десяти нельзя`); continue; }
      files.push(f);
    }
    if (overflow) {
      problems.push(overflow === 1
        ? 'Один файл не поместился: больше трёх фото не нужно'
        : `Ещё ${overflow} файла не поместились: больше трёх фото не нужно`);
    }
    if (err) err.textContent = problems.join('. ');
    draw();
  };

  input.addEventListener('change', () => { add([...input.files]); input.value = ''; });

  list.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-i]');
    if (!btn) return;
    files.splice(Number(btn.dataset.i), 1);
    if (err) err.textContent = '';
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
   Разметку впечатывает build.py, чтобы форму можно было отправить
   и без скрипта. Здесь только достраиваем, если её почему-то нет.  */
function initRegionSelect(form) {
  const sel = form.querySelector('[data-region-select]');
  if (!sel || sel.options.length > 1) return;
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

/* ── Заявка человеческим текстом ───────────────────────────
   Нужна там, где отправить некуда: человек должен видеть, что
   именно он написал, и уметь это забрать одним движением.      */
const CONSENT_LABELS = {
  consent: 'Согласие на обработку персональных данных',
  guardian_consent: 'Согласие законного представителя',
};

function asText(form, data, files) {
  const label = (name) => {
    if (CONSENT_LABELS[name]) return CONSENT_LABELS[name];
    const el = form.elements[name];
    const node = el instanceof RadioNodeList ? el[0] : el;
    if (!node) return name;
    const lab = node.closest('.field')?.querySelector('.field__label');
    if (!lab) return name;
    // «по желанию» и звёздочка обязательности — подсказки интерфейса,
    // в тексте заявки им делать нечего
    const copy = lab.cloneNode(true);
    copy.querySelectorAll('.field__opt, .field__req').forEach(n => n.remove());
    return copy.textContent.trim();
  };

  const lines = [];
  for (const [k, v] of data.entries()) {
    if (k.startsWith('_') || v instanceof File) continue;
    const val = CONSENT_LABELS[k] ? 'да' : String(v).trim();
    if (!val) continue;                     // необязательное и незаполненное — молчим
    lines.push(`${label(k)}: ${val}`);
  }
  if (files.length) lines.push(`Фотографии: ${files.map(f => f.name).join(', ')}`);
  return lines.join('\n');
}

/* ── Отправка ──────────────────────────────────────────────── */
async function send(form, data) {
  const res = await fetch(FORM_ENDPOINT, { method: 'POST', body: data, headers: { Accept: 'application/json' } });
  if (!res.ok) throw new Error(`Сервер ответил ${res.status}`);
}

/** Экран «отправлять пока некуда». Показывается вместо ложного «принято». */
function showUnwired(form, text) {
  let box = form.parentElement.querySelector('[data-unwired]');
  if (!box) {
    box = document.createElement('div');
    box.className = 'paper paper--wide unwired';
    box.setAttribute('data-unwired', '');
    box.setAttribute('tabindex', '-1');
    box.innerHTML = `
      <span class="paper__label">Заявка не отправлена</span>
      <p class="paper__title">Приём заявок ещё не подключён</p>
      <p>Мы не хотим показывать «спасибо, ждите ответа», когда письмо никуда не уходит.
         Ниже — то, что вы заполнили. Скопируйте и пришлите нам, мы ответим так же, как на обычную заявку.</p>
      <pre class="unwired__text" tabindex="0"></pre>
      <div class="unwired__actions">
        <button type="button" class="btn btn--primary" data-copy>Скопировать заявку</button>
        <a class="btn btn--outline" href="mailto:${contacts.email}?subject=${encodeURIComponent(form.dataset.subject || 'Заявка с сайта «ДРУГ»')}">Написать на почту</a>
        <a class="btn btn--ghost" href="${contacts.telegram}" target="_blank" rel="noopener">Написать в Telegram</a>
      </div>
      <p class="unwired__note" role="status"></p>`;
    form.parentElement.insertBefore(box, form.nextSibling);

    box.querySelector('[data-copy]').addEventListener('click', async () => {
      const note = box.querySelector('.unwired__note');
      const body = box.querySelector('.unwired__text').textContent;
      try {
        await navigator.clipboard.writeText(body);
        note.textContent = 'Заявка скопирована. Вставьте её в письмо или в Telegram.';
      } catch {
        note.textContent = 'Скопировать не вышло. Выделите текст выше и скопируйте вручную.';
      }
    });
  }
  box.querySelector('.unwired__text').textContent = text;
  box.querySelector('.unwired__note').textContent = '';
  box.focus();
  box.scrollIntoView({ behavior: 'smooth', block: 'center' });
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

    const setStatus = (text, kind = '') => {
      if (!status) return;
      status.className = kind ? `form__status form__status--${kind}` : 'form__status';
      status.textContent = text;
    };

    form.addEventListener('blur', (e) => {
      if (e.target.matches('input, textarea, select')) validateField(e.target);
    }, true);

    form.addEventListener('input', (e) => {
      // ошибку убираем сразу, как только человек начал исправлять
      if (e.target.hasAttribute('aria-invalid')) validateField(e.target);
    });

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      setStatus('');

      const fields = activeFields(form);
      const bad = fields.filter(el => !validateField(el));

      if (bad.length) {
        setStatus(bad.length === 1
          ? 'Одно поле осталось незаполненным, оно подсвечено выше.'
          : `Осталось поправить ${bad.length} полей, они подсвечены выше.`, 'error');
        bad[0].focus();
        bad[0].scrollIntoView({ block: 'center', behavior: 'smooth' });
        return;
      }

      const files = getFiles ? getFiles() : [];
      const data = new FormData(form);
      data.delete('photos');
      files.forEach((f, i) => data.append(`photo_${i + 1}`, f, f.name));
      data.append('_subject', form.dataset.subject || 'Заявка с сайта «ДРУГ»');

      if (!FORM_ENDPOINT) {
        console.warn('[ДРУГ] FORM_ENDPOINT не задан: заявка никуда не отправлена. '
          + 'Впишите адрес приёмника в _build/shell.py и пересоберите страницы.');
        showUnwired(form, asText(form, data, files));
        return;
      }

      if (btn) { btn.disabled = true; btn.textContent = 'Отправляем…'; }

      try {
        await send(form, data);
        form.classList.add('is-sent');
        sent?.classList.add('is-open');
        sent?.setAttribute('tabindex', '-1');
        sent?.focus();
        sent?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } catch (err) {
        if (btn) { btn.disabled = false; btn.textContent = btnLabel; }
        setStatus('Заявка не ушла, похоже, пропала связь. Попробуйте ещё раз через минуту. '
          + `Если не получится, напишите нам на почту ${contacts.email}`, 'error');
        console.error(err);
      }
    });
  });
}

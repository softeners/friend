/* ═══════════════════════════════════════════════════════════
   ДРУГ — пример зина на странице zines.html.
   Карточка раскрывается по кнопке, и только тогда внутри
   создаётся iframe с книжкой: при обычной загрузке страницы
   тяжёлые развороты не качаются.
   ═══════════════════════════════════════════════════════════ */

const DUR = 500;

export function initZinePreview() {
  const card = document.querySelector('[data-zine-preview]');
  if (!card) return;

  const openBtn = card.querySelector('[data-zine-open]');
  const closeBtn = card.querySelector('[data-zine-close]');
  const tools = card.querySelector('[data-zine-tools]');
  const stage = card.querySelector('[data-zine-stage]');
  const loading = card.querySelector('[data-zine-loading]');
  const src = card.dataset.src;
  const reduce = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  const openHeight = () => matchMedia('(max-width: 640px)').matches ? '85vh' : '75vh';
  let frame = null;
  let timer = 0;

  // Высоту анимируем явными значениями: от auto к vh CSS-переход не умеет.
  function setHeight(h) { card.style.setProperty('--zp-h', h); }

  function open() {
    clearTimeout(timer);
    setHeight(card.offsetHeight + 'px');
    card.offsetHeight; // фиксируем стартовую высоту перед переходом
    card.classList.add('is-open');
    openBtn.setAttribute('aria-expanded', 'true');
    tools.hidden = false;
    loading.classList.remove('is-hidden');
    setHeight(openHeight());

    frame = document.createElement('iframe');
    frame.className = 'zine-preview__frame';
    frame.src = src;
    frame.title = 'Пример зина «Друг. Сысерть»';
    frame.setAttribute('allow', 'fullscreen');
    frame.setAttribute('allowfullscreen', '');
    frame.addEventListener('load', () => {
      loading.classList.add('is-hidden');
      frame.classList.add('is-ready');
    }, { once: true });
    stage.appendChild(frame);
    closeBtn.focus({ preventScroll: true });
  }

  function close() {
    clearTimeout(timer);
    if (frame) { frame.remove(); frame = null; }
    tools.hidden = true;
    const from = card.offsetHeight;
    card.classList.remove('is-open');
    openBtn.setAttribute('aria-expanded', 'false');
    // Конечная высота — высота свёрнутой карточки
    setHeight('auto');
    const to = card.offsetHeight;
    setHeight(from + 'px');
    card.offsetHeight;
    setHeight(to + 'px');
    openBtn.focus({ preventScroll: true });
    timer = setTimeout(() => setHeight('auto'), reduce() ? 0 : DUR);
  }

  // На телефоне при повороте экрана подстраиваем раскрытую высоту
  addEventListener('resize', () => { if (frame) setHeight(openHeight()); });

  openBtn.addEventListener('click', open);
  closeBtn.addEventListener('click', close);
}

/* ═══════════════════════════════════════════════════════════
   ДРУГ — точка входа. Каждый модуль сам проверяет,
   есть ли на странице его разметка, и молча выходит, если нет.
   ═══════════════════════════════════════════════════════════ */

import { initCommon, initReveal } from './ui.js';
import { initMap } from './map.js';
import { initArchive } from './archive.js';
import { initHero } from './hero.js';
import { initIssues } from './issues.js';
import { initForms } from './forms.js';
import { initLightbox } from './lightbox.js';

initCommon();
initMap();
initIssues();
initArchive();
initHero();
initForms();
initLightbox();

// Модули выше дорисовывают разметку, поэтому наблюдателя запускаем ещё раз:
// иначе блоки с классом .reveal, созданные из JS, останутся прозрачными.
initReveal();

# -*- coding: utf-8 -*-
"""
Проверка сайта перед публикацией.

Не заменяет живой прогон в браузере, но ловит то, что ломается чаще всего
и молча: битые ссылки, пропавшую фотографию, разъехавшиеся разметку
и генератор, забытый адрес приёма заявок.

Запуск:

    python3 _build/check.py

Возвращает ненулевой код, если что-то сломано — можно вешать на хук
или запускать перед каждой выкладкой. Предупреждения кода не меняют:
это то, что ещё не доделано, а не то, что сломалось.
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, '..'))

errors = []
warnings = []


def pages():
    out = [f for f in os.listdir(SITE) if f.endswith('.html')]
    notes = os.path.join(SITE, 'notes')
    if os.path.isdir(notes):
        out += [f'notes/{f}' for f in os.listdir(notes) if f.endswith('.html')]
    return sorted(out)


def check_links():
    """Каждый href и src ведёт к существующему файлу."""
    n = 0
    for p in pages():
        base = os.path.dirname(os.path.join(SITE, p))
        html = open(os.path.join(SITE, p), encoding='utf-8').read()
        for m in re.finditer(r'(?:href|src|srcset|imagesrcset)="([^"]+)"', html):
            for part in m.group(1).split(','):
                url = part.strip().split(' ')[0]
                if not url or url.startswith(('http', 'mailto:', 'tel:', 'data:', '#')):
                    continue
                n += 1
                path = url.split('#')[0].split('?')[0]
                if not os.path.exists(os.path.normpath(os.path.join(base, path))):
                    errors.append(f'{p}: ссылка в никуда — {url}')
    print(f'  ссылок и путей проверено: {n}')


def check_photos():
    """У каждого слага из data.js есть все три размера и запасной JPEG."""
    src = open(os.path.join(SITE, 'js', 'data.js'), encoding='utf-8').read()
    slugs = set()
    for m in re.finditer(r"\b(?:cover|photo)\s*:\s*'([^']+)'", src):
        slugs.add(m.group(1))
    for m in re.finditer(r'gallery\s*:\s*\[([^\]]*)\]', src, re.S):
        slugs.update(re.findall(r"'([^']+)'", m.group(1)))
    # formatLabels содержит photo: 'Фото' — это подпись, а не слаг
    slugs = {s for s in slugs if re.fullmatch(r'[a-z0-9-]+', s)}

    have = set(os.listdir(os.path.join(SITE, 'assets', 'img', 'photo')))
    for s in sorted(slugs):
        missing = [v for v in (f'{s}-600.webp', f'{s}-1200.webp', f'{s}-1200.jpg') if v not in have]
        if missing:
            errors.append(f'js/data.js: для «{s}» нет файлов — {", ".join(missing)}')
    print(f'  фотографий из data.js проверено: {len(slugs)}')


def check_ids():
    """Повторяющийся id ломает и переходы по якорю, и связь label с полем."""
    for p in pages():
        html = open(os.path.join(SITE, p), encoding='utf-8').read()
        ids = re.findall(r'\sid="([^"]+)"', html)
        dupes = {i for i in ids if ids.count(i) > 1}
        for d in sorted(dupes):
            errors.append(f'{p}: id «{d}» встречается больше одного раза')
    print(f'  страниц на дубли id: {len(pages())}')


def check_build():
    """Разметка совпадает с генератором.

    Если кто-то правил HTML руками, следующая сборка сотрёт правки.
    Лучше узнать об этом сейчас, чем после выкладки.
    """
    before = {p: open(os.path.join(SITE, p), 'rb').read() for p in pages()}
    r = subprocess.run([sys.executable, 'build.py'], cwd=HERE, capture_output=True, text=True)
    if r.returncode:
        errors.append(f'сборка упала: {r.stderr.strip()[:300]}')
        return
    changed = [p for p in pages() if before.get(p) != open(os.path.join(SITE, p), 'rb').read()]
    if changed:
        errors.append('разметка разошлась с генератором, сборка её перезаписала: '
                      + ', '.join(changed[:6])
                      + ' — перенесите правки в _build/pages_*.py')
    print(f'  сборка идемпотентна: {"нет" if changed else "да"}')


def check_todo():
    """То, что ещё не доделано. Не ошибка, но публиковать с этим не стоит."""
    shell = open(os.path.join(HERE, 'shell.py'), encoding='utf-8').read()
    m = re.search(r"^FORM_ENDPOINT = '([^']*)'", shell, re.M)
    if m and not m.group(1):
        warnings.append('FORM_ENDPOINT пуст: формы честно скажут об этом человеку, '
                        'но заявки не отправляются (см. site/README.md, раздел 1)')

    data = open(os.path.join(SITE, 'js', 'data.js'), encoding='utf-8').read()
    todos = len(re.findall(r'//\s*TODO', data))
    if todos:
        warnings.append(f'js/data.js: {todos} пометок TODO — имена и цитаты героев ещё заглушки')

    privacy = open(os.path.join(SITE, 'privacy.html'), encoding='utf-8').read()
    if 'уточняются' in privacy:
        warnings.append('privacy.html: реквизиты оператора не заполнены')

    if 'softeners.github.io' in shell:
        warnings.append('SITE_URL указывает на GitHub Pages: при переезде на свой домен '
                        'поменяйте его и пересоберите, иначе превью ссылок и canonical '
                        'будут вести на старый адрес')


def main():
    print('Проверяю сайт «ДРУГ»\n')
    for fn in (check_links, check_photos, check_ids, check_build):
        fn()
    check_todo()

    print()
    if errors:
        print(f'Сломано ({len(errors)}):')
        for e in errors:
            print(f'  ✗ {e}')
    else:
        print('Сломанного не нашёл.')

    if warnings:
        print(f'\nНе доделано ({len(warnings)}):')
        for w in warnings:
            print(f'  • {w}')

    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())

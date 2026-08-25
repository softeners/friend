# -*- coding: utf-8 -*-
"""
Подрезает латинские начертания под нужды сайта.

Зачем. Шрифты — это почти весь вес страницы: 266–396 КБ из ~450 КБ трафика.
Разметку, стили и скрипты хостинг отдаёт сжатыми, а woff2 сжат уже внутри,
и gzip с него ничего не снимет. Единственный способ сделать первую загрузку
легче — везти меньше глифов.

Кириллические файлы не трогаем: там ровно то, что нужно. Латинские приходят
от Google Fonts с запасом на сто с лишним языков, а на сайте из латиницы
только ASCII, ©, «», · и ×.

Что оставляем. Не «только то, что встретилось», а всю Latin-1 плюс типографскую
пунктуацию: люди вписывают в формы имена и адреса, и Jürgen или Peña не должны
проваливаться в системный шрифт.

Запуск (нужен fontTools: pip3 install fonttools brotli):

    python3 _build/fonts.py            # подрезать
    python3 _build/fonts.py --check    # только показать, что получится

Скрипт идемпотентен: повторный запуск на уже подрезанном файле ничего
не меняет. Если понадобится начертание с более широкой латиницей, скачайте
файл заново с Google Fonts и добавьте нужные диапазоны в KEEP.
"""

import glob
import os
import subprocess
import sys

FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'fonts')

# Latin-1 целиком + то, что перечислено в unicode-range латинских @font-face
# в css/fonts.css. Диапазоны должны совпадать с ним, иначе браузер попросит
# файл ради символа, которого в нём уже нет.
KEEP = ','.join([
    'U+0020-00FF',                      # ASCII и Latin-1: ü, ñ, é, ©, «», ×
    'U+0131', 'U+0152-0153',            # ı, Œ œ — есть в unicode-range Google
    'U+02BB-02BC', 'U+02C6', 'U+02DA', 'U+02DC',
    'U+0304', 'U+0308', 'U+0329',       # комбинируемые диакритики
    'U+2000-2027',                      # пробелы разной ширины, тире, кавычки, многоточие
    'U+2030-205E',                      # ‰, †, ‹›
    'U+2074', 'U+2191', 'U+2193',       # ⁴, стрелки — есть в исходном наборе Google
    'U+20AC', 'U+2122', 'U+2212', 'U+2215',
    'U+FEFF', 'U+FFFD',
])

FEATURES = 'kern,liga,calt'


def main():
    check = '--check' in sys.argv
    files = sorted(glob.glob(os.path.join(FONTS, '*-latin.woff2')))
    if not files:
        raise SystemExit('Латинских начертаний не найдено — проверьте assets/fonts/')

    before = after = 0
    for src in files:
        tmp = src + '.tmp'
        subprocess.run([sys.executable, '-m', 'fontTools.subset', src,
                        f'--unicodes={KEEP}', f'--layout-features={FEATURES}',
                        '--flavor=woff2', '--output-file=' + tmp],
                       check=True, capture_output=True)
        a, b = os.path.getsize(src), os.path.getsize(tmp)
        before += a
        after += b
        name = os.path.basename(src)
        print(f'  {name:30s} {a / 1024:6.1f} → {b / 1024:6.1f} КБ')
        if check or b >= a:
            os.remove(tmp)
        else:
            os.replace(tmp, src)

    saved = before - after
    verb = 'сэкономит' if check else 'сэкономлено'
    print(f'\n{verb}: {saved / 1024:.0f} КБ из {before / 1024:.0f} КБ латиницы')
    if check:
        print('Это была примерка. Запустите без --check, чтобы применить.')


if __name__ == '__main__':
    main()

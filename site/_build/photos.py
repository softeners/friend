# -*- coding: utf-8 -*-
"""
Готовит фотографии для сайта.

Берёт оригиналы из материалы/photo-source/ и складывает в
site/assets/img/photo/ три размера в WebP плюс запасной JPEG.
Попутно снимает EXIF: там лежат GPS-координаты съёмки и модель камеры.

Запуск из корня проекта:
    python3 site/_build/photos.py

Файлы, которые уже обработаны, пропускаются — можно запускать повторно
после того, как добавили несколько новых кадров.
"""

import json
import os
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit('Нужна библиотека Pillow. Установите её:  pip3 install Pillow')

Image.MAX_IMAGE_PIXELS = None

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'материалы', 'photo-source')
DST = os.path.join(ROOT, 'site', 'assets', 'img', 'photo')

WIDTHS = (2000, 1200, 600)      # 1200 дополнительно сохраняется в JPEG
QUALITY_WEBP = 82
QUALITY_JPEG = 80

# Понятные имена вместо номеров с телефона.
# Слева — имя файла в photo-source, справа — slug для data.js.
RENAME = {
    'IMG_20220127_155623_159_(2).JPG': 'sunset-ridge',
    'IMG_20220127_160026_928_(2).jpg': 'mountain-range',
    'IMG_20220322_143516_380_(1)_(2).jpg': 'village-cat',
    'IMG_20220624_214458_996_(4).jpg': 'golden-valley',
    'IMG_3493_(2).JPG': 'kids-group',
    'IMG_3496_(2).JPG': 'child-portrait',
    'IMG_3498_(2).JPG': 'field-girl',
    'IMG_3507_(2).JPG': 'carousel',
}


def process(filename, force=False):
    slug = RENAME.get(filename, os.path.splitext(filename)[0].lower())
    done = os.path.join(DST, f'{slug}-1200.jpg')
    if os.path.exists(done) and not force:
        return slug, None

    im = Image.open(os.path.join(SRC, filename))
    im = ImageOps.exif_transpose(im).convert('RGB')   # поворот применяем, EXIF выбрасываем
    w, h = im.size

    for width in WIDTHS:
        out = im.copy()
        # не растягиваем кадр, если оригинал меньше нужной ширины
        out.thumbnail((min(width, w), 10 ** 6), Image.LANCZOS)
        out.save(os.path.join(DST, f'{slug}-{width}.webp'), 'WEBP',
                 quality=QUALITY_WEBP, method=5)
        if width == 1200:
            out.save(os.path.join(DST, f'{slug}-1200.jpg'), 'JPEG',
                     quality=QUALITY_JPEG, optimize=True, progressive=True)

    return slug, (w, h)


def main():
    force = '--force' in sys.argv
    if not os.path.isdir(SRC):
        sys.exit(f'Не нашёл папку с оригиналами: {SRC}')
    os.makedirs(DST, exist_ok=True)

    meta_path = os.path.join(DST, '_meta.json')
    meta = json.load(open(meta_path, encoding='utf-8')) if os.path.exists(meta_path) else {}

    files = sorted(f for f in os.listdir(SRC) if f.lower().endswith(('.jpg', '.jpeg', '.png')))
    new = skipped = 0

    for f in files:
        try:
            slug, size = process(f, force)
        except Exception as e:                      # noqa: BLE001 — сообщаем и идём дальше
            print(f'  ошибка: {f} — {e}')
            continue
        if size is None:
            skipped += 1
            continue
        meta[slug] = {'w': size[0], 'h': size[1], 'src': f}
        new += 1
        print(f'  {slug:22s} {size[0]}×{size[1]}')

    json.dump(meta, open(meta_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    total = sum(os.path.getsize(os.path.join(DST, x)) for x in os.listdir(DST))
    print(f'\nОбработано: {new}, пропущено (уже готовы): {skipped}')
    print(f'Всего в assets/img/photo: {total / 1048576:.1f} МБ')
    if new:
        print('\nТеперь можно указывать эти slug в site/js/data.js')


if __name__ == '__main__':
    main()

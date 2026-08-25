# -*- coding: utf-8 -*-
"""
Читает js/data.js во время сборки.

Зачем. Списки в обязательных <select> (регион проживания, издание) раньше
приходили с сервера пустыми и наполнялись скриптом. Если модуль не загрузился,
человек видел обязательное поле без единого варианта и не мог отправить форму.
Теперь варианты впечатываются в разметку.

Дублировать данные в Python нельзя: единственный источник — js/data.js,
иначе списки разойдутся при первой же правке. Поэтому читаем оттуда.
Разбор нарочно тупой: ищем поля по именам внутри объектов массива.
Если структура data.js изменится, сборка упадёт с понятной ошибкой,
а не соберёт страницу с пустым списком.
"""

import os
import re

DATA_JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'js', 'data.js')


def _array(name):
    """Тело массива `export const <name> = [ ... ];` целиком."""
    src = open(DATA_JS, encoding='utf-8').read()
    m = re.search(r'export const %s = \[(.*?)\n\];' % name, src, re.S)
    if not m:
        raise RuntimeError(f'В js/data.js не найден массив {name} — поправьте site_data.py')
    return m.group(1)


def _objects(body):
    """Разбивает тело массива на объекты верхнего уровня."""
    out, depth, start = [], 0, None
    for i, ch in enumerate(body):
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                out.append(body[start:i + 1])
    return out


def _field(obj, key):
    m = re.search(r"\b%s:\s*'((?:[^'\\]|\\.)*)'" % key, obj)
    if m:
        return m.group(1).replace("\\'", "'")
    m = re.search(r'\b%s:\s*(true|false|-?\d+(?:\.\d+)?)' % key, obj)
    return m.group(1) if m else None


def regions():
    """[(slug, name)] в порядке из data.js."""
    items = [(_field(o, 'slug'), _field(o, 'name')) for o in _objects(_array('regions'))]
    items = [i for i in items if i[0] and i[1]]
    if not items:
        raise RuntimeError('js/data.js: не разобрались регионы')
    return items


def zines_for_sale():
    """[(slug, title, price)] только те, что продаются."""
    out = []
    for o in _objects(_array('zines')):
        if _field(o, 'available') != 'true':
            continue
        out.append((_field(o, 'slug'), _field(o, 'title'), int(_field(o, 'price') or 0)))
    if not out:
        raise RuntimeError('js/data.js: нет ни одного издания с available: true')
    return out


def region_options():
    opts = ['<option value="" disabled selected>Выберите регион</option>']
    opts += [f'<option value="{name}">{name}</option>' for _, name in regions()]
    opts.append('<option value="Другой регион">Другой регион</option>')
    return '\n                    '.join(opts)


def rub(price):
    """900 → «900», 1200 → «1 200». Пробел неразрывный."""
    return f'{price:,}'.replace(',', '\u00a0')


def zine_options():
    return '\n                    '.join(
        f'<option value="{title}" data-price="{price}">{title}, {rub(price)}\u00a0₽</option>'
        for _, title, price in zines_for_sale())


def first_issue_cover():
    """Обложка первой карточки выпусков — она же самый крупный элемент
    первого экрана, то есть LCP. Возвращает slug или None."""
    for o in _objects(_array('issues')):
        cover = _field(o, 'cover')
        if cover:
            return cover
    return None


def first_zine_cover():
    for o in _objects(_array('zines')):
        cover = _field(o, 'cover')
        if cover:
            return cover
    return None

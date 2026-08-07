# -*- coding: utf-8 -*-
"""
Собирает HTML-страницы сайта «ДРУГ».

Запуск из папки site/_build:
    python3 build.py

Скрипт нужен, только если правите шапку, футер или структуру страниц сразу
везде. Обычные правки текста делаются прямо в готовых HTML-файлах.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pages_a as A
import pages_b as B
import notes as N
import privacy as P

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

FILES = {
    'index.html':              A.INDEX,
    'about.html':              A.ABOUT,
    'issues.html':             A.ISSUES,
    'archive.html':            A.ARCHIVE,
    'hero.html':               A.HERO,
    'expedition.html':         B.EXPEDITION,
    'become-hero.html':        B.BECOME_HERO,
    'become-participant.html': B.BECOME_PARTICIPANT,
    'zines.html':              B.ZINES,
    'partners.html':           B.PARTNERS,
    'news.html':               B.NEWS,
    'faq.html':                B.faq_page(),
    'privacy.html':            P.PRIVACY,
    'contacts.html':           B.CONTACTS,
    'notes/altay.html':        N.ALTAY_NOTES,
}


def main():
    os.makedirs(os.path.join(OUT, 'notes'), exist_ok=True)
    total = 0
    for name, html in FILES.items():
        path = os.path.join(OUT, name)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        total += len(html)
        print(f'  {name:26s} {len(html) / 1024:6.1f} KB')
    print(f'\nГотово: {len(FILES)} страниц, {total / 1024:.0f} KB разметки')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Build the freely accessible book for GitHub Pages."""
from __future__ import annotations
import argparse
import html
import os
from pathlib import Path
import re
import shutil
from urllib.parse import urlsplit
import build as book_build

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'build' / 'public'

SERIES = '''
<section class="section series-section" id="the-series" aria-labelledby="series-heading">
  <p class="eyebrow">The beginning of a series</p>
  <h2 id="series-heading">Mathematics and science, explained through stories</h2>
  <p class="section-intro">I'm Fyodor Amanov, and this is the first book in a planned series of illustrated journeys through mathematics and science. Each book will use stories, pictures, worked examples, and exploration to make challenging ideas easier to understand.</p>
  <div class="features">
    <div class="feature"><h3>The first book is completely free</h3><p>Read every chapter, download the illustrated PDF, and explore all twelve interactive demos. No payment, account, or email address is required. Share it with someone who might enjoy learning this way.</p></div>
    <div class="feature"><h3>More stories are planned</h3><p>I intend to write further books explaining mathematics and science through stories. Future volumes are intended to be paid releases. Topics and publication dates have not yet been announced.</p></div>
    <div class="feature"><h3>Help shape the next journey</h3><p>Which explanation helped you? Which topic would you like to explore next? <a href="https://github.com/FyodorAmanov1/multilinear-algebra-book/issues">Share your thoughts and follow the series on GitHub</a>.</p></div>
  </div>
</section>
'''


def build(base_url: str, pdf: Path) -> None:
    parsed = urlsplit(base_url)
    if parsed.scheme not in ('http', 'https') or not parsed.netloc or parsed.query or parsed.fragment or parsed.username or parsed.password:
        raise ValueError('Provide the full public website URL, including its repository path.')
    base_path = parsed.path.rstrip('/') + '/'
    if not pdf.is_file():
        raise ValueError('Build the complete PDF first: python scripts/build.py all')
    if PUBLIC.resolve() != ROOT.resolve() / 'build' / 'public' or PUBLIC.is_symlink():
        raise ValueError('Unexpected public output directory.')
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True)
    book = book_build.load_json(ROOT / 'content' / 'book.json')
    book.update(base_path=base_path, base_url=base_url.rstrip('/') + '/')
    book_build.SITE = PUBLIC
    shutil.copytree(ROOT / 'assets', PUBLIC / 'assets', ignore=shutil.ignore_patterns('*.pdf', '*.md', '*.txt', '*.json', 'store.js', 'readers.js', 'qr', '__pycache__'))
    chapters = book_build.chapter_metadata()
    pandoc = book_build.find_pandoc()
    for chapter in chapters:
        book_build.generate_chapter_html(book, pandoc, chapter, chapters)
    book_build.generate_answers_html(book, pandoc)
    book_build.generate_demo_pages(book, chapters)
    book_build.generate_static_pages(book, chapters)
    (PUBLIC / 'downloads').mkdir()
    shutil.copy2(pdf, PUBLIC / 'downloads' / 'book.pdf')
    url = html.escape(book['base_url'], quote=True)
    cover = url + 'assets/story/victorian-cover.png'
    social = f'''<link rel="canonical" href="{url}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="A free illustrated journey into mathematics | Fyodor Amanov">
<meta property="og:description" content="Read the complete free first book in a planned series explaining mathematics and science through stories, illustrations, and interactive demos. No signup required.">
<meta property="og:image" content="{cover}">
<meta name="twitter:card" content="summary_large_image">
'''
    for page in PUBLIC.rglob('*.html'):
        text = page.read_text(encoding='utf-8')
        text = text.replace('>Download</a>', '>Free PDF</a>').replace('>Download the book</a>', '>Download the free book</a>')
        text = text.replace('</head>', f'<link rel="stylesheet" href="{base_path}assets/css/store.css">\n</head>')
        if page == PUBLIC / 'index.html':
            text = text.replace('</head>', social + '</head>')
            text = text.replace('An intuitive introduction</p>', 'Book one · The complete first volume is free</p>')
            text = text.replace('A friendly, illustrated Wonderland walk through vectors, tensors, forms, and the ideas that make modern geometry tick.</p>', 'A friendly, illustrated Wonderland walk through vectors, tensors, and forms. The free first volume in a planned series explaining mathematics and science through stories. No signup required.</p>')
            text = re.sub(r'<div class="hero-card">\s*<svg.*?</svg>', f'<div class="hero-card"><img class="store-cover" src="{base_path}assets/story/victorian-cover.png" alt="Illustrated cover of the free first Wonderland mathematics book">', text, count=1, flags=re.DOTALL)
            text = text.replace('  </main>', SERIES + '  </main>')
        if page.parent.name == 'about':
            text = text.replace('  </main>', SERIES + '  </main>')
        text = text.replace('</footer>', f'<p><a href="{base_path}downloads/book.pdf">Download the free first book</a> · <a href="{base_path}#the-series">The planned series</a> · <a href="{base_path}about/">About</a></p>\n</footer>')
        page.write_text(text, encoding='utf-8')
    (PUBLIC / '.nojekyll').write_text('', encoding='utf-8')
    print(f'GitHub Pages website ready: {PUBLIC}\n{len(chapters)} open chapters, twelve demos, full answers, and the complete free PDF.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default=os.environ.get('BOOK_SITE_URL') or book_build.load_json(ROOT / 'content' / 'book.json')['base_url'])
    parser.add_argument('--pdf', type=Path, default=ROOT / 'build' / 'book' / 'main.pdf')
    args = parser.parse_args()
    build(args.base_url, args.pdf)

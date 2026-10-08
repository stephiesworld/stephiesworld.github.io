#!/usr/bin/env python3
"""Build the essays.

Reads content/essays/*.md (front matter: title, date, category, dek, optional order) and writes:
  - writing/<slug>.html         one page per essay
  - the essay list in writing.html  (between <!-- essays:start --> and <!-- essays:end -->)
  - redirect stubs for retired essays, so old links land somewhere useful
  - sitemap.xml

Run after adding or editing an essay:
  .venv/bin/python tools/build_writing.py
First time only:
  python3 -m venv .venv && .venv/bin/pip install markdown
"""
import datetime
import html
import math
import re
from pathlib import Path
from string import Template

try:
    import markdown
except ImportError:
    raise SystemExit('Missing the markdown package. Run:\n  python3 -m venv .venv && .venv/bin/pip install markdown')

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'content' / 'essays'
OUT = ROOT / 'writing'
SITE = 'https://stephiesworld.com'

# Few posts, in `order:`. Field guides are how to deploy agents; notes are how I think.
CATEGORY_ORDER = ['Field guides', 'Notes']

# Retired essays -> where their ideas live now (None = the writing index)
RETIRED = {
    'the-first-pass-by-the-numbers': 'customer-feedback-start-to-finish',
    'why-the-human-stays-in-the-loop': 'customer-feedback-start-to-finish',
    'your-data-is-already-a-graph': 'customer-feedback-start-to-finish',
    'agent-as-factory': 'what-making-things-taught-me',
    'the-dumpling-was-the-stress-test': 'what-making-things-taught-me',
    'eval-cheat-sheet': 'cheat-sheet',
    'harness-cheat-sheet': 'cheat-sheet',
    'who-is-feedback-for': None,
    'building-without-a-spec': None,
    'customer-signal-into-product': None,
    'enterprise-ai-opportunity': None,
    'million-decisions': None,
}

# Reference papers live in writing/ as standalone pages and close out the writing list.
REFERENCE = [
    ('cheat-sheet', 'AI Systems Cheat Sheet', 'harnesses and evals, plainly'),
]

STATIC_PAGES = [('', '1.0'), ('about.html', '0.9'), ('work.html', '0.9'), ('writing.html', '0.9'), ('nyc.html', '0.8'), ('paris.html', '0.8'), ('madrid.html', '0.7'), ('london.html', '0.7'), ('shanghai.html', '0.7'), ('grindelwald.html', '0.6'), ('books.html', '0.8')]

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
          'September', 'October', 'November', 'December']


def parse(path):
    raw = path.read_text(encoding='utf-8')
    meta, body = {}, raw
    m = re.match(r'^---\n(.*?)\n---\n', raw, re.S)
    if m:
        body = raw[m.end():]
        for line in m.group(1).splitlines():
            k, _, v = line.partition(':')
            meta[k.strip()] = v.strip().strip('"').strip("'")
    date = meta.get('date', '')
    dm = re.match(r'(\d{4})-(\d{2})', date)
    return {
        'slug': path.stem,
        'title': meta.get('title', path.stem),
        'raw_date': date,
        'date': f'{MONTHS[int(dm.group(2)) - 1]} {dm.group(1)}' if dm else date,
        'category': meta.get('category', 'Notes'),
        'dek': meta.get('dek', ''),
        'order': int(meta['order']) if meta.get('order', '').isdigit() else None,
        'body': body,
    }


def render(body):
    # Pull inline SVG diagrams out before Markdown sees them, then set them back as plates.
    svgs = []

    def stash(m):
        svgs.append(m.group(0))
        return f'\n\nSVGPLATE{len(svgs) - 1}\n\n'

    body = re.sub(r'<svg\b.*?</svg>', stash, body, flags=re.S)
    out = markdown.markdown(body, extensions=['tables', 'fenced_code', 'sane_lists'])
    for i, svg in enumerate(svgs):
        out = out.replace(f'<p>SVGPLATE{i}</p>', f'<figure class="plate">{svg}</figure>')
    # Diagrams kept as image files get the same plate
    out = re.sub(r'<p>(<img [^>]*>)</p>', r'<figure class="plate">\1</figure>', out)

    # Links written for the old site
    out = re.sub(r'href="/writing/([\w-]+)"', r'href="\1.html"', out)
    out = re.sub(r'href="/([\w-]+-cheat-sheet\.html)"', r'href="\1"', out)
    # Outbound links open in a new tab
    out = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', out)
    return out


def description(body_html):
    for p in re.findall(r'<p>(.*?)</p>', body_html, re.S):
        text = html.unescape(re.sub(r'<[^>]+>', '', p)).strip()
        if len(text) > 60:
            return text if len(text) <= 158 else text[:155].rsplit(' ', 1)[0] + '…'
    return ''


def ordered(essays):
    # By `order:` in front matter when set, otherwise newest first; then grouped by section
    essays = sorted(essays, key=lambda e: e['raw_date'], reverse=True)
    return sorted(essays, key=lambda e: e['order'] if e['order'] is not None else 99)


def main():
    essays = ordered([parse(p) for p in sorted(SRC.glob('*.md'))])
    page = Template((ROOT / 'tools' / 'essay_template.html').read_text(encoding='utf-8'))

    for i, e in enumerate(essays):
        body = render(e['body'])
        words = len(re.sub(r'<svg.*?</svg>|<[^>]+>', ' ', body, flags=re.S).split())
        prev_e = essays[i - 1] if i > 0 else None
        next_e = essays[i + 1] if i + 1 < len(essays) else None
        nav = ''
        if prev_e:
            nav += f'<a class="pn prev" href="{prev_e["slug"]}.html"><span class="label">&larr; previous</span><span class="pt">{html.escape(prev_e["title"])}</span></a>'
        else:
            nav += '<span></span>'
        if next_e:
            nav += f'<a class="pn next" href="{next_e["slug"]}.html"><span class="label">next &rarr;</span><span class="pt">{html.escape(next_e["title"])}</span></a>'
        e['minutes'] = max(1, math.ceil(words / 230))
        e['dek'] = e['dek'] or description(body)
        (OUT / f'{e["slug"]}.html').write_text(page.substitute(
            title=html.escape(e['title']),
            description=html.escape(e['dek']),
            slug=e['slug'],
            num=f'{i + 1:02d}',
            category=html.escape(e['category']),
            date=e['date'],
            minutes=max(1, math.ceil(words / 230)),
            body=body,
            nav=nav,
        ), encoding='utf-8')

    # ─── Writing index: each post with its first diagram as a lit thumbnail ───
    rows = []
    for i, e in enumerate(essays):
        m = re.search(r'<svg\b.*?</svg>', e['body'], re.S)
        thumb = f'<span class="thumb" aria-hidden="true">{m.group(0)}</span>' if m else '<span class="thumb none" aria-hidden="true"></span>'
        rows.append(
            f'        <li class="post"><a href="writing/{e["slug"]}.html">'
            f'<span class="no">{i + 1:02d}</span>'
            f'<span class="txt"><span class="cat label">{html.escape(e["category"])} &middot; {e["minutes"]} min</span>'
            f'<span class="tt">{html.escape(e["title"])}</span><span class="dk">{html.escape(e["dek"])}</span></span>'
            f'{thumb}</a></li>')
    for slug, name, sub in REFERENCE:
        rows.append(
            f'        <li class="ref"><a href="writing/{slug}.html">'
            f'<span class="tt">{name}</span><span class="dk">{sub[0].upper() + sub[1:]}.</span><span class="ar label">&rarr;</span></a></li>')
    index = ROOT / 'writing.html'
    src = index.read_text(encoding='utf-8')
    src = re.sub(r'(<!-- essays:start -->\n).*?(\s*<!-- essays:end -->)',
                 lambda m: m.group(1) + '\n'.join(rows) + m.group(2), src, flags=re.S)
    index.write_text(src, encoding='utf-8')

    # ─── Retired essays: tiny redirect pages ───
    for slug, to in RETIRED.items():
        url = f'{to}.html' if to else '../writing.html'
        canon = f'{SITE}/writing/{to}.html' if to else f'{SITE}/writing.html'
        (OUT / f'{slug}.html').write_text(f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <!-- Retired essay, folded into another. Kept so old links still land. -->
  <title>Writing · Stephie</title>
  <link rel="canonical" href="{canon}">
  <meta http-equiv="refresh" content="0; url={url}">
  <meta name="robots" content="noindex">
  <style>body {{ background: #161a2e; }}</style>
</head>
<body>
  <script>location.replace('{url}');</script>
</body>
</html>
''', encoding='utf-8')

    # ─── Sitemap ───
    today = datetime.date.today().isoformat()
    urls = [(f'{SITE}/{p}', pr) for p, pr in STATIC_PAGES]
    urls += [(f'{SITE}/writing/{e["slug"]}.html', '0.7') for e in essays]
    urls += [(f'{SITE}/writing/{slug}.html', '0.6') for slug, _, _ in REFERENCE]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, pr in urls:
        xml += ['  <url>', f'    <loc>{loc}</loc>', f'    <lastmod>{today}</lastmod>', f'    <priority>{pr}</priority>', '  </url>']
    xml.append('</urlset>')
    (ROOT / 'sitemap.xml').write_text('\n'.join(xml) + '\n', encoding='utf-8')

    print(f'Built {len(essays)} essays, writing.html index, {len(RETIRED)} redirects, sitemap.xml')


if __name__ == '__main__':
    main()

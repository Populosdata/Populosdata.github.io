#!/usr/bin/env python3
"""Build the /resources/ section from _resources/manifest.json.

Articles have a planned `order`, not a date. Each run releases AT MOST ONE article: the
unreleased article with the lowest order number, and only if it is vetted. If that article is
not vetted, nothing is released (a later vetted article does not jump the queue). At most one
article is released per calendar day (UTC), counted from releasedOn: a second run on a day that
already has a release does nothing and says so.
Releasing stamps `releasedOn` with today's date (UTC); that date is the only date ever shown
publicly (page, metadata, sitemap). Unreleased articles show "Coming soon" and no date.
The script only ever writes resources/*.html, _resources/manifest.json and sitemap.xml.

Usage:  python _tools/build_resources.py [--dry-run]
Env:    RESOURCES_TODAY=YYYY-MM-DD overrides today's date (tests only; the workflow never sets it).
Exit:   non-zero with a message on any invalid manifest or inconsistent state.
"""
import argparse
import datetime as dt
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.populosdata.com'
MANIFEST = '_resources/manifest.json'
SOURCE_DIR = '_unreleased'
OUT_DIR = 'resources'
SITEMAP = 'sitemap.xml'
CATEGORIES = {'Guides': 'guides', 'Case Studies': 'case-studies', 'Trends': 'trends'}
STATUSES = {'scheduled', 'published'}
FIELDS = {'slug': str, 'title': str, 'excerpt': str, 'category': str, 'readMinutes': int, 'order': int,
          'vetted': bool, 'releasedOn': (str, type(None)), 'image': (str, type(None)), 'status': str}
AUTHOR = 'Populos Team'
IMAGE_NOTE = ('Photographs and illustrations in this article are used to explain how out-of-home is measured. '
              'Any brand, advertiser or media owner shown is incidental, and nothing here is intended to '
              'criticise or endorse any of them.')


class BuildError(Exception):
    pass


def esc(s):
    return html.escape(s, quote=True)


def long_date(d):
    return f'{d.day} {d.strftime("%B %Y")}'


def load_manifest(root):
    path = os.path.join(root, MANIFEST)
    try:
        data = json.load(open(path, encoding='utf-8'))
    except FileNotFoundError:
        raise BuildError(f'{MANIFEST} not found')
    except json.JSONDecodeError as e:
        raise BuildError(f'{MANIFEST} is not valid JSON: {e}')
    if not isinstance(data, dict) or not isinstance(data.get('articles'), list) or not data['articles']:
        raise BuildError(f'{MANIFEST} must be an object with a non-empty "articles" list')
    seen, orders = set(), set()
    for n, a in enumerate(data['articles'], 1):
        where = f'{MANIFEST} article #{n}'
        if not isinstance(a, dict):
            raise BuildError(f'{where} is not an object')
        for f, t in FIELDS.items():
            if f not in a:
                raise BuildError(f'{where} is missing "{f}"')
            if not isinstance(a[f], t) or (t is int and isinstance(a[f], bool)):
                raise BuildError(f'{where} field "{f}" has the wrong type ({type(a[f]).__name__})')
        extra = set(a) - set(FIELDS)
        if extra:
            raise BuildError(f'{where} has unknown fields: {sorted(extra)}')
        if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', a['slug']):
            raise BuildError(f'{where} slug "{a["slug"]}" must be lower-case words joined by hyphens')
        if a['slug'] in seen:
            raise BuildError(f'{where} slug "{a["slug"]}" is duplicated')
        seen.add(a['slug'])
        if not a['title'].strip() or not a['excerpt'].strip():
            raise BuildError(f'{where} title and excerpt must not be empty')
        if a['category'] not in CATEGORIES:
            raise BuildError(f'{where} category "{a["category"]}" must be one of {sorted(CATEGORIES)}')
        if not 1 <= a['readMinutes'] <= 60:
            raise BuildError(f'{where} readMinutes must be between 1 and 60')
        if a['order'] < 1:
            raise BuildError(f'{where} order must be 1 or more')
        if a['order'] in orders:
            raise BuildError(f'{where} order {a["order"]} is duplicated')
        orders.add(a['order'])
        a['_released'] = None
        if a['releasedOn'] is not None:
            try:
                a['_released'] = dt.date.fromisoformat(a['releasedOn'])
            except ValueError:
                raise BuildError(f'{where} releasedOn "{a["releasedOn"]}" is not YYYY-MM-DD')
        if a['status'] not in STATUSES:
            raise BuildError(f'{where} status "{a["status"]}" must be one of {sorted(STATUSES)}')
        if (a['status'] == 'published') != (a['releasedOn'] is not None):
            raise BuildError(f'{where} status "{a["status"]}" disagrees with releasedOn {a["releasedOn"]!r}')
        if a['image'] is not None and not os.path.isfile(os.path.join(root, a['image'].lstrip('/'))):
            raise BuildError(f'{where} image "{a["image"]}" does not exist')
        if not os.path.isfile(os.path.join(root, SOURCE_DIR, a['slug'] + '.html')):
            raise BuildError(f'{where} source {SOURCE_DIR}/{a["slug"]}.html does not exist')
    return data


def header():
    return '''<header class="site-header">
  <nav class="site-nav" aria-label="Main">
    <a class="brand" href="/"><img src="/assets/populos-mark-navy.png" alt=""><span class="brand-text"><span class="brand-name">Populos</span><span class="brand-tag">The OOH Intelligence Platform</span></span></a>
    <div class="nav-right">
      <div class="nav-links">
        <a href="/#features">Features</a>
        <a href="/resources/" aria-current="page">Resources</a>
        <a href="/#pricing">Pricing</a>
        <a href="/#contact">Contact</a>
      </div>
      <a class="nav-cta" href="/early-access.html">Early Bird</a>
    </div>
  </nav>
</header>'''


def footer():
    return '''<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-grid">
      <div class="footer-col">
        <a class="brand" href="/"><img src="/assets/populos-mark-navy.png" alt=""><span class="brand-name">Populos</span></a>
        <span class="muted">The OOH Intelligence Platform.<br>A product of E Brandistry.</span>
      </div>
      <div class="footer-col">
        <span class="footer-head">PLATFORM</span>
        <a href="/#features">Features</a>
        <a href="/#product">Dashboard</a>
        <a href="/#standards">Standards</a>
        <a href="/#pricing">Plans</a>
        <a href="/resources/">Resources</a>
      </div>
      <div class="footer-col">
        <span class="footer-head">CONTACT</span>
        <a class="contact-link" href="mailto:hello@populosdata.com"><span>General</span>hello@populosdata.com</a>
        <a class="contact-link" href="mailto:sales@populosdata.com"><span>Sales &amp; partnerships</span>sales@populosdata.com</a>
        <a class="contact-link" href="tel:+233558890184"><span>Phone</span>+233 55 889 0184</a>
        <a class="contact-link" href="https://www.linkedin.com/company/populosdata" target="_blank" rel="noopener noreferrer"><span>LinkedIn</span>linkedin.com/company/populosdata</a>
        <a href="/early-access.html">Early Bird access</a>
        <span class="muted">Accra, Ghana</span>
      </div>
    </div>
    <div class="footer-legal">&copy; 2026 E Brandistry - Populos. All rights reserved.</div>
  </div>
</footer>'''


def page(title, description, canonical, og_type, body, extra_head=''):
    return f'''<!DOCTYPE html>
<html lang="en-GH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="icon" href="/assets/populos-mark-navy.png">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/og-card.png">
<meta name="twitter:card" content="summary_large_image">
{extra_head}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&amp;family=Inter:wght@400;500;600&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="/resources/resources.css">
</head>
<body>
{header()}
{body}
{footer()}
</body>
</html>
'''


def cover(a):
    if a['image']:
        return f'<div class="cover"><img src="{esc(a["image"])}" alt="" loading="lazy"></div>'
    return '<div class="cover cover-brand" aria-hidden="true"><img src="/assets/populos-mark-navy.png" alt=""><span>Populos</span></div>'


def byline(a, when):
    return (f'<div class="byline"><span class="avatar" aria-hidden="true"><img src="/assets/populos-mark-navy.png" alt=""></span>'
            f'<span><span class="author">{AUTHOR}</span><span class="meta">{when}<span class="dot" aria-hidden="true"></span>'
            f'{a["readMinutes"]} min read</span></span></div>')


def public_date(a):
    """The only date ever shown for an article: the day it was actually released."""
    return a['_released']


def released_when(a):
    d = public_date(a)
    return f'<time datetime="{d.isoformat()}">{long_date(d)}</time>'


def card(a):
    cat = f'<span class="category cat-{CATEGORIES[a["category"]]}">{esc(a["category"])}</span>'
    if a['releasedOn'] is not None:
        inner = (f'{cover(a)}<div class="card-body">{cat}<h2>{esc(a["title"])}</h2><p>{esc(a["excerpt"])}</p>'
                 f'{byline(a, released_when(a))}<span class="card-action">Read</span></div>')
        return f'<li class="card"><a class="card-link" href="/resources/{a["slug"]}.html">{inner}</a></li>'
    inner = (f'{cover(a)}<div class="card-body">{cat}<h2>{esc(a["title"])}</h2><p>{esc(a["excerpt"])}</p>'
             f'{byline(a, "Coming soon")}</div>')
    return f'<li class="card card-coming" aria-disabled="true">{inner}</li>'


def index_page(articles):
    released = sorted([a for a in articles if a['releasedOn'] is not None], key=lambda a: (a['_released'], a['order']), reverse=True)
    coming = sorted([a for a in articles if a['releasedOn'] is None], key=lambda a: a['order'])
    cards = '\n'.join(card(a) for a in released + coming)
    body = f'''<main class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">&rsaquo;</span><span aria-current="page">All blogs</span></nav>
  <div class="intro">
    <h1>The latest from Populos</h1>
    <p>Plain-language guides and perspectives on out-of-home audience measurement in Ghana, written by the Populos team. Free to read, no sign-up.</p>
  </div>
  <ul class="card-grid">
{cards}
  </ul>
</main>'''
    return page('Resources | Populos',
                'Guides and perspectives on out-of-home (OOH) audience measurement in Ghana from the Populos team. Free to read, no sign-up.',
                f'{SITE}/resources/', 'website', body)


def article_page(root, a):
    src = open(os.path.join(root, SOURCE_DIR, a['slug'] + '.html'), encoding='utf-8').read()
    url = f'{SITE}/resources/{a["slug"]}.html'
    when = released_when(a)
    body = f'''<main class="wrap article-wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">&rsaquo;</span><a href="/resources/">All blogs</a></nav>
  <article class="article">
    <span class="category cat-{CATEGORIES[a["category"]]}">{esc(a["category"])}</span>
    <h1>{esc(a["title"])}</h1>
    <p class="standfirst">{esc(a["excerpt"])}</p>
    {byline(a, when)}
    {cover(a)}
    <div class="article-body">
{src}    </div>
    <p class="image-note">{IMAGE_NOTE}</p>
    <p><a class="back" href="/resources/">&larr; All blogs</a></p>
  </article>
</main>'''
    extra = f'<meta property="article:published_time" content="{public_date(a).isoformat()}">\n<meta name="author" content="{AUTHOR}">\n'
    return page(f'{a["title"]} | Populos', a['excerpt'], url, 'article', body, extra)


def sitemap(root, articles):
    path = os.path.join(root, SITEMAP)
    current = open(path, encoding='utf-8').read()
    entries = re.findall(r'<url>\s*<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>\s*</url>', current)
    if not entries:
        raise BuildError(f'{SITEMAP} has no <url> entries to preserve')
    article_urls = {f'{SITE}/resources/{a["slug"]}.html' for a in articles}
    base = [(loc, mod) for loc, mod in entries if loc not in article_urls]
    pub = [(f'{SITE}/resources/{a["slug"]}.html', public_date(a).isoformat())
           for a in sorted(articles, key=lambda a: a['order']) if a['releasedOn'] is not None]
    urls = ''.join(f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{mod}</lastmod>\n  </url>\n' for loc, mod in base + pub)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n'


def next_release(articles):
    """The single article this run may release: the lowest unreleased order number, only if vetted."""
    unreleased = [a for a in articles if a['releasedOn'] is None]
    if not unreleased:
        return None, None
    first = min(unreleased, key=lambda a: a['order'])
    return (first if first['vetted'] is True else None), first


def build(root, today, dry_run):
    data = load_manifest(root)
    articles = data['articles']
    for a in articles:
        page_exists = os.path.isfile(os.path.join(root, OUT_DIR, a['slug'] + '.html'))
        if a['releasedOn'] is None and page_exists:
            raise BuildError(f'"{a["slug"]}" has a page but no releasedOn. Resolve by hand; nothing was changed.')
        if a['releasedOn'] is not None and a['vetted'] is not True:
            raise BuildError(f'"{a["slug"]}" was released on {a["releasedOn"]} but is no longer vetted. Resolve by hand; nothing was changed.')
        if a['releasedOn'] is not None and a['_released'] > today:
            raise BuildError(f'"{a["slug"]}" has releasedOn {a["releasedOn"]}, which is after today ({today}).')
    release, first = next_release(articles)
    today_release = next((a for a in articles if a['_released'] == today), None)
    if release is not None and today_release is not None:
        # One release per calendar day (UTC), counted from releasedOn: a second run today does nothing.
        release = None
    if release is not None:
        release['releasedOn'], release['_released'], release['status'] = today.isoformat(), today, 'published'
    outputs = {os.path.join(OUT_DIR, 'index.html'): index_page(articles), SITEMAP: sitemap(root, articles)}
    for a in articles:
        if a['releasedOn'] is not None:
            outputs[os.path.join(OUT_DIR, a['slug'] + '.html')] = article_page(root, a)
    clean = {'articles': [{k: v for k, v in a.items() if not k.startswith('_')} for a in articles]}
    outputs[MANIFEST] = json.dumps(clean, indent=2, ensure_ascii=False) + '\n'
    changed = []
    for rel, text in outputs.items():
        path = os.path.join(root, rel)
        old = open(path, encoding='utf-8').read() if os.path.isfile(path) else None
        if old != text:
            changed.append(rel.replace(os.sep, '/'))
            if not dry_run:
                with open(path, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(text)
    if release or first is None:
        waiting = None
    elif first['vetted'] is not True:
        waiting = f'{first["slug"]} (order {first["order"]}, not vetted)'
    else:
        waiting = (f'{first["slug"]} (order {first["order"]}, vetted) is held: an article was already released today '
                   f'({today_release["slug"]}), limit is one per day (UTC)')
    return (release['slug'] if release else None), waiting, changed


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--dry-run', action='store_true', help='report what would change and write nothing')
    ap.add_argument('--root', default=ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args()
    override = os.environ.get('RESOURCES_TODAY')
    today = dt.date.fromisoformat(override) if override else dt.datetime.now(dt.timezone.utc).date()
    try:
        released, waiting, changed = build(args.root, today, args.dry_run)
    except BuildError as e:
        print(f'::error title=Resources build failed::{e}')
        print(f'ERROR: {e}', file=sys.stderr)
        return 1
    mode = 'DRY RUN, nothing written' if args.dry_run else 'written'
    print(f'today (UTC) = {today}; released this run: {released or "none"}'
          + (f'; next in planned order: {waiting}' if waiting else '') + f'; {mode}; changed: {changed or "nothing"}')
    out = os.environ.get('GITHUB_OUTPUT')
    if out:
        with open(out, 'a', encoding='utf-8') as f:
            f.write(f'changed={"true" if changed and not args.dry_run else "false"}\n')
            f.write(f'published={released or ""}\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Build a self-contained presentation HTML using only Python's standard library."""
from __future__ import annotations

import argparse
import base64
import re
from pathlib import Path


def build(root: Path, destination: Path) -> None:
    html = (root / 'index.html').read_text(encoding='utf-8')
    css = (root / 'styles.css').read_text(encoding='utf-8')
    js = (root / 'app.js').read_text(encoding='utf-8')
    css_link = '<link rel="stylesheet" href="./styles.css">'
    js_link = '<script src="./app.js" defer></script>'
    if css_link not in html or js_link not in html:
        raise ValueError('Expected local CSS and JavaScript references are missing.')
    html = html.replace(css_link, '<style>\n' + css + '</style>')
    html = html.replace(js_link, '')
    html = html.replace('</body>', '<script>\n' + js + '</script>\n</body>')
    html = re.sub(r'<link[^>]+href="https://fonts[^>]+>\s*', '', html)
    types = {'.avif': 'image/avif', '.svg': 'image/svg+xml'}
    for asset in sorted((root / 'assets').iterdir()):
        mime = types.get(asset.suffix.lower())
        if mime:
            encoded = base64.b64encode(asset.read_bytes()).decode('ascii')
            html = html.replace('./assets/' + asset.name, f'data:{mime};base64,{encoded}')
    if './assets/' in html:
        raise ValueError('An unsupported or missing image is still referenced.')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html, encoding='utf-8')
    print(f'Created {destination} ({destination.stat().st_size:,} bytes)')


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=root / 'Assyabab-Prototype.html')
    args = parser.parse_args()
    build(root, args.output.resolve())


if __name__ == '__main__':
    main()

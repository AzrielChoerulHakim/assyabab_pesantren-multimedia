#!/usr/bin/env python3
"""Build a self-contained presentation HTML with exactly the website's typography."""
from __future__ import annotations

import argparse
import base64
import re
from pathlib import Path


def build(root: Path, destination: Path) -> None:
    root = root.resolve()
    html = (root / 'index.html').read_text(encoding='utf-8')

    def read_local(relative: str) -> str:
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError(f'Missing or unsafe local resource: {relative}')
        return path.read_text(encoding='utf-8')

    # Preserve the order of every local stylesheet, including refinement layers.
    html, count = re.subn(
        r'<link rel="stylesheet" href="\./([^"<>]+)">',
        lambda match: '<style>\n' + read_local(match[1]) + '\n</style>', html)
    if not count:
        raise ValueError('No local stylesheets found.')
    scripts: list[str] = []

    def collect_script(match: re.Match) -> str:
        scripts.append(read_local(match[1]))
        return ''

    html = re.sub(r'<script src="\./([^"<>]+)" defer></script>', collect_script, html)
    if not scripts:
        raise ValueError('No local scripts found.')
    html = html.replace('</body>', '\n'.join('<script>\n' + script + '\n</script>' for script in scripts) + '\n</body>')
    if 'fonts.googleapis.com' in html or 'fonts.gstatic.com' in html:
        raise ValueError('An external font dependency would break offline consistency.')
    # In the portable copy use the detailed src. No responsive network requests are needed.
    html = re.sub(r'\s+srcset="[^"]*"', '', html)
    html = re.sub(r'\s+sizes="[^"]*"', '', html)
    media_types = {'.avif': 'image/avif', '.svg': 'image/svg+xml'}
    for asset in sorted((root / 'assets').iterdir()):
        mime = media_types.get(asset.suffix.lower())
        if mime:
            encoded = base64.b64encode(asset.read_bytes()).decode('ascii')
            html = html.replace('./assets/' + asset.name, f'data:{mime};base64,{encoded}')
    if './assets/' in html:
        raise ValueError('An unsupported or missing image is still referenced.')
    destination = destination.resolve()
    if destination == root / 'index.html':
        raise ValueError('Do not overwrite the website source.')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html, encoding='utf-8')
    print(f'Created {destination} ({destination.stat().st_size:,} bytes)')


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=root / 'Assyabab-Prototype.html')
    args = parser.parse_args()
    build(root, args.output)


if __name__ == '__main__':
    main()

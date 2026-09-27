#!/usr/bin/env python3
"""Chromium regression checks using the self-contained export (no web server required).
Requires Python >=3.10, playwright, and a Chromium executable.
Run: python3 tools/test_ui.py --browser /usr/bin/chromium
"""
from __future__ import annotations
import argparse
import json
import re
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright
from build_offline import build

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--browser', default='/usr/bin/chromium')
    parser.add_argument('--screenshots', type=Path)
    args = parser.parse_args()
    screenshot_dir = args.screenshots
    if screenshot_dir:
        screenshot_dir.mkdir(parents=True, exist_ok=True)
    result = {'method': 'Chromium; inline self-contained export; not a live-host or physical-device test', 'viewports': []}
    with tempfile.TemporaryDirectory() as temp:
        portable = Path(temp) / 'presentation.html'
        build(ROOT, portable)
        html = portable.read_text()
        result['portable_bytes'] = len(html.encode())
        assert 'fonts.googleapis.com' not in html
        assert not re.search(r'(src|href)="\./', html)
        source = (ROOT/'index.html').read_text()
        for ref in re.findall(r'(?:src|href)="\./([^"?#]+)"', source):
            assert (ROOT/ref).is_file(), f'Missing asset: {ref}'
        for srcset in re.findall(r'srcset="([^"]+)"', source):
            for item in srcset.split(','):
                assert (ROOT/item.strip().split()[0]).is_file()
        result['source_references_exist'] = True
        result['font_network_dependencies'] = 0
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=args.browser, headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage'])
            result['chromium_version'] = browser.version
            for width in [320, 360, 390, 430, 700, 701, 768, 1024, 1440, 1920]:
                context = browser.new_context(viewport={'width': width, 'height': 900},
                    reduced_motion='reduce', is_mobile=width <= 430, has_touch=width <= 430)
                page = context.new_page()
                errors, requests = [], []
                page.on('pageerror', lambda error: errors.append(str(error)))
                page.on('request', lambda request: requests.append(request.url))
                page.set_content(html, wait_until='load')
                page.evaluate("Promise.all([...document.querySelectorAll('main img')].map(i=>{i.loading='eager';return i.decode().catch(()=>null)}))")
                metrics = page.evaluate("""() => ({
                    width: innerWidth,
                    horizontal_overflow: document.documentElement.scrollWidth > innerWidth,
                    hero_height: Math.round(document.querySelector('.hero').getBoundingClientRect().height),
                    hero_body_px: parseFloat(getComputedStyle(document.querySelector('.hero-description')).fontSize),
                    primary_button_px: parseFloat(getComputedStyle(document.querySelector('.hero-actions .button')).fontSize),
                    missing_images: [...document.querySelectorAll('main img')].filter(i=>!i.naturalWidth).map(i=>i.alt),
                    body_font: getComputedStyle(document.body).fontFamily
                })""")
                assert not metrics['horizontal_overflow'], f'Overflow at {width}'
                assert metrics['hero_body_px'] >= 15 and metrics['primary_button_px'] >= 14
                assert not metrics['missing_images']
                for index, name in enumerate(['Tahsin', 'Tahfizh', 'Tanghim', 'Tafsir']):
                    page.locator(f'[data-course-jump="{index}"]').click()
                    assert page.locator('.four-t-list details[open]').count() == 1
                    assert page.locator(f'#course-{index}').get_attribute('open') is not None
                    assert page.locator('[data-course-title]').inner_text() == name
                    assert page.locator(f'[data-course-jump="{index}"]').get_attribute('aria-pressed') == 'true'
                    assert page.locator('[data-course-compass]').evaluate("e=>e.style.getPropertyValue('--course-angle')") == f'{index*90}deg'
                page.locator('#course-1 summary').click()
                page.wait_for_function("document.querySelector('[data-course-title]').textContent==='Tahfizh'")
                assert page.locator('[data-course-title]').inner_text() == 'Tahfizh'
                page.locator('[data-course-jump="1"]').focus()
                page.keyboard.press('ArrowRight')
                assert page.locator('[data-course-title]').inner_text() == 'Tanghim'
                page.locator('#course-2 summary').click()
                page.wait_for_function("document.querySelector('[data-course-title]').textContent==='Empat fondasi'")
                assert page.locator('.four-t-list details[open]').count() == 0
                metrics['compass_bidirectional_and_keyboard'] = True
                page.locator('[data-day="malam"]').click()
                assert page.locator('[data-day-panel="malam"]').is_visible()
                assert not page.locator('[data-day-panel="pagi"]').is_visible()
                page.keyboard.press('Home')
                assert page.locator('[data-day-panel="pagi"]').is_visible()
                metrics['day_switch_and_keyboard'] = True
                page.locator('.curriculum > summary').click()
                assert page.locator('.curriculum-grid article').count() == 10
                assert page.locator('.curriculum-grid article').last.is_visible()
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
                metrics['expanded_curriculum'] = True
                gallery = page.locator('.gallery-track')
                before = gallery.evaluate('e=>e.scrollLeft')
                page.locator('[data-gallery-next]').click()
                assert gallery.evaluate('e=>e.scrollLeft') > before
                page.locator('[data-gallery-prev]').click()
                assert gallery.evaluate('e=>e.scrollLeft') < 3
                metrics['gallery_navigation'] = True
                photo = page.locator('[data-lightbox]').first
                photo.click()
                assert page.locator('.lightbox').is_visible()
                page.wait_for_function("document.querySelector('.lightbox img').naturalWidth > 0")
                assert page.locator('body').evaluate("e=>e.classList.contains('modal-open')")
                page.keyboard.press('Escape')
                page.wait_for_function("!document.body.classList.contains('modal-open')")
                assert not page.locator('.lightbox').is_visible()
                assert photo.evaluate('e=>document.activeElement===e')
                assert not page.locator('body').evaluate("e=>e.classList.contains('modal-open')")
                metrics['lightbox_and_focus_return'] = True
                if width <= 700:
                    page.locator('.menu-toggle').click()
                    assert page.locator('#mobile-menu').is_visible()
                    assert page.locator('main').evaluate('e=>e.inert')
                    page.locator('#mobile-menu a').last.focus()
                    page.keyboard.press('Tab')
                    assert page.locator('.menu-toggle').evaluate('e=>document.activeElement===e')
                    page.keyboard.press('Escape')
                    assert not page.locator('#mobile-menu').is_visible()
                    assert not page.locator('main').evaluate('e=>e.inert')
                    page.locator('.menu-toggle').click()
                    page.locator('#mobile-menu a[href="#pendidikan"]').click()
                    assert not page.locator('#mobile-menu').is_visible()
                    page.wait_for_function("document.activeElement.id==='pendidikan'")
                    metrics['menu_modal_focus_and_anchor'] = True
                page.locator('.faq-list details').first.locator('summary').click()
                assert page.locator('.faq-list details').first.locator('p').is_visible()
                metrics['faq'] = True
                assert not errors, errors
                assert not requests, requests
                metrics['javascript_errors'] = errors
                metrics['automatic_network_requests_inline'] = len(requests)
                result['viewports'].append(metrics)
                context.close()
            # No-JavaScript fallback must leave essential content and native details available.
            context = browser.new_context(viewport={'width':390,'height':844},java_script_enabled=False)
            page = context.new_page(); page.set_content(html)
            assert page.locator('h1').is_visible()
            assert all(page.locator(f'[data-day-panel="{key}"]').is_visible() for key in ['pagi','siang','sore','malam'])
            assert not page.locator('.menu-toggle').is_visible()
            assert page.locator('.compass-node:visible').count()==0
            assert page.locator('a[href^="https://wa.me/"]').count()==3
            page.locator('#course-1 summary').click()
            assert page.locator('#course-1 .course-body').is_visible()
            result['without_javascript'] = {'content':True,'all_days':True,'native_accordion':True,'contact_links':3}
            context.close()
            # Motion is present normally, but disabled when the system requests reduction.
            context = browser.new_context(viewport={'width':1440,'height':1000})
            page = context.new_page(); page.set_content(html)
            assert page.locator('html').evaluate("e=>e.classList.contains('has-motion')")
            page.locator('.hero-art').hover()
            page.mouse.move(1150,400)
            page.wait_for_timeout(100)
            assert page.locator('.quran-book').evaluate('e=>e.style.transform')
            page.emulate_media(reduced_motion='reduce')
            page.wait_for_timeout(100)
            assert not page.locator('html').evaluate("e=>e.classList.contains('has-motion')")
            assert not page.locator('.quran-book').evaluate('e=>e.style.transform')
            page.locator('[data-course-jump="2"]').click()
            assert page.locator('[data-course-title]').inner_text() == 'Tanghim'
            assert page.locator('.compass-status').evaluate('e=>e.getAnimations().length')==0
            result['reduced_motion_live_change'] = True
            context.close()
            if screenshot_dir:
                for width,height,name in [(1440,1000,'Desktop'),(390,844,'Mobile')]:
                    context=browser.new_context(viewport={'width':width,'height':height}, reduced_motion='reduce')
                    page=context.new_page();page.set_content(html)
                    page.evaluate("Promise.all([...document.querySelectorAll('main img')].map(i=>{i.loading='eager';return i.decode()}))")
                    page.screenshot(path=str(screenshot_dir/f'Assyabab-{name}-v2.png'))
                    page.screenshot(path=str(screenshot_dir/f'Assyabab-{name}-v2-Full.png'),full_page=True)
                    context.close()
            browser.close()
    path=ROOT/'docs/test-report-v2.json'
    path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))


if __name__=='__main__':
    main()

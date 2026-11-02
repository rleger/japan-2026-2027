# -*- coding: utf-8 -*-
"""Rend carnet_v7.html en PDF avec Chromium, et signale les pages qui débordent."""
import os, sys
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = 'file://' + os.path.join(ROOT, 'carnet_v7.html')
out = os.path.join(ROOT, sys.argv[1] if len(sys.argv) > 1 else 'Japon_hiver_carnet_v7.pdf')
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(src, wait_until='load')
    pg.wait_for_timeout(1200)
    pg.evaluate("document.fonts.ready")
    over = pg.evaluate('''() => Array.from(document.querySelectorAll('.page')).map(p => {
        const cs = getComputedStyle(p); const pad = parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom);
        const inner = p.clientHeight - pad;
        let max = 0; for (const c of p.children) { if (c.classList.contains('hdr') || c.classList.contains('ftr') || c.classList.contains('tab') || c.classList.contains('cover')) continue;
            const r = c.getBoundingClientRect(); const pr = p.getBoundingClientRect(); max = Math.max(max, r.bottom - pr.top - parseFloat(cs.paddingTop)); }
        return {n: p.dataset.n, used: Math.round(max), avail: Math.round(inner)};
    })''')
    bad = [o for o in over if o['used'] > o['avail'] - 4]
    for o in over: print(f"p{o['n']:>3} {o['used']:>5}/{o['avail']}{'  <-- DÉBORDE' if o in bad else ''}")
    pg.pdf(path=out, format='A4', print_background=True, prefer_css_page_size=True, margin={'top':'0','bottom':'0','left':'0','right':'0'})
    b.close()
print('PDF', out, os.path.getsize(out)//1024, 'ko')

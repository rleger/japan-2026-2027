# -*- coding: utf-8 -*-
"""Construit le carnet v7 : HTML (Jinja2) puis PDF (Chromium via Playwright)."""
import json, os, sys, re
from jinja2 import Environment, BaseLoader
sys.path.insert(0, os.path.dirname(__file__))
import content_a as A, content_b as B, content_c as C, content_d as D
from datetime import datetime
from zoneinfo import ZoneInfo
GEN = 'Carnet v7.0, généré le ' + datetime.now(ZoneInfo('Europe/Paris')).strftime('%d/%m/%Y à %H:%M')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = "file://" + ROOT + "/assets/img/"

# --- fragments -----------------------------------------------------------
HDR = '<div class="hdr"><span>{{ left }}</span><span>{{ right }}</span></div>'
FTR = '<div class="ftr"><span class="gen">{{ gen }}</span>{{ num }}</div>'
TAB = '{% if tab %}<div class="tab {{ theme }}">{{ tab }}</div>{% endif %}'

DAYHEAD = '''
<div class="day">
<div class="dayhead"><div class="num">{{ d.num }}</div><div><div class="dow">{{ d.dow }}</div>
<div class="ttl">{{ d.title }}{% if d.stars %}<span class="st">{{ d.stars }}</span>{% endif %}</div></div></div>
<div class="strip">{% for k,v in d.head %}<div><div class="k">{{ k }}</div><div class="v">{{ v }}</div></div>{% endfor %}</div>
{% if d.photos %}<div class="photos{% if d.photos|length == 2 %} two{% elif d.photos|length == 1 %} one{% endif %}">
<div class="big"><img src="{{ IMG }}{{ d.photos[0][0] }}"><div class="cap">{{ d.photos[0][1] }}</div></div>
{% if d.photos|length > 1 %}<div class="side">{% for f,c in d.photos[1:] %}<div><img src="{{ IMG }}{{ f }}"><div class="cap">{{ c }}</div></div>{% endfor %}</div>{% endif %}
</div>{% endif %}
<div class="daybody"><div class="txt">{% for k,v in d.sections %}<div class="lbl">{{ k }}</div><p>{{ v }}</p>{% endfor %}</div>
{% if d.pratique or d.table or d.repere %}<div class="side">
{% if d.pratique %}<div class="lbl">Pratique</div><ul>{% for p in d.pratique %}<li>{{ p }}</li>{% endfor %}</ul>{% endif %}
{% if d.table %}<div class="lbl">À table</div><p>{{ d.table }}</p>{% endif %}
{% if d.repere %}<div class="lbl">Repère</div><p class="rep">{{ d.repere }}</p>{% endif %}
</div>{% endif %}</div>
</div>'''

TRAJET = '''{% if d.trajet %}<div class="lbl" style="margin-top:9pt">Le trajet, heure par heure</div>
<table class="tr"><tr><th style="width:17mm">Heure</th><th style="width:48mm">Trajet</th><th>Comment</th><th style="width:19mm">Durée</th><th style="width:21mm">Réservation</th></tr>
{% for h,t,c,du,s in d.trajet %}<tr><td class="h">{{ h }}</td><td class="t">{{ t }}</td><td class="c">{{ c }}</td><td class="d">{{ du }}</td>
<td class="s">{% if s %}<span class="dot s-{{ s }}">{{ {'O':'Obligatoire','C':'À réserver','L':'Libre'}[s] }}</span>{% endif %}</td></tr>{% endfor %}</table>{% endif %}'''
COINCE = '''{% if d.coince %}<div class="coince"><div class="lbl">Si ça coince</div>{{ d.coince }}</div>{% endif %}'''
OPTIONS = '''{% if d.options %}<div class="lbl">Autres options et compléments</div><div class="opts">
{% for k,v in d.options %}<div class="row"><div class="k">{{ k }}</div><div>{{ v }}</div></div>{% endfor %}</div>{% endif %}'''

LODGE = '''<div class="lodge"><div class="ttl"><span class="lbl">Où dormir</span>{{ L.title }}</div>
<div class="cols2"><div><div class="lbl">{{ L.simple_label or 'Charme simple' }}</div>
{% for n,u,dsc,r,p in L.simple %}<div class="h"><a href="{{ u }}">{{ n }} ↗</a>{{ dsc }}{% if r %} · {{ r }}{% endif %} · <span class="pr">{{ p }}</span></div>{% endfor %}</div>
<div><div class="lbl">{{ L.elegant_label or 'Plus élégant' }}</div>
{% for n,u,dsc,r,p in L.elegant %}<div class="h"><a href="{{ u }}">{{ n }} ↗</a>{{ dsc }}{% if r %} · {{ r }}{% endif %} · <span class="pr">{{ p }}</span></div>{% endfor %}</div></div>
{% if L.note %}<div class="note">{{ L.note }}</div>{% endif %}</div>'''

OPENER = '''<div class="banner{% if not ch.banner %} nophoto{% endif %}{% if ch.map_wide %} short{% endif %}">{% if ch.banner %}<img src="{{ IMG }}{{ ch.banner }}">{% else %}<div class="deco">{{ ch.kanji }}</div>{% endif %}<div class="shade"></div>
<div class="region">{{ ch.region }}</div><div class="credit">{{ ch.banner_credit }}</div>
<div class="num">{{ ch.num }}</div><div class="ttl">{{ ch.title }}</div><div class="sub">{{ ch.subtitle }}</div>{% if ch.banner %}<div class="kj">{{ ch.kanji }}</div>{% endif %}<div class="bar"></div></div>
<div class="opener-body{% if ch.map_wide %} wide{% endif %}"><div class="l"><div class="intro">{{ ch.intro }}</div>
<div class="hist"><div class="lbl">Un peu d'histoire</div>{{ ch.history }}</div>
<div class="stats">{% for v,k in ch.stats %}<div><div class="v">{{ v }}</div><div class="k">{{ k }}</div></div>{% endfor %}</div></div>
{% if not ch.map_wide %}<div class="r"><div class="mapbox"><img src="{{ IMG }}{{ ch.map }}"></div><div class="caption">{{ ch.map_caption }}</div></div>{% endif %}</div>
{% if ch.map_wide %}<div class="mapwide"><div class="mapbox"><img src="{{ IMG }}{{ ch.map }}"></div><div class="caption">{{ ch.map_caption }}</div></div>{% endif %}'''

LOCALS = '''<div class="kicker">Vivre comme les gens d'ici</div><h1>{{ lc.title }}</h1>
<div class="loc2"><div class="taste"><div class="lbl">À goûter</div>{% for k,v in lc.taste %}<p><b>{{ k }} :</b> {{ v }}</p>{% endfor %}</div>
<div><div class="lbl">Comme les gens d'ici</div><ul>{% for c in lc.customs %}<li>{{ c }}</li>{% endfor %}</ul></div></div>
<div class="anec"><div class="lbl">Anecdotes</div>{% for a in lc.anecdotes %}<p>{{ a }}</p>{% endfor %}</div>'''

env = Environment(loader=BaseLoader(), autoescape=False)
def R(tpl, **kw):
    kw.setdefault('IMG', IMG)
    return env.from_string(tpl).render(**kw)

# --- page builders ---------------------------------------------------------
pages = []
def add(body, cls="navy", left="JAPON EN HIVER · CARNET V7", right="", tab="", full=False, nohdr=False, toc=None, tocsub=None):
    pages.append(dict(cls=cls, full=full, nohdr=nohdr, left=left, right=right, tab=tab, body=body, toc=toc, tocsub=tocsub))

def cover():
    c = A.COVER
    body = f'''<div class="cover" style="position:absolute;inset:0"><div class="kick">{c['kicker']}</div>
    <div class="t1">{c['title']}</div><div class="t2">{c['subtitle']}</div><div class="jp">{c['jp']}</div><div class="big">{c['kanji']}</div>
    <div class="bottom"><div class="dates">{c['dates']}</div><div class="line">{c['line']}</div>
    <div class="stops">{''.join('<span>'+s+'</span>' for s in c['stops'])}</div><div class="foot">{c['foot']}</div></div></div>'''
    pages.append(dict(cls="cover", full=True, nohdr=True, left="", right="", tab="", body=body, toc=None, tocsub=None, nofooter=True))

def toc_page():
    add("__TOC__", right="SOMMAIRE")

ICONS = dict(
    plane="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z",
    train="M12 2c-4 0-8 .5-8 4v9.5A3.5 3.5 0 0 0 7.5 19L6 20.5V21h12v-.5L16.5 19a3.5 3.5 0 0 0 3.5-3.5V6c0-3.5-4-4-8-4zM7.5 17a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm3.5-6H6V6h5v5zm5.5 6a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm1.5-6h-5V6h5v5z",
    bus="M4 16c0 .88.39 1.67 1 2.22V20a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1h8v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1.78c.61-.55 1-1.34 1-2.22V6c0-3.5-3.58-4-8-4s-8 .5-8 4v10zm3.5 1a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm9 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm1.5-6H6V6h12v5z",
    car="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z",
    walk="M13.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM9.8 8.9L7 23h2.1l1.8-8 2.1 2v6h2v-7.5l-2.1-2 .6-3C14.8 12 16.8 13 19 13v-2c-1.9 0-3.5-1-4.3-2.4l-1-1.6c-.4-.6-1-1-1.7-1-.3 0-.5.1-.8.1L6 8.3V13h2V9.6l1.8-.7z",
    bag="M17 6h-2V3c0-.55-.45-1-1-1h-4c-.55 0-1 .45-1 1v3H7c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2 0 .55.45 1 1 1s1-.45 1-1h6c0 .55.45 1 1 1s1-.45 1-1c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zM9.5 18H8V9h1.5v9zm3.25 0h-1.5V9h1.5v9zM13 6h-2V4h2v2zm3 12h-1.5V9H16v9z",
)
def ico(name):
    return f'<svg viewBox="0 0 24 24"><path d="{ICONS[name]}"/></svg>'
def chip(icon, text, kind):
    return f'<span class="chip {kind}">{ico(icon)}{text}</span>'

def timeline():
    t = A.TIMELINE
    rows = ''
    for i, (d, e, n, chips, bp) in enumerate(t['rows']):
        rows += f'''<div class="row{' bp' if bp else ''}"><div class="d">{d}</div><div class="rail"><span class="dot"></span></div>
        <div class="e"><div class="t">{e}</div><div class="n">Nuit : {n}</div></div><div class="c">{''.join(chip(*c) for c in chips)}</div></div>'''
    legend = ''.join(chip(*c) for c in t['legend'])
    body = f'''<div class="kicker">{t['kicker']}</div><h1>{t['title']}</h1><div class="lead">{t['intro']}</div>
    <div class="tl">{rows}</div><div class="tl-legend">{legend}<span class="chip bpk"><span class="sw"></span>{t['legend_bp']}</span></div>'''
    add(body, right="LA FRISE DU VOYAGE", toc="La frise du voyage")

def overview():
    o = A.OVERVIEW
    rows = ''.join(f'<tr><td class="d">{d}</td><td class="e{" m" if m else ""}">{e}</td><td class="n">{n}</td><td>{t}</td></tr>' for d,e,n,t,m in o['rows'])
    brief = ''.join(f'<div class="row"><div class="k">{k}</div><div>{v}</div></div>' for k,v in o['brief'])
    body = f'''<div class="kicker">{o['kicker']}</div><h1>{o['title']}</h1><div class="lead">{o['intro']}</div>
    <table class="ov"><tr><th style="width:24mm">Dates</th><th style="width:36mm">Étape</th><th style="width:12mm">Nuits</th><th>En quelques mots</th></tr>{rows}</table>
    <div class="lbl gold" style="margin-top:12pt">En bref</div><div class="brief">{brief}</div>'''
    add(body, right="LE VOYAGE EN UN COUP D'ŒIL", toc="Le voyage en un coup d'œil")

def map_page():
    m = A.MAP_PAGE
    cols = ''.join(f'<div><div class="lbl">{k}</div>{v}</div>' for k,v in m['cols'])
    body = f'''<div class="kicker">{m['kicker']}</div><h1>{m['title']}</h1>
    <div class="mapbox"><img src="{IMG}{m['image']}"></div><div class="caption">{m['caption']}</div><div class="cols3">{cols}</div>'''
    add(body, right="LE VOYAGE EN UN COUP D'ŒIL")

def before():
    b = A.BEFORE
    boxes = [f'<div class="box"><div class="lbl">{k}</div>{v}</div>' for k,v in b['boxes']]
    body = f'''<div class="kicker">{b['kicker']}</div><h1>{b['title']}</h1>
    <div class="cols2"><div>{boxes[0]}{boxes[3] if len(boxes) > 3 else ''}</div><div>{boxes[1]}{boxes[2]}</div></div><div class="fine">{b['foot']}</div>'''
    add(body, right="AVANT DE PARTIR", toc="Avant de partir")

def ck_rows(items):
    tags = {'B': 'BLOQUANT', 'I': 'IMPORTANT', 'U': 'UTILE'}
    return ''.join(f'<div class="ck {lv}"><div class="bx"></div><div class="dt">{d}</div><div class="tx"><b>{t}</b>{x}</div><div class="tg {lv}">{tags[lv]}</div></div>' for d,t,x,lv in items)

def checklist():
    """Sections : liste de (numéro, titre, sous-titre, items). Pagination : nombre d'items par page indiqué dans A.CHECK_PAGES."""
    c = A.CHECK_INTRO
    warn = ''.join(f'<div><div class="lbl">{k}</div>{v}</div>' for k,v in c['blocks'])
    head = f'''<div class="kicker">{c['kicker']}</div><h1>{c['title']}</h1><div class="lead" style="font-size:10.2pt">{c['intro']}</div>
    <div class="lbl" style="color:var(--red)">Ce qui peut bloquer</div><div class="warn4">{warn}</div>'''
    first = True
    for page in A.CHECK_PAGES:
        body = head if first else ''
        for (num, title, sub, items) in page:
            body += f'<div class="prio"><div class="n">{num}</div><div class="t">{title}</div><div class="s">{sub}</div></div>{ck_rows(items)}'
        add(body, right="CE QUE NOUS DEVONS FAIRE", toc=("Ce que nous devons faire, par priorité" if first else None))
        first = False

def strip_svg(st):
    """Frise de profil : nodes = (nom, altitude, x), segs = (libellé, détail, genre t/b/w/c)."""
    nodes, segs = st['nodes'], st['segs']
    amax = max(a for _, a, _ in nodes) or 1
    def y(alt): return 150 - alt / amax * 95
    pts = ' '.join(f"{x},{y(a):.0f}" for _, a, x in nodes)
    area = f"M{nodes[0][2]},175 L{pts.replace(' ', ' L')} L{nodes[-1][2]},175 Z"
    col = dict(t="#2d3f56", b="#2d3f56", w="#b8914f", c="#8c2f38")
    out = [f'<svg class="nkstrip" viewBox="0 0 900 236" xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<path d="{area}" fill="#f6efe2"/>')
    for i in range(len(nodes) - 1):
        (_, a1, x1), (_, a2, x2) = nodes[i], nodes[i + 1]
        k = segs[i][2]
        dash = ' stroke-dasharray="6,5"' if k == "b" else ''
        out.append(f'<line x1="{x1}" y1="{y(a1):.0f}" x2="{x2}" y2="{y(a2):.0f}" stroke="{col[k]}" stroke-width="{4 if k in "wc" else 2.2}"{dash}/>')
        xm = (x1 + x2) / 2
        out.append(f'<text x="{xm}" y="208" text-anchor="middle" font-family="Lato" font-size="12.5" font-weight="bold" fill="{col[k]}">{segs[i][0]}</text>')
        out.append(f'<text x="{xm}" y="226" text-anchor="middle" font-family="Lato" font-size="11.5" fill="#5e6572">{segs[i][1]}</text>')
    for n, a, x in nodes:
        out.append(f'<circle cx="{x}" cy="{y(a):.0f}" r="6" fill="#f9f6f0" stroke="#131f2d" stroke-width="2.2"/>')
        out.append(f'<text x="{x}" y="{y(a) - 26:.0f}" text-anchor="middle" font-family="DM Serif Display" font-size="15" fill="#131f2d">{n}</text>')
        out.append(f'<text x="{x}" y="{y(a) - 12:.0f}" text-anchor="middle" font-family="Lato" font-size="10.5" fill="#5e6572">{a} m</text>')
    out.append('<line x1="40" y1="175" x2="860" y2="175" stroke="#ddd6cb" stroke-width="0.8"/>')
    out.append('</svg>')
    if st.get('note'):
        out.append(f'<div class="stripnote">{st["note"]}</div>')
    return ''.join(out)

def chapter(ch, layout):
    """layout : liste de pages, chaque page = liste de blocs ('opener','locals',('day',i),('trajet',i),('coince',i),('options',i),'lodging','plans',('strip',key))"""
    hdr_right = f"{ch['region']} · {ch['title'].upper()}"
    for pi, blocks in enumerate(layout):
        parts, full = [], False
        for bl in blocks:
            if bl == 'opener':
                parts.append(R(OPENER, ch=ch)); full = True
                if ch.get('strip'):
                    parts.append(f'<div class="stripbox"><div class="lbl">{ch["strip"]["title"]}</div>' + strip_svg(ch['strip']) + '</div>')
            elif bl == 'locals':
                parts.append(R(LOCALS, lc=ch['locals']))
            elif bl == 'lodging':
                parts.append(R(LODGE, L=ch['lodging']))
            elif bl == 'plans':
                p = ch['plans']
                parts.append(f'''<div class="kicker">Plans</div><h1>{p['title']}</h1><div class="plans">
                <div style="flex:0 0 48%"><img src="{IMG}{p['left'][0]}"><div class="caption">{p['left'][1]}</div></div>
                <div><img src="{IMG}{p['right'][0]}"><div class="caption">{p['right'][1]}</div></div></div>''')
            else:
                kind, i = bl
                if kind == 'strip':
                    st = ch['strips'][i]
                    parts.append(f'<div class="stripbox inpage"><div class="lbl">{st["title"]}</div>' + strip_svg(st) + '</div>')
                    continue
                d = ch['days'][i]
                parts.append(R({'day': DAYHEAD, 'trajet': TRAJET, 'coince': COINCE, 'options': OPTIONS}[kind], d=d))
        body = ''.join(parts)
        toc = (ch['title'] if pi == 0 else None)
        dense = any(isinstance(b, tuple) and b[0]=='day' for b in blocks) and any(isinstance(b, tuple) and b[0] in ('trajet',) for b in blocks)
        add(body, cls=ch['theme'] + (' dense' if dense else ''), right=(ch['region'] if full else hdr_right), tab=ch['tab'], full=full, nohdr=full, tocsub=toc)

def budget():
    b = C.BUDGET
    rows = ''.join(f'<tr><td>{k}</td><td class="n">{a}</td><td class="n">{e}</td></tr>' for k,a,e in b['rows'])
    tot = ''.join(f'<tr class="{"tot" if i==0 else "tot2"}"><td>{k}</td><td class="n">{a}</td><td class="n">{e}</td></tr>' for i,(k,a,e) in enumerate(b['totals']))
    body = f'''<div class="kicker">{b['kicker']}</div><h1>{b['title']}</h1><div class="lead">{b['intro']}</div>
    <table class="bud"><tr><th>{b['col0']}</th><th style="width:34mm;text-align:right">{b['col1']}</th><th style="width:34mm;text-align:right">{b['col2']}</th></tr>{rows}{tot}</table>
    <div class="fine" style="margin-top:10pt">{b['note']}</div>'''
    add(body, right="BUDGET", toc="Budget")

def practical():
    p = C.PRACTICAL
    items = ''.join(f'<div class="it"><div class="lbl">{k}</div>{v}</div>' for k,v in p['items'])
    add(f'<div class="kicker">{p["kicker"]}</div><h1>{p["title"]}</h1><div class="prac">{items}</div>', right="INFOS PRATIQUES", toc="Infos pratiques")

def mode_emploi():
    m = D.MODE_EMPLOI
    half = m.get('split', 7)
    for i, part in enumerate((m['items'][:half], m['items'][half:])):
        items = ''.join(f'<div class="it"><div class="lbl">{k}</div>{v}</div>' for k,v in part)
        head = f'<div class="kicker">{m["kicker"]}</div><h1>{m["title"]}</h1><div class="lead">{m["intro"]}</div>' if i == 0 else '<h1 style="font-size:16pt">Mode d\'emploi, suite</h1>'
        add(f'{head}<div class="prac">{items}</div>', right="MODE D'EMPLOI", toc=("Mode d'emploi" if i == 0 else None))

def compare():
    c = C.COMPARE
    rows = ''.join(f'<tr{" class=tot" if k.startswith("Total") else ""}><td>{k}</td><td class="n">{a}</td><td class="n">{b}</td></tr>' for k,a,b in c['rows'])
    cols = ''.join(f'<div><div class="lbl" style="color:var(--red)">{k}</div>{v}</div>' for k,v in c['cols'])
    body = f'''<div class="kicker">{c['kicker']}</div><h1>{c['title']}</h1><div class="lead">{c['intro']}</div>
    <table class="cmp"><tr><th>{c['head'][0]}</th><th style="width:34mm;text-align:right">{c['head'][1]}</th><th style="width:34mm;text-align:right">{c['head'][2]}</th></tr>{rows}</table>
    <div class="cols2" style="font-size:8.8pt;margin-top:10pt">{cols}</div>
    <div class="box" style="margin-top:10pt"><div class="lbl">{c['verdict'][0]}</div>{c['verdict'][1]}</div>'''
    add(body, right="ALLIBERT OU PAR NOUS-MÊMES", toc="Allibert ou par nous-mêmes")

def changes():
    rows = ''.join(f'<div class="row"><div class="n">{i+1}</div><div class="k">{k}</div><div>{v}</div></div>' for i,(k,v) in enumerate(C.CHANGES))
    body = f'''<div class="kicker">Version 7.0</div><h1>Ce qui change par rapport à la version 6</h1>
    <div class="lead">{C.CHANGES_INTRO}</div><div class="chg">{rows}</div>'''
    add(body, right="CE QUI CHANGE", toc="Ce qui change dans la version 7")

def sources():
    src = ''.join(f'<li><a href="{u}">{t}</a></li>' for t,u in C.SOURCES)
    body = f'''<h1>Sources et crédits</h1><ul class="src">{src}</ul><div class="fine">{C.SOURCES_FOOT}</div>'''
    add(body, right="SOURCES ET CRÉDITS", toc="Sources et crédits")
    cred = json.load(open(os.path.join(ROOT, 'assets', 'img', 'jp_credits.json')))
    used = set()
    for mod in (B, C):
        for ch in mod.CHAPTERS:
            if ch.get('banner_file'): used.add(ch['banner_file'])
            for d in ch['days']:
                for f, _ in d.get('photos', []): used.add(f)
    rows = ''
    for e in cred:
        if e['file'] in used:
            rows += f'<tr><td><a href="{e["page"]}">{e["title"][:60]}</a></td><td>{e["author"]}</td><td>{e["license"]}</td></tr>'
    body2 = f'''<h1>Crédits photographiques</h1><div class="fine" style="margin:0 0 8pt 0">Photos issues de Wikimedia Commons, recadrées pour la mise en page ; chaque titre renvoie à la page d'origine. Les photos d'ouverture de chapitre reprennent des images des journées correspondantes.</div>
    <table class="cred"><tr><td style="font-weight:bold">Photo</td><td style="font-weight:bold">Auteur</td><td style="font-weight:bold">Licence</td></tr>{rows}</table>'''
    add(body2, right="SOURCES ET CRÉDITS")

# --- assemble --------------------------------------------------------------
cover(); toc_page(); timeline(); overview(); map_page(); before(); checklist()
for ch, layout in B.LAYOUTS + C.LAYOUTS:
    chapter(ch, layout)
budget(); compare(); practical(); mode_emploi(); changes(); sources()

toc_entries = []
for i, p in enumerate(pages):
    p['num'] = i + 1
    if p.get('toc'): toc_entries.append((p['toc'], i + 1, False))
    if p.get('tocsub'): toc_entries.append((p['tocsub'], i + 1, True))
first_ch = next(i for i,(t,n,s) in enumerate(toc_entries) if s)
toc_entries.insert(first_ch, ("L'itinéraire, jour après jour", toc_entries[first_ch][1], False))
tocrows = ''.join(f'<div class="row{" sub" if s else ""}"><span>{t}</span><span class="dots"></span><span>{n}</span></div>' for t,n,s in toc_entries)
rd = ''.join(f'<p>{x}</p>' for x in A.TOC_INTRO['read'])
tocbody = f'''<div class="kicker">Carnet de voyage</div><h1>Sommaire</h1><div class="toc">{tocrows}</div>
<div class="readbox"><div class="lbl">Lire ce carnet</div>{rd}<p style="margin-top:6pt"><b>{A.TOC_INTRO['v7']}</b></p></div>'''
for p in pages:
    if p['body'] == '__TOC__': p['body'] = tocbody

html = ['<!doctype html><html lang="fr"><head><meta charset="utf-8"><link rel="stylesheet" href="file://' + ROOT + '/src/style.css"><title>Japon en hiver, carnet v7</title></head><body>']
for p in pages:
    body = p['body']
    hdr = '' if p['nohdr'] else R(HDR, left=p['left'], right=p['right'])
    ftr = '' if p.get('nofooter') else R(FTR, num=p['num'], gen=GEN)
    tab = R(TAB, tab=p['tab'], theme=p['cls'])
    html.append(f'<div class="page {p["cls"]}{" full" if p["full"] else ""}" data-n="{p["num"]}">{hdr}{tab}{body}{ftr}</div>')
html.append('</body></html>')
out = os.path.join(ROOT, 'carnet_v7.html')
open(out, 'w').write('\n'.join(html))
print('pages', len(pages), '->', out)

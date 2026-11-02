# -*- coding: utf-8 -*-
"""Carnet v7, version mobile : un seul fichier HTML autonome (images, polices et scripts inclus), hors ligne, avec recherche."""
import base64, io, json, os, re, html as H
from datetime import date, timedelta
from PIL import Image
import content_a as A, content_b as B, content_c as C, content_d as D, content_e as E
try:
    import content_guide as G
except ImportError:
    G = None
MODE = 'allibert'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
FONTS = os.path.join(ROOT, "assets", "fonts")
OUT = os.path.join(ROOT, "Japon_hiver_v7_mobile.html" if MODE != "allibert" else "Japon_hiver_guide_allibert.html")
CHAPTERS = B.CHAPTERS + C.CHAPTERS
GEN = "2 novembre 2026"

# --- ressources inline ---------------------------------------------------------
_img_cache = {}
def img(name, maxw=760, q=66):
    key = (name, maxw, q)
    if key in _img_cache: return _img_cache[key]
    im = Image.open(os.path.join(IMG, name)).convert("RGB")
    w, h = im.size
    if w > maxw:
        im = im.resize((maxw, int(h * maxw / w)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True, progressive=True)
    uri = "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
    _img_cache[key] = uri
    return uri

def font(name):
    with open(os.path.join(FONTS, name), "rb") as f:
        return "data:font/ttf;base64," + base64.b64encode(f.read()).decode()

def esc(s): return H.escape(str(s), quote=False)
def cap(t): return t[:1].upper() + t[1:].lower().replace('allibert', 'Allibert').replace('jr ', 'JR ').replace('visit japan web', 'Visit Japan Web').replace('google maps', 'Google Maps').replace('takkyūbin', 'takkyūbin').replace('smartex', 'smartEX').replace('shinjuku, nagoya, namba, kyoto', 'Shinjuku, Nagoya, Namba, Kyoto').replace('azusa, hida, nozomi', 'Azusa, Hida, Nozomi').replace('suica', 'Suica')

def slug(s):
    s = re.sub(r"<[^>]+>", "", str(s)).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s.encode("ascii", "ignore").decode()).strip("-")
    return s

# --- icônes ---------------------------------------------------------------------
ICONS = dict(
    plane="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z",
    train="M12 2c-4 0-8 .5-8 4v9.5A3.5 3.5 0 0 0 7.5 19L6 20.5V21h12v-.5L16.5 19a3.5 3.5 0 0 0 3.5-3.5V6c0-3.5-4-4-8-4zM7.5 17a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm3.5-6H6V6h5v5zm5.5 6a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm1.5-6h-5V6h5v5z",
    bus="M4 16c0 .88.39 1.67 1 2.22V20a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1h8v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1.78c.61-.55 1-1.34 1-2.22V6c0-3.5-3.58-4-8-4s-8 .5-8 4v10zm3.5 1a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm9 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm1.5-6H6V6h12v5z",
    car="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z",
    walk="M13.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM9.8 8.9L7 23h2.1l1.8-8 2.1 2v6h2v-7.5l-2.1-2 .6-3C14.8 12 16.8 13 19 13v-2c-1.9 0-3.5-1-4.3-2.4l-1-1.6c-.4-.6-1-1-1.7-1-.3 0-.5.1-.8.1L6 8.3V13h2V9.6l1.8-.7z",
    bag="M17 6h-2V3c0-.55-.45-1-1-1h-4c-.55 0-1 .45-1 1v3H7c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2 0 .55.45 1 1 1s1-.45 1-1h6c0 .55.45 1 1 1s1-.45 1-1c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zM9.5 18H8V9h1.5v9zm3.25 0h-1.5V9h1.5v9zM13 6h-2V4h2v2zm3 12h-1.5V9H16v9z",
    search="M15.5 14h-.79l-.28-.27A6.47 6.47 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z",
    close="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z",
    days="M19 4h-1V2h-2v2H8V2H6v2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 16H5V9h14v11z",
    todo="M19 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zm-9 14l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z",
    bed="M7 13a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm12-6h-8v7H3V5H1v15h2v-3h18v3h2v-9a4 4 0 0 0-4-4z",
    info="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z",
    map="M20.5 3l-.16.03L15 5.1 9 3 3.36 4.9a.5.5 0 0 0-.36.48V20.5a.5.5 0 0 0 .5.5l.16-.03L9 18.9l6 2.1 5.64-1.9a.5.5 0 0 0 .36-.48V3.5a.5.5 0 0 0-.5-.5zM15 19l-6-2.11V5l6 2.11V19z",
    pin="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5z",
    ext="M19 19H5V5h7V3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14c1.1 0 2-.9 2-2v-7h-2v7zM14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z",
    chev="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z",
)
def ico(n, cls=""): return f'<svg class="i {cls}" viewBox="0 0 24 24"><path d="{ICONS[n]}"/></svg>'

RESA = {'O': ('Obligatoire', 'o'), 'C': ('À réserver', 'c'), 'L': ('Libre', 'l')}
LEVEL = {'B': ('Bloquant', 'b'), 'I': ('Important', 'i'), 'U': ('Utile', 'u')}

# --- dates des journées --------------------------------------------------------
def day_dates():
    d0 = date(2026, 12, 26); out = {}; i = 0
    for ch in CHAPTERS:
        for d in ch['days']:
            out[id(d)] = d0 + timedelta(days=i); i += 1
    return out
DATES = day_dates()
def dkey(d): return DATES[id(d)].isoformat()

# --- rendu des blocs -----------------------------------------------------------
def render_day(ch, d):
    k = dkey(d)
    if MODE == 'allibert':
        d = dict(d)
        ok = (ch['key'], d['num'])
        if ok in E.PRATIQUE_OVERRIDES: d['pratique'] = E.PRATIQUE_OVERRIDES[ok]
        if ok in E.COINCE_OVERRIDES: d['coince'] = E.COINCE_OVERRIDES[ok]
    head = "".join(f'<span class="hd"><b>{esc(a)}</b> {esc(b)}</span>' for a, b in d.get('head', []))
    photos = ""
    if d.get('photos'):
        photos = '<div class="photos">' + "".join(f'<figure><img src="{img(f)}" alt="{esc(c)}" loading="lazy"><figcaption>{esc(c)}</figcaption></figure>' for f, c in d['photos']) + '</div>'
    secs = "".join(f'<div class="sec"><div class="lbl">{esc(t)}</div><p>{x}</p></div>' for t, x in d.get('sections', []))
    side = ""
    if d.get('pratique'):
        side += '<div class="box prat"><div class="lbl">Pratique</div><ul>' + "".join(f'<li>{p}</li>' for p in d['pratique']) + '</ul></div>'
    if d.get('table'):
        side += f'<div class="box"><div class="lbl">À table</div><p>{d["table"]}</p></div>'
    if d.get('repere'):
        side += f'<div class="box rep"><div class="lbl">Repère</div><p><i>{d["repere"]}</i></p></div>'
    traj = ""
    if d.get('trajet'):
        rows = ""
        for r in d['trajet']:
            t, where, how, dur, s = (list(r) + ["", "", ""])[:5]
            badge = f'<span class="resa {RESA[s][1]}">{RESA[s][0]}</span>' if s in RESA else ""
            rows += f'<div class="tr"><div class="tt">{esc(t)}</div><div class="tb"><b>{esc(where)}</b>{("<small>" + esc(how) + "</small>") if how else ""}<div class="tm">{esc(dur)} {badge}</div></div></div>'
        traj = f'<details class="sub"><summary>{ico("train")} Le trajet, heure par heure</summary><div class="traj">{rows}</div></details>'
    coince = f'<details class="sub warn"><summary>⚠︎ Si ça coince</summary><p>{d["coince"]}</p></details>' if d.get('coince') else ""
    opts = ""
    if d.get('options'):
        opts = '<details class="sub"><summary>＋ Autres options et compléments</summary>' + "".join(f'<p><b>{esc(a)}</b> {b}</p>' for a, b in d['options']) + '</details>'
    stars = f'<span class="st">{d["stars"]}</span>' if d.get('stars') else ""
    return f'''<details class="day" id="d-{k}" data-date="{k}" data-s="day">
<summary><div class="dnum">{d["num"]}</div><div class="dtt"><div class="dow">{esc(d["dow"])}</div><div class="ttl">{esc(d["title"])}{stars}</div><div class="heads">{head}</div></div>{ico("chev","chev")}</summary>
<div class="dbody">{photos}{secs}{side}{traj}{coince}{opts}</div></details>'''

def render_strip(st):
    nodes, segs = st['nodes'], st['segs']
    out = f'<div class="strip"><div class="lbl">{esc(st["title"])}</div><div class="sline">'
    for i, n in enumerate(nodes):
        name, alt, _ = n
        out += f'<div class="snode"><span class="dot"></span><b>{esc(name)}</b><small>{alt} m</small></div>'
        if i < len(segs):
            lab, det, kind = segs[i]
            out += f'<div class="sseg s-{kind}">{esc(lab)}{(" · " + esc(det)) if det else ""}</div>'
    out += f'</div><p class="note">{st.get("note","")}</p></div>'
    return out


AREA_ORDER = ["Tokyo", "Kamakura", "Matsumoto", "Takayama", "Shirakawa-gō", "Ise", "Route de la côte", "Kumano", "Kii-Katsuura", "Kōya-san", "Osaka", "Kyoto", "Nara"]
CH_AREAS = dict(tokyo=["Tokyo", "Kamakura"], alpes=["Matsumoto", "Takayama", "Shirakawa-gō", "Ise"], kumano=["Route de la côte", "Kumano", "Kii-Katsuura"], koya=["Kōya-san", "Osaka"], kyoto=["Kyoto", "Nara"], retour=["Tokyo"])
KINDS = dict(manger=("Manger", "🍜"), cafe=("Café", "☕"), bain=("Bains", "♨"), course=("Course", "🏃"), photo=("Photo", "📷"), papeterie=("Papeterie", "✒"), voir=("À voir", "👁"), boutique=("Boutiques", "🛍"))
def maps_url(q): return "https://www.google.com/maps/search/?api=1&query=" + q.replace(" ", "+")

def render_hotels(ch):
    out = ""
    for name, when, addr, mq, site, notes in E.HOTELS.get(ch['key'], []):
        links = f'<a class="pill" href="{maps_url(mq)}" target="_blank" rel="noopener">{ico("pin")} Google Maps</a>'
        if site: links += f'<a class="pill" href="{site}" target="_blank" rel="noopener">{ico("ext")} Site</a>'
        out += f'''<div class="hotel" data-s="hotel" data-title="{esc(name)}"><div class="lbl">{ico("bed")} Hôtel Allibert · {esc(when)}</div><b>{esc(name)}</b><div class="addr">{esc(addr)}</div><p>{notes}</p><div class="links">{links}</div></div>'''
    return out

def guide_link(ch):
    if not G: return ""
    areas = CH_AREAS.get(ch['key'], [])
    out = "".join(f'<a class="btn ghost" href="#adresses" data-go="guide" data-target="area-{slug(a)}">{ico("pin")} Adresses : {esc(a)}</a>' for a in areas if any(g["area"] == a for g in G.GUIDE))
    runs = [g for g in G.GUIDE if g["kind"] == "course" and g["area"] in areas]
    if runs:
        out += '<div class="runs"><div class="lbl">🏃 Courir ici</div>' + "".join(f'<a class="runl" href="#adresses" data-go="guide" data-target="g-{slug(g["name"])}">{esc(g["name"])}<small>{esc(g.get("day",""))}</small>{ico("chev","chev")}</a>' for g in runs) + '</div>'
    return out

def render_guide():
    if not G: return '<div class="pad"><p class="note">Adresses en préparation.</p></div>'
    chips = "".join(f'<button class="fchip" data-k="{k}">{v[1]} {v[0]}</button>' for k, v in KINDS.items())
    out = f'''<div class="pad"><div class="kicker">LE GUIDE</div><h1>Adresses, étape par étape</h1><p class="intro">Restaurants, cafés, bains, boutiques photo et choses à voir, dans l'ordre du voyage. Chaque fiche ouvre Google Maps ; les horaires du Nouvel An sont donnés quand ils sont connus, sinon « inconnu » : vérifier la veille.</p>
<div class="filters"><button class="fchip on" data-k="all">Tout</button>{chips}</div></div>'''
    for area in AREA_ORDER:
        items = [g for g in G.GUIDE if g["area"] == area]
        if not items: continue
        cards = ""
        zoned = any(g.get("zone") for g in items)
        last_zone = None
        for g in sorted(items, key=lambda x: ((x.get("zone") or "") if zoned else "", list(KINDS).index(x["kind"]) if x["kind"] in KINDS else 9)):
            k = g["kind"]; kv = KINDS.get(k, (k, ""))
            if zoned and g.get("zone") != last_zone:
                last_zone = g.get("zone"); cards += f'<h3 class="zone">{esc(last_zone or "Ailleurs")}</h3>'
            links = f'<a class="pill" href="{maps_url(g["maps"])}" target="_blank" rel="noopener">{ico("pin")} Maps</a>'
            if g.get("website"): links += f'<a class="pill" href="{g["website"]}" target="_blank" rel="noopener">{ico("ext")} Site</a>'
            meta = []
            if g.get("hours") and g["hours"].lower() != "inconnu": meta.append(esc(g["hours"]))
            if g.get("booking") and g["booking"].lower() != "inconnu": meta.append(esc(g["booking"]))
            if g.get("day"): meta.append("Idéal : " + esc(g["day"]))
            cards += f'''<div class="gc k-{k}" id="g-{slug(g["name"])}" data-k="{k}" data-s="guide" data-title="{esc(g["name"])}"><div class="gk">{kv[1]} {kv[0]}{(" · " + esc(g["zone"])) if g.get("zone") else ""}</div><b>{esc(g["name"])}</b><p>{esc(g["what"])}</p>{('<div class="addr">' + esc(g["address"]) + '</div>') if g.get("address") else ""}{('<div class="meta">' + " · ".join(meta) + '</div>') if meta else ""}<div class="links">{links}</div></div>'''
        out += f'<section class="garea" id="area-{slug(area)}"><h2>{esc(area)}<small>{len(items)} adresses</small></h2>{cards}</section>'
    return out

def render_chapter(ch):
    key = ch['key']
    banner = f'<img src="{img(ch["banner"], 900, 62)}" alt="">' if ch.get('banner') else ''
    stats = "".join(f'<div><b>{esc(v)}</b><small>{esc(k)}</small></div>' for v, k in ch.get('stats', []))
    lc = ch.get('locals')
    locals_html = ""
    if lc:
        taste = "".join(f'<p><b>{esc(a)} :</b> {b}</p>' for a, b in lc['taste'])
        customs = "".join(f'<li>{c}</li>' for c in lc['customs'])
        anec = "".join(f'<p><i>{a}</i></p>' for a in lc['anecdotes'])
        locals_html = f'''<details class="sub loc" data-s="locals" data-title="{esc(lc["title"])}"><summary>{ico("pin")} {esc(lc["title"])}</summary>
<div class="lbl">À goûter</div>{taste}<div class="lbl">Comme les gens d'ici</div><ul>{customs}</ul><div class="lbl">Anecdotes</div>{anec}</details>'''
    mp = ""
    if ch.get('map'):
        mp = f'<figure class="mapfig"><img src="{img(ch["map"], 1400, 72)}" alt="Carte" loading="lazy" data-zoom><figcaption>{ch["map_caption"]}</figcaption></figure>'
    strips = "".join(render_strip(s) for s in ch.get('strips', []))
    days = "".join(render_day(ch, d) for d in ch['days'])
    return f'''<section class="chapter t-{ch["theme"]}" id="ch-{key}">
<div class="hero">{banner}<div class="shade"></div><div class="kj">{ch["kanji"]}</div><div class="htx"><div class="reg">{esc(ch["num"])} · {esc(ch["region"])}</div><h2>{esc(ch["title"])}</h2><div class="sub">{esc(ch["subtitle"])}</div></div></div>
<div class="chbody">
<p class="intro">{ch["intro"]}</p>
<div class="stats">{stats}</div>
<details class="sub" data-s="hist" data-title="{esc(ch["title"])} : un peu d'histoire"><summary>{ico("info")} Un peu d'histoire</summary><p>{ch["history"]}</p></details>
{locals_html}
{mp}{strips}
<div class="days">{days}</div>
{render_hotels(ch) if MODE == 'allibert' else f'<a class="btn ghost" href="#sleep/{key}" data-go="sleep" data-target="lg-{key}">{ico("bed")} Où dormir : {esc(ch["lodging"]["title"])}</a>'}
{guide_link(ch)}
</div></section>'''

def render_lodging(ch):
    lg = ch['lodging']
    def lst(items):
        out = ""
        for name, url, desc, score, price in items:
            tag = ""
            dl = desc.lower()
            if dl.startswith("notre choix") or "notre choix" in dl: tag = '<span class="tag choix">notre choix</span>'
            elif "allibert" in dl: tag = '<span class="tag alli">Allibert</span>'
            out += f'''<a class="lodge" href="{url}" target="_blank" rel="noopener" data-s="lodge" data-title="{esc(name)}">
<div class="ln"><b>{esc(name)}</b>{tag}<span class="score">{esc(score)}</span></div><div class="ld">{desc}</div><div class="lp">{esc(price)} {ico("ext")}</div></a>'''
        return out
    return f'''<section class="lg t-{ch["theme"]}" id="lg-{ch["key"]}"><h2><span class="kj">{ch["kanji"]}</span>{esc(lg["title"])}</h2>
<div class="lbl">{esc(lg["simple_label"])}</div>{lst(lg["simple"])}
<div class="lbl">{esc(lg["elegant_label"])}</div>{lst(lg["elegant"])}
<p class="note">{lg["note"]}</p></section>'''

def render_checklist():
    out = ""
    n = 0
    for page in (E.CHECK_PAGES if MODE == 'allibert' else A.CHECK_PAGES):
        for num, title, sub, items in page:
            rows = ""
            for dt, tt, detail, lvl in items:
                n += 1
                cid = f"c{n}-{slug(tt)[:30]}"
                lv = LEVEL.get(lvl, ('', ''))
                rows += f'''<div class="ck" data-s="check" data-title="{esc(tt)}"><input type="checkbox" id="{cid}" data-ck="{cid}"><label for="{cid}" class="box"></label>
<div class="ckb"><div class="ckh"><span class="when">{esc(dt)}</span> <span class="lvl {lv[1]}">{lv[0]}</span></div> <label for="{cid}" class="ckt">{esc(tt)}</label> <div class="ckd">{detail}</div></div></div>'''
            out += f'<section class="prio" id="prio-{num}"><h2><span class="pn">{num}</span>{esc(title)}<small>{esc(sub)}</small></h2>{rows}</section>'
    CI = E.CHECK_INTRO if MODE == 'allibert' else A.CHECK_INTRO
    blocks = "".join(f'<div class="warnbox"><b>{esc(a)}</b><p>{b}</p></div>' for a, b in CI['blocks'])
    return f'''<div class="pad"><div class="kicker">{esc(CI["kicker"])}</div><h1>{esc(CI["title"])}</h1><p class="intro">{CI["intro"]}</p>
<div class="progress"><div class="bar"><div id="pbar"></div></div><div id="ptxt"></div></div>
<details class="sub"><summary>⚠︎ Ce qui peut bloquer</summary>{blocks}</details></div>{out}'''

def render_timeline():
    rows = ""
    for dt, title, night, chips, car in A.TIMELINE['rows']:
        ch = "".join(f'<span class="chip {k}">{ico(i)}{esc(t)}</span>' for i, t, k in chips)
        # cible : la journée correspondante
        rows += f'<a class="tl{" car" if car else ""}" data-tl="{esc(dt)}"><div class="tld">{esc(dt)}</div><div class="tlb"><b>{esc(title)}</b><div class="chips">{ch}</div></div><div class="tln">{ico("bed")}{esc(night)}</div></a>'
    return f'<section class="timeline pad" id="timeline"><div class="kicker">{esc(A.TIMELINE["kicker"])}</div><h1>{esc(A.TIMELINE["title"])}</h1><div class="tls">{rows}</div><p class="note">{esc(A.TIMELINE["legend_bp"]).capitalize()} sur fond sable.</p></section>'

def render_info_allibert():
    inc = "".join(f"<li>{x}</li>" for x in E.INCLUDED["yes"]); exc = "".join(f"<li>{x}</li>" for x in E.INCLUDED["no"])
    before = "".join(f'<details class="sub" data-s="info" data-title="{esc(t)}"><summary>{esc(cap(t))}</summary><div class="rich">{b}</div></details>' for t, b in E.BEFORE_BOXES + [A.BEFORE['boxes'][0], A.BEFORE['boxes'][1]])
    prac = "".join(f'<details class="sub" data-s="info" data-title="{esc(t)}"><summary>{esc(cap(t))}</summary><p>{E.PRACTICAL_OVERRIDES.get(t, b)}</p></details>' for t, b in C.PRACTICAL['items'] + E.PRACTICAL_EXTRA)
    mode = "".join(f'<details class="sub" data-s="mode" data-title="{esc(t)}"><summary>{esc(cap(t))}</summary><p>{b}</p></details>' for t, b in D.MODE_EMPLOI['items'] if "RÉSERVÉS" not in t)
    bud = "".join(f'<tr><td>{esc(a)}</td><td>{esc(b)}</td><td>{esc(c)}</td></tr>' for a, b, c in E.BUDGET['rows']) + f'<tr class="tot"><td>{esc(E.BUDGET["total"][0])}</td><td>{esc(E.BUDGET["total"][1])}</td><td></td></tr>'
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)} {ico("ext")}</a></li>' for t, u in C.SOURCES)
    return f'''<div class="pad">
<div class="kicker">AVANT DE PARTIR</div><h1>Le voyage avec Allibert</h1><p class="intro">{E.INTRO}</p>
<details class="sub" data-s="info" data-title="Ce qui est compris"><summary>Ce qui est compris</summary><ul>{inc}</ul></details>
<details class="sub" data-s="info" data-title="Ce qui reste à notre charge"><summary>Ce qui reste à notre charge</summary><ul>{exc}</ul></details>
<div class="warnbox"><b>POINTS OUVERTS</b><p>{E.INCLUDED["todo"]}</p></div>
{before}
<div class="kicker">SUR PLACE</div><h1>{esc(C.PRACTICAL["title"])}</h1>{prac}
<div class="kicker">{esc(D.MODE_EMPLOI["kicker"])}</div><h1>{esc(D.MODE_EMPLOI["title"])}</h1><p class="intro">{D.MODE_EMPLOI["intro"]}</p>{mode}
<div class="kicker">{esc(E.BUDGET["kicker"])}</div><h1>{esc(E.BUDGET["title"])}</h1><p class="intro">{E.BUDGET["intro"]}</p>
<table class="tbl cmp"><thead><tr><th>{esc(E.BUDGET["col0"])}</th><th>{esc(E.BUDGET["col1"])}</th><th>{esc(E.BUDGET["col2"])}</th></tr></thead><tbody>{bud}</tbody></table><p class="note">{E.BUDGET["note"]}</p>
<div class="kicker">SOURCES</div><h1>Sources et crédits</h1><ul class="src">{src}</ul><p class="note">{C.SOURCES_FOOT} Photos : Wikimedia Commons, crédits dans le carnet PDF. {esc(E.FOOT)}. Version mobile générée le {GEN}.</p>
</div>'''

def render_info():
    if MODE == 'allibert': return render_info_allibert()
    before = "".join(f'<details class="sub" data-s="info" data-title="{esc(t)}"><summary>{esc(cap(t))}</summary><div class="rich">{b}</div></details>' for t, b in A.BEFORE['boxes'])
    prac = "".join(f'<details class="sub" data-s="info" data-title="{esc(t)}"><summary>{esc(cap(t))}</summary><p>{b}</p></details>' for t, b in C.PRACTICAL['items'])
    mode = "".join(f'<details class="sub" data-s="mode" data-title="{esc(t)}"><summary>{esc(cap(t))}</summary><p>{b}</p></details>' for t, b in D.MODE_EMPLOI['items'])
    bud = "".join(f'<tr><td>{esc(a)}</td><td>{esc(b)}</td><td>{esc(c)}</td></tr>' for a, b, c in C.BUDGET['rows'])
    cmp_rows = "".join(f'<tr><td>{esc(a)}</td><td>{esc(b)}</td><td>{esc(c)}</td></tr>' for a, b, c in C.COMPARE['rows'])
    changes = "".join(f'<p><b>{esc(a)}</b> {b}</p>' for a, b in C.CHANGES)
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)} {ico("ext")}</a></li>' for t, u in C.SOURCES)
    cover = A.COVER
    return f'''<div class="pad">
<div class="kicker">AVANT DE PARTIR</div><h1>{esc(A.BEFORE["title"])}</h1>{before}<p class="note">{A.BEFORE["foot"]}</p>
<div class="kicker">SUR PLACE</div><h1>{esc(C.PRACTICAL["title"])}</h1>{prac}
<div class="kicker">{esc(D.MODE_EMPLOI["kicker"])}</div><h1>{esc(D.MODE_EMPLOI["title"])}</h1><p class="intro">{D.MODE_EMPLOI["intro"]}</p>{mode}
<div class="kicker">{esc(C.BUDGET["kicker"])}</div><h1>{esc(C.BUDGET["title"])}</h1><p class="intro">{C.BUDGET["intro"]}</p>
<table class="tbl"><thead><tr><th>{esc(C.BUDGET["col0"])}</th><th>{esc(C.BUDGET["col1"])}</th><th>{esc(C.BUDGET["col2"])}</th></tr></thead><tbody>{bud}</tbody></table><p class="note">{C.BUDGET.get("note","")}</p>
<div class="kicker">{esc(C.COMPARE["kicker"])}</div><h1>{esc(C.COMPARE["title"])}</h1><p class="intro">{C.COMPARE["intro"]}</p>
<table class="tbl cmp"><thead><tr><th>{esc(C.COMPARE["head"][0])}</th><th>{esc(C.COMPARE["head"][1])}</th><th>{esc(C.COMPARE["head"][2])}</th></tr></thead><tbody>{cmp_rows}</tbody></table>
<div class="rich">{"".join("<p><b>"+esc(c[0].capitalize())+".</b> "+c[1]+"</p>" for c in (C.COMPARE.get("cols") or []))}</div><div class="warnbox"><b>{esc(C.COMPARE["verdict"][0])}</b><p>{C.COMPARE["verdict"][1]}</p></div>
<div class="kicker">VERSION 7.0</div><h1>Ce qui change par rapport à la version 6</h1><p class="intro">{C.CHANGES_INTRO}</p><div class="rich">{changes}</div>
<div class="kicker">SOURCES</div><h1>Sources et crédits</h1><ul class="src">{src}</ul><p class="note">{C.SOURCES_FOOT} Photos : Wikimedia Commons, crédits dans le carnet PDF. {esc(cover["foot"])}. Version mobile générée le {GEN}.</p>
</div>'''

def render_maps():
    out = f'<div class="pad"><div class="kicker">{esc(A.MAP_PAGE["kicker"])}</div><h1>{esc(A.MAP_PAGE["title"])}</h1>'
    out += f'<figure class="mapfig big"><img src="{img(A.MAP_PAGE["image"], 1600, 74)}" alt="Carte générale" data-zoom><figcaption>{A.MAP_PAGE["caption"]}</figcaption></figure>'
    out += "".join(f'<details class="sub"><summary>{esc(cap(t))}</summary><p>{b}</p></details>' for t, b in A.MAP_PAGE['cols'])
    for ch in CHAPTERS:
        if ch.get('map'):
            out += f'<h2 class="mh"><span class="kj">{ch["kanji"]}</span>{esc(ch["title"])}</h2><figure class="mapfig"><img src="{img(ch["map"], 1400, 72)}" alt="Carte" loading="lazy" data-zoom><figcaption>{ch["map_caption"]}</figcaption></figure>'
        if ch.get('plans'):
            p = ch['plans']
            out += f'<h2 class="mh">{esc(p["title"])}</h2>'
            for f, c in (p['left'], p['right']):
                out += f'<figure class="mapfig"><img src="{img(f, 1400, 72)}" alt="Plan" loading="lazy" data-zoom><figcaption>{c}</figcaption></figure>'
    return out + '</div>'

# --- assemblage ----------------------------------------------------------------
cover = A.COVER
home = f'''<section class="cover"><div class="ckj">{cover["kanji"]}</div><div class="ck1">{esc(E.KICKER if MODE == 'allibert' else cover["kicker"])}</div><h1 class="ct">Japon <i>en hiver</i></h1><div class="cd">{esc(cover["dates"])}</div><p>{esc(cover["line"])}</p>
<div class="stops">{"".join("<span>"+esc(s)+"</span>" for s in cover["stops"])}</div>
<button class="btn today" id="todayBtn">{ico("days")} Aujourd'hui</button></section>'''
brief = "".join(f'<details class="sub" data-s="info" data-title="{esc(a)}"><summary>{esc(a)}</summary><p>{E.BRIEF_OVERRIDES.get(a, b) if MODE == "allibert" else b}</p></details>' for a, b in A.OVERVIEW['brief'])
overview = f'<div class="pad"><div class="kicker">{esc(A.OVERVIEW["kicker"])}</div><h1>{esc(A.OVERVIEW["title"])}</h1><p class="intro">{A.OVERVIEW["intro"]}</p>{brief}</div>'
chapters = "".join(render_chapter(ch) for ch in CHAPTERS)
lodgings = "".join(render_lodging(ch) for ch in CHAPTERS)
toc = "".join(f'<a class="tocl t-{ch["theme"]}" href="#voyage" data-target="ch-{ch["key"]}"><span class="kj">{ch["kanji"]}</span><div><b>{esc(ch["title"])}</b><small>{esc(ch["subtitle"])}</small></div>{ico("chev","chev")}</a>' for ch in CHAPTERS)

CSS = r'''
@font-face{font-family:"DMS";src:url(FONT_R) format("truetype");font-weight:400;font-display:swap}
@font-face{font-family:"DMS";src:url(FONT_I) format("truetype");font-style:italic;font-display:swap}
:root{--navy:#131f2d;--navy2:#2d3f56;--red:#8c2f38;--gold:#b8914f;--paper:#f9f6f0;--panel:#f1ece2;--ink:#1f2430;--grey:#5e6572;--rule:#ddd6cb;--bg:#f9f6f0;--card:#fff;--sand:#f4ecd9;--theme:var(--navy);
 --ui:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;--body:Charter,"Iowan Old Style","Palatino Linotype",Georgia,"Noto Serif",serif;--jp:"Hiragino Mincho ProN","Yu Mincho","Noto Serif JP",serif}
@media(prefers-color-scheme:dark){:root{--paper:#121418;--bg:#121418;--card:#1b1f26;--panel:#20252e;--ink:#e8e4dc;--grey:#a39c90;--rule:#2f3540;--sand:#2a2721;--navy2:#9fb3cc;--gold:#d2ad6a}}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.5;padding-bottom:calc(64px + env(safe-area-inset-bottom))}
a{color:var(--red)} b{font-weight:600}
h1{font-family:"DMS",var(--body);font-weight:400;font-size:26px;line-height:1.1;margin:4px 0 10px}
h2{font-family:"DMS",var(--body);font-weight:400;font-size:22px;line-height:1.15;margin:0 0 8px}
.kicker{font-family:var(--ui);font-size:10.5px;font-weight:700;letter-spacing:.14em;color:var(--red);margin-top:26px}
.lbl{font-family:var(--ui);font-size:10.5px;font-weight:700;letter-spacing:.12em;color:var(--red);text-transform:uppercase;margin:12px 0 4px}
.pad{padding:0 16px}
p{margin:0 0 10px} .intro{font-size:17px;line-height:1.5}
.note{font-size:13px;color:var(--grey);line-height:1.45} .rich p{margin:0 0 8px} .rich ul{padding-left:18px}
.i{width:18px;height:18px;fill:currentColor;vertical-align:-4px;flex:none}
.t-red{--theme:var(--red)} .t-navy{--theme:var(--navy)}
.hidden{display:none!important}
/* top */
.top{position:sticky;top:0;z-index:20;background:var(--navy);color:#fff;display:flex;align-items:center;gap:10px;padding:calc(8px + env(safe-area-inset-top)) 14px 8px;font-family:var(--ui)}
.top .kj{font-family:var(--jp);font-size:24px;color:var(--gold);line-height:1}
.top .brand{flex:1;line-height:1.15} .top .brand b{font-family:"DMS";font-weight:400;font-size:18px;display:block} .top .brand small{font-size:11px;opacity:.75}
.top .jst{font-size:12px;opacity:.85;text-align:right;line-height:1.2} .top .jst b{display:block;font-size:15px;font-variant-numeric:tabular-nums}
.top button{background:none;border:0;color:#fff;padding:6px}
.search{position:sticky;top:0;z-index:21;background:var(--navy);padding:calc(8px + env(safe-area-inset-top)) 12px 10px;font-family:var(--ui)}
.search .row{display:flex;gap:8px;align-items:center}
.search input{flex:1;font:16px var(--ui);padding:10px 14px;border-radius:12px;border:0;background:#fff;color:#111}
.search button{background:none;border:0;color:#fff;padding:6px}
#results{position:fixed;inset:0;top:64px;z-index:19;background:var(--bg);overflow:auto;padding:8px 16px 90px}
.res{display:block;padding:12px 0;border-bottom:1px solid var(--rule);color:var(--ink);text-decoration:none}
.res .rk{font-family:var(--ui);font-size:10.5px;letter-spacing:.1em;color:var(--red);font-weight:700;text-transform:uppercase}
.res b{display:block;font-family:"DMS";font-weight:400;font-size:17px}
.res small{display:block;color:var(--grey);font-size:13px;line-height:1.4} mark{background:#f5e6a8;color:#111;border-radius:2px}
@media(prefers-color-scheme:dark){mark{background:#b8914f;color:#111}}
/* tabs */
.tabs{position:fixed;left:0;right:0;bottom:0;z-index:20;display:flex;background:var(--card);border-top:1px solid var(--rule);padding-bottom:env(safe-area-inset-bottom);font-family:var(--ui)}
.tabs button{flex:1;background:none;border:0;color:var(--grey);font:10.5px var(--ui);padding:8px 0 6px;display:flex;flex-direction:column;align-items:center;gap:2px}
.tabs button .i{width:24px;height:24px} .tabs button.on{color:var(--red)}
main>section.view{display:none} main>section.view.on{display:block}
/* cover */
.cover{position:relative;background:var(--navy);color:#fff;padding:28px 20px 24px;overflow:hidden}
.cover .ckj{position:absolute;right:-6px;top:-14px;font-family:var(--jp);font-size:170px;color:#1c2a3c;line-height:1}
.cover .ck1{position:relative;font-family:var(--ui);font-size:10px;letter-spacing:.14em;font-weight:700;color:var(--gold)}
.cover .ct{position:relative;font-size:48px;margin:6px 0 4px;color:#fff} .cover .ct i{display:block;font-size:30px;color:var(--gold)}
.cover .cd{position:relative;font-family:var(--ui);font-size:13px;opacity:.9} .cover p{position:relative;font-size:14px;opacity:.85;margin-top:6px}
.cover .stops{position:relative;display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 16px} .cover .stops span{font:11px var(--ui);background:rgba(255,255,255,.12);padding:3px 8px;border-radius:999px}
.btn{position:relative;display:inline-flex;align-items:center;gap:8px;font:600 14px var(--ui);background:var(--red);color:#fff;border:0;border-radius:12px;padding:10px 16px;text-decoration:none}
.btn.ghost{background:transparent;color:var(--red);border:1.5px solid var(--red);margin:14px 0 6px;width:100%;justify-content:center}
/* toc */
.toc{padding:14px 16px 4px}
.tocl{display:flex;align-items:center;gap:12px;background:var(--card);border-radius:14px;padding:12px 12px;margin-bottom:8px;text-decoration:none;color:var(--ink);border-left:4px solid var(--theme);box-shadow:0 1px 3px rgba(0,0,0,.06)}
.tocl .kj{font-family:var(--jp);font-size:20px;color:var(--theme);width:46px;flex:none;line-height:1.1} .tocl b{font-family:"DMS";font-weight:400;font-size:17px;display:block;line-height:1.15}
.tocl small{display:block;color:var(--grey);font-size:12.5px;font-family:var(--ui)} .tocl>div{flex:1} .tocl .chev{color:var(--grey);margin-left:auto}
/* timeline */
.tls{margin-top:8px} .tl{display:flex;gap:10px;padding:10px 10px;border-radius:12px;background:var(--card);margin-bottom:6px;color:var(--ink);text-decoration:none;align-items:flex-start}
.tl.car{background:var(--sand)} .tld{font:700 12px var(--ui);color:var(--red);width:58px;flex:none;padding-top:2px} .tlb{flex:1} .tlb b{font-family:"DMS";font-weight:400;font-size:16px;line-height:1.1;display:block}
.tln{font:11px var(--ui);color:var(--grey);text-align:right;flex:none;max-width:84px;display:flex;flex-direction:column;align-items:flex-end;gap:2px}
.chips{display:flex;flex-wrap:wrap;gap:4px 8px;margin-top:4px} .chip{font:11px var(--ui);color:var(--grey);display:inline-flex;align-items:center;gap:3px} .chip .i{width:14px;height:14px}
.chip.r{color:var(--red)} .chip.w{color:var(--gold)}
/* chapter */
.chapter{margin-top:26px}
.hero{position:relative;height:230px;background:var(--navy);overflow:hidden}
.hero img{width:100%;height:100%;object-fit:cover;display:block} .hero .shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.15),rgba(0,0,0,.05) 40%,rgba(0,0,0,.65))}
.hero .kj{position:absolute;right:14px;top:12px;font-family:var(--jp);font-size:40px;color:#fff;text-shadow:0 1px 6px rgba(0,0,0,.5);line-height:1}
.hero .htx{position:absolute;left:16px;right:16px;bottom:14px;color:#fff}
.hero .reg{font:700 10px var(--ui);letter-spacing:.14em;color:var(--gold)} .hero h2{font-size:30px;margin:2px 0;color:#fff;text-shadow:0 1px 6px rgba(0,0,0,.5)} .hero .sub{font-family:"DMS";font-style:italic;font-size:14px;opacity:.95}
.chapter{border-bottom:3px solid var(--theme)}
.chbody{padding:16px 16px 20px}
.stats{display:flex;gap:8px;margin:6px 0 12px} .stats div{flex:1;background:var(--card);border-radius:10px;padding:8px 10px;border-top:2px solid var(--theme)} .stats b{font-family:"DMS";font-weight:400;font-size:20px;display:block;line-height:1.1;color:var(--theme)} .stats small{font:11px var(--ui);color:var(--grey)}
details.sub{background:var(--card);border-radius:12px;margin:8px 0;padding:0 12px;box-shadow:0 1px 2px rgba(0,0,0,.05)}
details.sub>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:8px;padding:11px 0;font:600 14px var(--ui);color:var(--ink)}
details.sub>summary::-webkit-details-marker{display:none} details.sub>summary::after{content:"";margin-left:auto;width:8px;height:8px;border-right:2px solid var(--grey);border-bottom:2px solid var(--grey);transform:rotate(45deg);transition:transform .2s;flex:none}
details.sub[open]>summary::after{transform:rotate(-135deg)} details.sub>*:not(summary){margin-bottom:10px} details.sub>p:last-child,details.sub>div:last-child{padding-bottom:12px;margin-bottom:0}
details.sub.warn>summary{color:var(--red)} details.sub.loc .lbl:first-of-type{margin-top:0}
.mapfig{margin:12px 0;background:var(--card);border-radius:12px;padding:6px;box-shadow:0 1px 2px rgba(0,0,0,.05)} .mapfig img{width:100%;display:block;border-radius:8px;cursor:zoom-in} .mapfig figcaption{font-size:12.5px;color:var(--grey);line-height:1.4;padding:6px 4px 2px}
/* strips */
.strip{background:var(--card);border-radius:12px;padding:10px 12px;margin:10px 0} .sline{border-left:2px solid var(--rule);margin-left:6px;padding-left:14px}
.snode{position:relative;font-family:var(--ui);font-size:14px;padding:2px 0} .snode .dot{position:absolute;left:-20px;top:9px;width:10px;height:10px;border-radius:50%;background:var(--red);border:2px solid var(--paper)} .snode small{color:var(--grey);margin-left:6px}
.sseg{font:12.5px var(--ui);color:var(--grey);padding:4px 0 6px} .sseg.s-c{color:var(--red)} .sseg.s-t,.sseg.s-b{color:var(--navy2)}
/* days */
.days{margin-top:14px}
details.day{background:var(--card);border-radius:14px;margin:10px 0;box-shadow:0 1px 3px rgba(0,0,0,.07);border-left:4px solid var(--theme)}
details.day.today{box-shadow:0 0 0 2px var(--gold)}
details.day>summary{list-style:none;display:flex;gap:12px;padding:12px 12px 12px 10px;cursor:pointer;align-items:flex-start} details.day>summary::-webkit-details-marker{display:none}
.dnum{font-family:"DMS";font-size:34px;line-height:.9;color:var(--theme);width:44px;flex:none;text-align:center;padding-top:4px} .dnum sup{font-size:14px}
.dtt{flex:1} .dow{font:700 10.5px var(--ui);letter-spacing:.1em;color:var(--red)} .dtt .ttl{font-family:"DMS";font-size:19px;line-height:1.15;margin:2px 0 4px} .st{color:var(--gold);margin-left:6px;font-size:14px}
.heads{display:flex;flex-wrap:wrap;gap:3px 10px} .hd{font:11.5px var(--ui);color:var(--grey)} .hd b{color:var(--ink);font-weight:600}
details.day>summary .chev{color:var(--grey);margin-top:6px;transition:transform .2s} details.day[open]>summary .chev{transform:rotate(90deg)}
.dbody{padding:0 12px 12px}
.photos{display:flex;gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -12px 10px;padding:0 12px;-webkit-overflow-scrolling:touch}
.photos figure{flex:0 0 78%;margin:0;scroll-snap-align:start} .photos img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:10px;display:block} .photos figcaption{font:11px var(--ui);color:var(--grey);padding:4px 2px}
.sec{margin-bottom:6px} .sec .lbl{margin-top:8px}
.box{background:var(--panel);border-radius:10px;padding:8px 12px;margin:10px 0} .box .lbl{margin-top:0} .box ul{margin:0;padding-left:18px} .box li{margin-bottom:4px;font-size:14.5px} .box p{margin:0;font-size:14.5px}
.box.rep p{color:var(--grey)}
.traj{padding-bottom:8px} .tr{display:flex;gap:10px;padding:7px 0;border-top:1px solid var(--rule)} .tt{font:700 12px var(--ui);color:var(--red);width:60px;flex:none;padding-top:2px;line-height:1.3} .tb{flex:1;font-size:14.5px} .tb b{display:block;line-height:1.3} .tb small{display:block;color:var(--grey);font-size:13px;line-height:1.35}
.tm{font:11.5px var(--ui);color:var(--grey);margin-top:2px;display:flex;gap:8px;align-items:center}
.resa{font:700 10px var(--ui);letter-spacing:.06em;text-transform:uppercase;padding:1px 6px;border-radius:999px;border:1px solid} .resa.o{color:var(--red);border-color:var(--red)} .resa.c{color:var(--gold);border-color:var(--gold)} .resa.l{color:var(--grey);border-color:var(--rule)}
/* checklist */
.progress{margin:6px 0 14px;font:12px var(--ui);color:var(--grey)} .bar{height:6px;background:var(--rule);border-radius:3px;overflow:hidden;margin-bottom:4px} #pbar{height:100%;background:var(--red);width:0;transition:width .3s}
.warnbox{background:var(--sand);border-radius:10px;padding:8px 12px;margin:8px 0;font-size:14px} .warnbox b{font-family:var(--ui);font-size:11px;letter-spacing:.08em;color:var(--red)} .warnbox p{margin:2px 0 0}
.prio{padding:8px 16px 4px} .prio h2{display:flex;align-items:baseline;gap:10px;margin:18px 0 8px;padding-bottom:6px;border-bottom:2px solid var(--red)} .prio h2 .pn{font-family:"DMS";font-size:30px;color:var(--red)} .prio h2 small{font:12px var(--ui);color:var(--grey);margin-left:auto;text-align:right}
.ck{display:flex;gap:12px;background:var(--card);border-radius:12px;padding:12px;margin-bottom:8px;box-shadow:0 1px 2px rgba(0,0,0,.05)} .ck input{display:none}
.ck label.box{width:24px;height:24px;flex:none;border:2px solid var(--grey);border-radius:7px;margin:4px 0 0;position:relative;cursor:pointer;padding:0;background:none}
.ck input:checked+label.box{background:var(--red);border-color:var(--red)} .ck input:checked+label.box::after{content:"";position:absolute;left:7px;top:2px;width:6px;height:12px;border:solid #fff;border-width:0 2.5px 2.5px 0;transform:rotate(45deg)}
.ck input:checked~.ckb{opacity:.5} .ck input:checked~.ckb .ckt{text-decoration:line-through}
.ckb{flex:1;min-width:0} .ckh{display:flex;gap:8px;align-items:center;font:700 11px var(--ui)} .when{color:var(--grey);letter-spacing:.04em} .lvl{letter-spacing:.08em;text-transform:uppercase;font-size:9.5px;padding:1px 6px;border-radius:999px;color:#fff;background:var(--grey)} .lvl.b{background:var(--red)} .lvl.i{background:var(--gold)}
.ckt{display:block;font-family:"DMS";font-size:17px;line-height:1.2;margin:4px 0;cursor:pointer} .ckd{font-size:14px;line-height:1.45;color:var(--ink)} .ckd a{word-break:break-word}
/* lodging */
.lg{padding:14px 16px 10px;border-bottom:3px solid var(--theme)} .lg h2{display:flex;align-items:center;gap:10px} .lg h2 .kj,.mh .kj{font-family:var(--jp);font-size:18px;color:var(--theme)}
.lodge{display:block;background:var(--card);border-radius:12px;padding:10px 12px;margin-bottom:8px;color:var(--ink);text-decoration:none;box-shadow:0 1px 2px rgba(0,0,0,.05);border-left:3px solid var(--rule)}
.ln{display:flex;align-items:center;gap:8px;flex-wrap:wrap} .ln b{font-family:"DMS";font-weight:400;font-size:17px;color:var(--red)} .score{margin-left:auto;font:700 12px var(--ui);color:#fff;background:var(--navy2);padding:2px 7px;border-radius:6px}
.tag{font:700 9.5px var(--ui);letter-spacing:.08em;text-transform:uppercase;padding:2px 7px;border-radius:999px} .tag.choix{background:var(--gold);color:#fff} .tag.alli{background:var(--rule);color:var(--grey)}
.ld{font-size:13.5px;color:var(--grey);line-height:1.4;margin:3px 0} .lp{font:700 13px var(--ui);display:flex;align-items:center;gap:4px}
/* info */
.tbl{width:100%;border-collapse:collapse;font-size:13.5px;margin:6px 0 4px;background:var(--card);border-radius:10px;overflow:hidden} .tbl th{font:700 10.5px var(--ui);letter-spacing:.08em;text-transform:uppercase;text-align:left;padding:8px;background:var(--navy);color:#fff} .tbl td{padding:7px 8px;border-top:1px solid var(--rule);vertical-align:top} .tbl td:nth-child(n+2){white-space:nowrap;text-align:right} .tbl.cmp td:nth-child(n+2){white-space:normal;text-align:left;width:31%}
.src{padding-left:0;list-style:none} .src li{padding:6px 0;border-bottom:1px solid var(--rule);font-size:14px}
.mh{margin-top:22px;display:flex;align-items:center;gap:8px}
/* lightbox */
#lb{position:fixed;inset:0;z-index:50;background:#000;display:none;overflow:auto;-webkit-overflow-scrolling:touch} #lb.on{display:block} #lb img{display:block;min-width:100%;width:200%;max-width:none;margin:auto} #lb button{position:fixed;top:calc(10px + env(safe-area-inset-top));right:10px;background:rgba(0,0,0,.6);color:#fff;border:0;border-radius:50%;width:40px;height:40px;z-index:51} #lb .hint{position:fixed;bottom:16px;left:0;right:0;text-align:center;color:#fff;font:12px var(--ui);opacity:.7}
.flash{animation:flash 1.6s ease-out} @keyframes flash{0%{box-shadow:0 0 0 3px var(--gold)}100%{box-shadow:0 0 0 0 transparent}}
.day .photos img{content-visibility:auto}
.hotel{background:var(--card);border-radius:12px;padding:10px 12px;margin:14px 0 6px;border-left:4px solid var(--gold);box-shadow:0 1px 2px rgba(0,0,0,.05)} .hotel .lbl{margin-top:0;display:flex;align-items:center;gap:6px} .hotel b{font-family:"DMS";font-weight:400;font-size:18px;display:block;line-height:1.15} .hotel .addr,.gc .addr{font:12px var(--ui);color:var(--grey);margin:2px 0 4px} .hotel p{font-size:14px;line-height:1.45;margin:4px 0 6px}
.links{display:flex;gap:8px;flex-wrap:wrap;margin-top:4px} .pill{display:inline-flex;align-items:center;gap:4px;font:600 12px var(--ui);color:var(--red);border:1px solid var(--red);border-radius:999px;padding:4px 10px;text-decoration:none} .pill .i{width:14px;height:14px}
.filters{display:flex;gap:6px;overflow-x:auto;padding:4px 0 10px;margin:0 -16px;padding-left:16px;padding-right:16px;-webkit-overflow-scrolling:touch} .fchip{flex:none;font:600 12.5px var(--ui);background:var(--card);color:var(--ink);border:1px solid var(--rule);border-radius:999px;padding:7px 12px} .fchip.on{background:var(--red);color:#fff;border-color:var(--red)}
.garea{padding:6px 16px 10px} .garea h2{display:flex;align-items:baseline;gap:10px;margin:16px 0 8px;padding-bottom:6px;border-bottom:2px solid var(--red)} .garea h2 small{font:12px var(--ui);color:var(--grey);margin-left:auto}
.gc{background:var(--card);border-radius:12px;padding:10px 12px;margin-bottom:8px;box-shadow:0 1px 2px rgba(0,0,0,.05);border-left:3px solid var(--rule)} .gc.k-manger{border-left-color:var(--red)} .gc.k-cafe{border-left-color:#8a6d3b} .gc.k-bain{border-left-color:#3b7ea1} .gc.k-photo{border-left-color:var(--navy)} .gc.k-voir{border-left-color:var(--gold)} .gc.k-boutique{border-left-color:#6b5b95} .gc.k-course{border-left-color:#2f8f5b} .gc.k-papeterie{border-left-color:#8a5a2b}
.gc .gk{font:700 10px var(--ui);letter-spacing:.1em;text-transform:uppercase;color:var(--grey)} .gc b{font-family:"DMS";font-weight:400;font-size:17px;display:block;line-height:1.15;margin:2px 0} .gc p{font-size:14px;line-height:1.45;margin:2px 0 4px} .gc .meta{font:12px var(--ui);color:var(--grey);line-height:1.4;margin-bottom:4px}
.tbl tr.tot td{font-weight:700;background:var(--panel)}
.runs{margin:10px 0 4px} .runl{display:flex;align-items:center;gap:8px;background:var(--card);border-radius:10px;padding:9px 12px;margin-bottom:6px;color:var(--ink);text-decoration:none;font:600 14px var(--ui);border-left:3px solid #2f8f5b} .runl small{color:var(--grey);font-weight:400;margin-left:auto} .runl .chev{color:var(--grey)}
.zone{font:700 11px var(--ui);letter-spacing:.12em;text-transform:uppercase;color:var(--grey);margin:14px 0 6px}
'''

JS = r'''
(function(){
const $=s=>document.querySelector(s), $$=s=>Array.from(document.querySelectorAll(s));
// tabs
const views={voyage:'v-voyage',guide:'v-guide',todo:'v-todo',sleep:'v-sleep',info:'v-info',maps:'v-maps'};
function show(name,keep){ for(const k in views){ const el=document.getElementById(views[k]); if(el) el.classList.toggle('on',k===name); } $$('.tabs button').forEach(b=>b.classList.toggle('on',b.dataset.v===name)); if(!keep) window.scrollTo(0,0); try{localStorage.setItem('jp7.tab',name)}catch(e){} }
$$('.tabs button').forEach(b=>b.addEventListener('click',()=>{ closeSearch(); show(b.dataset.v); }));
function goTo(view,id,open){ closeSearch(); show(view,true); const el=document.getElementById(id); if(!el) return; let p=el; while(p){ if(p.tagName==='DETAILS') p.open=true; p=p.parentElement; } if(open&&el.tagName==='DETAILS') el.open=true; setTimeout(()=>{ el.scrollIntoView({block:'start'}); window.scrollBy(0,-8); el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash'); },60); }
$$('[data-target]').forEach(a=>a.addEventListener('click',e=>{ e.preventDefault(); goTo(a.dataset.go||'voyage',a.dataset.target,true); }));
// timeline → day
const dayByDate={}; $$('details.day').forEach(d=>dayByDate[d.dataset.date]=d.id);
const tlMap={'26 déc.':'2026-12-26','27 déc.':'2026-12-27','28 déc.':'2026-12-28','29 déc.':'2026-12-29','30 déc.':'2026-12-30','31 déc.':'2026-12-31','1er janv.':'2027-01-01','2 janv.':'2027-01-02','3 janv.':'2027-01-03','4 janv.':'2027-01-04','5 janv.':'2027-01-05','6 janv.':'2027-01-06','7 janv.':'2027-01-07','8 janv.':'2027-01-08','9 janv.':'2027-01-09','10 janv.':'2027-01-10','11 janv.':'2027-01-11'};
$$('.tl').forEach(a=>a.addEventListener('click',()=>{ const id=dayByDate[tlMap[a.dataset.tl]]; if(id) goTo('voyage',id,true); }));
// aujourd'hui (heure du Japon)
function jstDate(){ const f=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Tokyo',year:'numeric',month:'2-digit',day:'2-digit'}); return f.format(new Date()); }
function tick(){ try{ const t=new Intl.DateTimeFormat('fr-FR',{timeZone:'Asia/Tokyo',hour:'2-digit',minute:'2-digit'}).format(new Date()); $('#jst b').textContent=t; }catch(e){} }
tick(); setInterval(tick,20000);
const todayId=dayByDate[jstDate()]; if(todayId){ document.getElementById(todayId).classList.add('today'); }
$('#todayBtn').addEventListener('click',()=>{ const id=todayId||dayByDate['2026-12-26']; goTo('voyage',id,true); });
// checklist persistence
let st={}; try{ st=JSON.parse(localStorage.getItem('jp7.check')||'{}'); }catch(e){}
const cks=$$('input[data-ck]');
function prog(){ const n=cks.length, d=cks.filter(c=>c.checked).length; $('#pbar').style.width=(100*d/n)+'%'; $('#ptxt').textContent=d+' / '+n+' points faits'; }
cks.forEach(c=>{ c.checked=!!st[c.dataset.ck]; c.addEventListener('change',()=>{ st[c.dataset.ck]=c.checked; try{localStorage.setItem('jp7.check',JSON.stringify(st))}catch(e){} prog(); }); });
prog();
// search
const idx=[]; const norm=s=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
function add(el,kind,title,view){ const txt=(el.innerText||el.textContent).replace(/\n+/g,' · '); idx.push({el,kind,title,view,t:norm(txt),raw:txt}); }
$$('#v-voyage details.day').forEach(d=>add(d,'Journée',d.querySelector('.dow').textContent+' · '+d.querySelector('.ttl').textContent,'voyage'));
$$('#v-voyage details.sub[data-s]').forEach(d=>add(d,'Chapitre',d.dataset.title,'voyage'));
$$('#v-todo .ck').forEach(d=>add(d,'À faire',d.dataset.title,'todo'));
$$('#v-sleep .lodge').forEach(d=>add(d,'Dormir',d.dataset.title,'sleep'));
$$('#v-guide .gc').forEach(d=>add(d,'Adresse · '+d.closest('.garea').querySelector('h2').firstChild.textContent,d.dataset.title,'guide'));
$$('#v-voyage .hotel').forEach(d=>add(d,'Hôtel',d.dataset.title,'voyage'));
// filtres du guide
$$('.fchip').forEach(b=>b.addEventListener('click',()=>{ $$('.fchip').forEach(x=>x.classList.toggle('on',x===b)); const k=b.dataset.k; $$('.gc').forEach(c=>c.classList.toggle('hidden',k!=='all'&&c.dataset.k!==k)); $$('.zone').forEach(z=>{ let vis=false, n=z.nextElementSibling; while(n && !n.classList.contains('zone')){ if(n.classList.contains('gc') && !n.classList.contains('hidden')) vis=true; n=n.nextElementSibling; } z.classList.toggle('hidden',!vis); }); $$('.garea').forEach(a=>a.classList.toggle('hidden',!a.querySelector('.gc:not(.hidden)'))); }));
$$('#v-info details.sub[data-s]').forEach(d=>add(d,d.dataset.s==='mode'?'Mode d\'emploi':'Infos',d.dataset.title,'info'));
let uid=0; idx.forEach(x=>{ if(!x.el.id) x.el.id='s'+(uid++); });
const sbox=$('#search'), sin=$('#q'), res=$('#results');
function openSearch(){ sbox.classList.remove('hidden'); $('.top').classList.add('hidden'); res.classList.remove('hidden'); sin.focus(); render(sin.value); }
function closeSearch(){ sbox.classList.add('hidden'); $('.top').classList.remove('hidden'); res.classList.add('hidden'); }
$('#searchBtn').addEventListener('click',openSearch); $('#closeSearch').addEventListener('click',closeSearch);
function snippet(raw,q){ const i=norm(raw).indexOf(q); if(i<0) return raw.slice(0,140); const a=Math.max(0,i-60), b=Math.min(raw.length,i+q.length+90); let s=raw.slice(a,b).replace(/\s+/g,' '); return (a>0?'… ':'')+s+(b<raw.length?' …':''); }
function hl(s,q){ if(!q) return s; const r=new RegExp('('+q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig'); return s.replace(r,'<mark>$1</mark>'); }
function render(v){ const q=norm(v.trim()); res.innerHTML=''; if(q.length<2){ res.innerHTML='<p class="note" style="padding-top:14px">Tapez un lieu, un hôtel, un train, une date (« Nozomi », « Takayama », « permis », « 31 déc »)…</p>'; return; } const words=q.split(/\s+/); const hits=idx.filter(x=>words.every(w=>x.t.includes(w))).slice(0,60); if(!hits.length){ res.innerHTML='<p class="note" style="padding-top:14px">Rien trouvé.</p>'; return; } hits.forEach(x=>{ const a=document.createElement('a'); a.className='res'; a.href='#'; a.innerHTML='<span class="rk">'+x.kind+'</span><b>'+hl(x.title,words[0])+'</b><small>'+hl(snippet(x.raw,words[0]),words[0])+'</small>'; a.addEventListener('click',e=>{ e.preventDefault(); goTo(x.view,x.el.id,true); }); res.appendChild(a); }); }
sin.addEventListener('input',()=>render(sin.value));
// lightbox
const lb=$('#lb'), lbi=$('#lb img');
$$('img[data-zoom]').forEach(im=>im.addEventListener('click',()=>{ lbi.src=im.src; lb.classList.add('on'); }));
$('#lbClose').addEventListener('click',()=>lb.classList.remove('on'));
// état initial
let tab='voyage'; try{ tab=localStorage.getItem('jp7.tab')||'voyage'; }catch(e){}
show(views[tab]?tab:'voyage',true);
})();
'''

def build():
    css = CSS.replace("FONT_R", font("DMSerifDisplay-Regular.ttf")).replace("FONT_I", font("DMSerifDisplay-Italic.ttf"))
    doc = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="theme-color" content="#131f2d">
<title>Japon en hiver · {'guide Allibert' if MODE == 'allibert' else 'carnet v7'}</title><style>{css}</style></head><body>
<header class="top"><span class="kj">冬</span><div class="brand"><b>Japon en hiver</b><small>26 déc. → 11 janv. 2027 · {'avec Allibert' if MODE == 'allibert' else 'carnet v7'}</small></div><div class="jst" id="jst"><b>--:--</b>heure du Japon</div><button id="searchBtn" aria-label="Rechercher">{ico("search")}</button></header>
<div class="search hidden" id="search"><div class="row"><input id="q" type="search" placeholder="Rechercher dans le carnet…" autocomplete="off"><button id="closeSearch" aria-label="Fermer">{ico("close")}</button></div></div>
<div id="results" class="hidden"></div>
<main>
<section class="view on" id="v-voyage">{home}<nav class="toc">{toc}</nav>{overview}{render_timeline()}{chapters}</section>
<section class="view" id="v-todo">{render_checklist()}</section>
{'<section class="view" id="v-guide">' + render_guide() + '</section>' if MODE == 'allibert' else '<section class="view" id="v-sleep"><div class="pad"><div class="kicker">OÙ DORMIR</div><h1>Les hébergements, étape par étape</h1><p class="intro">Prix Booking du 1er novembre 2026 pour deux adultes aux dates du voyage ; chaque nom ouvre Booking aux bonnes dates. Toutes les adresses ont une salle de bain privée, sauf mention contraire.</p></div>' + lodgings + '</section>'}
<section class="view" id="v-info">{render_info()}</section>
<section class="view" id="v-maps">{render_maps()}</section>
</main>
<nav class="tabs"><button data-v="voyage" class="on">{ico("days")}Voyage</button>{'<button data-v="guide">' + ico("pin") + 'Adresses</button>' if MODE == 'allibert' else '<button data-v="sleep">' + ico("bed") + 'Dormir</button>'}<button data-v="todo">{ico("todo")}À faire</button><button data-v="info">{ico("info")}Infos</button><button data-v="maps">{ico("map")}Cartes</button></nav>
<div id="lb"><button id="lbClose" aria-label="Fermer">{ico("close")}</button><img alt=""><div class="hint">Faites défiler pour explorer la carte</div></div>
<script>{JS}</script></body></html>'''
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print(OUT, os.path.getsize(OUT) // 1024, "ko")

if __name__ == "__main__":
    build()

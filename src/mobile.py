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

MONTHS = {"déc": 12, "dec": 12, "janv": 1, "jan": 1}
def day_matches(dstr, d):
    """True si la chaîne 'day' d'une adresse vise la date d (datetime.date)."""
    if not dstr: return False
    t = dstr.lower().replace("1er", "1")
    parts = re.split(r";| ou bien | sinon ", t)
    for part in parts:
        m = re.search(r"(déc|dec|janv|jan)", part)
        if not m: continue
        month = MONTHS[m.group(1)]
        if month != d.month: continue
        nums = [int(x) for x in re.findall(r"\b(\d{1,2})\b", part[:m.start()])]
        if " au " in part[:m.start()] and len(nums) >= 2:
            a, b = nums[0], nums[1]
            if a <= d.day <= b: return True
        if d.day in nums: return True
    return False


def render_weather(k):
    if MODE != 'allibert': return ""
    pl = E.DAY_PLACE.get(k)
    if not pl: return ""
    links = "".join(f'<a class="pill" href="{u}" target="_blank" rel="noopener">{esc(t)}</a>' for t, u in E.WEATHER_LINKS.get(k, []))
    extra = f'<div class="links">{links}</div>' if links else ""
    if not links and k not in E.MOUNTAIN_DAYS and k in ("2026-12-26", "2027-01-11"): return ""
    return f'<div class="wx" data-lat="{pl[1]}" data-lon="{pl[2]}" data-date="{k}" data-place="{esc(pl[0])}"><div class="lbl">☀ Météo et lumière · {esc(pl[0])}</div><div class="wxsun"></div><div class="wxbody"><small>Prévisions Open-Meteo quand le réseau est là (jusqu\'à 16 jours avant).</small></div>{extra}</div>'

def render_night(k):
    if MODE != 'allibert': return ""
    if k in E.NIGHT_OTHER:
        return f'<div class="night"><div class="lbl">{ico("plane")} La nuit</div><b>{esc(E.NIGHT_OTHER[k])}</b></div>'
    ref = E.HOTEL_BY_DATE.get(k)
    if not ref: return ""
    name, when, addr, mq, site, notes = E.HOTELS[ref[0]][ref[1]]
    car = k in E.CAR_DAYS
    links = f'<a class="pill" href="{maps_url(mq)}" target="_blank" rel="noopener">{ico("pin")} Maps</a>' + dir_links(mq, car)
    if site: links += f'<a class="pill" href="{site}" target="_blank" rel="noopener">{ico("ext")} Site</a>'
    links += share_btn(name, addr, maps_url(mq))
    jp = E.HOTELS_JP.get(name, "")
    jph = f'<div class="jp" data-copy="{esc(jp)}"><span>{esc(jp)}</span><small>à montrer au chauffeur · toucher pour copier</small></div>' if jp else ""
    return f'''<div class="night" data-s="hotel" data-title="{esc(name)}"><div class="lbl">{ico("bed")} La nuit · {esc(when)}</div><b>{esc(name)}</b><div class="addr">{esc(addr)}</div>{jph}<details class="more"><summary>Accès, bains, horaires</summary><p>{notes}</p></details><div class="links">{links}</div></div>'''

def render_day_addresses(d_date):
    if not G or MODE != 'allibert': return ""
    items = [g for g in G.GUIDE if day_matches(g.get("day", ""), d_date)]
    if not items: return ""
    items.sort(key=lambda x: list(KINDS).index(x["kind"]) if x["kind"] in KINDS else 9)
    rows = "".join(f'<a class="dad" href="#adresses" data-go="guide" data-target="g-{slug(g["name"])}"><span class="dk">{KINDS.get(g["kind"], (g["kind"], ""))[1]}</span><span class="dn"><b>{esc(g["name"])}</b><small>{esc(KINDS.get(g["kind"], (g["kind"], ""))[0])}{(" · " + esc(g["zone"])) if g.get("zone") else ""}</small></span>{ico("chev","chev")}</a>' for g in items)
    return f'<div class="dayaddr"><div class="lbl">{ico("pin")} Adresses du jour</div>{rows}</div>'

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
<div class="dbody">{photos}{secs}{side}{traj}{coince}{opts}{render_weather(k)}{render_night(k)}{render_day_addresses(date.fromisoformat(k))}</div></details>'''

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


def dir_links(q, car=False):
    mode = "driving" if car else "transit"
    g = "https://www.google.com/maps/dir/?api=1&destination=" + q.replace(" ", "+") + "&travelmode=" + mode
    a = "https://maps.apple.com/?daddr=" + q.replace(" ", "+") + ("&dirflg=d" if car else "&dirflg=r")
    return f'<a class="pill" href="{g}" target="_blank" rel="noopener">{ico("walk")} Itinéraire</a><a class="pill alt" href="{a}" target="_blank" rel="noopener">Plans</a>'
def share_btn(title, text, url):
    return f'<button class="pill ghost" data-share-title="{esc(title)}" data-share-text="{esc(text)}" data-share-url="{url}">{ico("ext")} Partager</button>'
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
            links = f'<a class="pill" href="{maps_url(g["maps"])}" target="_blank" rel="noopener">{ico("pin")} Maps</a>' + dir_links(g["maps"], area in ("Kumano", "Kii-Katsuura", "Kōya-san", "Route de la côte"))
            if g.get("website"): links += f'<a class="pill" href="{g["website"]}" target="_blank" rel="noopener">{ico("ext")} Site</a>'
            links += share_btn(g["name"], g.get("address", ""), maps_url(g["maps"]))
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
<div class="hero{"" if ch.get("banner") else " nophoto"}">{banner}<div class="shade"></div><div class="kj">{ch["kanji"]}</div><div class="htx"><div class="reg">{esc(ch["num"])} · {esc(ch["region"])}</div><h2>{esc(ch["title"])}</h2><div class="sub">{esc(ch["subtitle"])}</div></div></div>
<div class="chbody">
<p class="intro">{ch["intro"]}</p>
<div class="stats">{stats}</div>
<details class="sub" data-s="hist" data-title="{esc(ch["title"])} : un peu d'histoire"><summary>{ico("info")} Un peu d'histoire</summary><p>{ch["history"]}</p></details>
{locals_html}
{mp}{strips}
<div class="days">{days}</div>
{'' if MODE == 'allibert' else f'<a class="btn ghost" href="#sleep/{key}" data-go="sleep" data-target="lg-{key}">{ico("bed")} Où dormir : {esc(ch["lodging"]["title"])}</a>'}
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
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)} {ico("ext")}</a></li>' for t, u in C.SOURCES)
    return f'''<div class="pad">
<div class="kicker">AVANT DE PARTIR</div><h1>Le voyage avec Allibert</h1><p class="intro">{E.INTRO}</p>
<details class="sub" data-s="info" data-title="Ce qui est compris"><summary>Ce qui est compris</summary><ul>{inc}</ul></details>
<details class="sub" data-s="info" data-title="Ce qui reste à notre charge"><summary>Ce qui reste à notre charge</summary><ul>{exc}</ul></details>
<div class="warnbox"><b>POINTS OUVERTS</b><p>{E.INCLUDED["todo"]}</p></div>
{before}
<div class="kicker">SUR PLACE</div><h1>{esc(C.PRACTICAL["title"])}</h1>{prac}
<div class="kicker">{esc(D.MODE_EMPLOI["kicker"])}</div><h1>{esc(D.MODE_EMPLOI["title"])}</h1><p class="intro">{D.MODE_EMPLOI["intro"]}</p>{mode}
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


def render_tools():
    fields = "".join(f'<label class="pf"><span>{esc(l)}</span><textarea data-paper="{k}" rows="1" placeholder="…">{esc(v)}</textarea></label>' for k, l, v in E.PAPERS_FIELDS)
    phrases = "".join(f'<button class="ph" data-jp="{esc(j)}" data-fr="{esc(f)}" data-ro="{esc(r)}"><b>{esc(f)}</b><span class="pj">{esc(j)}</span><small>{esc(r)}</small></button>' for f, j, r in E.PHRASES)
    numbers = "".join(f'<li><b>{esc(a)}</b><span>{esc(b)}</span></li>' for a, b in E.NUMBERS)
    pack = "".join(f'<div class="ck mini"><input type="checkbox" id="pk{i}" data-ck="pack{i}"><label for="pk{i}" class="box"></label><label for="pk{i}" class="ckt">{esc(x)}</label></div>' for i, x in enumerate(E.PACK))
    morning = "".join(f'<div class="ck mini"><input type="checkbox" id="mo{i}" data-morning="m{i}"><label for="mo{i}" class="box"></label><label for="mo{i}" class="ckt">{esc(x)}</label></div>' for i, x in enumerate(E.MORNING))
    days = []
    for ch in CHAPTERS:
        for d in ch["days"]:
            k = dkey(d); days.append((k, d["dow"].capitalize(), d["title"]))
    journal = "".join(f'<details class="sub jd" data-day="{k}"><summary>{esc(dow)}<small class="jsum"></small></summary><textarea data-journal="{k}" rows="4" placeholder="Quelques lignes sur la journée…"></textarea><div class="jrow"><label>Dépenses du jour <input type="number" inputmode="numeric" data-spend="{k}" placeholder="yens"> yens <span class="jeur"></span></label><label class="jphoto">{ico("ext")} Photo <input type="file" accept="image/*" data-photo="{k}" hidden></label></div><div class="jpics" data-pics="{k}"></div></details>' for k, dow, t in days)
    konbini = "".join(f'<a class="pill" href="https://www.google.com/maps/search/?api=1&query=7-Eleven+ATM+near+{esc(mq).replace(" ", "+")}" target="_blank" rel="noopener">{esc(when.split(",")[1].strip() if "," in when else when)} · {esc(name.split(" (")[0])}</a>' for key in ("tokyo","alpes","kumano","koya","kyoto","retour") for name, when, addr, mq, site, notes in E.HOTELS[key])
    return f'''<div class="pad">
<div class="kicker">OUTILS</div><h1>La boîte à outils</h1>
<details class="sub tool" id="t-papers" open><summary>{ico("todo")} Papiers et références</summary><p class="note">Tout reste sur ce téléphone (stockage local du navigateur), rien n'est envoyé. Un code à 4 chiffres peut masquer cette section : réglage en bas.</p><div class="pfields">{fields}</div>
<div class="lbl">Documents (PDF, photos de passeports, vouchers)</div><div class="files" id="fileList"></div><label class="btn ghost small">{ico("ext")} Ajouter un document <input type="file" id="fileAdd" multiple accept="application/pdf,image/*" hidden></label><p class="note">Les fichiers sont gardés dans la base locale du navigateur (IndexedDB) et s'ouvrent hors ligne. Garder aussi les originaux dans Fichiers ou Mail.</p></details>
<details class="sub tool"><summary>¥ Convertisseur</summary><div class="conv"><label>Yens <input type="number" inputmode="numeric" id="cvY" placeholder="1 000"></label><label>Euros <input type="number" inputmode="decimal" id="cvE" placeholder="5,7"></label></div><label class="rate">Taux : 1 € = <input type="number" inputmode="decimal" id="cvRate" value="175"> yens <small>(à régler à l'arrivée, il est mémorisé)</small></label>
<div class="quick" id="cvQuick"></div></details>
<details class="sub tool"><summary>話 Phrases à montrer</summary><p class="note">Toucher une phrase pour l'afficher en grand, à montrer.</p><div class="phrases">{phrases}</div></details>
<details class="sub tool"><summary>☎ Numéros utiles</summary><ul class="nums">{numbers}</ul></details>
<details class="sub tool"><summary>🏪 Konbini et distributeurs 7-Eleven, par étape</summary><p class="note">Les distributeurs 7-Eleven acceptent les cartes européennes ; recherche Google Maps autour de chaque hôtel.</p><div class="links wrap">{konbini}</div></details>
<details class="sub tool"><summary>☑ Valise, avant de partir</summary>{pack}</details>
<details class="sub tool"><summary>☀ Chaque matin <small id="moDate"></small></summary><p class="note">La liste se remet à zéro chaque jour.</p>{morning}</details>
<details class="sub tool" id="t-journal"><summary>✎ Carnet de route</summary><p class="note">Quelques lignes, une photo, la dépense du jour. Tout reste sur le téléphone ; exporter en fin de voyage.</p><div class="jtotal" id="jTotal"></div>{journal}<div class="links"><button class="pill" id="expJson">Exporter JSON</button><button class="pill" id="expTxt">Exporter texte</button></div></details>
<details class="sub tool"><summary>⚙ Réglages</summary><label class="sw"><input type="checkbox" id="bigText"> Grand texte (pour Claudie)</label><label class="sw">Code Papiers (4 chiffres, vide = aucun) <input type="password" inputmode="numeric" maxlength="4" id="pinSet" placeholder="····"></label><p class="note">Le code masque seulement l'affichage ; ce n'est pas un chiffrement.</p></details>
</div>'''

def render_now():
    return '''<section class="now" id="now"><div class="nowh"><span class="lbl">Maintenant · heure du Japon</span><b id="nowClock">--:--</b></div><div id="nowBody" class="nowbody"><p class="note">Le voyage commence le 26 décembre 2026.</p></div></section>'''

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
@font-face{font-family:"Inter";font-style:normal;font-weight:400;font-display:swap;src:url(INTER400) format("woff2")}
@font-face{font-family:"Inter";font-style:normal;font-weight:500;font-display:swap;src:url(INTER500) format("woff2")}
@font-face{font-family:"Inter";font-style:normal;font-weight:600;font-display:swap;src:url(INTER600) format("woff2")}
/* preflight (base Tailwind, condensé) */
*,::before,::after{box-sizing:border-box;border-width:0;border-style:solid;border-color:#e7e5e4}
html{line-height:1.5;-webkit-text-size-adjust:100%;tab-size:4;font-feature-settings:normal;font-variation-settings:normal;-webkit-tap-highlight-color:transparent}
body{margin:0;line-height:inherit}
hr{height:0;color:inherit;border-top-width:1px}
h1,h2,h3,h4,h5,h6{font-size:inherit;font-weight:inherit}
a{color:inherit;text-decoration:inherit}
b,strong{font-weight:bolder}
small{font-size:80%}
sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline} sup{top:-.5em}
table{text-indent:0;border-color:inherit;border-collapse:collapse}
button,input,optgroup,select,textarea{font-family:inherit;font-feature-settings:inherit;font-variation-settings:inherit;font-size:100%;font-weight:inherit;line-height:inherit;letter-spacing:inherit;color:inherit;margin:0;padding:0}
button,select{text-transform:none}
button,input:where([type=button]),input:where([type=reset]),input:where([type=submit]){-webkit-appearance:button;background-color:transparent;background-image:none}
:-moz-focusring{outline:auto} progress{vertical-align:baseline}
::-webkit-inner-spin-button,::-webkit-outer-spin-button{height:auto}
[type=search]{-webkit-appearance:textfield;outline-offset:-2px} ::-webkit-search-decoration{-webkit-appearance:none}
summary{display:list-item}
blockquote,dl,dd,h1,h2,h3,h4,h5,h6,hr,figure,p,pre{margin:0}
fieldset{margin:0;padding:0} legend{padding:0} ol,ul,menu{list-style:none;margin:0;padding:0}
textarea{resize:vertical} input::placeholder,textarea::placeholder{opacity:1;color:#a8a29e}
button,[role=button]{cursor:pointer} :disabled{cursor:default}
img,svg,video,canvas,audio,iframe,embed,object{display:block;vertical-align:middle} img,video{max-width:100%;height:auto}
[hidden]{display:none}
:root{--tint:#fbeeeb;--paper:#fafaf9;--paper2:#f5f5f4;--card:#ffffff;--ink:#1c1917;--ink2:#44403c;--mute:#78716c;--rule:#e7e5e4;--rule2:#d6d3d1;--shu:#b91c1c;--ai:#334155;--moss:#3f6212;--kin:#a16207;--theme:var(--ai);
 --ui:"Inter",-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Roboto,"Hiragino Sans","Noto Sans JP",Arial,sans-serif;--jp:"Hiragino Mincho ProN","Yu Mincho","Noto Serif JP",serif}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html{-webkit-text-size-adjust:100%;color-scheme:light}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--ui);font-size:15px;line-height:1.6;padding-bottom:calc(72px + env(safe-area-inset-bottom));font-feature-settings:"kern","liga";-webkit-font-smoothing:antialiased}
a{color:var(--shu);text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:2px} b{font-weight:600} .i{display:inline-block}
h1{font-weight:600;font-size:24px;line-height:1.2;letter-spacing:-.02em;margin:4px 0 12px}
h2{font-weight:600;font-size:18px;line-height:1.3;letter-spacing:-.01em;margin:0 0 8px}
.kicker{font-size:11px;font-weight:600;letter-spacing:.14em;color:var(--shu);text-transform:uppercase;margin-top:32px;display:flex;align-items:center;gap:10px} .kicker::after{content:"";flex:1;height:1px;background:var(--rule)}
.lbl{font-size:10.5px;font-weight:600;letter-spacing:.16em;color:var(--shu);text-transform:uppercase;margin:12px 0 4px}
.pad{padding:0 16px}
p{margin:0 0 10px} ul{list-style:disc;padding-left:18px} .rich ul,.box ul{list-style:disc} .intro{font-size:16px;line-height:1.55;color:var(--ink)}
.note{font-size:12.5px;color:var(--mute);line-height:1.5} .rich p{margin:0 0 8px} .rich ul{padding-left:18px}
.i{width:18px;height:18px;fill:currentColor;vertical-align:-4px;flex:none}
.t-red{--theme:var(--shu);--tint:#fbeeeb} .t-navy{--theme:var(--ai);--tint:#eef2f7}
.hidden{display:none!important}
/* en-tête */
.top{position:sticky;top:0;z-index:20;background:rgba(251,250,246,.94);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border-bottom:1px solid var(--rule);display:flex;align-items:center;gap:10px;padding:calc(8px + env(safe-area-inset-top)) 12px 8px 14px}
.top .kj{font-family:var(--jp);font-size:17px;color:#fff;background:var(--shu);width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:none;line-height:1}
.top .brand{flex:1;line-height:1.15} .top .brand b{font-weight:600;font-size:16px;display:block;letter-spacing:.01em} .top .brand small{font-size:11px;color:var(--mute)}
.top .jst{font-size:10.5px;color:var(--mute);text-align:right;line-height:1.2} .top .jst b{display:block;font-size:14px;color:var(--ink);font-variant-numeric:tabular-nums;font-weight:500}
.top button{background:none;border:0;color:var(--ink);padding:6px}
.search{position:sticky;top:0;z-index:21;background:var(--paper);border-bottom:1px solid var(--rule);padding:calc(8px + env(safe-area-inset-top)) 12px 10px}
.search .row{display:flex;gap:8px;align-items:center}
.search input{flex:1;font:15px var(--ui);padding:10px 14px;border-radius:8px;border:1px solid var(--rule2);background:#fff;color:var(--ink)} .search input:focus{outline:none;border-color:var(--ai)}
.search button{background:none;border:0;color:var(--ink);padding:6px}
#results{position:fixed;inset:0;top:64px;z-index:19;background:var(--paper);overflow:auto;padding:8px 16px 90px}
.res{display:block;padding:12px 0;border-bottom:1px solid var(--rule);color:var(--ink);text-decoration:none}
.res .rk{font-size:10px;letter-spacing:.14em;color:var(--shu);font-weight:600;text-transform:uppercase}
.res b{display:block;font-weight:600;font-size:15.5px;margin:2px 0}
.res small{display:block;color:var(--ink2);font-size:13px;line-height:1.45} mark{background:#f3e6b4;color:#111;border-radius:2px;padding:0 1px}
/* onglets latéraux, façon index de carnet */
.tabs{position:fixed;left:0;right:0;bottom:0;z-index:20;display:flex;background:rgba(255,255,255,.96);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border-top:1px solid var(--rule);padding-bottom:env(safe-area-inset-bottom)}
.tabs button{flex:1;background:none;border:0;color:var(--mute);font-family:var(--ui);padding:8px 0 7px;display:flex;flex-direction:column;align-items:center;gap:3px}
.tabs button .tk{font-family:var(--jp);font-size:19px;line-height:1.1;color:currentColor} .tabs button .tlab{font-size:10px;letter-spacing:.04em;font-weight:500}
.tabs button.on{color:var(--shu)}
main>section.view{display:none} main>section.view.on{display:block}
/* couverture */
.cover{position:relative;background:#fff;border-bottom:1px solid var(--rule);padding:32px 20px 26px;overflow:hidden}
.cover .ckj{position:absolute;right:-4px;top:-18px;font-family:var(--jp);font-size:150px;color:var(--paper2);line-height:1;z-index:0}
.cover>*{position:relative;z-index:1}
.cover .ck1{font-size:10px;letter-spacing:.18em;font-weight:600;color:var(--shu);text-transform:uppercase}
.cover .ct{font-size:46px;font-weight:600;letter-spacing:-.03em;margin:10px 0 2px;line-height:1} .cover .ct i{display:block;font-style:normal;font-family:var(--jp);font-size:26px;color:var(--ai);font-weight:400;margin-top:2px}
.cover .cd{font-size:13px;color:var(--ink2);margin-top:8px} .cover p{font-size:14px;color:var(--ink2);margin-top:6px}
.cover .stops{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 16px} .cover .stops span{font-size:11px;border:1px solid var(--rule2);padding:3px 9px;border-radius:999px;color:var(--ink2);background:#fff}
.btn{display:inline-flex;align-items:center;gap:8px;font:500 14px var(--ui);background:var(--shu);color:#fff;border:0;border-radius:8px;padding:10px 16px;text-decoration:none}
.btn.ghost{background:#fff;color:var(--shu);border:1px solid var(--shu);margin:12px 0 6px;width:100%;justify-content:center}
/* sommaire */
.toc{padding:14px 16px 4px}
.tocl{display:flex;align-items:center;gap:12px;background:#fff;border:1px solid var(--rule);border-radius:0 8px 8px 0;padding:12px;margin-bottom:8px;text-decoration:none;color:var(--ink);border-left:3px solid var(--theme)}
.tocl .kj{font-family:var(--jp);font-size:19px;color:var(--theme);width:44px;flex:none;line-height:1.1} .tocl b{font-weight:600;font-size:15.5px;display:block;line-height:1.2}
.tocl small{display:block;color:var(--mute);font-size:12.5px} .tocl>div{flex:1} .tocl .chev{color:var(--rule2);margin-left:auto}
/* frise */
.tls{margin-top:8px} .tl{display:flex;gap:10px;padding:10px;border:1px solid var(--rule);border-radius:8px;background:#fff;margin-bottom:6px;color:var(--ink);text-decoration:none;align-items:flex-start}
.tl.car{background:#fdf6ee;border-color:#f0dcc4} .tld{font-size:11.5px;font-weight:600;color:var(--shu);width:58px;flex:none;padding-top:2px;letter-spacing:.02em} .tlb{flex:1} .tlb b{font-weight:600;font-size:15px;line-height:1.2;display:block}
.tln{font-size:11px;color:var(--mute);text-align:right;flex:none;max-width:84px;display:flex;flex-direction:column;align-items:flex-end;gap:2px}
.chips{display:flex;flex-wrap:wrap;gap:4px 10px;margin-top:4px} .chip{font-size:11px;color:var(--ink2);display:inline-flex;align-items:center;gap:3px} .chip .i{width:14px;height:14px}
.chip.r{color:var(--shu)} .chip.w{color:var(--moss)}
/* chapitres */
.chapter{margin-top:28px;border-bottom:2px solid var(--theme)}
.hero{position:relative;background:var(--paper2);overflow:hidden}
.hero img{width:100%;height:210px;object-fit:cover;display:block} .hero .shade{display:none}
.hero .kj{position:absolute;right:12px;top:12px;font-family:var(--jp);font-size:22px;color:#fff;background:var(--shu);border-radius:50%;width:44px;height:44px;display:flex;align-items:center;justify-content:center;line-height:1}
.hero.nophoto{padding-top:70px} .hero.nophoto .kj{width:auto;height:auto;background:none;color:var(--theme);font-size:110px;right:10px;top:-14px;opacity:.14}
.hero .htx{position:relative;background:#fff;padding:12px 16px 12px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.hero .reg{font-size:10px;letter-spacing:.16em;color:var(--shu);font-weight:600;text-transform:uppercase} .hero h2{font-size:22px;font-weight:500;margin:2px 0 1px} .hero .sub{font-size:12.5px;color:var(--ink2)}
.chbody{padding:16px 16px 20px}
.stats{display:flex;gap:8px;margin:6px 0 12px} .stats div{flex:1;background:#fff;border:1px solid var(--rule);border-radius:8px;padding:8px 10px;border-top:2px solid var(--theme)} .stats b{font-weight:500;font-size:20px;display:block;line-height:1.1;color:var(--theme)} .stats small{font-size:11px;color:var(--mute)}
details.sub{background:#fff;border:1px solid var(--rule);border-radius:12px;margin:8px 0;padding:0 14px;box-shadow:0 1px 2px rgba(0,0,0,.03)}
details.sub>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:8px;padding:11px 0;font-weight:600;font-size:14px;color:var(--ink)}
details.sub>summary::-webkit-details-marker{display:none} details.sub>summary::after{content:"";margin-left:auto;width:7px;height:7px;border-right:1.5px solid var(--mute);border-bottom:1.5px solid var(--mute);transform:rotate(45deg);transition:transform .2s;flex:none}
details.sub[open]>summary::after{transform:rotate(-135deg)} details.sub>*:not(summary){margin-bottom:10px} details.sub>p:last-child,details.sub>div:last-child{padding-bottom:12px;margin-bottom:0}
details.sub.warn>summary{color:var(--shu)} details.sub.loc .lbl:first-of-type{margin-top:0}
.mapfig{margin:12px 0;background:#fff;border:1px solid var(--rule);border-radius:8px;padding:6px} .mapfig img{width:100%;display:block;border-radius:4px;cursor:zoom-in} .mapfig figcaption{font-size:12.5px;color:var(--mute);line-height:1.45;padding:6px 4px 2px}
/* frises de trajet */
.strip{background:#fff;border:1px solid var(--rule);border-radius:8px;padding:10px 12px;margin:10px 0} .sline{border-left:1px solid var(--rule2);margin-left:6px;padding-left:14px}
.snode{position:relative;font-size:14px;padding:2px 0} .snode .dot{position:absolute;left:-19px;top:9px;width:8px;height:8px;border-radius:50%;background:var(--shu);border:2px solid #fff} .snode small{color:var(--mute);margin-left:6px}
.sseg{font-size:12.5px;color:var(--mute);padding:4px 0 6px} .sseg.s-c{color:var(--shu)} .sseg.s-t,.sseg.s-b{color:var(--ai)}
/* journées */
.days{margin-top:14px}
details.day{background:#fff;border:1px solid var(--rule);border-radius:12px;margin:12px 0;box-shadow:0 1px 2px rgba(0,0,0,.03)}
details.day.today{box-shadow:0 0 0 2px var(--kin)}
details.day>summary{list-style:none;display:flex;gap:12px;padding:12px 12px 12px 10px;cursor:pointer;align-items:flex-start;background:var(--tint);border-radius:12px} details.day[open]>summary{border-radius:12px 12px 0 0;border-bottom:1px solid var(--rule)} details.day>summary::-webkit-details-marker{display:none}
.dnum{font-weight:600;font-size:30px;line-height:1;color:var(--shu);width:44px;flex:none;text-align:center;padding-top:5px;letter-spacing:-.04em} .dnum sup{font-size:13px;font-weight:500}
.dtt{flex:1} .dow{font-size:10px;font-weight:600;letter-spacing:.14em;color:var(--shu);text-transform:uppercase} .dtt .ttl{font-weight:600;font-size:17px;line-height:1.25;letter-spacing:-.01em;margin:3px 0 5px} .st{color:var(--kin);margin-left:6px;font-size:13px}
.heads{display:flex;flex-wrap:wrap;gap:3px 10px} .hd{font-size:11.5px;color:var(--mute)} .hd b{color:var(--ink2);font-weight:600}
details.day>summary .chev{color:var(--rule2);margin-top:6px;transition:transform .2s} details.day[open]>summary .chev{transform:rotate(90deg)}
.dbody{padding:0 12px 12px}
.photos{display:flex;gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -12px 10px;padding:0 12px;-webkit-overflow-scrolling:touch}
.photos figure{flex:0 0 78%;margin:0;scroll-snap-align:start} .photos img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:6px;display:block} .photos figcaption{font-size:11px;color:var(--mute);padding:4px 2px}
.sec{margin-bottom:6px} .sec .lbl{margin-top:8px} .sec p{font-size:15px;line-height:1.65}
.box{background:var(--paper2);border-radius:8px;padding:8px 12px;margin:10px 0} .box .lbl{margin-top:0} .box ul{margin:0;padding-left:18px} .box li{margin-bottom:4px;font-size:14px} .box p{margin:0;font-size:14px}
.box.rep p{color:var(--ink2)}
.traj{padding-bottom:8px} .tr{display:flex;gap:10px;padding:7px 0;border-top:1px solid var(--rule)} .tt{font-size:12px;font-weight:600;color:var(--shu);width:60px;flex:none;padding-top:2px;line-height:1.3;font-variant-numeric:tabular-nums} .tb{flex:1;font-size:14px} .tb b{display:block;line-height:1.3} .tb small{display:block;color:var(--ink2);font-size:12.5px;line-height:1.4}
.tm{font-size:11.5px;color:var(--mute);margin-top:2px;display:flex;gap:8px;align-items:center}
.resa{font-size:9.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;padding:1px 6px;border-radius:999px;border:1px solid} .resa.o{color:var(--shu);border-color:var(--shu)} .resa.c{color:var(--kin);border-color:var(--kin)} .resa.l{color:var(--mute);border-color:var(--rule2)}
/* checklist */
.progress{margin:6px 0 14px;font-size:12px;color:var(--mute)} .bar{height:4px;background:var(--rule);border-radius:2px;overflow:hidden;margin-bottom:4px} #pbar{height:100%;background:var(--shu);width:0;transition:width .3s}
.warnbox{background:#fdf6ee;border:1px solid #f0dcc4;border-radius:8px;padding:8px 12px;margin:8px 0;font-size:14px} .warnbox b{font-size:10.5px;letter-spacing:.12em;color:var(--shu);text-transform:uppercase} .warnbox p{margin:2px 0 0}
.prio{padding:8px 16px 4px} .prio h2{display:flex;align-items:baseline;gap:10px;margin:18px 0 8px;padding-bottom:6px;border-bottom:1px solid var(--rule2)} .prio h2 .pn{font-weight:300;font-size:30px;color:var(--shu)} .prio h2 small{font-size:12px;color:var(--mute);margin-left:auto;text-align:right}
.ck{display:flex;gap:12px;background:#fff;border:1px solid var(--rule);border-radius:8px;padding:12px;margin-bottom:8px} .ck input{display:none}
.ck label.box{width:22px;height:22px;flex:none;border:1.5px solid var(--rule2);border-radius:6px;margin:4px 0 0;position:relative;cursor:pointer;padding:0;background:#fff}
.ck input:checked+label.box{background:var(--shu);border-color:var(--shu)} .ck input:checked+label.box::after{content:"";position:absolute;left:7px;top:2px;width:5px;height:11px;border:solid #fff;border-width:0 2px 2px 0;transform:rotate(45deg)}
.ck input:checked~.ckb{opacity:.45} .ck input:checked~.ckb .ckt{text-decoration:line-through}
.ckb{flex:1;min-width:0} .ckh{display:flex;gap:8px;align-items:center;font-size:11px;font-weight:600} .when{color:var(--mute);letter-spacing:.04em} .lvl{letter-spacing:.1em;text-transform:uppercase;font-size:9px;padding:1px 6px;border-radius:999px;color:#fff;background:var(--mute)} .lvl.b{background:var(--shu)} .lvl.i{background:var(--kin)}
.ckt{display:block;font-weight:600;font-size:15.5px;line-height:1.25;margin:4px 0;cursor:pointer} .ckd{font-size:13.5px;line-height:1.5;color:var(--ink2)} .ckd a{word-break:break-word}
/* hôtels, adresses */
.hotel{background:#fff;border:1px solid var(--rule);border-radius:0 8px 8px 0;padding:10px 12px;margin:14px 0 6px;border-left:3px solid var(--kin)} .hotel .lbl{margin-top:0;display:flex;align-items:center;gap:6px} .hotel b{font-weight:600;font-size:16px;display:block;line-height:1.2} .hotel .addr,.gc .addr{font-size:12px;color:var(--mute);margin:2px 0 4px} .hotel p{font-size:13.5px;line-height:1.5;margin:4px 0 6px;color:var(--ink2)}
.links{display:flex;gap:8px;flex-wrap:wrap;margin-top:4px} .pill{display:inline-flex;align-items:center;gap:4px;font:500 12px var(--ui);color:var(--ai);border:1px solid var(--ai);border-radius:999px;padding:4px 10px;text-decoration:none;background:#fff} .pill .i{width:13px;height:13px}
.filters{display:flex;gap:6px;overflow-x:auto;padding:4px 0 10px;margin:0 -16px;padding-left:16px;padding-right:16px;-webkit-overflow-scrolling:touch} .fchip{flex:none;font:500 12.5px var(--ui);background:#fff;color:var(--ink);border:1px solid var(--rule2);border-radius:999px;padding:7px 12px} .fchip.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.garea{padding:6px 16px 10px} .garea h2{display:flex;align-items:baseline;gap:10px;margin:16px 0 8px;padding-bottom:6px;border-bottom:1px solid var(--rule2)} .garea h2 small{font-size:12px;color:var(--mute);margin-left:auto}
.gc{background:#fff;border:1px solid var(--rule);border-radius:0 8px 8px 0;padding:10px 12px;margin-bottom:8px;border-left:3px solid var(--rule2)} .gc.k-manger{border-left-color:var(--shu)} .gc.k-cafe{border-left-color:#8a6d3b} .gc.k-bain{border-left-color:#3b7ea1} .gc.k-photo{border-left-color:var(--ink)} .gc.k-voir{border-left-color:var(--kin)} .gc.k-boutique{border-left-color:#6b5b95} .gc.k-course{border-left-color:var(--moss)} .gc.k-papeterie{border-left-color:#8a5a2b}
.gc .gk{font-size:10px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--mute)} .gc b{font-weight:600;font-size:15.5px;display:block;line-height:1.25;margin:2px 0} .gc p{font-size:13.5px;line-height:1.5;margin:2px 0 4px;color:var(--ink2)} .gc .meta{font-size:12px;color:var(--mute);line-height:1.45;margin-bottom:4px}
.runs{margin:10px 0 4px} .runl{display:flex;align-items:center;gap:8px;background:#fff;border:1px solid var(--rule);border-radius:0 8px 8px 0;padding:9px 12px;margin-bottom:6px;color:var(--ink);text-decoration:none;font:500 14px var(--ui);border-left:3px solid var(--moss)} .runl small{color:var(--mute);font-weight:400;margin-left:auto;font-size:11.5px} .runl .chev{color:var(--rule2)}
.night{background:#fff;border:1px solid var(--rule);border-radius:0 12px 12px 0;padding:10px 14px;margin:14px 0 6px;border-left:3px solid var(--kin)} .night .lbl{margin-top:0;display:flex;align-items:center;gap:6px;color:var(--kin)} .night b{font-weight:600;font-size:15.5px;display:block;line-height:1.25} .night .addr{font-size:12px;color:var(--mute);margin:2px 0 6px} .night details.more{margin:4px 0 8px} .night details.more summary{list-style:none;cursor:pointer;font-size:12.5px;color:var(--ai);font-weight:500} .night details.more summary::-webkit-details-marker{display:none} .night details.more p{font-size:13.5px;color:var(--ink2);line-height:1.55;margin:6px 0 0}
.dayaddr{margin:12px 0 2px} .dayaddr .lbl{display:flex;align-items:center;gap:6px} .dad{display:flex;align-items:center;gap:10px;padding:8px 0;border-top:1px solid var(--rule);color:var(--ink);text-decoration:none} .dad:first-of-type{border-top:0} .dad .dk{font-size:16px;width:24px;text-align:center;flex:none} .dad .dn{flex:1;min-width:0} .dad .dn b{display:block;font-weight:500;font-size:14px;line-height:1.3} .dad .dn small{display:block;color:var(--mute);font-size:11.5px} .dad .chev{color:var(--rule2)}
.zone{font-size:10.5px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin:14px 0 6px}
/* infos */
.tbl{width:100%;border-collapse:collapse;font-size:13px;margin:6px 0 4px;background:#fff;border:1px solid var(--rule);border-radius:8px;overflow:hidden} .tbl th{font-size:10px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;text-align:left;padding:8px;background:var(--paper2);color:var(--ink2);border-bottom:1px solid var(--rule2)} .tbl td{padding:7px 8px;border-top:1px solid var(--rule);vertical-align:top} .tbl td:nth-child(n+2){white-space:nowrap;text-align:right} .tbl.cmp td:nth-child(n+2){white-space:normal;text-align:left;width:25%}
.tbl tr.tot td{font-weight:600;background:var(--paper2)}
.src{padding-left:0;list-style:none} .src li{padding:6px 0;border-bottom:1px solid var(--rule);font-size:13.5px}
.mh{margin-top:22px;display:flex;align-items:center;gap:8px} .mh .kj{font-family:var(--jp);font-size:18px;color:var(--theme)}
/* plein écran carte */
#lb{position:fixed;inset:0;z-index:50;background:#fff;display:none;overflow:auto;-webkit-overflow-scrolling:touch} #lb.on{display:block} #lb img{display:block;min-width:100%;width:200%;max-width:none;margin:auto} #lb button{position:fixed;top:calc(10px + env(safe-area-inset-top));right:10px;background:#fff;border:1px solid var(--rule2);color:var(--ink);border-radius:50%;width:40px;height:40px;z-index:51} #lb .hint{position:fixed;bottom:16px;left:0;right:0;text-align:center;color:var(--mute);font-size:12px}
.flash{animation:flash 1.6s ease-out} @keyframes flash{0%{box-shadow:0 0 0 3px var(--kin)}100%{box-shadow:0 0 0 0 transparent}}
.day .photos img{content-visibility:auto}

/* outils, maintenant, extras */
.pill.alt{color:var(--ink2);border-color:var(--rule2)} .pill.ghost{background:none;border-style:dashed;color:var(--mute)} button.pill{font-family:var(--ui);cursor:pointer}
.jp{background:var(--paper2);border-radius:8px;padding:8px 10px;margin:6px 0;cursor:pointer} .jp span{display:block;font-family:var(--jp);font-size:16px;line-height:1.5} .jp small{display:block;color:var(--mute);font-size:11px;margin-top:2px}
.wx{background:#fff;border:1px solid var(--rule);border-radius:0 12px 12px 0;padding:10px 14px;margin:14px 0 6px;border-left:3px solid #0369a1} .wx .lbl{margin-top:0;color:#0369a1} .wxsun{font-size:13px;color:var(--ink2);margin:2px 0 4px} .wxbody{font-size:13.5px;line-height:1.5} .wxbody small{color:var(--mute);font-size:12px} .wxrow{display:flex;gap:10px;flex-wrap:wrap;align-items:baseline} .wxrow b{font-size:22px;font-weight:600} .wx .links{margin-top:8px}
.now{margin:14px 16px 0;background:#fff;border:1px solid var(--rule);border-radius:14px;padding:12px 14px;box-shadow:0 1px 2px rgba(0,0,0,.03)} .nowh{display:flex;align-items:baseline;justify-content:space-between} .nowh .lbl{margin:0} .nowh b{font-size:26px;font-weight:600;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.nowbody{margin-top:6px} .nowstep{display:flex;gap:10px;padding:8px 0;border-top:1px solid var(--rule)} .nowstep .tt{font-size:12px;font-weight:600;color:var(--shu);width:56px;flex:none;padding-top:2px} .nowstep .tb{flex:1;font-size:14px} .nowstep .tb b{display:block;line-height:1.3} .nowstep .tb small{color:var(--ink2);display:block;font-size:12.5px} .nowstep.next{background:#fff7ed;margin:0 -14px;padding:8px 14px;border-top:0}
.nowline{font-size:13.5px;color:var(--ink2);margin:4px 0} .nowline b{color:var(--ink)} .now .links{margin-top:8px}
.pfields{display:grid;gap:8px} .pf span{display:block;font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--mute);margin-bottom:2px} .pf textarea,.jd textarea{width:100%;min-height:38px;font:14px var(--ui);padding:8px 10px;border:1px solid var(--rule2);border-radius:8px;background:#fff;color:var(--ink);resize:vertical;line-height:1.45}
.files{display:grid;gap:6px;margin:4px 0 8px} .file{display:flex;align-items:center;gap:8px;background:var(--paper2);border-radius:8px;padding:8px 10px;font-size:13.5px} .file a{flex:1;color:var(--ink);text-decoration:none;font-weight:500;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap} .file button{background:none;border:0;color:var(--mute);font-size:16px;padding:0 4px}
.btn.small{font-size:13px;padding:8px 12px;width:auto;margin:4px 0}
.conv{display:flex;gap:10px} .conv label{flex:1;font-size:12px;color:var(--mute)} .conv input,.rate input{width:100%;font:18px var(--ui);padding:8px 10px;border:1px solid var(--rule2);border-radius:8px;margin-top:2px} .rate{display:block;font-size:13px;color:var(--ink2);margin:10px 0} .rate input{width:80px;display:inline-block;font-size:14px;padding:4px 6px} .rate small{display:block;color:var(--mute);font-size:11.5px}
.quick{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px} .quick span{font-size:12px;background:var(--paper2);border-radius:999px;padding:4px 9px;color:var(--ink2)}
.phrases{display:grid;gap:6px;margin-bottom:10px} .ph{text-align:left;background:#fff;border:1px solid var(--rule);border-radius:10px;padding:9px 12px;font-family:var(--ui);cursor:pointer;color:var(--ink)} .ph b{display:block;font-size:13.5px;font-weight:600} .ph .pj{display:block;font-family:var(--jp);font-size:15px;margin:2px 0} .ph small{color:var(--mute);font-size:11.5px}
#phrase{position:fixed;inset:0;z-index:60;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px;text-align:center} #phrase.hidden{display:none} #phrase button{position:absolute;top:calc(12px + env(safe-area-inset-top));right:12px;background:none;border:1px solid var(--rule2);border-radius:50%;width:40px;height:40px;color:var(--ink)} .phjp{font-family:var(--jp);font-size:44px;line-height:1.3} .phro{font-size:18px;color:var(--ink2);margin-top:14px} .phfr{font-size:15px;color:var(--mute);margin-top:18px}
.nums{list-style:none;padding:0;margin:0 0 10px} .nums li{padding:8px 0;border-top:1px solid var(--rule);font-size:14px} .nums li:first-child{border-top:0} .nums b{display:block;font-weight:600} .nums span{color:var(--ink2);font-size:13.5px}
.links.wrap{margin-bottom:10px}
.ck.mini{padding:8px 10px;margin-bottom:6px;align-items:center} .ck.mini .ckt{font-size:14px;font-weight:500;margin:0}
.jd summary small{margin-left:auto;color:var(--mute);font-weight:400;font-size:12px} .jrow{display:flex;gap:10px;align-items:center;margin:8px 0;font-size:13px;color:var(--ink2);flex-wrap:wrap} .jrow input[type=number]{width:90px;font:14px var(--ui);padding:5px 8px;border:1px solid var(--rule2);border-radius:6px} .jphoto{display:inline-flex;align-items:center;gap:4px;border:1px solid var(--rule2);border-radius:999px;padding:4px 10px;cursor:pointer;color:var(--ai);font-weight:500} .jpics{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px} .jpics img{width:72px;height:72px;object-fit:cover;border-radius:6px}
.jtotal{font-size:13.5px;color:var(--ink2);margin:6px 0 8px} .jtotal b{color:var(--ink)}
.sw{display:flex;align-items:center;gap:10px;font-size:14px;margin:8px 0} .sw input[type=password]{width:80px;font:16px var(--ui);padding:5px 8px;border:1px solid var(--rule2);border-radius:6px;letter-spacing:.3em}
#toast{position:fixed;left:50%;bottom:calc(84px + env(safe-area-inset-bottom));transform:translateX(-50%) translateY(20px);background:var(--ink);color:#fff;font-size:13px;padding:8px 14px;border-radius:999px;opacity:0;transition:all .25s;pointer-events:none;z-index:70} #toast.on{opacity:1;transform:translateX(-50%)}
html.big{font-size:118%} html.big body{font-size:17px} html.big .sec p{font-size:17px} html.big .gc p,html.big .ckd,html.big .hotel p,html.big .night p{font-size:15.5px}
#lnav,#rside{display:none}
/* grand écran */
@media(min-width:900px){
 body{padding-bottom:40px;background:#f5f5f4}
 .top{left:0;right:0;padding-left:260px;padding-right:340px;background:rgba(250,250,249,.96)}
 .tabs{display:none}
 main{margin-left:240px;margin-right:320px;max-width:none}
 main>section.view{max-width:760px;margin:0 auto;background:var(--paper);min-height:100vh;box-shadow:0 0 0 1px var(--rule)}
 #lnav{display:block;position:fixed;left:0;top:0;bottom:0;width:240px;overflow:auto;background:#fff;border-right:1px solid var(--rule);padding:18px 14px 30px;z-index:25}
 .lbrand{display:flex;align-items:center;gap:10px;margin-bottom:16px} .lbrand .kj{font-family:var(--jp);font-size:15px;color:#fff;background:var(--shu);width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center} .lbrand b{font-size:15px;font-weight:600}
 .lnavtabs{display:grid;gap:2px;margin-bottom:18px} .lnavtabs button{display:flex;align-items:center;gap:10px;background:none;border:0;border-radius:8px;padding:8px 10px;font:500 14px var(--ui);color:var(--ink2);text-align:left;cursor:pointer} .lnavtabs button.on{background:var(--paper2);color:var(--shu)} .lnavtabs .tk{font-family:var(--jp);font-size:15px;width:20px}
 .lnavdays a{display:block;padding:5px 10px;border-radius:6px;font-size:13px;color:var(--ink2);text-decoration:none} .lnavdays a.chap{font-weight:600;color:var(--ink);margin-top:10px;font-size:12.5px;letter-spacing:.02em} .lnavdays a:hover{background:var(--paper2)} .lnavdays a.today{color:var(--shu);font-weight:600}
 #rside{display:block;position:fixed;right:0;top:0;bottom:0;width:320px;overflow:auto;background:#fff;border-left:1px solid var(--rule);padding:70px 16px 30px;z-index:25}
 #rside .now{margin:0 0 14px} #rside .mapfig{margin:0 0 14px} #rside .rtitle{font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin:14px 0 6px}
 .cover{padding:40px 32px 30px} .cover .ct{font-size:56px} .pad,.chbody,.garea,.prio{padding-left:32px;padding-right:32px} .toc{padding-left:32px;padding-right:32px} .now{margin-left:32px;margin-right:32px} .chapter .days{display:block}
 .photos figure{flex:0 0 46%} .hero img{height:300px}
 #results{left:240px;right:320px} .search{padding-left:260px;padding-right:340px}
}
'''

JS = r'''
(function(){
const $=s=>document.querySelector(s), $$=s=>Array.from(document.querySelectorAll(s));
// tabs
const views={voyage:'v-voyage',guide:'v-guide',todo:'v-todo',tools:'v-tools',sleep:'v-sleep',info:'v-info',maps:'v-maps'};
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
const cks=$$('#v-todo input[data-ck]');
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
$$('#v-voyage .night[data-s]').forEach(d=>add(d,'Hôtel',d.dataset.title,'voyage'));
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
document.addEventListener('click',e=>{ const im=e.target.closest('img[data-zoom]'); if(im){ lbi.src=im.src; lb.classList.add('on'); } });
$('#lbClose').addEventListener('click',()=>lb.classList.remove('on'));
// état initial
let tab='voyage'; try{ tab=localStorage.getItem('jp7.tab')||'voyage'; }catch(e){}
show(views[tab]?tab:'voyage',true);
})();

// ---------- extras : outils, maintenant, grand écran ----------
(function(){
const $=s=>document.querySelector(s), $$=s=>Array.from(document.querySelectorAll(s));
const toast=(m)=>{ const t=$('#toast'); t.textContent=m; t.classList.add('on'); clearTimeout(t._t); t._t=setTimeout(()=>t.classList.remove('on'),1800); };
const LS={get:(k,d)=>{ try{ const v=localStorage.getItem(k); return v===null?d:JSON.parse(v);}catch(e){return d;} }, set:(k,v)=>{ try{localStorage.setItem(k,JSON.stringify(v));}catch(e){} }};
// service worker (seulement en https, GitHub Pages)
if('serviceWorker' in navigator && location.protocol==='https:'){ navigator.serviceWorker.register('sw.js').catch(()=>{}); }
// copier l'adresse japonaise
$$('[data-copy]').forEach(el=>el.addEventListener('click',()=>{ navigator.clipboard&&navigator.clipboard.writeText(el.dataset.copy).then(()=>toast('Adresse copiée')); }));
// partager
$$('[data-share-title]').forEach(b=>b.addEventListener('click',e=>{ e.preventDefault(); const d={title:b.dataset.shareTitle,text:b.dataset.shareTitle+' · '+b.dataset.shareText,url:b.dataset.shareUrl}; if(navigator.share){ navigator.share(d).catch(()=>{}); } else if(navigator.clipboard){ navigator.clipboard.writeText(d.text+' '+d.url); toast('Copié'); } }));
// grand texte
const big=$('#bigText'); if(big){ big.checked=!!LS.get('jp7.big',false); document.documentElement.classList.toggle('big',big.checked); big.addEventListener('change',()=>{ LS.set('jp7.big',big.checked); document.documentElement.classList.toggle('big',big.checked); }); }
// convertisseur
const rate=$('#cvRate'), cvY=$('#cvY'), cvE=$('#cvE');
if(rate){ rate.value=LS.get('jp7.rate',175); const quick=()=>{ const r=parseFloat(rate.value)||175; $('#cvQuick').innerHTML=[500,1000,2000,3000,5000,10000,20000].map(y=>'<span>'+y.toLocaleString('fr-FR')+' ¥ = '+(y/r).toLocaleString('fr-FR',{maximumFractionDigits:y<2000?1:0})+' €</span>').join(''); }; quick();
 rate.addEventListener('input',()=>{ LS.set('jp7.rate',parseFloat(rate.value)||175); quick(); }); cvY.addEventListener('input',()=>{ const r=parseFloat(rate.value)||175; cvE.value=cvY.value?(cvY.value/r).toFixed(1):''; }); cvE.addEventListener('input',()=>{ const r=parseFloat(rate.value)||175; cvY.value=cvE.value?Math.round(cvE.value*r):''; }); }
// phrases
$$('.ph').forEach(b=>b.addEventListener('click',()=>{ $('.phjp').textContent=b.dataset.jp; $('.phro').textContent=b.dataset.ro; $('.phfr').textContent=b.dataset.fr; $('#phrase').classList.remove('hidden'); }));
const phc=$('#phClose'); if(phc) phc.addEventListener('click',()=>$('#phrase').classList.add('hidden'));
// papiers (champs)
const papers=LS.get('jp7.papers',{});
const fits=[]; $$('textarea[data-paper]').forEach(t=>{ if(papers[t.dataset.paper]!==undefined) t.value=papers[t.dataset.paper]; const fit=()=>{ t.style.height='auto'; t.style.height=Math.max(38,t.scrollHeight+2)+'px'; }; fits.push(fit); t.addEventListener('input',()=>{ papers[t.dataset.paper]=t.value; LS.set('jp7.papers',papers); fit(); }); });
const fitAll=()=>fits.forEach(f=>f()); $$('.tabs button[data-v=tools]').forEach(b=>b.addEventListener('click',()=>setTimeout(fitAll,30))); setTimeout(fitAll,100);
// code papiers
const pin=$('#pinSet'); if(pin){ pin.value=LS.get('jp7.pin',''); pin.addEventListener('change',()=>{ LS.set('jp7.pin',pin.value.replace(/\D/g,'').slice(0,4)); toast(pin.value?'Code enregistré':'Code retiré'); });
 const tp=$('#t-papers'); if(tp && LS.get('jp7.pin','')){ tp.open=false; tp.addEventListener('toggle',()=>{ if(tp.open && !tp._ok){ const c=prompt('Code Papiers'); if(c===LS.get('jp7.pin','')){ tp._ok=true; } else { tp.open=false; } } }); } }
// documents (IndexedDB)
let db=null; const req=indexedDB.open('jp7',1); req.onupgradeneeded=e=>{ e.target.result.createObjectStore('files',{keyPath:'id'}); e.target.result.createObjectStore('pics',{keyPath:'id'}); }; req.onsuccess=e=>{ db=e.target.result; listFiles(); listPics(); };
function tx(store,mode){ return db.transaction(store,mode).objectStore(store); }
function listFiles(){ if(!db) return; const out=$('#fileList'); if(!out) return; tx('files','readonly').getAll().onsuccess=e=>{ out.innerHTML=''; e.target.result.forEach(f=>{ const d=document.createElement('div'); d.className='file'; const a=document.createElement('a'); a.textContent=f.name; a.href='#'; a.addEventListener('click',ev=>{ ev.preventDefault(); const url=URL.createObjectURL(f.blob); window.open(url,'_blank'); }); const x=document.createElement('button'); x.textContent='×'; x.addEventListener('click',()=>{ tx('files','readwrite').delete(f.id).onsuccess=listFiles; }); d.append(a,x); out.appendChild(d); }); if(!e.target.result.length) out.innerHTML='<p class="note">Aucun document pour l\'instant.</p>'; }; }
const fa=$('#fileAdd'); if(fa) fa.addEventListener('change',()=>{ Array.from(fa.files).forEach(f=>{ tx('files','readwrite').put({id:Date.now()+Math.random(),name:f.name,blob:f}).onsuccess=listFiles; }); fa.value=''; toast('Document ajouté'); });
// checklists valise (persistance) et matin (reset quotidien)
const packSt=LS.get('jp7.pack',{}); $$('input[data-ck^="pack"]').forEach(c=>{ c.checked=!!packSt[c.dataset.ck]; c.addEventListener('change',()=>{ packSt[c.dataset.ck]=c.checked; LS.set('jp7.pack',packSt); }); });
const jst=()=>new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Tokyo',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
let mo=LS.get('jp7.morning',{d:'',v:{}}); if(mo.d!==jst()){ mo={d:jst(),v:{}}; LS.set('jp7.morning',mo); } const md=$('#moDate'); if(md) md.textContent=' · '+mo.d;
$$('input[data-morning]').forEach(c=>{ c.checked=!!mo.v[c.dataset.morning]; c.addEventListener('change',()=>{ mo.v[c.dataset.morning]=c.checked; LS.set('jp7.morning',mo); }); });
// carnet de route
const jr=LS.get('jp7.journal',{});
function jtotal(){ const r=LS.get('jp7.rate',175); let t=0; Object.values(jr).forEach(v=>{ t+=parseInt(v.spend||0)||0; }); const el=$('#jTotal'); if(el) el.innerHTML='Dépenses notées : <b>'+t.toLocaleString('fr-FR')+' yens</b> (≈ '+Math.round(t/r).toLocaleString('fr-FR')+' €)'; $$('.jd').forEach(d=>{ const k=d.dataset.day, v=jr[k]||{}; d.querySelector('.jsum').textContent=(v.text?'✎ ':'')+(v.spend?v.spend+' ¥':''); d.querySelector('.jeur').textContent=v.spend?'(≈ '+Math.round(v.spend/r)+' €)':''; }); }
$$('textarea[data-journal]').forEach(t=>{ const k=t.dataset.journal; t.value=(jr[k]||{}).text||''; t.addEventListener('input',()=>{ jr[k]=jr[k]||{}; jr[k].text=t.value; LS.set('jp7.journal',jr); jtotal(); }); });
$$('input[data-spend]').forEach(i=>{ const k=i.dataset.spend; i.value=(jr[k]||{}).spend||''; i.addEventListener('input',()=>{ jr[k]=jr[k]||{}; jr[k].spend=i.value; LS.set('jp7.journal',jr); jtotal(); }); });
jtotal();
function listPics(){ if(!db) return; tx('pics','readonly').getAll().onsuccess=e=>{ $$('.jpics').forEach(z=>z.innerHTML=''); e.target.result.forEach(p=>{ const z=document.querySelector('.jpics[data-pics="'+p.day+'"]'); if(!z) return; const im=document.createElement('img'); im.src=URL.createObjectURL(p.blob); im.title='toucher pour supprimer'; im.addEventListener('click',()=>{ if(confirm('Supprimer cette photo ?')) tx('pics','readwrite').delete(p.id).onsuccess=listPics; }); z.appendChild(im); }); }; }
$$('input[data-photo]').forEach(i=>i.addEventListener('change',()=>{ const f=i.files[0]; if(!f) return; const img=new Image(); img.onload=()=>{ const c=document.createElement('canvas'); const sc=Math.min(1,1200/Math.max(img.width,img.height)); c.width=img.width*sc; c.height=img.height*sc; c.getContext('2d').drawImage(img,0,0,c.width,c.height); c.toBlob(b=>{ tx('pics','readwrite').put({id:Date.now()+Math.random(),day:i.dataset.photo,blob:b}).onsuccess=listPics; },'image/jpeg',.8); }; img.src=URL.createObjectURL(f); i.value=''; }));
function dl(name,content,type){ const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([content],{type})); a.download=name; a.click(); }
const ej=$('#expJson'); if(ej) ej.addEventListener('click',()=>dl('carnet-japon.json',JSON.stringify({journal:jr,papers:papers,rate:LS.get('jp7.rate',175)},null,1),'application/json'));
const et=$('#expTxt'); if(et) et.addEventListener('click',()=>{ let out='Carnet de route, Japon 2026-2027\n\n'; $$('.jd').forEach(d=>{ const k=d.dataset.day, v=jr[k]||{}; if(v.text||v.spend) out+=d.querySelector('summary').firstChild.textContent+' ('+k+')\n'+(v.text||'')+'\n'+(v.spend?'Dépenses : '+v.spend+' yens\n':'')+'\n'; }); dl('carnet-japon.txt',out,'text/plain'); });
// soleil (approximation NOAA)
function sun(lat,lon,dateStr){ const d=new Date(dateStr+'T12:00:00+09:00'); const n=Math.floor((d-new Date(Date.UTC(d.getUTCFullYear(),0,1)))/864e5)+1; const r=Math.PI/180; const decl=23.44*r*Math.sin(r*(360/365)*(n-81)); const ha=Math.acos((Math.sin(-0.833*r)-Math.sin(lat*r)*Math.sin(decl))/(Math.cos(lat*r)*Math.cos(decl)))/r/15; const eot=9.87*Math.sin(2*r*(360/365)*(n-81))-7.53*Math.cos(r*(360/365)*(n-81))-1.5*Math.sin(r*(360/365)*(n-81)); const tz=lon>100?9:1; const solarNoon=12-lon/15+tz-eot/60; const f=h=>{ const hh=Math.floor(h), mm=Math.round((h-hh)*60); return hh+' h '+String(mm).padStart(2,'0'); }; return {rise:f(solarNoon-ha),set:f(solarNoon+ha)}; }
$$('.wx').forEach(w=>{ const su=sun(+w.dataset.lat,+w.dataset.lon,w.dataset.date); w.querySelector('.wxsun').textContent='Lever '+su.rise+' · coucher '+su.set+' (heure locale)'; });
// météo Open-Meteo (si réseau, 16 jours avant au plus)
async function weather(w){ const d=w.dataset.date; const today=new Date(); const target=new Date(d+'T00:00:00'); const diff=(target-today)/864e5; if(diff>16||diff<-1) return; try{ const u='https://api.open-meteo.com/v1/forecast?latitude='+w.dataset.lat+'&longitude='+w.dataset.lon+'&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,snowfall_sum,weathercode&timezone=Asia%2FTokyo&start_date='+d+'&end_date='+d; const r=await fetch(u); const j=await r.json(); const dd=j.daily; const codes={0:'ciel clair',1:'peu nuageux',2:'nuageux',3:'couvert',45:'brouillard',48:'brouillard givrant',51:'bruine',53:'bruine',55:'bruine',61:'pluie faible',63:'pluie',65:'pluie forte',71:'neige faible',73:'neige',75:'neige forte',77:'grains de neige',80:'averses',81:'averses',82:'fortes averses',85:'averses de neige',86:'averses de neige',95:'orage'}; const b=w.querySelector('.wxbody'); b.innerHTML='<div class="wxrow"><b>'+Math.round(dd.temperature_2m_min[0])+'° / '+Math.round(dd.temperature_2m_max[0])+'°</b><span>'+(codes[dd.weathercode[0]]||'')+'</span><span>'+(dd.precipitation_sum[0]||0)+' mm'+(dd.snowfall_sum[0]?' · neige '+dd.snowfall_sum[0]+' cm':'')+'</span></div><small>Open-Meteo, prévision chargée '+new Date().toLocaleTimeString('fr-FR',{hour:'2-digit',minute:'2-digit'})+'</small>'; }catch(e){} }
if(navigator.onLine) $$('.wx').forEach(weather);
// « Maintenant »
const dayEls=$$('details.day');
function parseTime(t){ const m=t.match(/(\d{1,2})\s*h\s*(\d{2})?/); if(!m) return null; return parseInt(m[1])*60+parseInt(m[2]||'0'); }
function renderNow(){ const nb=$('#nowBody'); if(!nb) return; const now=new Date(); const dstr=jst(); const hm=new Intl.DateTimeFormat('fr-FR',{timeZone:'Asia/Tokyo',hour:'2-digit',minute:'2-digit'}).format(now); $('#nowClock').textContent=hm; const [h,m]=hm.split(':').map(Number); const cur=h*60+m;
 const day=dayEls.find(x=>x.dataset.date===dstr); if(!day){ const first=dayEls[0]; const dl=Math.ceil((new Date(first.dataset.date)-new Date(dstr))/864e5); nb.innerHTML=dl>0?'<p class="nowline">Départ dans <b>'+dl+' jours</b>. Première étape : '+first.querySelector('.ttl').textContent+'.</p>':'<p class="nowline">Le voyage est terminé. Bon retour.</p>'; return; }
 const rows=Array.from(day.querySelectorAll('.traj .tr')).map(r=>({t:r.querySelector('.tt').textContent,min:parseTime(r.querySelector('.tt').textContent),b:r.querySelector('.tb b').textContent,s:(r.querySelector('.tb small')||{}).textContent||''})).filter(r=>r.min!==null);
 let next=rows.find(r=>r.min>=cur), prev=null; rows.forEach(r=>{ if(r.min<cur) prev=r; });
 let html='<p class="nowline"><b>'+day.querySelector('.dow').textContent.toLowerCase()+'</b> · '+day.querySelector('.ttl').textContent+'</p>';
 if(prev) html+='<div class="nowstep"><div class="tt">'+prev.t+'</div><div class="tb"><b>'+prev.b+'</b><small>'+prev.s+'</small></div></div>';
 if(next){ const dm=next.min-cur; html+='<div class="nowstep next"><div class="tt">'+next.t+'</div><div class="tb"><b>'+next.b+'</b><small>'+next.s+'</small><small>dans '+(dm>=60?Math.floor(dm/60)+' h '+String(dm%60).padStart(2,'0'):dm+' min')+'</small></div></div>'; } else html+='<p class="nowline">Plus rien de programmé aujourd\'hui.</p>';
 const night=day.querySelector('.night'); if(night){ html+='<p class="nowline">Ce soir : <b>'+night.querySelector('b').textContent+'</b></p><div class="links">'+night.querySelector('.links').innerHTML+'</div>'; }
 const wx=day.querySelector('.wx'); if(wx){ html+='<p class="nowline">'+wx.querySelector('.wxsun').textContent+'</p>'; }
 html+='<a class="btn ghost" href="#" data-open-day="'+day.id+'">Ouvrir la journée</a>';
 nb.innerHTML=html; nb.querySelector('[data-open-day]').addEventListener('click',e=>{ e.preventDefault(); day.open=true; day.scrollIntoView({block:'start'}); }); }
renderNow(); setInterval(renderNow,60000);
// grand écran : navigation gauche, colonne droite
const desktop=()=>window.matchMedia('(min-width:900px)').matches;
function buildLnav(){ const lt=$('.lnavtabs'); if(!lt) return; lt.innerHTML=''; $$('.tabs button').forEach(b=>{ const c=document.createElement('button'); c.innerHTML='<span class="tk">'+b.querySelector('.tk').textContent+'</span>'+b.querySelector('.tlab').textContent; c.dataset.v=b.dataset.v; c.className=b.classList.contains('on')?'on':''; c.addEventListener('click',()=>{ b.click(); buildLnav(); }); lt.appendChild(c); });
 const ld=$('.lnavdays'); ld.innerHTML=''; $$('.chapter').forEach(ch=>{ const a=document.createElement('a'); a.href='#'; a.className='chap'; a.textContent=ch.querySelector('h2').textContent; a.addEventListener('click',e=>{ e.preventDefault(); $('.tabs button[data-v=voyage]').click(); ch.scrollIntoView(); buildLnav(); }); ld.appendChild(a); ch.querySelectorAll('details.day').forEach(d=>{ const x=document.createElement('a'); x.href='#'; x.textContent=d.querySelector('.dow').textContent.toLowerCase()+' · '+d.querySelector('.ttl').textContent; if(d.classList.contains('today')) x.classList.add('today'); x.addEventListener('click',e=>{ e.preventDefault(); $('.tabs button[data-v=voyage]').click(); d.open=true; d.scrollIntoView(); buildLnav(); }); ld.appendChild(x); }); }); }
function layout(){ if(desktop()){ dayEls.forEach(d=>d.open=true); buildLnav(); const rs=$('#rside'); const nowEl=$('#now'); if(rs && nowEl && !rs.contains(nowEl)){ rs.appendChild(nowEl); } if(rs && !rs.querySelector('.mapfig')){ const t=document.createElement('div'); t.className='rtitle'; t.textContent='Carte générale'; rs.appendChild(t); const mf=document.querySelector('#v-info .mapfig.big'); if(mf) rs.appendChild(mf.cloneNode(true)); } } }
layout(); window.addEventListener('resize',layout);
})();
'''

NUM = r"\d{1,3}(?:[ \u202f\u00a0,]\d{3})+|\d+"
def _yen(n): return int(re.sub(r"[^\d]", "", n))
def _eur(y):
    e = y / 175.0
    if e < 1.5: return f"{e:.1f} €".replace(".", ",")
    if e < 100: return f"{round(e)} €"
    return f"{int(round(e, -1)):,} €".replace(",", "\u202f")
def euros(html):
    """Ajoute (≈ x €) après chaque montant en yens qui n'est pas déjà suivi d'une parenthèse."""
    rng = re.compile(r"(?<![\w€])(" + NUM + r")\s*(?:à|et|ou|-)\s*(" + NUM + r")\s?(yens?|¥)(?!\s*\(|\s*\d|[\w])")
    def frng(m):
        a, b = _yen(m.group(1)), _yen(m.group(2))
        if a < 50 or b < 50 or a > 5_000_000: return m.group(0)
        return f"{m.group(1)} à {m.group(2)} {m.group(3)} (≈ {_eur(a)} à {_eur(b)})"
    html = rng.sub(frng, html)
    one = re.compile(r"(?<![\w€])(" + NUM + r")\s?(yens?|¥)(?!\s*\(|\s*\d|[\w])")
    def fone(m):
        y = _yen(m.group(1))
        if y < 50 or y > 5_000_000: return m.group(0)
        return f"{m.group(1)} {m.group(2)} (≈ {_eur(y)})"
    return one.sub(fone, html)

def build():
    i180 = "data:image/png;base64," + base64.b64encode(open(os.path.join(ROOT, "pwa", "icon-180.png"), "rb").read()).decode()
    i192 = "data:image/png;base64," + base64.b64encode(open(os.path.join(ROOT, "pwa", "icon-192.png"), "rb").read()).decode()
    i512 = "data:image/png;base64," + base64.b64encode(open(os.path.join(ROOT, "pwa", "icon-512.png"), "rb").read()).decode()
    manifest = json.dumps(dict(name="Japon en hiver", short_name="Japon", start_url="./index.html", display="standalone", background_color="#fafaf9", theme_color="#fafaf9", icons=[dict(src=i192, sizes="192x192", type="image/png"), dict(src=i512, sizes="512x512", type="image/png")]))
    manifest_uri = "data:application/manifest+json;base64," + base64.b64encode(manifest.encode()).decode()
    def wf(n):
        with open(os.path.join(FONTS, n), "rb") as f: return "data:font/woff2;base64," + base64.b64encode(f.read()).decode()
    css = CSS.replace("INTER400", wf("inter-latin-400-normal.woff2")).replace("INTER500", wf("inter-latin-500-normal.woff2")).replace("INTER600", wf("inter-latin-600-normal.woff2"))
    doc = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="theme-color" content="#fafaf9"><meta name="apple-mobile-web-app-status-bar-style" content="default"><meta name="apple-mobile-web-app-title" content="Japon"><link rel="apple-touch-icon" href="{{ICON180}}"><link rel="icon" href="{{ICON192}}"><link rel="manifest" href="{{MANIFEST}}">
<title>Japon en hiver · {'guide Allibert' if MODE == 'allibert' else 'carnet v7'}</title><style>{css}</style></head><body>
<header class="top"><span class="kj">冬</span><div class="brand"><b>Japon en hiver</b><small>26 déc. 2026 → 11 janv. 2027</small></div><div class="jst" id="jst"><b>--:--</b>heure du Japon</div><button id="searchBtn" aria-label="Rechercher">{ico("search")}</button></header>
<div class="search hidden" id="search"><div class="row"><input id="q" type="search" placeholder="Rechercher dans le carnet…" autocomplete="off"><button id="closeSearch" aria-label="Fermer">{ico("close")}</button></div></div>
<div id="results" class="hidden"></div>
<main>
<section class="view on" id="v-voyage">{home}{render_now() if MODE == 'allibert' else ''}<nav class="toc">{toc}</nav>{overview}{render_timeline()}{chapters}</section>
<section class="view" id="v-todo">{render_checklist()}</section>
{'<section class="view" id="v-guide">' + render_guide() + '</section>' if MODE == 'allibert' else '<section class="view" id="v-sleep"><div class="pad"><div class="kicker">OÙ DORMIR</div><h1>Les hébergements, étape par étape</h1><p class="intro">Prix Booking du 1er novembre 2026 pour deux adultes aux dates du voyage ; chaque nom ouvre Booking aux bonnes dates. Toutes les adresses ont une salle de bain privée, sauf mention contraire.</p></div>' + lodgings + '</section>'}
{'<section class="view" id="v-tools">' + render_tools() + '</section>' if MODE == 'allibert' else ''}
<section class="view" id="v-info">{(render_maps() if MODE == 'allibert' else '')}{render_info()}</section>
{'' if MODE == 'allibert' else '<section class="view" id="v-maps">' + render_maps() + '</section>'}
</main>
<nav class="tabs"><button data-v="voyage" class="on"><span class="tk">旅</span><span class="tlab">Voyage</span></button>{'<button data-v="guide"><span class="tk">処</span><span class="tlab">Adresses</span></button>' if MODE == 'allibert' else '<button data-v="sleep"><span class="tk">宿</span><span class="tlab">Dormir</span></button>'}<button data-v="todo"><span class="tk">済</span><span class="tlab">À faire</span></button>{'<button data-v="tools"><span class="tk">具</span><span class="tlab">Outils</span></button>' if MODE == 'allibert' else ''}<button data-v="info"><span class="tk">案</span><span class="tlab">Infos</span></button>{'' if MODE == 'allibert' else '<button data-v="maps"><span class="tk">図</span><span class="tlab">Cartes</span></button>'}</nav>
<aside id="lnav"><div class="lbrand"><span class="kj">冬</span><b>Japon en hiver</b></div><div class="lnavtabs"></div><div class="lnavdays"></div></aside><aside id="rside"></aside>
<div id="phrase" class="hidden"><button id="phClose" aria-label="Fermer">{ico("close")}</button><div class="phjp"></div><div class="phro"></div><div class="phfr"></div></div>
<div id="toast"></div>
<div id="lb"><button id="lbClose" aria-label="Fermer">{ico("close")}</button><img alt=""><div class="hint">Faites défiler pour explorer la carte</div></div>
<script>{JS}</script></body></html>'''
    if MODE == 'allibert':
        for x, y in E.TEXT_FIXES: doc = doc.replace(x, y)
    doc = euros(doc).replace('{ICON180}', i180).replace('{ICON192}', i192).replace('{MANIFEST}', manifest_uri)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print(OUT, os.path.getsize(OUT) // 1024, "ko")

if __name__ == "__main__":
    build()

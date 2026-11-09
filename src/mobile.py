# -*- coding: utf-8 -*-
"""Carnet v7, version mobile : un seul fichier HTML autonome (images, polices et scripts inclus), hors ligne, avec recherche."""
import base64, io, json, os, re, html as H
from datetime import date, timedelta
from PIL import Image
import content_a as A, content_b as B, content_c as C, content_d as D, content_e as E
import daymaps as DM
try:
    import content_guide as G
except ImportError:
    G = None
try:
    import content_dj as DJ
except ImportError:
    DJ = None
DJS = "Direction Japon HS n°2"
if G is not None and DJ is not None:
    G.GUIDE = list(G.GUIDE)
    for _g in DJ.DJ_GUIDE:
        _d = dict(_g); _d["src"] = "dj"
        if _d.get("hours", "").lower().startswith("non indiqu"): _d["hours"] = "Horaires " + _d["hours"][0].lower() + _d["hours"][1:]
        if _d.get("price"): _d["hours"] = (_d.get("hours", "") + (" ; " if _d.get("hours") else "") + _d["price"]).strip()
        G.GUIDE.append(_d)
    for _a in getattr(DJ, "ALREADY_IN_GUIDE", []):
        for _g in G.GUIDE:
            if _g["name"] == _a["existing"]: _g["djnote"] = (_a["page"], _a.get("adds", ""))
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
    sun="M6.76 4.84l-1.8-1.79-1.41 1.41 1.79 1.79 1.42-1.41zM4 10.5H1v2h3v-2zm9-9.95h-2V3.5h2V.55zm7.45 3.91l-1.41-1.41-1.79 1.79 1.41 1.41 1.79-1.79zm-3.21 13.7l1.79 1.8 1.41-1.41-1.8-1.79-1.4 1.4zM20 10.5v2h3v-2h-3zm-8-5c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm-1 16.95h2V19.5h-2v2.95zm-7.45-3.91l1.41 1.41 1.79-1.8-1.41-1.41-1.79 1.8z",
    warn="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z",
    plus="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z",
    book="M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 4h5v8l-2.5-1.5L6 12V4z",
    people="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z",
    fork="M11 9H9V2H7v7H5V2H3v7c0 2.12 1.66 3.84 3.75 3.97V22h2.5v-9.03C11.34 12.84 13 11.12 13 9V2h-2v7zm5-3v8h2.5v8H21V2c-2.76 0-5 2.24-5 4z",
    compass="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm2.19 12.19L6 18l3.81-8.19L18 6l-3.81 8.19zM12 10.9c-.61 0-1.1.49-1.1 1.1s.49 1.1 1.1 1.1 1.1-.49 1.1-1.1-.49-1.1-1.1-1.1z",
    clock="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z",
    phone="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z",
    store="M20 4H4v2h16V4zm1 10v-2l-1-5H4l-1 5v2h1v6h10v-6h4v6h2v-6h1zm-9 4H6v-4h6v4z",
    check="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z",
    pen="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z",
    tune="M3 17v2h6v-2H3zM3 5v2h10V5H3zm10 16v-2h8v-2h-8v-2h-2v6h2zM7 9v2H3v2h4v2h2V9H7zm14 4v-2H11v2h10zm-6-4h2V7h4V5h-4V3h-2v6z",
    refresh="M17.65 6.35A7.958 7.958 0 0 0 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08A5.99 5.99 0 0 1 12 18c-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z",
    run="M13.49 5.48c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm-3.6 13.9l1-4.4 2.1 2v6h2v-7.5l-2.1-2 .6-3c1.3 1.5 3.3 2.5 5.5 2.5v-2c-1.9 0-3.5-1-4.3-2.4l-1-1.6c-.4-.6-1-1-1.7-1-.3 0-.5.1-.8.1l-5.2 2.2v4.7h2v-3.4l1.8-.7-1.6 8.1-4.9-1-.4 2 7 1.4z",
    camera="M12 15.2a3.2 3.2 0 1 0 0-6.4 3.2 3.2 0 0 0 0 6.4zM9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z",
    cup="M20 3H4v10c0 2.21 1.79 4 4 4h6c2.21 0 4-1.79 4-4v-3h2c1.11 0 2-.89 2-2V5c0-1.11-.89-2-2-2zm0 5h-2V5h2v3zM2 21h18v-2H2v2z",
    drop="M12 2c-5.33 4.55-8 8.48-8 11.8 0 4.98 3.8 8.2 8 8.2s8-3.22 8-8.2c0-3.32-2.67-7.25-8-11.8z",
    eye="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z",
    yen="M13.92 11H18v2h-4v2h4v2h-4v4h-4v-4H6v-2h4v-2H6v-2h4.08L5 3h3.5l3.5 7 3.5-7H19z",
    translate="M12.87 15.07l-2.54-2.51.03-.03A17.52 17.52 0 0 0 14.07 6H17V4h-7V2H8v2H1v2h11.17C11.5 7.92 10.44 9.75 9 11.35 8.07 10.32 7.3 9.19 6.69 8h-2c.73 1.63 1.73 3.17 2.98 4.56l-5.09 5.02L4 19l5-5 3.11 3.11.76-2.04zM18.5 10h-2L12 22h2l1.12-3h4.75L21 22h2l-4.5-12zm-2.62 7l1.62-4.33L19.12 17h-3.24z",
)
# badge d'icône coloré : chaque famille d'information a sa couleur et son pictogramme
SH = dict(dj="book", prog="clock", prat="check", table="fork", rep="compass", traj="train", coince="warn", opts="plus", wx="sun", night="bed", addr="pin", hist="book", loc="people", taste="fork", anec="book",
          manger="fork", cafe="cup", bain="drop", course="run", photo="camera", papeterie="pen", voir="eye", boutique="bag", hotel="bed", run="run",
          papers="todo", conv="yen", phrases="translate", nums="phone", konbini="store", pack="bag", morning="sun", journal="pen", settings="tune", block="warn", info="info", check="check", yen="yen")
def shi(kind): return f'<span class="shi s-{kind}">{ico(SH.get(kind, "info"))}</span>'
def sh(kind, text): return f'<div class="sh s-{kind}">{shi(kind)}<span>{text}</span></div>'
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
    return f'<div class="callout c-wx wx" data-lat="{pl[1]}" data-lon="{pl[2]}" data-date="{k}" data-place="{esc(pl[0])}">{sh("wx", "Météo et lumière · " + esc(pl[0]))}<div class="wxsun"></div><div class="wxbody"><small>Prévisions Open-Meteo quand le réseau est là (jusqu\'à 16 jours avant).</small></div>{extra}</div>'

def render_night(k):
    if MODE != 'allibert': return ""
    if k in E.NIGHT_OTHER:
        return f'<div class="callout c-night night">{sh("night", "La nuit")}<b>{esc(E.NIGHT_OTHER[k])}</b></div>'
    ref = E.HOTEL_BY_DATE.get(k)
    if not ref: return ""
    name, when, addr, mq, site, notes = E.HOTELS[ref[0]][ref[1]]
    car = k in E.CAR_DAYS
    links = f'<a class="pill" href="{maps_url(mq)}" target="_blank" rel="noopener">{ico("pin")} Maps</a>' + dir_links(mq, car)
    if site: links += f'<a class="pill" href="{site}" target="_blank" rel="noopener">{ico("ext")} Site</a>'
    links += share_btn(name, addr, maps_url(mq))
    jp = E.HOTELS_JP.get(name, "")
    jph = f'<div class="jp" data-copy="{esc(jp)}"><span>{esc(jp)}</span><small>à montrer au chauffeur · toucher pour copier</small></div>' if jp else ""
    return f'''<div class="callout c-night night" data-s="hotel" data-title="{esc(name)}">{sh("night", "La nuit · " + esc(when))}<b>{esc(name)}</b><div class="addr">{esc(addr)}</div>{jph}<details class="more"><summary>Accès, bains, horaires</summary><p>{notes}</p></details><div class="links">{links}</div></div>'''

def render_day_addresses(d_date):
    if not G or MODE != 'allibert': return ""
    items = [g for g in G.GUIDE if day_matches(g.get("day", ""), d_date)]
    if not items: return ""
    items.sort(key=lambda x: list(KINDS).index(x["kind"]) if x["kind"] in KINDS else 9)
    rows = "".join(f'<a class="dad" href="#adresses" data-go="guide" data-target="g-{slug(g["name"])}">{shi(g["kind"])}<span class="dn"><b>{esc(g["name"])}</b><small>{esc(KINDS.get(g["kind"], (g["kind"], ""))[0])}{(" · " + esc(g["zone"])) if g.get("zone") else ""}{(" · " + DJS + ", p. " + str(g.get("page", ""))) if g.get("src") == "dj" else ""}</small></span>{ico("chev","chev")}</a>' for g in items)
    return f'<div class="dayaddr">{sh("addr", "Adresses du jour")}{rows}</div>'

def render_day(ch, d):
    k = dkey(d)
    if MODE == 'allibert':
        d = dict(d)
        ok = (ch['key'], d['num'])
        if ok in E.PRATIQUE_OVERRIDES: d['pratique'] = E.PRATIQUE_OVERRIDES[ok]
        if ok in E.COINCE_OVERRIDES: d['coince'] = E.COINCE_OVERRIDES[ok]
        if ok in getattr(E, 'HEAD_OVERRIDES', {}): d['head'] = E.HEAD_OVERRIDES[ok]
        if ok in getattr(E, 'SECTION_OVERRIDES', {}): d['sections'] = E.SECTION_OVERRIDES[ok]
        if ok in getattr(E, 'TRAJET_OVERRIDES', {}): d['trajet'] = E.TRAJET_OVERRIDES[ok]
    head = "".join(f'<span class="hd"><b>{esc(a)}</b> {esc(b)}</span>' for a, b in d.get('head', []))
    photos = ""
    plist = list(d.get('photos') or [])
    if MODE == 'allibert': plist = list(E.ALLIBERT_PHOTOS.get(k, [])) + plist
    if plist:
        photos = '<div class="photos">' + "".join(f'<figure{" class=sq" if f.startswith("allibert/a") else ""}><img src="{img(f)}" alt="{esc(c)}" loading="lazy"><figcaption>{esc(c)}</figcaption></figure>' for f, c in plist) + '</div>'
    secs = "".join(f'<div class="sec">{sh("prog", esc(t))}<p>{x}</p></div>' for t, x in d.get('sections', []))
    side = ""
    if d.get('pratique'):
        side += '<div class="callout c-prat">' + sh("prat", "Pratique") + '<ul>' + "".join(f'<li>{p}</li>' for p in d['pratique']) + '</ul></div>'
    if d.get('table'):
        side += f'<div class="callout c-table">{sh("table", "À table")}<p>{d["table"]}</p></div>'
    if d.get('repere'):
        side += f'<div class="callout c-rep">{sh("rep", "Repère")}<p>{d["repere"]}</p></div>'
    traj = ""
    if d.get('trajet'):
        rows = ""
        for r in d['trajet']:
            t, where, how, dur, s = (list(r) + ["", "", ""])[:5]
            badge = f'<span class="resa {RESA[s][1]}">{RESA[s][0]}</span>' if s in RESA else ""
            rows += f'<div class="tr"><div class="tt">{esc(t)}</div><div class="tb"><b>{esc(where)}</b>{("<small>" + esc(how) + "</small>") if how else ""}<div class="tm">{esc(dur)} {badge}</div></div></div>'
        traj = f'<details class="sub c-traj"><summary>{shi("traj")}Le trajet, heure par heure</summary><div class="traj">{rows}</div></details>'
    coince = f'<details class="sub c-coince"><summary>{shi("coince")}Si ça coince</summary><p>{d["coince"]}</p></details>' if d.get('coince') else ""
    opts = ""
    if d.get('options'):
        opts = '<details class="sub c-opts"><summary>' + shi("opts") + 'Autres options et compléments</summary>' + "".join(f'<p><b>{esc(a)}</b> {b}</p>' for a, b in d['options']) + '</details>'
    stars = f'<span class="st">{d["stars"]}</span>' if d.get('stars') else ""
    dmap = ""
    if MODE == 'allibert' and k in DM.DAYS:
        dsvg, dsty = DM.day_svg(k); stay = DM.stay_of(k)
        badge = f'<span class="dmst">{stay["n"]}</span>' if stay else ""
        dmap = f'<div class="dmapw"><div class="dmap" style="{dsty}">{dsvg}</div><p class="dmcap">{badge}{esc(DM.DAYS[k]["label"])}<a href="#" class="dmall" data-ov="1">Vue d\'ensemble</a></p></div>'
    return f'''<details class="day" id="d-{k}" data-date="{k}" data-s="day">
<summary><div class="dnum">{d["num"]}</div><div class="dtt"><div class="dow">{esc(d["dow"])}</div><div class="ttl">{esc(d["title"])}{stars}</div><div class="heads">{head}</div></div>{ico("chev","chev")}</summary>
<div class="dbody">{dmap}{photos}{secs}{side}{render_dj_day(k)}{traj}{coince}{opts}{render_weather(k)}{render_night(k)}{render_day_addresses(date.fromisoformat(k))}</div></details>'''

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
        out += f'''<div class="hotel" data-s="hotel" data-title="{esc(name)}">{sh("hotel", "Hôtel Allibert · " + esc(when))}<b>{esc(name)}</b><div class="addr">{esc(addr)}</div><p>{notes}</p><div class="links">{links}</div></div>'''
    return out

def guide_link(ch):
    if not G: return ""
    areas = CH_AREAS.get(ch['key'], [])
    out = "".join(f'<a class="btn ghost" href="#adresses" data-go="guide" data-target="area-{slug(a)}">{ico("pin")} Adresses : {esc(a)}</a>' for a in areas if any(g["area"] == a for g in G.GUIDE))
    return out

def dj_src(g):
    if g.get("src") == "dj":
        return f'<div class="djsrc">{ico("book")}<span>Source : {DJS}, p. {g.get("page", "")}</span></div>'
    if g.get("djnote"):
        pg, adds = g["djnote"]
        return f'<div class="djsrc">{ico("book")}<span>Aussi dans {DJS}, p. {pg}{(" : " + esc(adds)) if adds else ""}</span></div>'
    return ""

def render_dj_day(k):
    if DJ is None: return ""
    notes = [n for n in DJ.DJ_DAY_NOTES if n["date"] == k]
    if not notes: return ""
    body = "".join(f'<div class="djn"><b>{esc(n["title"])}</b><p>{esc(n["text"])} <span class="djp">p. {n["page"]}</span></p></div>' for n in notes)
    return f'<div class="callout c-dj">{sh("dj", "Lu dans " + DJS)}{body}</div>'

def render_dj_chapter(key):
    if DJ is None: return ""
    notes = DJ.DJ_CHAPTER.get(key, [])
    if not notes: return ""
    body = "".join(f'<div class="djn"><b>{esc(n["title"])}</b><p>{esc(n["text"])} <span class="djp">p. {n["page"]}</span></p></div>' for n in notes)
    return f'<details class="sub c-djs" data-s="hist" data-title="Lu dans {DJS}"><summary>{shi("dj")}Lu dans {DJS}</summary>{body}<p class="note">Résumés de la rédaction de ce guide ; numéros de page du magazine.</p></details>'

def render_guide():
    if not G: return '<div class="pad"><p class="note">Adresses en préparation.</p></div>'
    chips = "".join(f'<button class="fchip" data-k="{k}">{ico(SH[k])}{v[0]}</button>' for k, v in KINDS.items()) + (f'<button class="fchip djf" data-k="dj">{ico("book")}Direction Japon</button>' if DJ else "")
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
            cards += f'''<div class="gc k-{k}" id="g-{slug(g["name"])}" data-k="{k}" data-src="{g.get("src", "")}" data-s="guide" data-title="{esc(g["name"])}"><div class="gk">{shi(k)}<span>{kv[0]}{(" · " + esc(g["zone"])) if g.get("zone") else ""}</span></div><b>{esc(g["name"])}</b><p>{esc(g["what"])}</p>{('<div class="addr">' + esc(g["address"]) + '</div>') if g.get("address") else ""}{('<div class="meta">' + " · ".join(meta) + '</div>') if meta else ""}{dj_src(g)}<div class="links">{links}</div></div>'''
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
        locals_html = f'''<details class="sub loc" data-s="locals" data-title="{esc(lc["title"])}"><summary>{shi("loc")}{esc(lc["title"])}</summary>
{sh("taste", "À goûter")}{taste}{sh("loc", "Comme les gens d'ici")}<ul>{customs}</ul>{sh("anec", "Anecdotes")}{anec}</details>'''
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
<details class="sub" data-s="hist" data-title="{esc(ch["title"])} : un peu d'histoire"><summary>{shi("hist")}Un peu d'histoire</summary><p>{ch["history"]}</p></details>
{locals_html}
{render_dj_chapter(key)}
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
<details class="sub c-coince"><summary>{shi("block")}Ce qui peut bloquer</summary>{blocks}</details></div>{out}'''

def render_timeline():
    rows = ""
    for dt, title, night, chips, car in A.TIMELINE['rows']:
        ch = "".join(f'<span class="chip {k}">{ico(i)}{esc(t)}</span>' for i, t, k in chips)
        # cible : la journée correspondante
        rows += f'<a class="tl{" car" if car else ""}" data-tl="{esc(dt)}"><div class="tld">{esc(dt)}</div><div class="tlb"><b>{esc(title)}</b><div class="chips">{ch}</div></div><div class="tln">{ico("bed")}{esc(night)}</div></a>'
    return f'<section class="timeline pad" id="timeline"><div class="kicker">{esc(A.TIMELINE["kicker"])}</div><h1>{esc(A.TIMELINE["title"])}</h1><div class="tls">{rows}</div><p class="note">{esc(A.TIMELINE["legend_bp"]).capitalize()} sur fond sable.</p></section>'

def render_info_allibert():
    inc = "".join(f"<li>{x}</li>" for x in E.INCLUDED["yes"]); exc = "".join(f"<li>{x}</li>" for x in E.INCLUDED["no"])
    before = "".join(f'<details class="sub" data-s="info" data-title="{esc(t)}"><summary>{shi("info")}{esc(cap(t))}</summary><div class="rich">{b}</div></details>' for t, b in E.BEFORE_BOXES + [A.BEFORE['boxes'][0], A.BEFORE['boxes'][1]])
    prac = "".join(f'<details class="sub" data-s="info" data-title="{esc(t)}"><summary>{shi("info")}{esc(cap(t))}</summary><p>{E.PRACTICAL_OVERRIDES.get(t, b)}</p></details>' for t, b in C.PRACTICAL['items'] + E.PRACTICAL_EXTRA)
    mode = "".join(f'<details class="sub" data-s="mode" data-title="{esc(t)}"><summary>{shi("info")}{esc(cap(t))}</summary><p>{b}</p></details>' for t, b in D.MODE_EMPLOI['items'] if "RÉSERVÉS" not in t)
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)} {ico("ext")}</a></li>' for t, u in C.SOURCES)
    return f'''<div class="pad">
<div class="kicker">AVANT DE PARTIR</div><h1>Le voyage avec Allibert</h1><p class="intro">{E.INTRO}</p>
<details class="sub" data-s="info" data-title="Ce qui est compris"><summary>{shi("check")}Ce qui est compris</summary><ul>{inc}</ul></details>
<details class="sub" data-s="info" data-title="Ce qui reste à notre charge"><summary>{shi("yen")}Ce qui reste à notre charge</summary><ul>{exc}</ul></details>
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
<details class="sub tool" id="t-papers" open><summary>{shi("papers")}Papiers et références</summary><p class="note">Tout reste sur ce téléphone (stockage local du navigateur), rien n'est envoyé. Un code à 4 chiffres peut masquer cette section : réglage en bas.</p><div class="pfields">{fields}</div>
<div class="lbl">Documents (PDF, photos de passeports, vouchers)</div><div class="files" id="fileList"></div><label class="btn ghost small">{ico("ext")} Ajouter un document <input type="file" id="fileAdd" multiple accept="application/pdf,image/*" hidden></label><p class="note">Les fichiers sont gardés dans la base locale du navigateur (IndexedDB) et s'ouvrent hors ligne. Garder aussi les originaux dans Fichiers ou Mail.</p></details>
<details class="sub tool"><summary>{shi("conv")}Convertisseur</summary><div class="conv"><label>Yens <input type="number" inputmode="numeric" id="cvY" placeholder="1 000"></label><label>Euros <input type="number" inputmode="decimal" id="cvE" placeholder="5,7"></label></div><label class="rate">Taux : 1 € = <input type="number" inputmode="decimal" id="cvRate" value="175"> yens <small>(à régler à l'arrivée, il est mémorisé)</small></label>
<div class="quick" id="cvQuick"></div></details>
<details class="sub tool"><summary>{shi("phrases")}Phrases à montrer</summary><p class="note">Toucher une phrase pour l'afficher en grand, à montrer.</p><div class="phrases">{phrases}</div></details>
<details class="sub tool"><summary>{shi("nums")}Numéros utiles</summary><ul class="nums">{numbers}</ul></details>
<details class="sub tool"><summary>{shi("konbini")}Konbini et distributeurs 7-Eleven</summary><p class="note">Les distributeurs 7-Eleven acceptent les cartes européennes ; recherche Google Maps autour de chaque hôtel.</p><div class="links wrap">{konbini}</div></details>
<details class="sub tool"><summary>{shi("pack")}Valise, avant de partir</summary>{pack}</details>
<details class="sub tool"><summary>{shi("morning")}Chaque matin <small id="moDate"></small></summary><p class="note">La liste se remet à zéro chaque jour.</p>{morning}</details>
<details class="sub tool" id="t-journal"><summary>{shi("journal")}Carnet de route</summary><p class="note">Quelques lignes, une photo, la dépense du jour. Tout reste sur le téléphone ; exporter en fin de voyage.</p><div class="jtotal" id="jTotal"></div>{journal}<div class="links"><button class="pill" id="expJson">Exporter JSON</button><button class="pill" id="expTxt">Exporter texte</button></div></details>
<details class="sub tool"><summary>{shi("settings")}Réglages</summary><label class="sw"><input type="checkbox" id="bigText"> Grand texte (pour Claudie)</label><label class="sw">Code Papiers (4 chiffres, vide = aucun) <input type="password" inputmode="numeric" maxlength="4" id="pinSet" placeholder="····"></label><p class="note">Le code masque seulement l'affichage ; ce n'est pas un chiffrement.</p></details>
</div>'''

def render_where():
    mico = dict(train="train", bus="bus", car="car", plane="plane")
    rows = ""
    nums = {}
    for ch in CHAPTERS:
        for d in ch["days"]: nums[dkey(d)] = d["num"]
    for st in DM.STAYS:
        mode, how = st["come"]
        ref = E.HOTEL_BY_DATE.get(st["days"][0]); hotel = E.HOTELS[ref[0]][ref[1]][0] if ref else ""
        chips = "".join(f'<button data-day="d-{k}" data-k="{k}">{nums.get(k, "")}</button>' for k in st["days"])
        side = f'<small class="sside">{ico("plus")}{esc(st["side"])}</small>' if st.get("side") else ""
        rows += f'<div class="pair"><div class="leg">{ico(mico[mode])}<span>{esc(how)}</span></div>'
        rows += f'<div class="stay" data-n="{st["n"]}"><span class="sn">{st["n"]}</span><div class="sb"><div class="sl"><b>{esc(DM.P[st["key"]][0])}</b><span>{esc(st["dates"])} · {st["nights"]} nuit{"s" if st["nights"] > 1 else ""}</span></div><small class="sh2">{ico("bed")}{esc(hotel)}</small>{side}<div class="schips">{chips}</div></div></div></div>'
    rows += f'<div class="leg">{ico("plane")}<span>{esc(DM.DEPART)}</span></div>'
    legend = '<div class="ovleg"><span><i class="l-train"></i>train</span><span><i class="l-bus"></i>car</span><span><i class="l-car"></i>voiture</span><span><i class="l-ex"></i>excursion</span></div>'
    return f'<section class="where" id="where"><div class="whereh"><h2>Le voyage en un coup d\'œil</h2></div><div class="wgrid"><div class="wmap"><div class="dmap ov">{DM.overview_svg()}</div>{legend}</div><div class="stays">{rows}</div></div></section>'

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

def render_daynav():
    out = ""
    for ch in CHAPTERS:
        out += f'<div class="dnch"><span class="kj">{ch["kanji"]}</span>{esc(ch["title"])}</div>'
        for d in ch["days"]:
            k = dkey(d)
            out += f'<a class="dnr" href="#" data-day="d-{k}" data-date="{k}"><span class="dnn">{d["num"]}</span><span class="dnt"><b>{esc(d["title"])}</b><small>{esc(d["dow"].capitalize())}</small></span></a>'
    return f'<div id="dn" class="hidden"><div class="cvbg" id="dnBg"></div><div class="cvsheet dnsheet" role="dialog" aria-label="Les jours du voyage"><div class="cvhead"><b>Les jours du voyage</b><button id="dnClose" aria-label="Fermer">{ico("close")}</button></div><a href="#" class="dnov" data-ov="1">{ico("map")}Vue d\'ensemble : les 9 étapes sur la carte</a><div class="dnlist">{out}</div></div></div>'

# --- assemblage ----------------------------------------------------------------
cover = A.COVER
home = f'''<section class="cover"><div class="ckj">{cover["kanji"]}</div><div class="ck1">{esc(E.KICKER if MODE == 'allibert' else cover["kicker"])}</div><h1 class="ct">Japon <i>en hiver</i></h1><div class="cd">{esc(cover["dates"])}</div><p>{esc(cover["line"])}</p>
<div class="stops">{"".join("<span>"+esc(s)+"</span>" for s in cover["stops"])}</div>
<button class="btn today" id="todayBtn">{ico("days")} Aujourd'hui</button></section>{f'<figure class="coverph"><img src="{img(E.COVER_PHOTO[0], 1200, 70)}" alt=""><figcaption>{esc(E.COVER_PHOTO[1])}</figcaption></figure>' if MODE == 'allibert' else ''}'''
brief = "".join(f'<details class="sub" data-s="info" data-title="{esc(a)}"><summary>{shi("info")}{esc(a)}</summary><p>{E.BRIEF_OVERRIDES.get(a, b) if MODE == "allibert" else b}</p></details>' for a, b in A.OVERVIEW['brief'])
overview = f'<div class="pad"><div class="kicker">{esc(A.OVERVIEW["kicker"])}</div><h1>{esc(A.OVERVIEW["title"])}</h1><p class="intro">{A.OVERVIEW["intro"]}</p>{brief}</div>'
chapters = "".join(render_chapter(ch) for ch in CHAPTERS)
lodgings = "".join(render_lodging(ch) for ch in CHAPTERS)
toc = "".join(f'<a class="tocl t-{ch["theme"]}" href="#voyage" data-target="ch-{ch["key"]}"><span class="kj">{ch["kanji"]}</span><div><b>{esc(ch["title"])}</b><small>{esc(ch["subtitle"])}</small></div>{ico("chev","chev")}</a>' for ch in CHAPTERS)

CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme.css"), encoding="utf-8").read()

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
$$('.fchip').forEach(b=>b.addEventListener('click',()=>{ $$('.fchip').forEach(x=>x.classList.toggle('on',x===b)); const k=b.dataset.k; $$('.gc').forEach(c=>c.classList.toggle('hidden',k!=='all'&&(k==='dj'?c.dataset.src!=='dj':c.dataset.k!==k))); $$('.zone').forEach(z=>{ let vis=false, n=z.nextElementSibling; while(n && !n.classList.contains('zone')){ if(n.classList.contains('gc') && !n.classList.contains('hidden')) vis=true; n=n.nextElementSibling; } z.classList.toggle('hidden',!vis); }); $$('.garea').forEach(a=>a.classList.toggle('hidden',!a.querySelector('.gc:not(.hidden)'))); }));
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
window.__goTo=goTo; window.__todayId=todayId;
})();

// ---------- extras : outils, maintenant, grand écran ----------
(function(){
const $=s=>document.querySelector(s), $$=s=>Array.from(document.querySelectorAll(s));
const toast=(m)=>{ const t=$('#toast'); t.textContent=m; t.classList.add('on'); clearTimeout(t._t); t._t=setTimeout(()=>t.classList.remove('on'),1800); };
const LS={get:(k,d)=>{ try{ const v=localStorage.getItem(k); return v===null?d:JSON.parse(v);}catch(e){return d;} }, set:(k,v)=>{ try{localStorage.setItem(k,JSON.stringify(v));}catch(e){} }};
// service worker (seulement en https, GitHub Pages)
if('serviceWorker' in navigator && location.protocol==='https:'){ navigator.serviceWorker.register('sw.js').catch(()=>{}); }
// le voyage en un coup d'œil
const ov=$('#where'); if(ov){
 function stSel(n){ $$('#where .st').forEach(g=>g.classList.toggle('sel',g.dataset.n===String(n))); $$('#where .rt').forEach(p=>p.classList.toggle('sel',p.dataset.to===String(n))); $$('#where .stay').forEach(r=>r.classList.toggle('sel',r.dataset.n===String(n))); }
 $$('#where .stay').forEach(r=>r.addEventListener('click',e=>{ if(e.target.closest('button')) return; stSel(r.dataset.n); }));
 $$('#where .st').forEach(g=>g.addEventListener('click',()=>{ stSel(g.dataset.n); const r=document.querySelector('#where .stay[data-n="'+g.dataset.n+'"]'); if(r) r.scrollIntoView({block:'nearest',behavior:'smooth'}); }));
 $$('#where .schips button').forEach(b=>b.addEventListener('click',()=>window.__goTo('voyage',b.dataset.day,true)));
 const t=window.__todayId? window.__todayId.slice(2):null; const r0=t && document.querySelector('#where .schips button[data-k="'+t+'"]');
 if(r0){ r0.classList.add('today'); stSel(r0.closest('.stay').dataset.n); } }
document.addEventListener('click',e=>{ const a=e.target.closest('[data-ov]'); if(!a) return; e.preventDefault(); const dn=$('#dn'); if(dn) dn.classList.add('hidden'); const w=$('#where'); if(!w) return; if(window.matchMedia('(min-width:900px)').matches){ w.scrollIntoView({block:'start'}); w.classList.remove('flash'); void w.offsetWidth; w.classList.add('flash'); } else { window.__goTo('voyage','where',false); } });
// navigation rapide entre les jours
const dn=$('#dn'); const dnOpen=()=>{ dn.classList.remove('hidden'); const t=dn.querySelector('.dnr.today'); if(t) t.scrollIntoView({block:'center'}); }; const dnCloseF=()=>dn.classList.add('hidden');
$('#dnBtn').addEventListener('click',dnOpen); $('#dnClose').addEventListener('click',dnCloseF); $('#dnBg').addEventListener('click',dnCloseF);
$$('.dnr').forEach(a=>{ if(window.__todayId && a.dataset.day===window.__todayId) a.classList.add('today'); a.addEventListener('click',e=>{ e.preventDefault(); dnCloseF(); window.__goTo('voyage',a.dataset.day,true); }); });
document.addEventListener('keydown',e=>{ if(e.key==='Escape') dnCloseF(); });
// convertisseur rapide, accessible partout
const cv=$('#cv'), cvY2=$('#cvY2'), cvE2=$('#cvE2'), cvBig=$('#cvBig');
const fmt=(n,d)=>n.toLocaleString('fr-FR',{maximumFractionDigits:d});
const getRate=()=>parseFloat(LS.get('jp7.rate',175))||175;
function cvRender(){ const r=getRate(); const live=LS.get('jp7.rateLive',null); $('#cvRateLine').textContent='Taux : 1 € = '+fmt(r,1)+' yens'+(live&&live.d?' (BCE, '+live.d+')':' (taux réglé à la main)'); $('#cvQuickBtns').innerHTML=[500,1000,2000,3000,5000,8000,10000,15000,20000,30000,50000].map(y=>'<button data-y="'+y+'"><b>'+fmt(y,0)+' ¥</b><span>'+fmt(y/r,y<2000?1:0)+' €</span></button>').join(''); $$('#cvQuickBtns button').forEach(b=>b.addEventListener('click',()=>{ cvY2.value=b.dataset.y; cvFromY(); })); const ri=$('#cvRate'); if(ri) ri.value=r; }
function cvFromY(){ const r=getRate(); const y=parseFloat(cvY2.value); cvE2.value=isNaN(y)?'':(y/r).toFixed(y/r<20?1:0); cvBig.textContent=isNaN(y)?'':fmt(y,0)+' ¥ = '+fmt(y/r,y/r<20?1:0)+' €'; }
function cvFromE(){ const r=getRate(); const e=parseFloat(cvE2.value); cvY2.value=isNaN(e)?'':Math.round(e*r); cvBig.textContent=isNaN(e)?'':fmt(e,1)+' € = '+fmt(Math.round(e*r),0)+' ¥'; }
cvY2.addEventListener('input',cvFromY); cvE2.addEventListener('input',cvFromE);
function cvOpen(){ cvRender(); cv.classList.remove('hidden'); setTimeout(()=>cvY2.focus(),50); } function cvCloseF(){ cv.classList.add('hidden'); }
$('#cvBtn').addEventListener('click',cvOpen); $('#cvClose').addEventListener('click',cvCloseF); $('#cvBg').addEventListener('click',cvCloseF);
document.addEventListener('keydown',e=>{ if(e.key==='Escape') cvCloseF(); });
// taux du jour (BCE via frankfurter.app), au plus une fois par jour
(async()=>{ const live=LS.get('jp7.rateLive',null); const today=new Date().toISOString().slice(0,10); if(live&&live.fetched===today) return; if(!navigator.onLine) return; try{ const j=await fetch('https://api.frankfurter.app/latest?from=EUR&to=JPY').then(r=>r.json()); const v=j&&j.rates&&j.rates.JPY; if(v){ LS.set('jp7.rateLive',{v:v,d:j.date,fetched:today}); LS.set('jp7.rate',Math.round(v*10)/10); const ri=$('#cvRate'); if(ri){ ri.value=Math.round(v*10)/10; ri.dispatchEvent(new Event('input')); } } }catch(e){} })();
// recharger en forçant le réseau (vide le cache du service worker)
const rb=$('#refreshBtn'); if(rb) rb.addEventListener('click',async()=>{ toast('Mise à jour…'); try{ if('caches' in window){ const ks=await caches.keys(); await Promise.all(ks.map(k=>caches.delete(k))); } if(navigator.serviceWorker){ const rs=await navigator.serviceWorker.getRegistrations(); await Promise.all(rs.map(r=>r.unregister())); } }catch(e){} const u=new URL(location.href); u.searchParams.set('r',Date.now()); location.replace(u.toString()); });
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
function layout(){ if(desktop()){ dayEls.forEach(d=>d.open=true); buildLnav(); const rs=$('#rside'); const nowEl=$('#now'); if(rs && nowEl && !rs.contains(nowEl)){ rs.appendChild(nowEl); } } }
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
    with open(DM.base_jpeg(), "rb") as f: daymap = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
    css = CSS.replace("DAYMAP_RATIO", f"{DM.PX}/{DM.H}").replace("DAYMAP", daymap).replace("INTER400", wf("inter-latin-400-normal.woff2")).replace("INTER500", wf("inter-latin-500-normal.woff2")).replace("INTER600", wf("inter-latin-600-normal.woff2"))
    doc = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="theme-color" content="#fafaf9"><meta name="apple-mobile-web-app-status-bar-style" content="default"><meta name="apple-mobile-web-app-title" content="Japon"><link rel="apple-touch-icon" href="{{ICON180}}"><link rel="icon" href="{{ICON192}}"><link rel="manifest" href="{{MANIFEST}}">
<title>Japon en hiver · {'guide Allibert' if MODE == 'allibert' else 'carnet v7'}</title><style>{css}</style></head><body>
<header class="top"><span class="kj">冬</span><div class="brand"><b>Japon en hiver</b><small>26 déc. → 11 janv. 2027</small></div><div class="jst" id="jst"><b>--:--</b>heure du Japon</div><button id="dnBtn" aria-label="Les jours du voyage">{ico("days")}</button><button id="cvBtn" aria-label="Convertisseur yens euros">{ico("yen")}</button><button id="refreshBtn" aria-label="Recharger la dernière version">{ico("refresh")}</button><button id="searchBtn" aria-label="Rechercher">{ico("search")}</button></header>
<div class="search hidden" id="search"><div class="row"><input id="q" type="search" placeholder="Rechercher dans le carnet…" autocomplete="off"><button id="closeSearch" aria-label="Fermer">{ico("close")}</button></div></div>
<div id="results" class="hidden"></div>
<div class="app"><main>
<section class="view on" id="v-voyage">{home}{render_now() if MODE == 'allibert' else ''}{render_where() if MODE == 'allibert' else ''}<nav class="toc">{toc}</nav>{overview}{render_timeline()}{chapters}</section>
<section class="view" id="v-todo">{render_checklist()}</section>
{'<section class="view" id="v-guide">' + render_guide() + '</section>' if MODE == 'allibert' else '<section class="view" id="v-sleep"><div class="pad"><div class="kicker">OÙ DORMIR</div><h1>Les hébergements, étape par étape</h1><p class="intro">Prix Booking du 1er novembre 2026 pour deux adultes aux dates du voyage ; chaque nom ouvre Booking aux bonnes dates. Toutes les adresses ont une salle de bain privée, sauf mention contraire.</p></div>' + lodgings + '</section>'}
{'<section class="view" id="v-tools">' + render_tools() + '</section>' if MODE == 'allibert' else ''}
<section class="view" id="v-info">{(render_maps() if MODE == 'allibert' else '')}{render_info()}</section>
{'' if MODE == 'allibert' else '<section class="view" id="v-maps">' + render_maps() + '</section>'}
</main>
<nav class="tabs"><button data-v="voyage" class="on"><span class="tk">旅</span><span class="tlab">Voyage</span></button>{'<button data-v="guide"><span class="tk">処</span><span class="tlab">Adresses</span></button>' if MODE == 'allibert' else '<button data-v="sleep"><span class="tk">宿</span><span class="tlab">Dormir</span></button>'}<button data-v="todo"><span class="tk">済</span><span class="tlab">À faire</span></button>{'<button data-v="tools"><span class="tk">具</span><span class="tlab">Outils</span></button>' if MODE == 'allibert' else ''}<button data-v="info"><span class="tk">案</span><span class="tlab">Infos</span></button>{'' if MODE == 'allibert' else '<button data-v="maps"><span class="tk">図</span><span class="tlab">Cartes</span></button>'}</nav>
<aside id="lnav"><div class="lbrand"><span class="kj">冬</span><b>Japon en hiver</b></div><div class="lnavtabs"></div><div class="lnavdays"></div></aside><aside id="rside"></aside></div>
<div id="phrase" class="hidden"><button id="phClose" aria-label="Fermer">{ico("close")}</button><div class="phjp"></div><div class="phro"></div><div class="phfr"></div></div>
<div id="cv" class="hidden"><div class="cvbg" id="cvBg"></div><div class="cvsheet" role="dialog" aria-label="Convertisseur"><div class="cvhead"><b>Yens en euros</b><button id="cvClose" aria-label="Fermer">{ico("close")}</button></div>
<div class="cvrate" id="cvRateLine">Taux : 1 € = 175 yens</div>
<div class="cvquick" id="cvQuickBtns"></div>
<div class="cvio"><label><span>Yens</span><input type="number" inputmode="numeric" id="cvY2" placeholder="1 000"></label><label><span>Euros</span><input type="number" inputmode="decimal" id="cvE2" placeholder="5,7"></label></div>
<div class="cvbig" id="cvBig"></div>
<p class="note">Taux de la Banque centrale européenne quand le réseau est là (mis à jour une fois par jour), sinon le dernier taux connu. Modifiable dans Outils.</p></div></div>
{render_daynav()}
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

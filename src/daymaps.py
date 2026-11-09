# -*- coding: utf-8 -*-
"""Cartes « où serons-nous » : un fond de relief partagé (GSI, pâli) et des surcouches SVG.
Vue d'ensemble : étapes de nuit numérotées, trajets par mode. Carte du jour : zoom sur la région du jour."""
import math, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
TILE = "relief_ovA_8_221_99_227_103.png"
TW, TE, TS, TN = 130.78125, 140.625, 31.952162238024968, 37.718590325588146
W, E, S, N = 134.05, 140.55, 33.2, 36.75   # cadre (lon ouest, est ; lat sud, nord)
PX = 720                                    # largeur du repère SVG

def my(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
H = int(round(PX * (my(N) - my(S)) / math.radians(E - W)))

def xy(lat, lon):
    return round((lon - W) / (E - W) * PX, 1), round((my(N) - my(lat)) / (my(N) - my(S)) * H, 1)

def base_jpeg():
    """Fond pâli et recadré (relief GSI sur terre, mer bleu pâle), deux fois la résolution du repère."""
    out = os.path.join(IMG, "daymap_base3.jpg")
    if os.path.exists(out): return out
    import numpy as np
    im = Image.open(os.path.join(IMG, TILE)).convert("RGBA")
    w, h = im.size
    pxd = w / (TE - TW); yN, yS = my(TN), my(TS); pyd = h / (yN - yS)
    box = (int((W - TW) * pxd), int((yN - my(N)) * pyd), int((E - TW) * pxd), int((yN - my(S)) * pyd))
    im = im.crop(box).resize((PX * 2, H * 2), Image.LANCZOS)
    a = np.asarray(im).astype(float)
    g = a[..., :3].mean(axis=2, keepdims=True); alpha = a[..., 3:4] / 255.0
    land = (255 - (255 - g) * 0.62) * np.array([1.0, 0.985, 0.955])
    sea = np.array([213.0, 225.0, 236.0])
    Image.fromarray((land * alpha + sea * (1 - alpha)).clip(0, 255).astype("uint8")).save(out, "JPEG", quality=72, optimize=True, progressive=True)
    return out

# ---------------------------------------------------------------- lieux
P = dict(
    tokyo=("Tokyo", 35.68, 139.76), haneda=("Haneda", 35.55, 139.78), kamakura=("Kamakura", 35.32, 139.55),
    matsumoto=("Matsumoto", 36.24, 137.97), takayama=("Takayama", 36.14, 137.25), shirakawa=("Shirakawa-gō", 36.26, 136.91),
    nagoya=("Nagoya", 35.17, 136.88), ise=("Ise", 34.49, 136.71), kawayu=("Kawayu Onsen", 33.84, 135.77),
    nachi=("Nachi", 33.67, 135.89), katsuura=("Kii-Katsuura", 33.63, 135.94), koya=("Kōya-san", 34.21, 135.59),
    kix=("Aéroport KIX", 34.43, 135.24), osaka=("Osaka", 34.69, 135.50), kyoto=("Kyoto", 35.00, 135.76), nara=("Nara", 34.68, 135.84),
    # points de passage (non affichés)
    kofu=("", 35.66, 138.57), hirayu=("", 36.19, 137.56), gero=("", 35.81, 137.24), tsu=("", 34.72, 136.51),
    owase=("", 34.07, 136.19), kumanoshi=("", 33.89, 136.10), shingu=("", 33.73, 135.99), totsukawa=("", 33.99, 135.79),
    gojo=("", 34.35, 135.69), hashimoto=("", 34.32, 135.61), hamamatsu=("", 34.70, 137.73), shizuoka=("", 34.97, 138.39), odawara=("", 35.26, 139.15),
)
# trajets : (de, à) -> (mode, points de passage)
SEG = {
    ("haneda", "tokyo"): ("train", []), ("tokyo", "kamakura"): ("train", []),
    ("tokyo", "matsumoto"): ("train", ["kofu"]), ("matsumoto", "takayama"): ("bus", ["hirayu"]),
    ("takayama", "shirakawa"): ("bus", []), ("takayama", "nagoya"): ("train", ["gero"]), ("nagoya", "ise"): ("train", ["tsu"]),
    ("ise", "kawayu"): ("car", ["owase", "kumanoshi", "shingu"]), ("kawayu", "nachi"): ("car", ["shingu"]), ("nachi", "katsuura"): ("car", []),
    ("katsuura", "koya"): ("car", ["shingu", "kawayu", "totsukawa", "gojo"]), ("koya", "kix"): ("car", ["hashimoto"]), ("kix", "osaka"): ("train", []),
    ("osaka", "kyoto"): ("train", []), ("kyoto", "nara"): ("train", []), ("kyoto", "tokyo"): ("train", ["nagoya", "hamamatsu", "shizuoka", "odawara"]),
    ("tokyo", "haneda"): ("train", []),
}
ROUTE = [("tokyo", "matsumoto"), ("matsumoto", "takayama"), ("takayama", "nagoya"), ("nagoya", "ise"), ("ise", "kawayu"), ("kawayu", "nachi"),
         ("nachi", "katsuura"), ("katsuura", "koya"), ("koya", "kix"), ("kix", "osaka"), ("osaka", "kyoto"), ("kyoto", "tokyo")]
SIDE = [("takayama", "shirakawa"), ("kyoto", "nara"), ("tokyo", "kamakura")]
DASH = dict(train="", bus="7 5", car="2 5", plane="1 7", opt="4 5")
MODE_FR = dict(train="train", bus="car (autocar)", car="voiture", plane="avion")

# ---------------------------------------------------------------- étapes de nuit
STAYS = [
    dict(n=1, key="tokyo", dates="27 → 30 déc.", nights=3, days=["2026-12-27", "2026-12-28", "2026-12-29"],
         come=("plane", "Vol AF274 Paris → Haneda, 13 h 35, puis 40 min de train"), side="option Kamakura le 29, 1 h de train"),
    dict(n=2, key="matsumoto", dates="30 déc.", nights=1, days=["2026-12-30"], come=("train", "Azusa depuis Shinjuku, 2 h 40"), segs=[("tokyo", "matsumoto")]),
    dict(n=3, key="takayama", dates="31 déc. → 2 janv.", nights=2, days=["2026-12-31", "2027-01-01"], come=("bus", "car par le col d'Abō, 2 h 30"),
         segs=[("matsumoto", "takayama")], side="Shirakawa-gō le 1er janvier, car 50 min"),
    dict(n=4, key="ise", dates="2 janv.", nights=1, days=["2027-01-02"], come=("train", "Hida jusqu'à Nagoya 2 h 20, puis Kintetsu 1 h 25"), segs=[("takayama", "nagoya"), ("nagoya", "ise")]),
    dict(n=5, key="kawayu", dates="3 → 5 janv.", nights=2, days=["2027-01-03", "2027-01-04"], come=("car", "voiture par la côte (Owase, Kumano, Shingū), environ 4 h de route"), segs=[("ise", "kawayu")],
         side="Kumano Kodo à pied le 4"),
    dict(n=6, key="katsuura", dates="5 janv.", nights=1, days=["2027-01-05"], come=("car", "voiture via Nachi et la cascade"), segs=[("kawayu", "nachi"), ("nachi", "katsuura")]),
    dict(n=7, key="osaka", dates="6 janv.", nights=1, days=["2027-01-06"], come=("car", "voiture par Kōya-san, rendue à l'aéroport du Kansai, puis train 40 min"),
         segs=[("katsuura", "koya"), ("koya", "kix"), ("kix", "osaka")]),
    dict(n=8, key="kyoto", dates="7 → 9 janv.", nights=2, days=["2027-01-07", "2027-01-08"], come=("train", "train depuis Osaka, 15 à 30 min ; guide à l'hôtel à 10 h"), segs=[("osaka", "kyoto")],
         side="Nara le 8, 45 min de train"),
    dict(n=9, key="tokyo", dates="9 → 10 janv.", nights=1, days=["2027-01-09", "2027-01-10"], come=("train", "Nozomi Kyoto → Tokyo, 2 h 15"), segs=[("kyoto", "tokyo")]),
]
DEPART = "Vol de nuit AF279 Haneda → Paris le 10 janvier à 22 h 55, arrivée le 11 à 5 h 50"

# ---------------------------------------------------------------- journées : étapes (lieu, trajet pour y arriver) et nuit
DAYS = {
    "2026-12-26": dict(legs=[("haneda", "plane")], night=None, label="En vol vers Tokyo ; arrivée à Haneda le 27 à 19 h 55"),
    "2026-12-27": dict(legs=[("haneda", None), ("tokyo", "train")], night="tokyo", label="Arrivée à Haneda 19 h 55, 40 min de train, nuit à Tokyo"),
    "2026-12-28": dict(legs=[("tokyo", None)], night="tokyo", label="Tokyo : Asakusa, Nezu et Yanaka"),
    "2026-12-29": dict(legs=[("tokyo", None), ("kamakura", "opt")], night="tokyo", label="Tokyo moderne ; option Kamakura à 1 h de train"),
    "2026-12-30": dict(legs=[("tokyo", None), ("matsumoto", "train")], night="matsumoto", label="Matinée à Tokyo, Azusa vers Matsumoto (2 h 40)"),
    "2026-12-31": dict(legs=[("matsumoto", None), ("takayama", "bus")], night="takayama", label="Car par le col d'Abō (2 h 30), réveillon à Takayama"),
    "2027-01-01": dict(legs=[("takayama", None), ("shirakawa", "bus"), ("takayama", "bus")], night="takayama", label="Aller et retour à Shirakawa-gō, 50 min de car chaque sens"),
    "2027-01-02": dict(legs=[("takayama", None), ("nagoya", "train"), ("ise", "train")], night="ise", label="Hida jusqu'à Nagoya, Kintetsu jusqu'à Ise"),
    "2027-01-03": dict(legs=[("ise", None), ("kawayu", "car")], night="kawayu", label="Naikū à l'aube, puis la voiture par la côte jusqu'à Kawayu Onsen"),
    "2027-01-04": dict(legs=[("kawayu", None)], night="kawayu", label="Kumano Kodo à pied autour de Hongū"),
    "2027-01-05": dict(legs=[("kawayu", None), ("nachi", "car"), ("katsuura", "car")], night="katsuura", label="Nachi et la cascade, puis la côte à Kii-Katsuura"),
    "2027-01-06": dict(legs=[("katsuura", None), ("koya", "car"), ("kix", "car"), ("osaka", "train")], night="osaka", label="Kōya-san en voiture, voiture rendue à l'aéroport du Kansai, train vers Osaka"),
    "2027-01-07": dict(legs=[("osaka", None), ("kyoto", "train")], night="kyoto", label="Train vers Kyoto, journée guidée"),
    "2027-01-08": dict(legs=[("kyoto", None), ("nara", "train"), ("kyoto", "train")], night="kyoto", label="Aller et retour à Nara, 45 min de train"),
    "2027-01-09": dict(legs=[("kyoto", None), ("tokyo", "train")], night="tokyo", label="Nozomi vers Tokyo (2 h 15)"),
    "2027-01-10": dict(legs=[("tokyo", None), ("haneda", "train")], night=None, label="Journée à Tokyo, puis Haneda et le vol de nuit"),
    "2027-01-11": dict(legs=[("haneda", "plane")], night=None, label="Arrivée à Paris à 5 h 50, TGV vers Besançon"),
}

def pt(key): _, la, lo = P[key]; return xy(la, lo)

def poly(a, b):
    mode, via = SEG.get((a, b)) or (SEG.get((b, a)) or ("train", []))
    if (a, b) not in SEG and (b, a) in SEG: via = list(reversed(via))
    return mode, [pt(a)] + [pt(v) for v in via] + [pt(b)]

def path_d(pts): return "M" + " L".join(f"{x},{y}" for x, y in pts)

# décalage des étiquettes (dx, dy, ancrage), en unités du repère
LAB = dict(tokyo=(-20, -16, "end"), haneda=(14, 22, "start"), kamakura=(-12, 20, "end"), matsumoto=(16, -10, "start"), takayama=(16, 22, "start"),
           shirakawa=(-14, -10, "end"), nagoya=(14, 20, "start"), ise=(16, 8, "start"), kawayu=(-16, 6, "end"), nachi=(14, -8, "start"),
           katsuura=(16, 18, "start"), koya=(14, 10, "start"), kix=(-12, 22, "end"), osaka=(-16, 8, "end"), kyoto=(16, -6, "start"), nara=(14, 16, "start"))

SHORT = dict(kawayu="Kawayu", kix="KIX")
def label(key, fs, cls="lb", scale=1.0, short=False):
    n = SHORT.get(key, P[key][0]) if short else P[key][0]; x, y = pt(key); dx, dy, anc = LAB.get(key, (12, 4, "start"))
    return f'<text class="{cls}" x="{x + dx * scale}" y="{y + dy * scale}" text-anchor="{anc}" font-size="{fs}">{n}</text>'

# ---------------------------------------------------------------- vue d'ensemble
def overview_svg():
    g = ""
    for a, b in ROUTE:
        mode, pts = poly(a, b)
        st = next((s["n"] for s in STAYS if (a, b) in s.get("segs", [])), 0)
        g += f'<path class="rt" data-to="{st}" d="{path_d(pts)}" stroke-dasharray="{DASH[mode]}"/>'
    for a, b in SIDE:
        mode, pts = poly(a, b)
        g += f'<path class="rt side" d="{path_d(pts)}" stroke-dasharray="{DASH["opt" if b == "kamakura" else mode]}"/>'
    x, y = pt("haneda")
    g += f'<path class="rt" data-to="1" d="M{x - 150},{y - 110} L{x},{y}" stroke-dasharray="{DASH["plane"]}"/>'
    # excursions et passages
    for key in ("shirakawa", "nara", "kamakura", "koya", "nachi", "nagoya", "kix"):
        x, y = pt(key)
        g += f'<circle cx="{x}" cy="{y}" r="6" class="ex"/>' + label(key, 21, "lb lbs", short=True)
    # étapes numérotées (Tokyo : 1 et 9)
    for s in STAYS:
        x, y = pt(s["key"])
        if s["n"] == 9: x += 34
        g += f'<g class="st" data-n="{s["n"]}"><circle cx="{x}" cy="{y}" r="17"/><text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="central">{s["n"]}</text></g>'
    for key, dx in (("tokyo", 0), ("matsumoto", 0), ("takayama", 0), ("ise", 0), ("kawayu", 0), ("katsuura", 0), ("osaka", 0), ("kyoto", 0)):
        n = SHORT.get(key, P[key][0]); x, y = pt(key); ldx, ldy, anc = LAB[key]
        g += f'<text class="lb" x="{x + dx + ldx + (6 if anc == "start" else -6)}" y="{y + ldy}" text-anchor="{anc}" font-size="25">{n}</text>'
    return f'<svg viewBox="0 0 {PX} {H}" xmlns="http://www.w3.org/2000/svg" aria-label="Carte du voyage, étapes numérotées">{g}</svg>'

# ---------------------------------------------------------------- carte du jour (zoomée)
LF = 1.05   # taille des étiquettes (1 : environ 12,5 px à l'écran sur un téléphone)
def _lab_box(key, fs, scale):
    n = P[key][0]; x, y = pt(key); dx, dy, anc = LAB.get(key, (12, 4, "start"))
    w = len(n) * 0.58 * fs; tx = x + dx * scale; ty = y + dy * scale
    x0 = tx if anc == "start" else tx - w
    return [(x0, ty - fs), (x0 + w, ty + fs * .3)]

def day_view(k):
    d = DAYS[k]; base = []
    prev = None
    for key, mode in d["legs"]:
        if prev and mode and mode != "opt": base += poly(prev, key)[1]
        base.append(pt(key)); prev = key
    for key, mode in d["legs"]:
        if mode == "opt": base.append(pt(key))
    vw = 300
    for _ in range(3):
        z = vw / PX; fs = 26 * z * LF; pts = list(base)
        for key, _m in d["legs"]: pts += _lab_box(key, fs, z * 1.9)
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        pad = 36 * z / (300 / PX) ** 0 if False else 40
        x0, x1, y0, y1 = min(xs) - pad, max(xs) + pad, min(ys) - pad, max(ys) + pad
        if any(m == "plane" for _, m in d["legs"]): x0 -= 120; y0 -= 90
        w, h = max(x1 - x0, 300), max(y1 - y0, 225)
        if w / h < 1.25: w = h * 1.25
        if w / h > 1.8: h = w / 1.8
        w = min(w, PX); h = min(h, H); vw = w
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    x = min(max(cx - w / 2, 0), PX - w); y = min(max(cy - h / 2, 0), H - h)
    return round(x, 1), round(y, 1), round(w, 1), round(h, 1)

def day_svg(k):
    d = DAYS[k]; legs = d["legs"]
    vx, vy, vw, vh = day_view(k)
    z = vw / PX                       # 1 = carte entière
    sw = lambda v: round(v * z * 1.9, 2)  # épaisseurs et tailles constantes à l'écran
    g = ""
    for a, b in ROUTE + SIDE:
        mode, pts = poly(a, b)
        g += f'<path d="{path_d(pts)}" fill="none" stroke="#1e3a5f" stroke-opacity=".22" stroke-width="{sw(1.6)}" stroke-dasharray="{" ".join(str(sw(float(v))) for v in DASH[mode].split()) if DASH[mode] else ""}" stroke-linecap="round" stroke-linejoin="round"/>'
    prev = None
    for key, mode in legs:
        if prev and mode:
            m, pts = poly(prev, key)
            col = "#8d8a94" if mode == "opt" else "#c73e2a"
            dash = DASH["opt" if mode == "opt" else m]
            g += f'<path d="{path_d(pts)}" fill="none" stroke="{col}" stroke-width="{sw(3.2)}" stroke-dasharray="{" ".join(str(sw(float(v))) for v in dash.split()) if dash else ""}" stroke-linecap="round" stroke-linejoin="round"/>'
        prev = key
    if legs and legs[0][1] == "plane":
        x, y = pt("haneda")
        g += f'<path d="M{x - 200},{y - 150} L{x},{y}" fill="none" stroke="#c73e2a" stroke-width="{sw(3.2)}" stroke-dasharray="{sw(1)} {sw(8)}" stroke-linecap="round"/>'
    seen = []; fs = round(26 * z * LF, 1)
    for key, mode in legs:
        if key in seen: continue
        seen.append(key); x, y = pt(key)
        if mode == "opt":
            g += f'<circle cx="{x}" cy="{y}" r="{sw(6)}" fill="#fff" stroke="#8d8a94" stroke-width="{sw(2.4)}"/>' + label(key, fs, "lb lbo", z * 1.9)
        elif key == d["night"]:
            g += f'<circle cx="{x}" cy="{y}" r="{sw(15)}" fill="#c73e2a" fill-opacity=".16"/><circle cx="{x}" cy="{y}" r="{sw(8)}" fill="#c73e2a" stroke="#fff" stroke-width="{sw(2.4)}"/>' + label(key, fs, "lb lbn", z * 1.9)
        else:
            g += f'<circle cx="{x}" cy="{y}" r="{sw(6.5)}" fill="#fff" stroke="#c73e2a" stroke-width="{sw(2.8)}"/>' + label(key, fs, "lb", z * 1.9)
    style = (f"aspect-ratio:{vw}/{vh};background-size:{PX / vw * 100:.2f}% {H / vh * 100:.2f}%;"
             f"background-position:{(vx / (PX - vw) * 100) if PX - vw > .5 else 0:.2f}% {(vy / (H - vh) * 100) if H - vh > .5 else 0:.2f}%")
    svg = f'<svg viewBox="{vx} {vy} {vw} {vh}" xmlns="http://www.w3.org/2000/svg" aria-label="Carte du jour">{g}</svg>'
    return svg, style

def stay_of(k):
    for s in STAYS:
        if k in s["days"]: return s
    return None

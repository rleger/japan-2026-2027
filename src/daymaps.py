# -*- coding: utf-8 -*-
"""Cartes « où sommes-nous » : un fond de relief partagé (GSI, pâli) et une surcouche SVG vectorielle par journée."""
import math, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
TILE = "relief_ovA_8_221_99_227_103.png"
TW, TE, TS, TN = 130.78125, 140.625, 31.952162238024968, 37.718590325588146
# cadre de la carte (lon ouest, est ; lat sud, nord)
W, E, S, N = 134.75, 140.45, 33.25, 36.85
PX = 720  # largeur en pixels

def my(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
# hauteur : rapport des étendues Mercator (longitude en radians)
H = int(round(PX * (my(N) - my(S)) / math.radians(E - W)))

def xy(lat, lon):
    x = (lon - W) / (E - W) * PX
    y = (my(N) - my(lat)) / (my(N) - my(S)) * H
    return round(x, 1), round(y, 1)

def base_jpeg():
    """Fond pâli, recadré, en JPEG (chemin du fichier) : relief GSI sur terre, mer bleu pâle."""
    out = os.path.join(IMG, "daymap_base.jpg")
    if os.path.exists(out): return out
    import numpy as np
    im = Image.open(os.path.join(IMG, TILE)).convert("RGBA")
    w, h = im.size
    pxd = w / (TE - TW); yN, yS = my(TN), my(TS); pyd = h / (yN - yS)
    box = (int((W - TW) * pxd), int((yN - my(N)) * pyd), int((E - TW) * pxd), int((yN - my(S)) * pyd))
    im = im.crop(box).resize((PX * 2, H * 2), Image.LANCZOS)
    a = np.asarray(im).astype(float)
    g = a[..., :3].mean(axis=2, keepdims=True)
    alpha = a[..., 3:4] / 255.0
    land = 255 - (255 - g) * 0.62
    land = land * np.array([1.0, 0.985, 0.955])
    sea = np.array([213.0, 225.0, 236.0])
    rgb = land * alpha + sea * (1 - alpha)
    Image.fromarray(rgb.clip(0, 255).astype("uint8")).resize((PX, H), Image.LANCZOS).save(out, "JPEG", quality=74, optimize=True)
    return out

# lieux
P = dict(
    tokyo=("Tokyo", 35.68, 139.76), haneda=("Haneda", 35.55, 139.78), kamakura=("Kamakura", 35.32, 139.55),
    matsumoto=("Matsumoto", 36.24, 137.97), takayama=("Takayama", 36.14, 137.25), shirakawa=("Shirakawa-gō", 36.26, 136.91),
    nagoya=("Nagoya", 35.17, 136.88), ise=("Ise", 34.49, 136.71), kawayu=("Kawayu, Hongū", 33.84, 135.77),
    nachi=("Nachi", 33.67, 135.89), katsuura=("Kii-Katsuura", 33.63, 135.94), koya=("Kōya-san", 34.21, 135.59),
    osaka=("Osaka", 34.70, 135.50), kyoto=("Kyoto", 35.00, 135.77), nara=("Nara", 34.68, 135.84),
)
# par date : étapes de la journée (lieu, mode du trajet pour y arriver), puis lieu de la nuit
# modes : plane, train, bus, car, walk ; "opt" = option
DAYS = {
    "2026-12-26": dict(legs=[("haneda", "plane")], night="haneda", label="En vol vers Tokyo, arrivée le 27 au soir"),
    "2026-12-27": dict(legs=[("haneda", None), ("tokyo", "train")], night="tokyo", label="Arrivée à Haneda 19 h 55, nuit à Tokyo"),
    "2026-12-28": dict(legs=[("tokyo", None)], night="tokyo", label="Tokyo, Asakusa et Yanaka"),
    "2026-12-29": dict(legs=[("tokyo", None), ("kamakura", "opt")], night="tokyo", label="Tokyo moderne ; option Kamakura à 1 h de train"),
    "2026-12-30": dict(legs=[("tokyo", None), ("matsumoto", "train")], night="matsumoto", label="Matinée à Tokyo, Azusa vers Matsumoto"),
    "2026-12-31": dict(legs=[("matsumoto", None), ("takayama", "bus")], night="takayama", label="Bus par le col d'Abō, réveillon à Takayama"),
    "2027-01-01": dict(legs=[("takayama", None), ("shirakawa", "bus"), ("takayama", "bus")], night="takayama", label="Aller-retour à Shirakawa-gō"),
    "2027-01-02": dict(legs=[("takayama", None), ("nagoya", "train"), ("ise", "train")], night="ise", label="Hida vers Nagoya, Kintetsu vers Ise"),
    "2027-01-03": dict(legs=[("ise", None), ("kawayu", "car")], night="kawayu", label="Voiture d'Ise à Kawayu Onsen"),
    "2027-01-04": dict(legs=[("kawayu", None)], night="kawayu", label="Kumano Kodo autour de Hongū"),
    "2027-01-05": dict(legs=[("kawayu", None), ("nachi", "car"), ("katsuura", "car")], night="katsuura", label="Nachi, puis la côte à Kii-Katsuura"),
    "2027-01-06": dict(legs=[("katsuura", None), ("koya", "car"), ("osaka", "train")], night="osaka", label="Kōya-san en voiture, puis Osaka"),
    "2027-01-07": dict(legs=[("osaka", None), ("kyoto", "train")], night="kyoto", label="Kyoto, journée guidée"),
    "2027-01-08": dict(legs=[("kyoto", None), ("nara", "train"), ("kyoto", "train")], night="kyoto", label="Aller-retour à Nara"),
    "2027-01-09": dict(legs=[("kyoto", None), ("tokyo", "train")], night="tokyo", label="Nozomi vers Tokyo"),
    "2027-01-10": dict(legs=[("tokyo", None), ("haneda", "train")], night="haneda", label="Tokyo, puis Haneda, vol de nuit"),
    "2027-01-11": dict(legs=[("haneda", "plane")], night="haneda", label="Arrivée à Paris le matin"),
}
NIGHT_ORDER = ["tokyo", "matsumoto", "takayama", "ise", "kawayu", "katsuura", "osaka", "kyoto", "tokyo"]
NIGHT_SEGS = [("tokyo", "matsumoto", "train"), ("matsumoto", "takayama", "bus"), ("takayama", "nagoya", "train"), ("nagoya", "ise", "train"), ("ise", "kawayu", "car"), ("kawayu", "nachi", "car"), ("nachi", "katsuura", "car"), ("katsuura", "koya", "car"), ("koya", "osaka", "train"), ("osaka", "kyoto", "train"), ("kyoto", "tokyo", "train")]
DASH = dict(train="", bus="6 4", car="2 4", plane="1 5", walk="1 3", opt="3 4")
# décalage des étiquettes (dx, dy, ancrage)
LAB = dict(tokyo=(12, 6, "start"), haneda=(12, 18, "start"), kamakura=(12, 16, "start"), matsumoto=(12, -8, "start"), takayama=(12, 18, "start"), shirakawa=(-12, -8, "end"),
           nagoya=(12, 16, "start"), ise=(12, 6, "start"), kawayu=(12, 20, "start"), nachi=(12, -6, "start"), katsuura=(12, 16, "start"), koya=(-12, -6, "end"), osaka=(-12, 10, "end"), kyoto=(12, -6, "start"), nara=(12, 16, "start"))

def pt(key): n, la, lo = P[key]; return xy(la, lo)

def route_path(stroke="#1e3a5f", op=.28, width=1.5):
    out = ""
    for a, b, m in NIGHT_SEGS:
        x1, y1 = pt(a); x2, y2 = pt(b)
        out += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-opacity="{op}" stroke-width="{width}" stroke-dasharray="{DASH.get(m, "")}" stroke-linecap="round"/>'
    return out

def label(key, cls="lb"):
    n, la, lo = P[key]; x, y = pt(key); dx, dy, anc = LAB.get(key, (10, 4, "start"))
    return f'<text class="{cls}" x="{x + dx}" y="{y + dy}" text-anchor="{anc}">{n}</text>'

def day_svg(k):
    d = DAYS[k]
    legs = d["legs"]
    g = route_path()
    # toutes les étapes de nuit en points discrets
    for key in set(NIGHT_ORDER):
        x, y = pt(key); g += f'<circle cx="{x}" cy="{y}" r="2.6" fill="#1e3a5f" fill-opacity=".35"/>'
    # trajets du jour
    prev = None
    for key, mode in legs:
        if prev and mode:
            x1, y1 = pt(prev); x2, y2 = pt(key)
            col = "#9a9aa6" if mode == "opt" else "#c73e2a"
            g += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="2.6" stroke-dasharray="{DASH.get(mode, "")}" stroke-linecap="round"/>'
        prev = key
    seen = []
    for key, mode in legs:
        if key in seen: continue
        seen.append(key)
        x, y = pt(key)
        if mode == "opt":
            g += f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="#9a9aa6" stroke-width="2"/>' + label(key, "lb lbo")
        elif key == d["night"] or len(legs) == 1:
            g += f'<circle cx="{x}" cy="{y}" r="11" fill="#c73e2a" fill-opacity=".18"/><circle cx="{x}" cy="{y}" r="6" fill="#c73e2a" stroke="#fff" stroke-width="2"/>' + label(key, "lb lbn")
        else:
            g += f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="#c73e2a" stroke-width="2.4"/>' + label(key)
    # vol : trait vers le bord
    if legs and legs[0][1] == "plane":
        x, y = pt("haneda")
        g += f'<line x1="{x}" y1="{y}" x2="{x - 120}" y2="{y - 90}" stroke="#c73e2a" stroke-width="2.6" stroke-dasharray="1 6" stroke-linecap="round"/>'
    return f'<svg viewBox="0 0 {PX} {H}" xmlns="http://www.w3.org/2000/svg" aria-label="Carte du jour">{g}</svg>'

def overview_svg():
    g = route_path("#1e3a5f", .55, 2)
    nums = {"tokyo": "27 → 30", "matsumoto": "30", "takayama": "31, 1", "ise": "2", "kawayu": "3, 4", "katsuura": "5", "osaka": "6", "kyoto": "7, 8", "nara": "8", "shirakawa": "1", "koya": "6", "nachi": "5", "nagoya": ""}
    # segments d'excursion
    for a, b, m in (("takayama", "shirakawa", "bus"), ("kyoto", "nara", "train")):
        x1, y1 = pt(a); x2, y2 = pt(b)
        g += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#1e3a5f" stroke-opacity=".55" stroke-width="2" stroke-dasharray="{DASH[m]}" stroke-linecap="round"/>'
    for key in ("tokyo", "matsumoto", "takayama", "shirakawa", "ise", "kawayu", "nachi", "katsuura", "koya", "osaka", "kyoto", "nara"):
        x, y = pt(key)
        night = key in NIGHT_ORDER
        g += f'<g class="ov" data-k="{key}"><circle cx="{x}" cy="{y}" r="{6 if night else 4.5}" fill="{"#1e3a5f" if night else "#fff"}" stroke="{"#fff" if night else "#1e3a5f"}" stroke-width="2"/>' + label(key, "lb") + '</g>'
    x, y = pt("haneda")
    g += f'<line x1="{x}" y1="{y}" x2="{x - 120}" y2="{y - 90}" stroke="#1e3a5f" stroke-opacity=".55" stroke-width="2" stroke-dasharray="1 6" stroke-linecap="round"/>'
    # marqueur mobile pour la journée choisie
    g += '<circle id="ovDot" cx="-50" cy="-50" r="12" fill="#c73e2a" fill-opacity=".2"/><circle id="ovDot2" cx="-50" cy="-50" r="6.5" fill="#c73e2a" stroke="#fff" stroke-width="2"/>'
    return f'<svg viewBox="0 0 {PX} {H}" xmlns="http://www.w3.org/2000/svg" aria-label="Carte du voyage">{g}</svg>'

def day_points():
    """Pour le JS : par date, les coordonnées du lieu de la nuit (ou du jour) et l'étiquette."""
    out = {}
    for k, d in DAYS.items():
        key = d["night"] if d["night"] != "haneda" else (d["legs"][-1][0] if d["legs"][-1][0] != "haneda" else "tokyo")
        x, y = pt(key)
        out[k] = dict(x=x, y=y, label=d["label"], place=P[key][0])
    return out

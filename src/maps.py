# -*- coding: utf-8 -*-
"""Cartes du carnet v7 : fonds de relief GSI (tuiles déjà téléchargées) + tracés, dans le style du carnet."""
import math, os, re, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import matplotlib.patheffects as pe
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
for f in os.listdir(os.path.join(ROOT, "assets", "fonts")):
    fm.fontManager.addfont(os.path.join(ROOT, "assets", "fonts", f))
SERIF, SANS, BODY = "DM Serif Display", "Lato", "Spectral"
NAVY, NAVY2, RED, GOLD, GREY, PAPER, INK = "#131f2d", "#2d3f56", "#8c2f38", "#b8914f", "#5e6572", "#f9f6f0", "#1f2430"
Image.MAX_IMAGE_PIXELS = None

# --- géoréférencement des tuiles --------------------------------------------
def tile_bounds(name):
    m = re.search(r"_(\d+)_(\d+)_(\d+)_(\d+)_(\d+)\.png$", name)
    z, x0, y0, x1, y1 = map(int, m.groups())
    n = 2 ** z
    def lon(x): return x / n * 360.0 - 180.0
    def lat(y): return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    return lon(x0), lon(x1 + 1), lat(y1 + 1), lat(y0)  # W, E, S, N

def merc_y(lat):
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))

class TileMap:
    """Carte sur une tuile : coordonnées en degrés, projection Web Mercator (comme la tuile)."""
    def __init__(self, tile, bbox=None, width_in=7.0, alpha=1.0, pale=True, sea=True):
        self.im = Image.open(os.path.join(IMG, tile)).convert("RGB")
        sea_fill = sea
        if pale:
            import numpy as np
            a = np.asarray(self.im).astype(float)
            sea = a.max(axis=2) < 18
            a = a * 0.42 + np.array([249, 246, 240]) * 0.58
            if sea_fill:
                a[sea] = np.array([223, 230, 236])
            self.im = Image.fromarray(a.clip(0, 255).astype("uint8"))
        W, E, S, N = tile_bounds(tile)
        if bbox:
            w, e, s, n = bbox
            px = self.im.width / (E - W)
            yN, yS = merc_y(N), merc_y(S)
            py = self.im.height / (yN - yS)
            box = (int((w - W) * px), int((yN - merc_y(n)) * py), int((e - W) * px), int((yN - merc_y(s)) * py))
            self.im = self.im.crop(box)
            W, E, S, N = w, e, s, n
        self.S, self.N = S, N
        self.W, self.E = math.radians(W), math.radians(E)
        self.yN, self.yS = merc_y(N), merc_y(S)
        aspect = (self.yN - self.yS) / (self.E - self.W)
        self.fig = plt.figure(figsize=(width_in, width_in * aspect), dpi=100, facecolor=PAPER)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.imshow(self.im, extent=(self.W, self.E, self.yS, self.yN), aspect="auto", alpha=alpha, zorder=0, interpolation="lanczos")
        self.ax.set_xlim(self.W, self.E); self.ax.set_ylim(self.yS, self.yN); self.ax.axis("off")
        self.halo = [pe.withStroke(linewidth=3, foreground="white", alpha=0.85)]

    def xy(self, lon, lat): return math.radians(lon), merc_y(lat)

    def line(self, pts, kind="car", z=5, label=None):
        sty = dict(car=dict(color=RED, lw=3.0, ls="-"), walk=dict(color=GOLD, lw=3.2, ls=(0, (4, 2))),
                   train=dict(color=NAVY2, lw=2.2, ls="-"), bus=dict(color=NAVY2, lw=2.0, ls=(0, (3, 2))),
                   road=dict(color="#9a8f82", lw=1.2, ls="-"))[kind]
        xs, ys = zip(*[self.xy(*p) for p in pts])
        self.ax.plot(xs, ys, color=sty["color"], lw=sty["lw"], ls=sty["ls"], zorder=z, solid_capstyle="round",
                     dash_capstyle="round", path_effects=[pe.Stroke(linewidth=sty["lw"] + 2.2, foreground="white", alpha=0.8), pe.Normal()])

    def place(self, lon, lat, name, kind="dot", dx=6, dy=0, ha="left", va="center", size=9, bold=False, italic=False, color=INK):
        x, y = self.xy(lon, lat)
        if kind == "night":
            self.ax.plot(x, y, marker="s", ms=9, mfc=RED, mec="white", mew=1.2, zorder=9)
        elif kind == "dot":
            self.ax.plot(x, y, marker="o", ms=5.5, mfc=NAVY, mec="white", mew=1.0, zorder=9)
        elif kind == "ring":
            self.ax.plot(x, y, marker="o", ms=7, mfc="white", mec=NAVY, mew=1.4, zorder=9)
        elif kind == "park":
            self.ax.plot(x, y, marker="s", ms=8, mfc="white", mec=NAVY2, mew=1.4, zorder=9)
            self.ax.text(x, y, "P", ha="center", va="center", fontsize=6, fontfamily=SANS, fontweight="bold", color=NAVY2, zorder=10)
        elif kind == "hike":
            self.ax.plot(x, y, marker="^", ms=9, mfc=GOLD, mec="white", mew=1.0, zorder=9)
        if name:
            self.ax.annotate(name, (x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va=va, fontsize=size,
                             fontfamily=SANS if not italic else BODY, fontweight="bold" if bold else "normal",
                             style="italic" if italic else "normal", color=color, zorder=11, path_effects=self.halo)

    def label(self, lon, lat, text, size=8.5, color=GREY, rot=0, italic=True, ha="center"):
        x, y = self.xy(lon, lat)
        self.ax.text(x, y, text, ha=ha, va="center", fontsize=size, fontfamily=BODY if italic else SANS, style="italic" if italic else "normal",
                     color=color, rotation=rot, zorder=11, path_effects=self.halo)

    def scale(self, km, corner="bl"):
        lat0 = (self.S + self.N) / 2
        dlon = math.radians(km / (111.32 * math.cos(math.radians(lat0))))
        pad = (self.E - self.W) * 0.04
        x0 = self.W + pad if "l" in corner else self.E - pad - dlon
        y = self.yS + (self.yN - self.yS) * (0.05 if "b" in corner else 0.95)
        self.ax.plot([x0, x0 + dlon], [y, y], color=NAVY, lw=2, zorder=12, solid_capstyle="butt")
        self.ax.text(x0 + dlon / 2, y + (self.yN - self.yS) * 0.012, f"{km} km", ha="center", va="bottom", fontsize=8, fontfamily=SANS, color=NAVY, zorder=12, path_effects=self.halo)

    def north(self):
        x = self.E - (self.E - self.W) * 0.05; y = self.yN - (self.yN - self.yS) * 0.05
        self.ax.annotate("N", (x, y), ha="center", va="top", fontsize=10, fontfamily=SANS, fontweight="bold", color=NAVY, zorder=12, path_effects=self.halo)
        self.ax.annotate("", (x, y + (self.yN - self.yS) * 0.03), (x, y - (self.yN - self.yS) * 0.02), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.5), zorder=12)

    def legend(self, items, corner="br"):
        """items : liste de (kind, texte)."""
        n = len(items)
        w = (self.E - self.W) * 0.30; h = (self.yN - self.yS) * (0.035 * n + 0.02)
        x0 = self.E - w - (self.E - self.W) * 0.03 if "r" in corner else self.W + (self.E - self.W) * 0.03
        y0 = self.yS + (self.yN - self.yS) * 0.03 if "b" in corner else self.yN - h - (self.yN - self.yS) * 0.03
        self.ax.add_patch(plt.Rectangle((x0, y0), w, h, facecolor="white", edgecolor="#ddd6cb", lw=0.8, alpha=0.92, zorder=12))
        for i, (kind, txt) in enumerate(items):
            y = y0 + h - (self.yN - self.yS) * (0.035 * (i + 0.5) + 0.01)
            xa, xb = x0 + w * 0.06, x0 + w * 0.22
            if kind in ("car", "walk", "train", "bus", "road"):
                sty = dict(car=(RED, 3, "-"), walk=(GOLD, 3.2, (0, (4, 2))), train=(NAVY2, 2.2, "-"), bus=(NAVY2, 2, (0, (3, 2))), road=("#9a8f82", 1.2, "-"))[kind]
                self.ax.plot([xa, xb], [y, y], color=sty[0], lw=sty[1], ls=sty[2], zorder=13, solid_capstyle="round", dash_capstyle="round")
            elif kind == "night":
                self.ax.plot((xa + xb) / 2, y, marker="s", ms=8, mfc=RED, mec="white", mew=1, zorder=13)
            elif kind == "park":
                self.ax.plot((xa + xb) / 2, y, marker="s", ms=8, mfc="white", mec=NAVY2, mew=1.3, zorder=13)
                self.ax.text((xa + xb) / 2, y, "P", ha="center", va="center", fontsize=6, fontfamily=SANS, fontweight="bold", color=NAVY2, zorder=14)
            elif kind == "hike":
                self.ax.plot((xa + xb) / 2, y, marker="^", ms=8, mfc=GOLD, mec="white", mew=1, zorder=13)
            self.ax.text(x0 + w * 0.28, y, txt, ha="left", va="center", fontsize=7.5, fontfamily=SANS, color=INK, zorder=13)

    def credit(self, txt="Relief : GSI Japon · tracés indicatifs"):
        self.ax.text(self.E - (self.E - self.W) * 0.01, self.yS + (self.yN - self.yS) * 0.008, txt, ha="right", va="bottom", fontsize=6, fontfamily=SANS, color=GREY, zorder=12, path_effects=self.halo)

    def save(self, name, dpi=200):
        out = os.path.join(IMG, name)
        self.fig.savefig(out, dpi=dpi, facecolor=PAPER)
        plt.close(self.fig)
        print(out)
        return out


# --- Kumano, en voiture -------------------------------------------------------
def kumano():
    m = TileMap("relief_kumano_12_3590_1636_3596_1642.png", bbox=(135.60, 136.08, 33.56, 33.95), width_in=7.2, alpha=0.92)
    R168 = [(135.99, 33.725), (135.96, 33.745), (135.93, 33.76), (135.90, 33.78), (135.86, 33.80), (135.82, 33.815), (135.785, 33.823), (135.775, 33.835), (135.772, 33.845), (135.76, 33.86), (135.75, 33.90), (135.745, 33.95)]
    R42 = [(136.08, 33.90), (136.04, 33.84), (136.01, 33.78), (135.99, 33.725), (135.975, 33.69), (135.95, 33.66), (135.94, 33.63), (135.92, 33.615), (135.89, 33.60), (135.86, 33.59), (135.80, 33.57), (135.70, 33.56)]
    nachi_rd = [(135.94, 33.63), (135.92, 33.645), (135.90, 33.66), (135.887, 33.666)]
    yuno_rd = [(135.772, 33.845), (135.765, 33.838), (135.758, 33.83)]
    kawayu_rd = [(135.785, 33.823), (135.78, 33.816), (135.775, 33.813)]
    for r in (R168, R42, nachi_rd, yuno_rd, kawayu_rd):
        m.line(r, "road", z=3)
    # 3 janv. : arrivée d'Ise par la 42 puis la 168
    m.line(R42[:4] + R168[:], "car", z=5)
    # 5 janv. : Yunomine → Shingū → Nachi → Katsuura (même 168/42) ; 6 janv. : vers Kōya par la 168 nord
    m.line([(135.99, 33.725), (135.975, 33.69), (135.95, 33.66), (135.94, 33.63)] + nachi_rd[1:], "car", z=5)
    m.line(yuno_rd, "car", z=5)
    # marche du 4 janv.
    m.line([(135.742, 33.857), (135.755, 33.852), (135.765, 33.848), (135.772, 33.845)], "walk", z=6)
    m.line([(135.772, 33.845), (135.768, 33.838), (135.762, 33.834), (135.758, 33.83)], "walk", z=6)
    m.line([(135.887, 33.666), (135.890, 33.669), (135.891, 33.672)], "walk", z=6)
    # lieux
    m.place(135.758, 33.830, "Yunomine Onsen", "night", dx=-8, ha="right", bold=True, size=10)
    m.place(135.775, 33.813, "Kawayu", "ring", dx=-7, ha="right")
    m.place(135.772, 33.845, "Hongū Taisha", "dot", dx=7, dy=4)
    m.place(135.770, 33.836, "Ōyunohara", "dot", dx=7, dy=-4, italic=True, size=8)
    m.place(135.742, 33.857, "Hosshinmon-ōji", "hike", dx=-7, dy=6, ha="right")
    m.place(135.785, 33.823, "Ukegawa, Kumano Iori", "ring", dx=7, dy=-3)
    m.place(135.99, 33.725, "Shingū, Hayatama Taisha", "dot", dx=7, dy=3)
    m.place(135.887, 33.666, "Daimon-zaka", "hike", dx=-7, dy=-7, ha="right")
    m.place(135.891, 33.674, "Nachi Taisha, cascade", "dot", dx=-7, dy=3, ha="right")
    m.place(135.945, 33.63, "Kii-Katsuura", "dot", dx=7, dy=4)
    m.place(135.951, 33.624, "Hotel Urashima", "night", dx=7, dy=-6, bold=True, size=10)
    m.place(136.08, 33.90, "", "dot")
    m.label(136.0, 33.93, "3 janv. : d'Ise par Owase\net la route 42, 3 h 30", size=8, color=RED, italic=False, ha="right")
    m.label(135.745, 33.94, "6 janv. : vers Kōya-san par\nTotsukawa et Gojō, 3 h 30", size=8, color=RED, italic=False, ha="left")
    m.label(135.87, 33.80, "Kumano-gawa", size=8, rot=-28)
    m.label(135.99, 33.60, "Océan Pacifique", size=9, color="#7f8c9a")
    m.scale(10, "br")
    m.north()
    m.legend([("night", "Nuit"), ("car", "Voiture"), ("walk", "Marche"), ("hike", "Départ de marche"), ("road", "Route")], "bl")
    m.credit()
    return m.save("map_kumano.png")


# --- Kōya-san, en voiture -----------------------------------------------------
def koya():
    m = TileMap("relief_koya_14_14360_6531_14365_6534.png", bbox=(135.552, 135.648, 34.193, 34.236), width_in=7.2, alpha=0.92, sea=False)
    main = [(135.555, 34.214), (135.567, 34.2135), (135.577, 34.213), (135.583, 34.213), (135.590, 34.2125), (135.600, 34.2125), (135.606, 34.213), (135.612, 34.214)]
    m.line(main, "road", z=3)
    m.line([(135.577, 34.213), (135.574, 34.205), (135.57, 34.197)], "road", z=3)
    m.line([(135.555, 34.214), (135.577, 34.213)], "car", z=5)
    m.line([(135.577, 34.213), (135.606, 34.213)], "car", z=5)
    m.line([(135.606, 34.213), (135.612, 34.2145), (135.618, 34.2165), (135.626, 34.2185)], "walk", z=6)
    m.line([(135.600, 34.2125), (135.606, 34.2142), (135.612, 34.2145)], "walk", z=6)
    m.place(135.577, 34.213, "Daimon", "dot", dx=-7, dy=6, ha="right")
    m.place(135.583, 34.2135, "Danjō Garan", "dot", dx=0, dy=9, ha="center")
    m.place(135.588, 34.2128, "Kongōbu-ji", "dot", dx=4, dy=-11, ha="left")
    m.place(135.583, 34.2113, "", "park")
    m.place(135.600, 34.2125, "Ichinohashi", "dot", dx=0, dy=9, ha="center")
    m.place(135.606, 34.2127, "", "park")
    m.place(135.606, 34.2105, "parking d'Okunoin-mae", "", dx=0, dy=-6, ha="center", italic=True, size=8)
    m.place(135.626, 34.2185, "Mausolée de Kūkai, Tōrō-dō", "dot", dx=7, dy=4)
    m.place(135.57, 34.197, "", "dot")
    m.label(135.561, 34.219, "route 480 depuis Kudoyama (arrivée),\npuis retour vers l'aéroport du Kansai", size=8, color=RED, italic=False, ha="left")
    m.label(135.573, 34.2015, "route 371 vers Ryūjin :\nfermée la nuit en hiver, à éviter", size=8, color=GREY, italic=False, ha="left")
    m.label(135.613, 34.2225, "Okunoin : 2 km d'allée sous les cèdres", size=8.5, color=GOLD, italic=False)
    m.scale(1, "bl")
    m.north()
    m.legend([("car", "Voiture"), ("walk", "Marche"), ("park", "Parking"), ("road", "Route")], "br")
    m.credit()
    return m.save("map_koya.png")


# --- Alpes japonaises : Tokyo → Matsumoto → Takayama → Shirakawa-gō → Nagoya → Ise -------------------
def alpes():
    m = TileMap("relief_ovA_8_221_99_227_103.png", bbox=(136.25, 140.25, 34.22, 36.95), width_in=7.2, alpha=0.95)
    azusa = [(139.767, 35.681), (139.700, 35.690), (139.34, 35.655), (138.94, 35.61), (138.57, 35.667), (138.31, 35.86), (138.16, 35.99), (137.95, 36.11), (137.97, 36.238)]
    bus1 = [(137.97, 36.238), (137.80, 36.19), (137.63, 36.21), (137.56, 36.19), (137.40, 36.17), (137.252, 36.142)]
    bus2 = [(137.252, 36.142), (137.12, 36.15), (136.99, 36.10), (136.93, 36.19), (136.906, 36.258)]
    hida = [(137.252, 36.142), (137.20, 36.07), (137.22, 36.0), (137.24, 35.80), (137.16, 35.67), (137.02, 35.44), (136.76, 35.41), (136.88, 35.17)]
    kintetsu = [(136.88, 35.17), (136.68, 35.06), (136.62, 34.97), (136.51, 34.73), (136.53, 34.58), (136.71, 34.49)]
    m.line(azusa, "train"); m.line(hida, "train"); m.line(kintetsu, "train")
    m.line(bus1, "bus"); m.line(bus2, "bus")
    m.place(139.767, 35.681, "Tokyo", "night", dx=7, dy=-4, bold=True, size=10)
    m.place(139.700, 35.690, "Shinjuku", "dot", dx=-6, dy=7, ha="right", size=8)
    m.place(138.57, 35.667, "Kōfu", "dot", dx=0, dy=-10, ha="center", size=8)
    m.place(137.97, 36.238, "Matsumoto", "night", dx=8, dy=4, bold=True, size=10)
    m.place(137.56, 36.19, "Hirayu Onsen", "dot", dx=0, dy=9, ha="center", size=8)
    m.place(137.252, 36.142, "Takayama", "night", dx=-8, dy=-6, ha="right", bold=True, size=10)
    m.place(136.906, 36.258, "Shirakawa-gō", "ring", dx=-8, dy=0, ha="right", bold=True)
    m.place(137.24, 35.80, "Gero", "dot", dx=7, dy=0, size=8)
    m.place(136.88, 35.17, "Nagoya", "dot", dx=8, dy=0, bold=True)
    m.place(136.71, 34.49, "Ise", "night", dx=8, dy=0, bold=True, size=10)
    m.place(138.73, 35.36, "", "hike")
    m.label(138.73, 35.30, "Mont Fuji, 3 776 m", size=8)
    m.label(137.55, 36.45, "ALPES JAPONAISES", size=9, color=GREY, italic=False)
    m.label(138.9, 35.85, "30 déc. : Azusa, 2 h 30", size=8, color=NAVY2, italic=False)
    m.label(137.6, 36.30, "31 déc. : car, 2 h 30", size=8, color=NAVY2, italic=False)
    m.label(136.75, 36.0, "1er janv. : car Nohi,\n50 min chaque sens", size=8, color=NAVY2, italic=False)
    m.label(137.55, 35.55, "2 janv. : Hida, 2 h 30", size=8, color=NAVY2, italic=False, rot=0)
    m.label(136.95, 34.82, "2 janv. : Kintetsu, 1 h 20", size=8, color=NAVY2, italic=False, ha="left")
    m.label(139.6, 35.0, "Océan Pacifique", size=9, color="#7f8c9a")
    m.label(137.2, 36.85, "Mer du Japon", size=9, color="#7f8c9a")
    m.scale(50, "tl")
    m.north()
    m.legend([("night", "Nuit"), ("train", "Train"), ("bus", "Car")], "br")
    m.credit()
    return m.save("map_alpes.png")


if __name__ == "__main__":
    kumano(); koya(); alpes()

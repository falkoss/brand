#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Generates the falkOSS brand kit: master SVGs, PNG exports, and the head assets of falkoss.org (web/) and
labs.falkoss.org (web-labs/) – the websites copy them into their assets/.

The mark: a falcon seen from below, all straight edges, over the lake as two flat waveforms (Falkensee – Falcon
Lake) – amber like an amber-phosphor terminal on near-black. The wordmark is drawn from angular, chamfered strokes
(no font needed): "falk" in light, "OSS" in amber.

Needs rsvg-convert (Homebrew: librsvg). Run from anywhere:
    python3 generate.py
Edit this file, not the exports.
"""
import os, shutil, struct, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SVG, PNG = os.path.join(HERE, "svg"), os.path.join(HERE, "png")
SITE = os.path.join(HERE, "web")          # → falkoss/website/assets/
LABS = os.path.join(HERE, "web-labs")     # → falkoss-labs/website/assets/

NIGHT = "#0B0D10"        # near-black – backgrounds
FALCON = "#FFB000"       # amber, like an amber-phosphor terminal – the falcon, OSS, accents
LAKE = "#5B7083"         # steel – the lake, lines, secondary
MIST = "#E6EDF3"         # light text on dark
INK = "#0B0D10"          # text on light
REED = "#7D8590"         # muted text
FALCON_DARK = "#B87800"  # amber on light backgrounds
LAKE_DARK = "#4A5D70"    # steel on light backgrounds


def svg(view_box, body, size=None):
    dims = f' width="{size[0]}" height="{size[1]}"' if size else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}"{dims}>\n{body}\n</svg>\n'


# --- mark ------------------------------------------------------------------------------------------------------------

def falcon(color):
    """Falcon from below in a 1024 box, all straight edges: wings bent at the wrist and swept back to a point,
    a faceted body and a squared tail – an insignia, not an illustration."""
    def wing(sign):
        pts = [(506, 380), (340, 344), (270, 382), (104, 540), (292, 482), (506, 492)]
        return "M" + " L".join(f"{a if sign < 0 else 1024 - a},{b}" for a, b in pts) + " Z"
    body = "M512,292 L548,322 L546,410 L532,566 L492,566 L478,410 L476,322 Z"
    tail = "M492,552 L532,552 L566,690 L512,712 L458,690 Z"
    return (f'<g fill="{color}"><path d="{wing(-1)}"/><path d="{wing(1)}"/><path d="{body}"/>'
            f'<path d="{tail}"/></g>')


def lake(color, width=28):
    """The lake as two flat waveforms (straight segments)."""
    w = ('<polyline points="200,806 328,806 376,778 472,834 568,778 664,834 712,806 824,806"/>'
         '<polyline points="312,902 712,902"/>')
    return f'<g fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="square" stroke-linejoin="miter">{w}</g>'


def mark(bird=FALCON, water=LAKE):
    return falcon(bird) + lake(water)


def icon(bg=NIGHT, rounded=True):
    """App/avatar icon: the mark on night, rounded square (macOS-like radius) or full bleed."""
    r = 160 if rounded else 0
    return svg("0 0 1024 1024", f'<rect width="1024" height="1024" rx="{r}" fill="{bg}"/>'
               f'<g transform="translate(512 540) scale(0.86) translate(-512 -600)">{mark()}</g>')


def small_icon(bg=NIGHT):
    """16–48 px: the falcon a little larger, one heavy line for the lake."""
    return svg("0 0 1024 1024", f'<rect width="1024" height="1024" rx="160" fill="{bg}"/>'
               f'<g transform="translate(512 500) scale(1.02) translate(-512 -560)">{falcon(FALCON)}'
               f'<line x1="232" y1="830" x2="792" y2="830" stroke="{LAKE}" stroke-width="70"/></g>')


# --- wordmark (strokes on a 100-unit cap height, baseline y=100) -----------------------------------------------------

GLYPHS = {
    # (advance width, path) – angular, chamfered terminal letters; x-height 40..100, ascender 8, caps 12..100
    "f": (40, "M14,100 V24 L28,10 H38 M2,44 H32"),
    "a": (56, "M48,44 V100 M48,58 L36,44 H16 L6,54 V90 L16,100 H36 L48,88"),
    "b": (56, "M8,8 V100 M8,58 L20,44 H40 L50,54 V90 L40,100 H20 L8,88"),
    "l": (22, "M10,8 V100"),
    "k": (52, "M10,8 V100 M46,44 L10,78 M26,64 L48,100"),
    "O": (80, "M20,12 H60 L74,26 V86 L60,100 H20 L6,86 V26 Z"),
    "S": (64, "M58,12 H18 L6,24 V44 L18,56 H46 L58,68 V88 L46,100 H4"),
    "s": (52, "M48,44 H14 L4,54 V64 L14,72 H38 L48,80 V90 L38,100 H2"),
}


def wordmark_body(light=MIST, accent=FALCON, stroke=13, text="falkOSS"):
    x, parts = 0, []
    for ch in text:
        if ch == " ":
            x += 30
            continue
        adv, d = GLYPHS[ch]
        color = accent if ch.isupper() else light
        parts.append(f'<path d="{d}" transform="translate({x} 0)" stroke="{color}"/>')
        x += adv + 6
    width = x - 6
    body = (f'<g fill="none" stroke-width="{stroke}" stroke-linecap="square" stroke-linejoin="miter">'
            + "".join(parts) + "</g>")
    return body, width


def wordmark(light=MIST, accent=FALCON):
    body, width = wordmark_body(light, accent)
    return svg(f"-8 0 {width + 16} 112", body)


def lockup(light=MIST, accent=FALCON, bg=None, bird=FALCON, water=LAKE):
    """Mark left, wordmark right – headers, documents."""
    body, width = wordmark_body(light, accent)
    w = 150 + width * 1.0 + 24
    back = f'<rect x="-24" y="-24" width="{w + 48}" height="208" rx="24" fill="{bg}"/>' if bg else ""
    return svg(f"-24 -24 {w + 48} 208", back
               + f'<g transform="translate(-30 -40) scale(0.2)">{mark(bird, water)}</g>'
               + f'<g transform="translate(184 26) scale(1.0)">{body}</g>')


# --- labs: falkoss-labs, the home for small projects – same falcon, "labs" in steel where the lake was --------------

def labs_icon(bg=NIGHT, rounded=False):
    """Avatar for the falkoss-labs organisation: the falcon, and "labs" drawn in steel in place of the lake."""
    r = 160 if rounded else 0
    body, width = wordmark_body(LAKE, LAKE, text="labs")
    k = 2.0
    return svg("0 0 1024 1024", f'<rect width="1024" height="1024" rx="{r}" fill="{bg}"/>'
               f'<g transform="translate(512 430) scale(0.78) translate(-512 -500)">{falcon(FALCON)}</g>'
               f'<g transform="translate({512 - width * k / 2} 632) scale({k})">{body}</g>')


def labs_lockup(light=MIST, accent=FALCON, labs=LAKE, bird=FALCON, water=LAKE):
    """falkOSS lockup with "labs" after the wordmark, in steel."""
    body, width = wordmark_body(light, accent)
    tag, tag_w = wordmark_body(labs, labs, text="labs")
    w = 150 + width + 36 + tag_w + 24
    return svg(f"-24 -24 {w + 48} 208",
               f'<g transform="translate(-30 -40) scale(0.2)">{mark(bird, water)}</g>'
               f'<g transform="translate(184 26)">{body}</g>'
               f'<g transform="translate({184 + width + 36} 26)">{tag}</g>')


def labs_social():
    """1280×640 link preview for labs.falkoss.org."""
    body, width = wordmark_body()
    tag, _ = wordmark_body(LAKE, LAKE, text="labs")
    mono = 'font-family="SF Mono, Menlo, Consolas, monospace"'
    grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="640" stroke="#151A20"/>' for x in range(0, 1281, 64)) + \
           "".join(f'<line x1="0" y1="{y}" x2="1280" y2="{y}" stroke="#151A20"/>' for y in range(0, 641, 64))
    return svg("0 0 1280 640", f'<rect width="1280" height="640" fill="{NIGHT}"/>{grid}'
               f'<g transform="translate(96 96) scale(0.44)">{mark()}</g>'
               f'<text x="560" y="196" {mono} font-size="26" fill="{REED}">$ ls ~/labs</text>'
               f'<g transform="translate(560 226) scale(1.0)">{body}</g>'
               f'<g transform="translate({560 + width + 30} 226) scale(1.0)">{tag}</g>'
               f'<text x="562" y="400" {mono} font-size="28" fill="{MIST}">plugins · tools · forks · experiments</text>'
               f'<text x="562" y="446" {mono} font-size="24" fill="{REED}">// small free software from Falkensee</text>'
               f'<rect x="562" y="472" width="16" height="30" fill="{FALCON}"/>')


def social():
    """1280×640: GitHub social preview, link previews – terminal style."""
    body, width = wordmark_body()
    mono = 'font-family="SF Mono, Menlo, Consolas, monospace"'
    grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="640" stroke="#151A20"/>' for x in range(0, 1281, 64)) + \
           "".join(f'<line x1="0" y1="{y}" x2="1280" y2="{y}" stroke="#151A20"/>' for y in range(0, 641, 64))
    return svg("0 0 1280 640", f'<rect width="1280" height="640" fill="{NIGHT}"/>{grid}'
               f'<g transform="translate(96 96) scale(0.44)">{mark()}</g>'
               f'<text x="560" y="196" {mono} font-size="26" fill="{REED}">$ whoami</text>'
               f'<g transform="translate(560 226) scale(1.3)">{body}</g>'
               f'<text x="562" y="420" {mono} font-size="28" fill="{MIST}">Falcon Lake Open Source Software</text>'
               f'<text x="562" y="466" {mono} font-size="24" fill="{REED}">// free software from Falkensee</text>'
               f'<rect x="562" y="492" width="16" height="30" fill="{FALCON}"/>')


# --- wallpapers ------------------------------------------------------------------------------------------------------

MONO = 'font-family="SF Mono, Menlo, Consolas, monospace"'
WALLPAPER_SIZES = {
    "5120x2880": (5120, 2880),   # desktop 16:9 – 5K, scales down to 4K, 1440p, 1080p
    "3456x2234": (3456, 2234),   # desktop 16:10 – MacBook Pro 16"
    "1320x2868": (1320, 2868),   # mobile – iPhone Pro Max, crops well to other phones
}
MARK_BOX = (104, 292, 920, 916)     # falcon + lake in the 1024 box
FALCON_BOX = (104, 292, 920, 712)   # falcon alone


def place(content, box, cx, cy, width):
    """Put content whose bounding box is `box` centred on (cx, cy), `width` wide."""
    x0, y0, x1, y1 = box
    k = width / (x1 - x0)
    return (f'<g transform="translate({cx - k * (x0 + x1) / 2:.1f} {cy - k * (y0 + y1) / 2:.1f}) '
            f'scale({k:.4f})">{content}</g>')


def grid(w, h, step, sw):
    """The faint terminal grid of the social preview, centred on the canvas."""
    ox, oy = (w / 2) % step, (h / 2) % step
    xs = "".join(f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{h}"/>' for x in frange(ox, w, step))
    ys = "".join(f'<line x1="0" y1="{y:.1f}" x2="{w}" y2="{y:.1f}"/>' for y in frange(oy, h, step))
    return f'<g stroke="#151A20" stroke-width="{sw:.1f}">{xs}{ys}</g>'


def frange(start, stop, step):
    while start <= stop:
        yield start
        start += step


def wallpaper_minimal(w, h):
    """Quiet: the mark, small, on night – nothing else."""
    portrait = h > w
    width = (0.30 * w) if portrait else (0.15 * h)
    cy = 0.60 * h if portrait else 0.5 * h   # phones: below the clock
    return svg(f"0 0 {w} {h}", f'<rect width="{w}" height="{h}" fill="{NIGHT}"/>'
               + place(mark(), MARK_BOX, w / 2, cy, width))


def wallpaper_official(w, h):
    """The official look: grid, lockup (stacked on phones), the claim, the address."""
    s = min(w, h)
    body, ww = wordmark_body()
    out = f'<rect width="{w}" height="{h}" fill="{NIGHT}"/>' + grid(w, h, s / 18, max(1, s / 1440))
    if h > w:
        fs = 0.034 * w
        out += place(mark(), MARK_BOX, w / 2, 0.50 * h, 0.40 * w)
        out += place(body, (-7, 0, ww + 7, 107), w / 2, 0.635 * h, 0.62 * w)
        out += (f'<text x="{w / 2}" y="{0.70 * h:.0f}" {MONO} font-size="{fs:.0f}" fill="{MIST}" '
                f'text-anchor="middle">Falcon Lake Open Source Software</text>'
                f'<text x="{w / 2}" y="{0.70 * h + 1.6 * fs:.0f}" {MONO} font-size="{fs:.0f}" fill="{REED}" '
                f'text-anchor="middle">// from Falkensee</text>'
                f'<text x="{w / 2}" y="{0.93 * h:.0f}" {MONO} font-size="{0.8 * fs:.0f}" fill="{REED}" '
                f'text-anchor="middle">falkoss.org</text>')
    else:
        fs = 0.022 * h
        lock = (f'<g transform="translate(-30 -40) scale(0.2)">{mark()}</g>'
                f'<g transform="translate(184 26)">{body}</g>')
        out += place(lock, (-10, 18, 184 + ww + 7, 143), w / 2, 0.46 * h, 0.40 * w)
        out += (f'<text x="{w / 2}" y="{0.46 * h + 0.13 * h:.0f}" {MONO} font-size="{fs:.0f}" fill="{MIST}" '
                f'text-anchor="middle">Falcon Lake Open Source Software '
                f'<tspan fill="{REED}">– from Falkensee</tspan></text>'
                f'<text x="{w / 2}" y="{0.94 * h:.0f}" {MONO} font-size="{0.7 * fs:.0f}" fill="{REED}" '
                f'text-anchor="middle">falkoss.org</text>')
    return svg(f"0 0 {w} {h}", out)


TERMINAL = [
    ("$", "whoami"),
    ("", "falk{OSS}"),
    ("$", "expand falkOSS"),
    ("", "{FA}lcon {L}a{K}e → {FALK}ensee + {OSS}"),
    ("$", 'initials "Falcon Lake Open Source Software"'),
    ("", "{FLOSS}"),
    ("$", "cat /etc/motd"),
    ("#", "free software"),
    ("#", "no telemetry"),
    ("#", "everything included"),
    ("$", ""),
]


def terminal_lines(x, y, fs):
    """A short shell session; {…} is amber, the last prompt gets a block cursor."""
    out, lh = [], 1.55 * fs
    for i, (kind, text) in enumerate(TERMINAL):
        ty = y + i * lh
        if kind == "$":
            spans = f'<tspan fill="{REED}">$ </tspan>{text}'
            if not text:
                out.append(f'<rect x="{x + 2 * 0.602 * fs:.1f}" y="{ty - 0.82 * fs:.1f}" width="{0.6 * fs:.1f}" '
                           f'height="{1.0 * fs:.1f}" fill="{FALCON}"/>')
            color = MIST
        else:
            spans = text.replace("{", f'<tspan fill="{FALCON}">').replace("}", "</tspan>")
            color = REED if kind == "#" else MIST
        out.append(f'<text x="{x:.1f}" y="{ty:.1f}" {MONO} font-size="{fs:.1f}" fill="{color}" '
                   f'xml:space="preserve">{spans}</text>')
    return "".join(out)


def horizon(w, y0, u, rows=4):
    """The lake's waveform drawn out to a horizon: rows of flat lines with the lake's pulse at irregular places,
    receding into the night; a straight line closes it like the line under the lake in the mark."""
    import random
    rnd = random.Random(1923)
    colors = [LAKE, "#3A4A59", "#29343F", "#1D252D"]
    out = []
    for r in range(rows):
        y, a = y0 + r * 120 * u, 28 * u * (1 - 0.18 * r)
        x, pts = -rnd.uniform(0, 600) * u, []
        while x < w + 800 * u:
            pts.append((x, y))
            x += rnd.choice((128, 256, 384, 640, 896)) * u
            seg = [(0, 0), (48, -a / u), (144, a / u), (240, -a / u), (336, a / u), (384, 0)]
            pts += [(x + dx * u, y + dy * u) for dx, dy in seg]
            x += 384 * u
        p = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
        out.append(f'<polyline points="{p}" stroke="{colors[r]}" stroke-width="{28 * u * (1 - 0.15 * r):.1f}"/>')
    yl = y0 + rows * 120 * u
    out.append(f'<line x1="0" y1="{yl:.1f}" x2="{w}" y2="{yl:.1f}" stroke="{colors[-1]}" stroke-width="{20 * u:.1f}"/>')
    return (f'<g fill="none" stroke-linecap="square" stroke-linejoin="miter">' + "".join(out) + "</g>")


def wallpaper_terminal(w, h):
    """Playful: a shell session that spells the name out, a big falcon, the lake stretched to a horizon."""
    out = f'<rect width="{w}" height="{h}" fill="{NIGHT}"/>' + grid(w, h, min(w, h) / 18, max(1, min(w, h) / 1440))
    if h > w:
        fw = 0.70 * w
        out += horizon(w, 0.50 * h, fw / 816 * 0.55)
        out += place(falcon(FALCON), FALCON_BOX, w / 2, 0.36 * h, fw)
        out += terminal_lines(0.08 * w, 0.66 * h, 0.032 * w)
    else:
        fw = 0.34 * w
        out += horizon(w, 0.72 * h, fw / 816 * 0.55)
        out += place(falcon(FALCON), FALCON_BOX, 0.68 * w, 0.40 * h, fw)
        out += terminal_lines(0.08 * w, 0.20 * h, 0.024 * h)
    return svg(f"0 0 {w} {h}", out)


def wallpaper_blackout(w, h):
    """For dark-mode purists: true black (OLED off), the mark small in greys in the top-left corner."""
    portrait = h > w
    width = 0.14 * w if portrait else 0.05 * w
    k = width / (MARK_BOX[2] - MARK_BOX[0])
    margin = 0.07 * w if portrait else 0.035 * w
    top = 0.075 * h if portrait else 0.05 * h   # below the status bar / menu bar
    cx = margin + width / 2
    cy = top + k * (MARK_BOX[3] - MARK_BOX[1]) / 2
    return svg(f"0 0 {w} {h}", f'<rect width="{w}" height="{h}" fill="#000000"/>'
               + place(mark("#6B7178", "#3A3F45"), MARK_BOX, cx, cy, width))


FALCON_POLYS = (
    [(506, 380), (340, 344), (270, 382), (104, 540), (292, 482), (506, 492)],
    [(1024 - 506, 380), (1024 - 340, 344), (1024 - 270, 382), (1024 - 104, 540), (1024 - 292, 482), (1024 - 506, 492)],
    [(512, 292), (548, 322), (546, 410), (532, 566), (492, 566), (478, 410), (476, 322)],
    [(492, 552), (532, 552), (566, 690), (512, 712), (458, 690)],
)
GREY_BIRD, GREY_LAKE = "#A6ABB0", "#4A4F55"
GREY_STEPS = ["#3A3D41", "#2E3134", "#25272A", "#1D1F21", "#17181A", "#121314"]   # receding, stepped


def lake_ripples(cx=512, cy=902, flat=0.24):
    """Ripples spreading from the lake, below it only: the lower halves of flattened octagons (water seen at an
    angle), fading out in steps of grey into the black."""
    import math
    out, r, gap = [], 340, 60
    for i in range(len(GREY_STEPS)):
        R = r / math.cos(math.pi / 8)
        pts = [(cx + R * math.cos(math.pi / 8 + k * math.pi / 4), cy + flat * R * math.sin(math.pi / 8 + k * math.pi / 4))
               for k in range(4)]
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        out.append(f'<polyline points="{p}" stroke="{GREY_STEPS[i]}"/>')
        r += gap
        gap *= 1.25
    return f'<g fill="none" stroke-width="7" stroke-linejoin="miter">{"".join(out)}</g>'


def rotate(pts, pivot, deg):
    import math
    a = math.radians(deg)
    px, py = pivot
    return [(px + (x - px) * math.cos(a) - (y - py) * math.sin(a),
             py + (x - px) * math.sin(a) + (y - py) * math.cos(a)) for x, y in pts]


def wallpaper_wingbeat(w, h):
    """Black and greys: the mark very large in the middle, its wings echoed as outlines through one upstroke –
    a stroboscopic photo of a wingbeat, each echo a step darker."""
    portrait = h > w
    width = 0.66 * w if portrait else 0.36 * w
    left, right = FALCON_POLYS[0], FALCON_POLYS[1]
    echoes = []
    for i, deg in enumerate((10, 20, 30, 40, 50)):
        color = GREY_STEPS[i]
        for poly, sign, pivot in ((left, 1, (506, 436)), (right, -1, (518, 436))):
            pts = rotate(poly, pivot, sign * deg)
            p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
            echoes.append(f'<polygon points="{p}" stroke="{color}"/>')
    body = (lake_ripples()
            + f'<g fill="none" stroke-width="7" stroke-linejoin="miter">{"".join(reversed(echoes))}</g>'
            + mark(GREY_BIRD, GREY_LAKE))
    box = (40, 40, 984, 916)   # the raised wings reach well above the mark
    return svg(f"0 0 {w} {h}", f'<rect width="{w}" height="{h}" fill="#000000"/>'
               + place(body, box, w / 2, 0.50 * h, width * (box[2] - box[0]) / (MARK_BOX[2] - MARK_BOX[0])))


WALLPAPERS = {"minimal": wallpaper_minimal, "official": wallpaper_official, "terminal": wallpaper_terminal,
              "blackout": wallpaper_blackout, "wingbeat": wallpaper_wingbeat}


def favicon_svg():
    """Transparent mark for browsers; follows light/dark mode."""
    style = (f'<style>.b{{fill:{FALCON}}}.w{{stroke:{LAKE}}}'
             f'@media (prefers-color-scheme: light){{.b{{fill:{FALCON_DARK}}}.w{{stroke:{LAKE_DARK}}}}}</style>')
    return svg("120 260 784 680", style
               + falcon(FALCON).replace(f'fill="{FALCON}"', 'class="b"')
               + f'<line class="w" x1="232" y1="830" x2="792" y2="830" stroke-width="70"/>')


# --- output ----------------------------------------------------------------------------------------------------------

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def render(src, dst, w, h=None):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    args = ["rsvg-convert", "-w", str(w)] + (["-h", str(h)] if h else []) + ["-o", dst, src]
    subprocess.run(args, check=True)


def ico(dst, pngs):
    """favicon.ico with PNG entries (16, 32, 48)."""
    data = [open(p, "rb").read() for p in pngs]
    sizes = [16, 32, 48]
    out = struct.pack("<HHH", 0, 1, len(data))
    offset = 6 + 16 * len(data)
    for s, d in zip(sizes, data):
        out += struct.pack("<BBBBHHII", s, s, 0, 0, 1, 32, len(d), offset)
        offset += len(d)
    with open(dst, "wb") as f:
        f.write(out + b"".join(data))


def main():
    for d in (SVG, PNG):
        if os.path.isdir(d):
            shutil.rmtree(d)   # generated output only
    files = {
        "falkoss-icon.svg": icon(),
        "falkoss-icon-square.svg": icon(rounded=False),
        "falkoss-icon-small.svg": small_icon(),
        "falkoss-mark-on-dark.svg": svg("120 260 784 680", mark()),
        "falkoss-mark-on-light.svg": svg("120 260 784 680", mark(FALCON_DARK, LAKE_DARK)),
        "falkoss-mark-black.svg": svg("120 260 784 680", mark("#000000", "#000000")),
        "falkoss-mark-white.svg": svg("120 260 784 680", mark("#FFFFFF", "#FFFFFF")),
        "falkoss-wordmark-on-dark.svg": wordmark(),
        "falkoss-wordmark-on-light.svg": wordmark(INK, FALCON_DARK),
        "falkoss-lockup-on-dark.svg": lockup(),
        "falkoss-lockup-on-light.svg": lockup(INK, FALCON_DARK, bird=FALCON_DARK, water=LAKE_DARK),
        "falkoss-social-1280x640.svg": social(),
        "favicon.svg": favicon_svg(),
        "falkoss-labs-icon.svg": labs_icon(rounded=True),
        "falkoss-labs-icon-square.svg": labs_icon(),
        "falkoss-labs-lockup-on-dark.svg": labs_lockup(),
        "falkoss-labs-social-1280x640.svg": labs_social(),
        "falkoss-labs-mark.svg": labs_icon(bg="none").replace('viewBox="0 0 1024 1024"', 'viewBox="140 250 744 600"'),
        "falkoss-labs-lockup-on-light.svg": labs_lockup(INK, FALCON_DARK, LAKE_DARK, FALCON_DARK, LAKE_DARK),
    }
    for name, content in files.items():
        write(os.path.join(SVG, name), content)
    s = lambda n: os.path.join(SVG, n)
    for size in (64, 128, 256, 512, 1024):
        render(s("falkoss-icon.svg"), os.path.join(PNG, "icon", f"falkoss-icon-{size}.png"), size)
        render(s("falkoss-icon-square.svg"), os.path.join(PNG, "icon-square", f"falkoss-icon-square-{size}.png"), size)
    for size in (16, 32, 48):
        render(s("falkoss-icon-small.svg"), os.path.join(PNG, "icon-small", f"falkoss-icon-small-{size}.png"), size)
    for size in (256, 512, 1024):
        for v in ("on-dark", "on-light", "black", "white"):
            render(s(f"falkoss-mark-{v}.svg"), os.path.join(PNG, "mark", f"falkoss-mark-{v}-{size}.png"), size)
    for v in ("on-dark", "on-light"):
        render(s(f"falkoss-wordmark-{v}.svg"), os.path.join(PNG, "wordmark", f"falkoss-wordmark-{v}-1200.png"), 1200)
        render(s(f"falkoss-lockup-{v}.svg"), os.path.join(PNG, "lockup", f"falkoss-lockup-{v}-1200.png"), 1200)
    render(s("falkoss-icon-square.svg"), os.path.join(PNG, "social", "github-avatar-500.png"), 500)
    render(s("falkoss-social-1280x640.svg"), os.path.join(PNG, "social", "falkoss-social-1280x640.png"), 1280, 640)
    render(s("falkoss-labs-icon-square.svg"), os.path.join(PNG, "social", "github-avatar-labs-500.png"), 500)
    for size in (256, 512, 1024):
        render(s("falkoss-labs-icon.svg"), os.path.join(PNG, "labs", f"falkoss-labs-icon-{size}.png"), size)
    render(s("falkoss-labs-social-1280x640.svg"), os.path.join(PNG, "labs", "falkoss-labs-social-1280x640.png"), 1280, 640)
    for v in ("on-dark", "on-light"):
        render(s(f"falkoss-labs-lockup-{v}.svg"), os.path.join(PNG, "labs", f"falkoss-labs-lockup-{v}-1200.png"), 1200)
    for style, make in WALLPAPERS.items():
        for size, (w, h) in WALLPAPER_SIZES.items():
            name = f"falkoss-wallpaper-{style}-{size}"
            write(os.path.join(SVG, "wallpaper", name + ".svg"), make(w, h))
            render(os.path.join(SVG, "wallpaper", name + ".svg"), os.path.join(PNG, "wallpaper", name + ".png"), w, h)

    # Website head assets
    os.makedirs(SITE, exist_ok=True)
    shutil.copy(s("favicon.svg"), os.path.join(SITE, "favicon.svg"))
    shutil.copy(s("falkoss-lockup-on-dark.svg"), os.path.join(SITE, "falkoss-lockup-on-dark.svg"))
    shutil.copy(s("falkoss-mark-on-dark.svg"), os.path.join(SITE, "falkoss-mark.svg"))
    render(s("falkoss-icon-square.svg"), os.path.join(SITE, "apple-touch-icon.png"), 180)
    render(s("falkoss-icon.svg"), os.path.join(SITE, "icon-192.png"), 192)
    render(s("falkoss-icon.svg"), os.path.join(SITE, "icon-512.png"), 512)
    shutil.copy(os.path.join(PNG, "social", "falkoss-social-1280x640.png"), os.path.join(SITE, "social.png"))
    os.makedirs(os.path.join(SITE, "projects"), exist_ok=True)
    shutil.copy(os.path.join(PNG, "labs", "falkoss-labs-icon-256.png"), os.path.join(SITE, "projects", "falkoss-labs.png"))
    ico(os.path.join(SITE, "favicon.ico"),
        [os.path.join(PNG, "icon-small", f"falkoss-icon-small-{n}.png") for n in (16, 32, 48)])
    write(os.path.join(SITE, "site.webmanifest"),
          '{\n  "name": "falkOSS",\n  "short_name": "falkOSS",\n  "icons": [\n'
          '    {"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"},\n'
          '    {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}\n  ],\n'
          f'  "theme_color": "{NIGHT}",\n  "background_color": "{NIGHT}",\n  "display": "standalone"\n}}\n')

    # The head assets of labs.falkoss.org: the same favicon, the labs icon, lockup, mark and social preview
    os.makedirs(LABS, exist_ok=True)
    shutil.copy(s("favicon.svg"), os.path.join(LABS, "favicon.svg"))
    shutil.copy(os.path.join(SITE, "favicon.ico"), os.path.join(LABS, "favicon.ico"))
    shutil.copy(s("falkoss-labs-lockup-on-dark.svg"), os.path.join(LABS, "falkoss-labs-lockup-on-dark.svg"))
    shutil.copy(s("falkoss-labs-mark.svg"), os.path.join(LABS, "falkoss-labs-mark.svg"))
    render(s("falkoss-labs-icon-square.svg"), os.path.join(LABS, "apple-touch-icon.png"), 180)
    render(s("falkoss-labs-icon.svg"), os.path.join(LABS, "icon-192.png"), 192)
    render(s("falkoss-labs-icon.svg"), os.path.join(LABS, "icon-512.png"), 512)
    shutil.copy(os.path.join(PNG, "labs", "falkoss-labs-social-1280x640.png"), os.path.join(LABS, "social.png"))
    write(os.path.join(LABS, "site.webmanifest"),
          '{\n  "name": "falkOSS labs",\n  "short_name": "falkOSS labs",\n  "icons": [\n'
          '    {"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"},\n'
          '    {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}\n  ],\n'
          f'  "theme_color": "{NIGHT}",\n  "background_color": "{NIGHT}",\n  "display": "standalone"\n}}\n')
    print("brand kit written to", HERE)


if __name__ == "__main__":
    main()

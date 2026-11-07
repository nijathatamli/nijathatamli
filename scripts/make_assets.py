#!/usr/bin/env python3
"""Generates the static animated SVGs used by the profile README (header, divider, footer)."""
import pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"

# ---------------------------------------------------------------- header
W, H = 1200, 340
LINES = [
    "Software & Systems Engineer",
    "Cybersecurity  ·  Full-Stack  ·  AI",
    "5x Hackathon Winner  ·  ICPC  ·  CTF",
]
CYCLE, SLOT = 12.0, 4.0
FS = 28                    # font size of the typed line
CW = FS * 0.6              # monospace advance (we force it with textLength)
X0, Y0 = 600, 224          # centred later per line

def keytimes(i, w):
    t0 = i * SLOT / CYCLE
    pts = [(0, 0.0), (t0, 0.0), (t0 + 1.5 / CYCLE, w), (t0 + 3.4 / CYCLE, w), (t0 + SLOT / CYCLE, 0.0), (1.0, 0.0)]
    out = []
    for t, v in pts:
        if out and t <= out[-1][0] + 1e-9:
            if t == out[-1][0]: out[-1] = (t, v)   # same instant: later value wins
            continue
        out.append((t, v))
    if out[-1][0] < 1.0: out.append((1.0, 0.0))
    return out

typed = []
for i, line in enumerate(LINES):
    w = round(len(line) * CW, 1)
    x = round((W - w) / 2, 1)
    kt = keytimes(i, w)
    ktimes = ";".join(f"{t:.4f}" for t, _ in kt)
    clipw = ";".join(f"{v}" for _, v in kt)
    curx = ";".join(f"{round(x + v, 1)}" for _, v in kt)
    a, b = i * SLOT / CYCLE, (i * SLOT + 3.6) / CYCLE
    pts = sorted(set([0.0, round(a, 4), round(b, 4)]))
    vis = ";".join("1" if (t >= round(a, 4) and t < round(b, 4)) else "0" for t in pts)
    vkt = ";".join(f"{t:.4f}" for t in pts)
    typed.append(f'''
  <clipPath id="c{i}"><rect x="{x}" y="{Y0-FS}" width="0" height="{FS+14}">
    <animate attributeName="width" values="{clipw}" keyTimes="{ktimes}" dur="{CYCLE}s" repeatCount="indefinite"/></rect></clipPath>
  <text x="{x}" y="{Y0}" font-family="'SFMono-Regular',Menlo,Consolas,'Courier New',monospace" font-size="{FS}" fill="#9fb3c8"
        textLength="{w}" lengthAdjust="spacing" clip-path="url(#c{i})">{line.replace("&","&amp;")}</text>
  <g opacity="0"><animate attributeName="opacity" values="{vis}" keyTimes="{vkt}" calcMode="discrete" dur="{CYCLE}s" repeatCount="indefinite"/>
    <rect y="{Y0-FS+2}" width="3" height="{FS}" rx="1.5" fill="#58a6ff">
      <animate attributeName="x" values="{curx}" keyTimes="{ktimes}" dur="{CYCLE}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect></g>''')

dots = []
import random
random.seed(7)
for _ in range(26):
    x, y, r = random.randint(20, W-20), random.randint(20, H-60), random.choice([1.2, 1.6, 2.0])
    d = random.uniform(5, 11); b = random.uniform(0, 6)
    dots.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#58a6ff" opacity="0.0"><animate attributeName="opacity" values="0;.55;0" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/>'
                f'<animate attributeName="cy" values="{y};{y-18}" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>')

header = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Nijat Hatamli - Software and Systems Engineer">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1220"/><stop offset="1" stop-color="#101a2e"/></linearGradient>
    <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#58a6ff"/><stop offset=".5" stop-color="#a371f7"/><stop offset="1" stop-color="#3fb950"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;-1 0" dur="14s" repeatCount="indefinite"/></linearGradient>
    <linearGradient id="wave1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#58a6ff" stop-opacity=".35"/><stop offset="1" stop-color="#a371f7" stop-opacity=".35"/></linearGradient>
    <linearGradient id="wave2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a371f7" stop-opacity=".25"/><stop offset="1" stop-color="#3fb950" stop-opacity=".25"/></linearGradient>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <g opacity=".5" stroke="#1f2b44" stroke-width="1">
      {''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(0, W+1, 60))}
      {''.join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0, H+1, 60))}
    </g>
    {''.join(dots)}
    <g><path fill="url(#wave1)" d="M0 270 C 150 230 300 310 450 270 S 750 230 900 270 S 1050 310 1200 270 S 1350 230 1500 270 S 1650 310 1800 270 S 2100 230 2250 270 V {H} H0 Z">
        <animateTransform attributeName="transform" type="translate" values="0 0;-600 0" dur="18s" repeatCount="indefinite"/></path></g>
    <g><path fill="url(#wave2)" d="M0 290 C 200 260 350 330 600 290 S 900 255 1200 290 S 1500 330 1800 290 S 2100 255 2400 290 V {H} H0 Z">
        <animateTransform attributeName="transform" type="translate" values="-600 0;0 0" dur="24s" repeatCount="indefinite"/></path></g>
    <text x="{W/2}" y="138" text-anchor="middle" font-family="'Segoe UI',Helvetica,Arial,sans-serif" font-size="68" font-weight="800" fill="url(#name)" letter-spacing="1">Nijat Hatamli
      <animate attributeName="opacity" values="0;1" dur="1.2s" fill="freeze"/></text>
    <text x="{W/2}" y="178" text-anchor="middle" font-family="'Segoe UI',Helvetica,Arial,sans-serif" font-size="18" fill="#6e7f99" letter-spacing="6">BAKU  ·  AZERBAIJAN</text>
    {''.join(typed)}
  </g>
</svg>
'''
(OUT / "header.svg").write_text(header, encoding="utf-8")

# ---------------------------------------------------------------- divider
divider = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="6" viewBox="0 0 1200 6" role="presentation">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
    <stop offset="0" stop-color="#58a6ff" stop-opacity="0"/><stop offset=".25" stop-color="#58a6ff"/><stop offset=".5" stop-color="#a371f7"/><stop offset=".75" stop-color="#3fb950"/><stop offset="1" stop-color="#3fb950" stop-opacity="0"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-0.6 0;0.6 0;-0.6 0" dur="8s" repeatCount="indefinite"/></linearGradient></defs>
  <rect y="2" width="1200" height="2" rx="1" fill="url(#g)"/>
</svg>
'''
(OUT / "divider.svg").write_text(divider, encoding="utf-8")

# ---------------------------------------------------------------- footer
footer = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="120" viewBox="0 0 {W} 120" role="img" aria-label="Thanks for visiting">
  <defs>
    <linearGradient id="f1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#58a6ff" stop-opacity=".35"/><stop offset="1" stop-color="#a371f7" stop-opacity=".35"/></linearGradient>
    <linearGradient id="f2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a371f7" stop-opacity=".25"/><stop offset="1" stop-color="#3fb950" stop-opacity=".25"/></linearGradient>
    <clipPath id="ff"><rect width="{W}" height="120" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#ff)">
    <rect width="{W}" height="120" fill="#0b1220"/>
    <path fill="url(#f1)" d="M0 60 C 150 20 300 100 450 60 S 750 20 900 60 S 1050 100 1200 60 S 1350 20 1500 60 S 1650 100 1800 60 S 2100 20 2250 60 V 120 H0 Z"><animateTransform attributeName="transform" type="translate" values="0 0;-600 0" dur="18s" repeatCount="indefinite"/></path>
    <path fill="url(#f2)" d="M0 80 C 200 50 350 110 600 80 S 900 45 1200 80 S 1500 110 1800 80 S 2100 45 2400 80 V 120 H0 Z"><animateTransform attributeName="transform" type="translate" values="-600 0;0 0" dur="24s" repeatCount="indefinite"/></path>
    <text x="{W/2}" y="42" text-anchor="middle" font-family="'Segoe UI',Helvetica,Arial,sans-serif" font-size="20" fill="#9fb3c8" letter-spacing="1">Thanks for stopping by  ·  nijat.tech</text>
  </g>
</svg>
'''
(OUT / "footer.svg").write_text(footer, encoding="utf-8")
print("ok", [p.name for p in OUT.iterdir()])

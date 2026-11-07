#!/usr/bin/env python3
"""Builds assets/stats.svg from public GitHub data (run daily by .github/workflows/stats.yml).
Only public numbers are used. Needs the `gh` CLI with GH_TOKEN set."""
import json, subprocess, sys, pathlib, collections, html

USER = sys.argv[1] if len(sys.argv) > 1 else "nijathatamli"
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "stats.svg"

def gh(*args):
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr)
    return json.loads(r.stdout)

user = gh("api", f"users/{USER}")
repos = gh("api", "--paginate", f"users/{USER}/repos?per_page=100&type=owner")
repos = [r for r in (repos if isinstance(repos, list) else []) if not r["fork"]]
langs = collections.Counter()
SKIP = {"Jupyter Notebook", "Dockerfile", "Makefile", "MDX"}
for r in repos:
    try:
        for k, v in gh("api", f"repos/{USER}/{r['name']}/languages").items():
            if k not in SKIP: langs[k] += v
    except SystemExit:
        pass
total = sum(langs.values()) or 1
top = langs.most_common(6)

COL = {"TypeScript": "#3178c6", "JavaScript": "#f1e05a", "Python": "#3572A5", "C": "#7a7a7a", "C++": "#f34b7d",
       "Rust": "#dea584", "Shell": "#89e051", "HTML": "#e34c26", "CSS": "#9b6bd1", "Go": "#00ADD8", "Java": "#b07219"}
# live numbers + facts taken from nijat.tech (update by hand when they change)
tiles = [("Public repos", len(repos)), ("Followers", user["followers"]), ("Hackathons won", "5"), ("Competitions", "10+")]

W, H = 1200, 250
parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GitHub activity summary">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1220"/><stop offset="1" stop-color="#101a2e"/></linearGradient>
<clipPath id="r"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>
<g clip-path="url(#r)"><rect width="{W}" height="{H}" fill="url(#bg)"/>
<g font-family="'Segoe UI',Helvetica,Arial,sans-serif">''']
x0 = 40
for i, (label, val) in enumerate(tiles):
    x = x0 + i * 135 if False else x0 + (i % 2) * 290
    y = 55 + (i // 2) * 105
    parts.append(f'<text x="{x}" y="{y+40}" font-size="46" font-weight="800" fill="#e6edf3">{val if isinstance(val, str) else format(val, ",")}'
                 f'<animate attributeName="opacity" values="0;1" dur="0.8s" begin="{i*0.15:.2f}s" fill="freeze"/></text>'
                 f'<text x="{x}" y="{y+66}" font-size="14" fill="#7d8ea8" letter-spacing=".5">{html.escape(label.upper())}</text>')
# language bar
bx, by, bw = 660, 70, 500
parts.append(f'<text x="{bx}" y="48" font-size="14" fill="#7d8ea8" letter-spacing=".5">TOP LANGUAGES  (public repositories)</text>')
parts.append(f'<clipPath id="bar"><rect x="{bx}" y="{by}" width="{bw}" height="16" rx="8"/></clipPath><g clip-path="url(#bar)">')
cx = bx
for name, n in top:
    w = bw * n / sum(v for _, v in top)
    parts.append(f'<rect x="{cx:.1f}" y="{by}" width="{w:.1f}" height="16" fill="{COL.get(name, "#8b949e")}"/>')
    cx += w
parts.append('</g>')
for i, (name, n) in enumerate(top):
    lx = bx + (i % 2) * 250; ly = 125 + (i // 2) * 36
    parts.append(f'<circle cx="{lx+6}" cy="{ly-5}" r="6" fill="{COL.get(name, "#8b949e")}"/>'
                 f'<text x="{lx+20}" y="{ly}" font-size="16" fill="#c9d1d9">{html.escape(name)} <tspan fill="#7d8ea8">{100*n/total:.1f}%</tspan></text>')
parts.append('</g></g></svg>')
OUT.write_text("\n".join(parts), encoding="utf-8")
print("stats written:", {l: v for l, v in tiles}, [n for n, _ in top])

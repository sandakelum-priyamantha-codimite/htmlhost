#!/usr/bin/env python3
"""Generate the NTK print alignment test pages.

Each page is a single SVG whose viewBox is in inches, so every mark is
placed at an exact physical distance from the paper edge.

Run:  python3 build.py
"""
from pathlib import Path

OUT = Path(__file__).parent

CHECKS_DEFAULT = [
    "Outer border should remain evenly positioned 0.25 in from all four page edges.",
    "Inner border should remain evenly positioned 0.50 in from all four page edges.",
    "Center target should remain at the physical center of the sheet.",
    "Compare top and left offsets across NTK, Chrome, Edge, and a non-Chromium renderer.",
    "Repeat using the same printer, tray, scaling, and driver settings.",
]

PAGES = [
    {
        "file": "a4.html",
        "name": "A4",
        "css_size": "A4",
        "w": 210 / 25.4, "h": 297 / 25.4,
        "size_text": "210 x 297 mm (8.27 x 11.69 in)",
        "footer_size": "A4 - 210 x 297 mm",
        "title": "Native Toolkit - A4 Alignment Test",
        "top_refs": [1.65, 1.90, 2.15, 2.40, 2.65, 2.90, 3.15],
        "checks": CHECKS_DEFAULT,
        "crop_marks": False,
    },
    {
        "file": "letter.html",
        "name": "US Letter",
        "css_size": "letter",
        "w": 8.5, "h": 11.0,
        "size_text": "8.5 x 11 in (215.9 x 279.4 mm)",
        "footer_size": "US Letter - 8.5 x 11 in",
        "title": "Native Toolkit - US Letter Alignment Test",
        "top_refs": [1.85, 2.10, 2.35, 2.60, 2.85, 3.10, 3.35, 3.60],
        "checks": [
            "Outer border should remain evenly positioned 0.25 in from all four page edges.",
            "Inner border should remain evenly positioned 0.50 in from all four page edges.",
            "Center target should remain at the physical center of the Letter sheet.",
            "Compare top and left offsets against a control print from the normal OS print path.",
            "Repeat with media size omitted and with an explicit supported Letter media size.",
        ],
        "crop_marks": True,
    },
    {
        "file": "legal.html",
        "name": "US Legal",
        "css_size": "legal",
        "w": 8.5, "h": 14.0,
        "size_text": "8.5 x 14 in (215.9 x 355.6 mm)",
        "footer_size": "US Legal - 8.5 x 14 in",
        "title": "Native Toolkit - US Legal Alignment Test",
        "top_refs": [1.65, 1.90, 2.15, 2.40, 2.65, 2.90, 3.15],
        "checks": CHECKS_DEFAULT,
        "crop_marks": False,
    },
]


def f(n):
    """Format a number for SVG (trim trailing zeros)."""
    return f"{n:.4f}".rstrip("0").rstrip(".")


def svg_body(p):
    w, h = p["w"], p["h"]
    cx, cy = w / 2, h / 2
    o, i = 0.25, 0.5  # outer / inner border offsets
    s = []
    a = s.append

    # Borders
    a(f'<rect class="border" x="{o}" y="{o}" width="{f(w-2*o)}" height="{f(h-2*o)}"/>')
    a(f'<rect class="border" x="{i}" y="{i}" width="{f(w-2*i)}" height="{f(h-2*i)}"/>')

    # Crop marks: outer border lines extended to the paper edge
    if p["crop_marks"]:
        for x in (o, w - o):
            a(f'<line class="line" x1="{f(x)}" y1="0" x2="{f(x)}" y2="{o}"/>')
            a(f'<line class="line" x1="{f(x)}" y1="{f(h-o)}" x2="{f(x)}" y2="{f(h)}"/>')
        for y in (o, h - o):
            a(f'<line class="line" x1="0" y1="{f(y)}" x2="{o}" y2="{f(y)}"/>')
            a(f'<line class="line" x1="{f(w-o)}" y1="{f(y)}" x2="{f(w)}" y2="{f(y)}"/>')

    # Corner labels and footer (in the band between the borders)
    lab_top, lab_bot = 0.42, h - 0.32
    a(f'<text x="0.30" y="{lab_top}" font-size="0.085">0.25 in from TOP / LEFT</text>')
    a(f'<text x="{f(w-0.30)}" y="{lab_top}" font-size="0.085" class="end">TOP / RIGHT</text>')
    a(f'<text x="0.30" y="{f(lab_bot)}" font-size="0.085">BOTTOM / LEFT</text>')
    a(f'<text x="{f(w-0.30)}" y="{f(lab_bot)}" font-size="0.085" class="end">BOTTOM / RIGHT</text>')
    a(f'<text x="{f(cx)}" y="{f(lab_bot)}" font-size="0.085" class="mid">'
      f'NTK HTML alignment diagnostic - {p["footer_size"]}</text>')

    # Dashed centre lines
    a(f'<line class="dash" x1="{f(cx)}" y1="{i}" x2="{f(cx)}" y2="{f(h-i)}"/>')
    a(f'<line class="dash" x1="{i}" y1="{f(cy)}" x2="{f(w-i)}" y2="{f(cy)}"/>')

    # Header
    a(f'<text x="{f(cx)}" y="0.82" font-size="0.25" class="b mid">{p["title"]}</text>')
    a(f'<text x="{f(cx)}" y="1.02" font-size="0.13" class="mid">Page size: {p["size_text"]}</text>')
    a(f'<text x="{f(cx)}" y="1.20" font-size="0.13" class="mid">'
      'Print at 100% / Actual Size where applicable</text>')

    # Top margin reference
    a(f'<text x="0.70" y="{f(p["top_refs"][0]-0.20)}" font-size="0.11" class="b">TOP MARGIN REFERENCE</text>')
    for y in p["top_refs"]:
        a(f'<line class="line" x1="0.77" y1="{y:.2f}" x2="1.08" y2="{y:.2f}"/>'
          f'<text x="1.15" y="{f(y+0.033)}" font-size="0.095">{y:.2f} in from top</text>')

    # Horizontal alignment reference (ticks measured from the left paper edge)
    a(f'<text x="{f(cx)}" y="{f(cy-0.62)}" font-size="0.11" class="b mid">HORIZONTAL ALIGNMENT REFERENCE</text>')
    for n in range(1, int(w - i) + 1):
        if n >= w - i:
            break
        lx = n - 0.07 if abs(n - cx) < 0.1 else n  # keep label off the centre line
        a(f'<line class="line" x1="{n}" y1="{f(cy-0.40)}" x2="{n}" y2="{f(cy-0.23)}"/>'
          f'<text x="{f(lx)}" y="{f(cy-0.08)}" font-size="0.095" class="mid">{n}"</text>')

    # Centre target
    a(f'<circle class="line" cx="{f(cx)}" cy="{f(cy)}" r="0.33"/>')
    a(f'<circle class="line" cx="{f(cx)}" cy="{f(cy)}" r="0.17"/>')
    a(f'<line class="line" x1="{f(cx-0.485)}" y1="{f(cy)}" x2="{f(cx+0.485)}" y2="{f(cy)}"/>')
    a(f'<line class="line" x1="{f(cx)}" y1="{f(cy-0.485)}" x2="{f(cx)}" y2="{f(cy+0.485)}"/>')
    a(f'<text x="{f(cx)}" y="{f(cy+0.71)}" font-size="0.11" class="b mid">PAGE CENTER</text>')

    # Validation checks (anchored to the bottom of the sheet)
    vy = h - 2.29
    a(f'<text x="0.70" y="{f(vy)}" font-size="0.15" class="b">Validation checks</text>')
    for k, line in enumerate(p["checks"], 1):
        a(f'<text x="0.70" y="{f(vy+0.03+0.2*k)}" font-size="0.105">{k}. {line}</text>')

    return "\n  ".join(s)


def svg_full(p):
    """Full-bleed variant: marks run to the paper edge."""
    w, h = p["w"], p["h"]
    cx, cy = w / 2, h / 2
    s = []
    a = s.append
    sw = 0.0139

    # Edge border, inset by half its stroke so it sits exactly on the edge
    a(f'<rect class="border" x="{f(sw/2)}" y="{f(sw/2)}" width="{f(w-sw)}" height="{f(h-sw)}"/>')

    # Clip gauges: lines at 1-10 mm from each edge
    gx, gy = round(w * 0.25, 2), round(h * 0.25, 2)
    gl = 0.4
    for d in range(1, 11):
        m = d / 25.4
        lab = d % 2 == 0
        # top / bottom: horizontal lines
        for y, ty in ((m, m + 0.02), (h - m, h - m + 0.02)):
            a(f'<line class="hair" x1="{f(gx)}" y1="{f(y)}" x2="{f(gx+gl)}" y2="{f(y)}"/>')
            if lab:
                a(f'<text x="{f(gx+gl+0.04)}" y="{f(ty)}" font-size="0.055">{d}</text>')
        # left / right: vertical lines
        for x in (m, w - m):
            a(f'<line class="hair" x1="{f(x)}" y1="{f(gy)}" x2="{f(x)}" y2="{f(gy+gl)}"/>')
            if lab:
                a(f'<text x="{f(x)}" y="{f(gy+gl+0.08)}" font-size="0.055" class="mid">{d}</text>')
    a(f'<text x="{f(gx)}" y="0.53" font-size="0.07">mm from top edge</text>')
    a(f'<text x="{f(gx)}" y="{f(h-0.47)}" font-size="0.07">mm from bottom edge</text>')
    a(f'<text x="0.06" y="{f(gy-0.07)}" font-size="0.07">mm from left</text>')
    a(f'<text x="{f(w-0.06)}" y="{f(gy-0.07)}" font-size="0.07" class="end">mm from right</text>')

    # Edge rulers (1/8 in ticks, measured from the top-left corner)
    def skip(v, lo):
        return v < 0.3 or (lo - 0.05 <= v <= lo + gl + 0.25)
    for k in range(1, int(w * 8) + 1):
        x = k / 8
        if x > w - 0.3 or skip(x, gx):
            continue
        L = 0.2 if k % 8 == 0 else 0.12 if k % 4 == 0 else 0.06
        a(f'<line class="hair" x1="{f(x)}" y1="0" x2="{f(x)}" y2="{L}"/>')
        a(f'<line class="hair" x1="{f(x)}" y1="{f(h)}" x2="{f(x)}" y2="{f(h-L)}"/>')
        if k % 8 == 0:
            a(f'<text x="{f(x)}" y="0.31" font-size="0.075" class="mid">{k//8}</text>')
            a(f'<text x="{f(x)}" y="{f(h-0.25)}" font-size="0.075" class="mid">{k//8}</text>')
    for k in range(1, int(h * 8) + 1):
        y = k / 8
        if y > h - 0.3 or skip(y, gy):
            continue
        L = 0.2 if k % 8 == 0 else 0.12 if k % 4 == 0 else 0.06
        a(f'<line class="hair" x1="0" y1="{f(y)}" x2="{L}" y2="{f(y)}"/>')
        a(f'<line class="hair" x1="{f(w)}" y1="{f(y)}" x2="{f(w-L)}" y2="{f(y)}"/>')
        if k % 8 == 0:
            a(f'<text x="0.25" y="{f(y+0.027)}" font-size="0.075">{k//8}</text>')
            a(f'<text x="{f(w-0.25)}" y="{f(y+0.027)}" font-size="0.075" class="end">{k//8}</text>')

    # Corner labels and footer
    a('<text x="0.30" y="0.55" font-size="0.085">TOP / LEFT (0 in)</text>')
    a(f'<text x="{f(w-0.30)}" y="0.55" font-size="0.085" class="end">TOP / RIGHT</text>')
    a(f'<text x="0.30" y="{f(h-0.47)}" font-size="0.085">BOTTOM / LEFT</text>')
    a(f'<text x="{f(w-0.30)}" y="{f(h-0.47)}" font-size="0.085" class="end">BOTTOM / RIGHT</text>')
    a(f'<text x="{f(cx)}" y="{f(h-0.62)}" font-size="0.085" class="mid">'
      f'NTK HTML full-bleed diagnostic - {p["footer_size"]}</text>')

    # Dashed centre lines, edge to edge
    a(f'<line class="dash" x1="{f(cx)}" y1="0" x2="{f(cx)}" y2="{f(h)}"/>')
    a(f'<line class="dash" x1="0" y1="{f(cy)}" x2="{f(w)}" y2="{f(cy)}"/>')

    # Header
    title = p["title"].replace("Alignment Test", "Full-Bleed Test")
    a(f'<text x="{f(cx)}" y="0.95" font-size="0.25" class="b mid">{title}</text>')
    a(f'<text x="{f(cx)}" y="1.15" font-size="0.13" class="mid">Page size: {p["size_text"]}</text>')
    a(f'<text x="{f(cx)}" y="1.33" font-size="0.13" class="mid">'
      'Print at 100% / Actual Size with no margins</text>')

    # Horizontal alignment reference
    a(f'<text x="{f(cx)}" y="{f(cy-0.62)}" font-size="0.11" class="b mid">HORIZONTAL ALIGNMENT REFERENCE</text>')
    for n in range(1, int(w)):
        lx = n - 0.07 if abs(n - cx) < 0.1 else n
        a(f'<line class="line" x1="{n}" y1="{f(cy-0.40)}" x2="{n}" y2="{f(cy-0.23)}"/>'
          f'<text x="{f(lx)}" y="{f(cy-0.08)}" font-size="0.095" class="mid">{n}"</text>')

    # Centre target
    a(f'<circle class="line" cx="{f(cx)}" cy="{f(cy)}" r="0.33"/>')
    a(f'<circle class="line" cx="{f(cx)}" cy="{f(cy)}" r="0.17"/>')
    a(f'<line class="line" x1="{f(cx-0.485)}" y1="{f(cy)}" x2="{f(cx+0.485)}" y2="{f(cy)}"/>')
    a(f'<line class="line" x1="{f(cx)}" y1="{f(cy-0.485)}" x2="{f(cx)}" y2="{f(cy+0.485)}"/>')
    a(f'<text x="{f(cx)}" y="{f(cy+0.71)}" font-size="0.11" class="b mid">PAGE CENTER</text>')

    # Validation checks
    checks = [
        "The border line sits on the paper edge; any edge where it is missing is being clipped.",
        "Read each mm gauge: the first visible line is the unprintable margin on that edge.",
        "Ruler ticks should measure true inches; 1\" to 7\" should span exactly 6 in.",
        "Center target should remain at the physical center of the sheet.",
        "Print with margins set to none and the matching page size (no scaling).",
    ]
    vy = h - 2.29
    a(f'<text x="0.70" y="{f(vy)}" font-size="0.15" class="b">Validation checks</text>')
    for k, line in enumerate(checks, 1):
        a(f'<text x="0.70" y="{f(vy+0.03+0.2*k)}" font-size="0.105">{k}. {line}</text>')

    return "\n  ".join(s)


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{page_title}</title>
<!-- Generated by build.py - edit the generator, not this file. -->
<style>
  /* {name} = {w_in} x {h_in} in. The sheet starts at 0,0 with no page
     margins, so print with margins "none" and the matching page size. */
  html, body {{
    margin: 0; padding: 0;
    width: {w_in}in; height: {h_in}in;
    overflow: hidden;            /* never spill onto a second page */
    background: #fff;
  }}
  .sheet {{ display: block; width: {w_in}in; height: {h_in}in; }}
  .sheet text {{ fill: #000; font-family: Arial, Helvetica, sans-serif; }}
  .b {{ font-weight: bold; }}
  .mid {{ text-anchor: middle; }}
  .end {{ text-anchor: end; }}
  .hair   {{ stroke: #000; stroke-width: 0.0069; fill: none; }}   /* 0.5pt */
  .line   {{ stroke: #000; stroke-width: 0.0104; fill: none; }}   /* 0.75pt */
  .border {{ stroke: #000; stroke-width: 0.0139; fill: none; }}   /* 1pt */
  .dash   {{ stroke: #000; stroke-width: 0.0104; stroke-dasharray: 0.06 0.04; fill: none; }}
</style>
</head>
<body>
<!-- viewBox units are inches -->
<svg class="sheet" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"
     role="img" aria-label="{page_title}">
  {body}
</svg>
</body>
</html>
"""


def main():
    for p in PAGES:
        for variant, render, suffix, label in (
            ("standard", svg_body, "", "Alignment Test"),
            ("full", svg_full, "-full", "Full-Bleed Test"),
        ):
            fname = p["file"].replace(".html", suffix + ".html")
            html = TEMPLATE.format(
                name=p["name"], page_title=f'{p["name"]} {label}',
                w=f(p["w"]), h=f(p["h"]),
                w_in=f(round(p["w"], 4)), h_in=f(round(p["h"], 4)),
                body=render(p),
            )
            (OUT / fname).write_text(html)
            print("wrote", fname)


if __name__ == "__main__":
    main()

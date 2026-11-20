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


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} Alignment Test</title>
<!-- Generated by build.py - edit the generator, not this file. -->
<style>
  /* {name} = {w_in} x {h_in} in. No browser margins: every mark is
     positioned from the physical paper edge. */
  @page {{ size: {css_size} portrait; margin: 0; }}

  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{ background: #e5e5e5; font-family: Arial, Helvetica, sans-serif; }}

  .sheet {{
    display: block;
    width: {w_in}in;
    height: {h_in}in;
    margin: 10mm auto;
    background: #fff;
    box-shadow: 0 0 6px rgba(0,0,0,0.25);
  }}
  .sheet text {{ fill: #000; font-family: Arial, Helvetica, sans-serif; }}
  .b {{ font-weight: bold; }}
  .mid {{ text-anchor: middle; }}
  .end {{ text-anchor: end; }}
  .line   {{ stroke: #000; stroke-width: 0.0104; fill: none; }}   /* 0.75pt */
  .border {{ stroke: #000; stroke-width: 0.0139; fill: none; }}   /* 1pt */
  .dash   {{ stroke: #000; stroke-width: 0.0104; stroke-dasharray: 0.06 0.04; fill: none; }}

  .back {{
    display: block; width: {w_in}in; margin: 6mm auto -4mm;
    font-size: 13px; color: #333;
  }}

  @media print {{
    body {{ background: #fff; }}
    .sheet {{ margin: 0; box-shadow: none; }}
    .back {{ display: none; }}
  }}
  @media screen and (max-width: {max_w}in) {{
    .sheet {{ width: 100%; height: auto; margin: 0; box-shadow: none; }}
    .back {{ width: auto; margin: 12px 16px; }}
  }}
</style>
</head>
<body>
<a class="back" href="./">&larr; All alignment tests</a>
<!-- viewBox units are inches -->
<svg class="sheet" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"
     role="img" aria-label="{name} alignment test page">
  {body}
</svg>
</body>
</html>
"""


def main():
    for p in PAGES:
        html = TEMPLATE.format(
            name=p["name"], css_size=p["css_size"],
            w=f(p["w"]), h=f(p["h"]),
            w_in=f(round(p["w"], 4)), h_in=f(round(p["h"], 4)),
            max_w=f(round(p["w"] + 0.5, 2)),
            body=svg_body(p),
        )
        (OUT / p["file"]).write_text(html)
        print("wrote", p["file"])


if __name__ == "__main__":
    main()

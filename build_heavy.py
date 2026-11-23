#!/usr/bin/env python3
"""Generate heavy-a4.html: a ~3.5 MB, exactly-10-page A4 print stress test.

Every page is a fixed 210 x 297 mm sheet (overflow hidden, page break
after all but the last), so the print job is always 10 pages. Each sheet
carries the kinds of content that make print pipelines slow:

  * a large embedded raster (base64 PNG of incompressible noise + gradient)
  * a dense SVG plot with thousands of vector elements
  * a full-width data table with hundreds of cells
  * a block of small body text

Output is deterministic (fixed random seed).

Run:  python3 build_heavy.py
"""
import base64
import random
import struct
import zlib
from pathlib import Path

OUT = Path(__file__).parent / "heavy-a4.html"
PAGES = 10
SEED = 20261123

# Per-page payload knobs (tune these to move the file size)
IMG_W, IMG_H = 240, 136      # raster pixels per page (RGB noise)
SVG_POINTS = 3200            # scatter circles per page
SVG_LINE_PTS = 600           # points per polyline (x3 lines)
TABLE_ROWS = 44
TABLE_COLS = 10

WORDS = ("lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod "
         "tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam "
         "quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo "
         "consequat duis aute irure in reprehenderit voluptate velit esse cillum "
         "fugiat nulla pariatur excepteur sint occaecat cupidatat non proident "
         "sunt culpa qui officia deserunt mollit anim id est laborum").split()


def png(w, h, rnd, hue):
    """Build an RGB PNG of gradient + noise (noise keeps it from compressing)."""
    rows = bytearray()
    for y in range(h):
        rows.append(0)  # filter: none
        for x in range(w):
            n = rnd.randrange(0, 90)
            r = (x * 255 // w + hue) % 256
            g = (y * 255 // h + hue * 2) % 256
            b = ((x + y) * 128 // (w + h) + hue * 3) % 256
            rows += bytes(((r + n) % 256, (g + n) % 256, (b + n) % 256))

    def chunk(kind, data):
        c = kind + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(rows), 9)) + chunk(b"IEND", b""))


def svg_plot(rnd, page):
    W, H = 1900, 620
    s = [f'<svg class="plot" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fafafa" stroke="#000" stroke-width="2"/>']
    for gx in range(0, W, 50):
        s.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}" stroke="#ddd" stroke-width="1"/>')
    for gy in range(0, H, 50):
        s.append(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}" stroke="#ddd" stroke-width="1"/>')
    palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
    for _ in range(SVG_POINTS):
        x = rnd.uniform(5, W - 5)
        y = rnd.gauss(H / 2, H / 6)
        y = min(max(y, 5), H - 5)
        c = palette[rnd.randrange(len(palette))]
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(1.5, 4):.1f}" '
                 f'fill="{c}" fill-opacity="0.55"/>')
    for k, col in enumerate(("#000", "#d62728", "#1f77b4")):
        v = H / 2 + (k - 1) * 120
        pts = []
        for i in range(SVG_LINE_PTS):
            v += rnd.uniform(-9, 9)
            v = min(max(v, 10), H - 10)
            pts.append(f"{i * W / (SVG_LINE_PTS - 1):.1f},{v:.1f}")
        s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="2.5"/>')
    s.append(f'<text x="20" y="40" font-size="32" font-family="Arial" font-weight="bold">'
             f'Series plot - sheet {page} of {PAGES} - {SVG_POINTS} points</text>')
    s.append("</svg>")
    return "\n".join(s)


def table(rnd, page):
    head = "".join(f"<th>Col {c + 1}</th>" for c in range(TABLE_COLS))
    body = []
    for r in range(TABLE_ROWS):
        cells = [f"<td>P{page:02d}-R{r + 1:03d}</td>"]
        for _ in range(TABLE_COLS - 1):
            cells.append(f"<td>{rnd.uniform(-99999, 99999):,.2f}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    return (f'<table><thead><tr>{head}</tr></thead><tbody>\n'
            + "\n".join(body) + "\n</tbody></table>")


def text_block(rnd, n=230):
    return " ".join(rnd.choice(WORDS) for _ in range(n)).capitalize() + "."


def page_html(rnd, n):
    img = base64.b64encode(png(IMG_W, IMG_H, rnd, n * 23)).decode()
    brk = "" if n == PAGES else " brk"
    return f"""<section class="page{brk}">
  <header><span class="b">Heavy Print Stress Test - A4</span><span>Page {n} / {PAGES}</span></header>
  <div class="row">
    <img src="data:image/png;base64,{img}" alt="Raster block {n}">
    <div class="meta">
      <p class="b">Sheet {n} of {PAGES}</p>
      <p>Raster: {IMG_W}&times;{IMG_H} px RGB noise PNG (base64 inline).</p>
      <p>Vector: {SVG_POINTS} circles, 3 &times; {SVG_LINE_PTS}-point polylines, grid.</p>
      <p>Table: {TABLE_ROWS} rows &times; {TABLE_COLS} columns.</p>
      <p>Expected: exactly {PAGES} pages, page number at top-right, nothing clipped at the footer line.</p>
    </div>
  </div>
  {svg_plot(rnd, n)}
  {table(rnd, n)}
  <p class="txt">{text_block(rnd)}</p>
  <footer><span>heavy-a4.html</span><span>End of sheet {n}</span></footer>
</section>"""


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Heavy A4 Stress Test</title>
<!-- Generated by build_heavy.py - edit the generator, not this file. -->
<style>
  /* Each .page is one A4 sheet. Print with page size A4, margins none,
     scale 100%: the job must come out as exactly {pages} pages. */
  html, body {{ margin: 0; padding: 0; background: #fff; }}
  body {{ font-family: Arial, Helvetica, sans-serif; color: #000;
         -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  .page {{ box-sizing: border-box; width: 210mm; height: 297mm; overflow: hidden;
          padding: 8mm 10mm; position: relative; display: flex; flex-direction: column; gap: 2.5mm; }}
  .brk {{ break-after: page; page-break-after: always; }}
  header, footer {{ display: flex; justify-content: space-between; font-size: 10pt; }}
  header {{ border-bottom: 0.75pt solid #000; padding-bottom: 1.5mm; }}
  footer {{ margin-top: auto; border-top: 0.75pt solid #000; padding-top: 1.5mm; font-size: 8pt; }}
  .b {{ font-weight: bold; }}
  .row {{ display: flex; gap: 4mm; height: 52mm; }}
  .row img {{ width: 92mm; height: 52mm; display: block; image-rendering: pixelated; }}
  .meta {{ font-size: 8.5pt; line-height: 1.35; }}
  .meta p {{ margin: 0 0 1.2mm; }}
  .plot {{ width: 190mm; height: 62mm; display: block; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 5.6pt; table-layout: fixed; }}
  th, td {{ border: 0.35pt solid #555; padding: 0.25mm 0.8mm; text-align: right; white-space: nowrap; overflow: hidden; }}
  th {{ background: #e5e5e5; text-align: center; }}
  td:first-child {{ text-align: left; font-weight: bold; }}
  tbody tr:nth-child(even) td {{ background: #f3f3f3; }}
  .txt {{ font-size: 6.5pt; line-height: 1.25; margin: 0; text-align: justify; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def main():
    rnd = random.Random(SEED)
    body = "\n".join(page_html(rnd, n) for n in range(1, PAGES + 1))
    OUT.write_text(TEMPLATE.format(pages=PAGES, body=body))
    print(f"wrote {OUT.name}: {OUT.stat().st_size / 1e6:.2f} MB, {PAGES} pages")


if __name__ == "__main__":
    main()

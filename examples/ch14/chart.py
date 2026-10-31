from html import escape
import math
from pathlib import Path


def bar_chart(values):
    for label, value in values.items():
        if not isinstance(label, str) or not label:
            raise ValueError("Labels must be nonempty strings")
        if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
            raise ValueError("Values must be finite and nonnegative")
    rows = sorted(values.items())
    maximum = max(values.values(), default=0) or 1
    height = 140 + 70 * len(rows)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="850" height="{height}">',
             '<title>Workshop costs by category</title>',
             '<desc>Horizontal bars start at zero. Labels give exact cents.</desc>',
             '<rect width="100%" height="100%" fill="white"/>',
             '<g font-family="sans-serif" font-size="20" fill="#172b3a">',
             '<text x="25" y="40">Workshop costs by category (cents)</text>',
             '<text x="230" y="80">0</text>']
    for index, (label, value) in enumerate(rows):
        y = 100 + 70 * index
        width = value / maximum * 400
        parts.append(f'<text x="25" y="{y+25}">{escape(label)}</text>')
        parts.append(f'<rect x="230" y="{y}" width="{width:.2f}" height="35" fill="#176b87"/>')
        parts.append(f'<text x="650" y="{y+25}">{value:g} cents</text>')
    if not rows:
        parts.append('<text x="25" y="110">No accepted records.</text>')
    parts.append('</g></svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    svg = bar_chart({"materials": 1500, "travel": 300})
    with Path("costs.svg").open("x", encoding="utf-8") as stream:
        stream.write(svg)
    print("Created costs.svg")

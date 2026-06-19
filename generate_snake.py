import json
from datetime import datetime, timedelta

CELL = 14
GAP = 3

with open("contributions.json", "r") as f:
    data = json.load(f)

dates = [datetime.strptime(d, "%Y-%m-%d") for d in data.keys()]

if not dates:
    raise RuntimeError("No submissions")

start = min(dates)

cells = []

for date_str, count in data.items():
    d = datetime.strptime(date_str, "%Y-%m-%d")

    delta = (d - start).days

    x = delta // 7
    y = d.weekday()

    cells.append({
        "x": x,
        "y": y,
        "count": count
    })

max_x = max(c["x"] for c in cells)

width = (max_x + 2) * (CELL + GAP)
height = 8 * (CELL + GAP)

def color(count):
    if count == 0:
        return "#ebedf0"
    elif count < 5:
        return "#9be9a8"
    elif count < 15:
        return "#40c463"
    elif count < 30:
        return "#30a14e"
    else:
        return "#216e39"

svg = []

svg.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" height="{height}" '
    f'viewBox="0 0 {width} {height}">'
)

svg.append('<rect width="100%" height="100%" fill="#0d1117"/>')

path_points = []

for cell in sorted(cells, key=lambda c: (c["x"], c["y"])):

    px = cell["x"] * (CELL + GAP) + CELL // 2
    py = cell["y"] * (CELL + GAP) + CELL // 2

    path_points.append((px, py))

for cell in cells:

    px = cell["x"] * (CELL + GAP)
    py = cell["y"] * (CELL + GAP)

    svg.append(
        f'<rect x="{px}" y="{py}" '
        f'width="{CELL}" height="{CELL}" '
        f'rx="2" ry="2" '
        f'fill="{color(cell["count"])}"/>'
    )

if len(path_points) > 1:

    path = f"M {path_points[0][0]} {path_points[0][1]} "

    for x, y in path_points[1:]:
        path += f"L {x} {y} "

    svg.append(
        f'''
        <circle r="5" fill="#58a6ff">
            <animateMotion
                dur="20s"
                repeatCount="indefinite"
                path="{path}" />
        </circle>
        '''
    )

    svg.append(
        f'''
        <circle r="4" fill="#1f6feb">
            <animateMotion
                dur="20s"
                begin="-0.4s"
                repeatCount="indefinite"
                path="{path}" />
        </circle>
        '''
    )

    svg.append(
        f'''
        <circle r="3" fill="#1158c7">
            <animateMotion
                dur="20s"
                begin="-0.8s"
                repeatCount="indefinite"
                path="{path}" />
        </circle>
        '''
    )

svg.append("</svg>")

with open("vnoi-snake.svg", "w", encoding="utf8") as f:
    f.write("\n".join(svg))

print("Generated vnoi-snake.svg")

import json
from datetime import datetime

CELL = 14
GAP = 3

with open("contributions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if not data:
    raise RuntimeError("No contribution data found")

dates = [datetime.strptime(d, "%Y-%m-%d") for d in data.keys()]
start = min(dates)

cells = []

for date_str, count in data.items():
    d = datetime.strptime(date_str, "%Y-%m-%d")

    delta = (d - start).days

    week = delta // 7
    weekday = d.weekday()

    cells.append({
        "week": week,
        "day": weekday,
        "count": count
    })

max_week = max(c["week"] for c in cells)

width = (max_week + 2) * (CELL + GAP)
height = 7 * (CELL + GAP) + GAP

def color(count):
    if count == 0:
        return "#161b22"
    elif count < 5:
        return "#0e4429"
    elif count < 15:
        return "#006d32"
    elif count < 30:
        return "#26a641"
    else:
        return "#39d353"

svg = []

svg.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" '
    f'height="{height}" '
    f'viewBox="0 0 {width} {height}">'
)

svg.append(
    '<rect width="100%" height="100%" fill="#0d1117"/>'
)

# draw contributions

for cell in cells:
    x = cell["week"] * (CELL + GAP)
    y = cell["day"] * (CELL + GAP)

    svg.append(
        f'<rect '
        f'x="{x}" '
        f'y="{y}" '
        f'width="{CELL}" '
        f'height="{CELL}" '
        f'rx="2" '
        f'fill="{color(cell["count"])}"/>'
    )

# generate snake path over ENTIRE grid

path_points = []

for row in range(7):

    if row % 2 == 0:

        for col in range(max_week + 1):

            x = col * (CELL + GAP) + CELL / 2
            y = row * (CELL + GAP) + CELL / 2

            path_points.append((x, y))

    else:

        for col in reversed(range(max_week + 1)):

            x = col * (CELL + GAP) + CELL / 2
            y = row * (CELL + GAP) + CELL / 2

            path_points.append((x, y))

path = (
    f"M {path_points[0][0]} {path_points[0][1]} "
)

for x, y in path_points[1:]:
    path += f"L {x} {y} "

# snake body

SEGMENTS = 12

for i in range(SEGMENTS):

    radius = max(2, 6 - i * 0.3)

    opacity = max(0.15, 1 - i * 0.07)

    svg.append(
        f'''
        <circle
            r="{radius}"
            fill="#58a6ff"
            opacity="{opacity}">
            <animateMotion
                dur="25s"
                repeatCount="indefinite"
                begin="-{i * 0.18}s"
                path="{path}" />
        </circle>
        '''
    )

# eyes

head_x = path_points[0][0]
head_y = path_points[0][1]

svg.append("</svg>")

with open("vnoi-snake.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))

print("Generated vnoi-snake.svg")

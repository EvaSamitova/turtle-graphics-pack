#!/usr/bin/env python3
"""
Turtle Graphics — New Figures Pack (+ filled snowflake, + bee)

Layout:
- Sun:          top-left
- Spiral:       bottom-left (shorter, thicker)
- Honeycomb:    bottom-right (gold, larger) + a small bee
- Snowflake:    top-right (now white-filled with purple outline)
- Flower:       centered (petals only)
"""

import turtle
import math

# ---------- helpers ----------
def move_to(t, x, y):
    t.penup(); t.goto(x, y); t.pendown()

# ---------- figures ----------
def render_sun(t, x, y, radius=55, rays=24, long_ray=75, short_ratio=0.6,
               body_fill="#FFD66B", ray_color="#DAA520", outline="#C68900"):
    prev_color = t.pencolor()
    # rays
    t.pencolor(ray_color)
    for i in range(rays):
        ang = i * (360 / rays)
        ray_len = long_ray if i % 2 == 0 else long_ray * short_ratio
        t.penup(); t.goto(x, y); t.setheading(ang); t.forward(radius)
        t.pendown(); t.forward(ray_len)
    # body
    t.pencolor(outline); t.fillcolor(body_fill)
    t.penup(); t.goto(x, y - radius); t.setheading(0)
    t.pendown(); t.begin_fill(); t.circle(radius); t.end_fill()
    t.pencolor(prev_color)

def render_log_spiral(t, x, y, turns=3.8, a=2.0, b=0.20, color="#1B9AAA", pensize=3):
    prev_c, prev_p = t.pencolor(), t.pensize()
    t.pencolor(color); t.pensize(pensize)
    move_to(t, x, y); t.setheading(0)
    steps = int(turns * 180)
    for i in range(steps):
        theta = i * math.pi / 90
        r = a * math.exp(b * theta)
        t.goto(x + r * math.cos(theta), y + r * math.sin(theta))
    t.pencolor(prev_c); t.pensize(prev_p)

def _hexagon(t, size):
    for _ in range(6):
        t.forward(size); t.right(60)

def render_hex_grid(t, x, y, cols=5, rows=4, size=36, color="gold", pensize=2):
    prev_c, prev_p = t.pencolor(), t.pensize()
    t.pencolor(color); t.pensize(pensize)
    h = math.sin(math.radians(60)) * size
    for r in range(rows):
        for c in range(cols):
            ox = x + c * (size * 1.5)
            oy = y - r * (2 * h)
            if r % 2 == 1:
                ox += size * 0.75
            move_to(t, ox, oy); _hexagon(t, size)
    t.pencolor(prev_c); t.pensize(prev_p)

def _koch(t, length, depth):
    if depth == 0:
        t.forward(length); return
    length /= 3.0
    _koch(t, length, depth - 1); t.left(60)
    _koch(t, length, depth - 1); t.right(120)
    _koch(t, length, depth - 1); t.left(60)
    _koch(t, length, depth - 1)

def render_koch_snowflake(t, x, y, size=180, depth=3,
                          outline="#6F3FD6", fill="white"):
    """
    Large Koch snowflake centered around (x, y). Now filled white.
    """
    prev_c, prev_f = t.pencolor(), t.fillcolor()
    t.pencolor(outline); t.fillcolor(fill)
    move_to(t, x - size / 2, y - size / (2 * math.sqrt(3)))
    t.begin_fill()
    for _ in range(3):
        _koch(t, size, depth); t.right(120)
    t.end_fill()
    t.pencolor(prev_c); t.fillcolor(prev_f)

def render_flower(t, x, y, petals=12, r=60,
                  color="#e76f51", fill="#ffdcdc"):
    """
    Arc-petal flower without a central circle.
    """
    prev_pencolor, prev_fill = t.pencolor(), t.fillcolor()
    t.pencolor(color); t.fillcolor(fill)

    move_to(t, x, y - r)
    t.begin_fill()
    for _ in range(petals):
        t.circle(r, 60)
        t.left(120)
        t.circle(r, 60)
        t.left(360 / petals - 120)
    t.end_fill()

    t.pencolor(prev_pencolor); t.fillcolor(prev_fill)

# ---------- a tiny bee (shapes only) ----------
def render_bee(t, x, y, scale=1.0):
    """
    Cute bee composed of filled shapes (no images):
    - body: yellow oval with black stripes
    - head: black circle
    - wings: white ellipses
    - stinger: small triangle
    """
    prev_pc, prev_fc, prev_ps = t.pencolor(), t.fillcolor(), t.pensize()

    # helper: ellipse by polygon
    def ellipse(cx, cy, rx, ry, steps=60, fill=None, outline="black"):
        pts = []
        for i in range(steps+1):
            th = 2*math.pi * i/steps
            pts.append((cx + rx*math.cos(th), cy + ry*math.sin(th)))
        t.pencolor(outline)
        if fill:
            t.fillcolor(fill); t.begin_fill()
        move_to(t, *pts[0])
        for px, py in pts[1:]:
            t.goto(px, py)
        if fill: t.end_fill()

    s = scale
    # body (yellow oval)
    ellipse(x, y, 28*s, 18*s, fill="#FFD166", outline="black")

    # stripes (three black bands)
    t.pencolor("black"); t.pensize(max(1, int(6*s)))
    for off in (-10*s, 0, 10*s):
        move_to(t, x - 20*s, y + off); t.setheading(0); t.forward(40*s)

    # head
    t.pencolor("black"); t.fillcolor("black")
    move_to(t, x - 34*s, y + 12*s); t.begin_fill(); t.circle(8*s); t.end_fill()

    # wings (white ellipses)
    ellipse(x + 8*s, y + 22*s, 16*s, 10*s, fill="white", outline="#888")
    ellipse(x + 22*s, y + 26*s, 14*s, 9*s,  fill="white", outline="#888")

    # stinger (tiny triangle)
    t.pencolor("black"); t.fillcolor("#222")
    move_to(t, x + 30*s, y); t.begin_fill()
    t.setheading(-20); t.forward(10*s)
    t.left(120); t.forward(10*s)
    t.goto(x + 30*s, y); t.end_fill()

    # restore
    t.pencolor(prev_pc); t.fillcolor(prev_fc); t.pensize(prev_ps)

# ---------- main ----------
def main():
    screen = turtle.Screen()
    screen.bgcolor("lightblue")
    screen.setup(1100, 800)

    t = turtle.Turtle(visible=False)
    t.speed(0)

    # Sun (top-left)
    render_sun(t, -330, 260, radius=55, rays=24, long_ray=75)

    # Spiral (bottom-left)
    render_log_spiral(t, -310, -120, turns=3.8, a=2.0, b=0.20, pensize=3)

    # Honeycomb (bottom-right) + bee
    render_hex_grid(t, 210, -10, cols=5, rows=4, size=36, color="gold", pensize=2)
    render_bee(t, 520, -10, scale=0.9)  # position near the honeycomb

    # Snowflake (top-right, now white-filled)
    render_koch_snowflake(t, 360, 250, size=180, depth=3,
                          outline="#6F3FD6", fill="white")

    # Flower (center)
    render_flower(t, 0, 50, petals=12, r=60)

    screen.exitonclick()

if __name__ == "__main__":
    main()

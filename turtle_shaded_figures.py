#!/usr/bin/env python3
"""
Turtle Graphics Pack — shaded front faces

Figures:
1) Double rhombuses (white fill, black contour only)
2) Triangle with inset
3) Prism with shaded front and dashed back
4) Olympic rings
5) Compass rose (centered circle, N/E/S/W in light purple)
6) Marked square (dashed top/bottom, diagonals, dots)
"""

import turtle
import math

# ---------- helpers ----------
def move_to(t: turtle.Turtle, x: float, y: float):
    t.penup(); t.goto(x, y); t.pendown()

def dashed_to(t: turtle.Turtle, x: float, y: float, dash_len=10, gap_len=6):
    """Draw a dashed segment from current position to (x, y)."""
    x0, y0 = t.position()
    dx, dy = x - x0, y - y0
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    ux, uy = dx / dist, dy / dist
    drawn = 0.0
    draw = True
    while drawn < dist:
        step = min(dash_len if draw else gap_len, dist - drawn)
        nx, ny = x0 + ux * (drawn + step), y0 + uy * (drawn + step)
        if draw: t.pendown()
        else:    t.penup()
        t.goto(nx, ny)
        drawn += step
        draw = not draw
    t.pendown()

def dot_at(t: turtle.Turtle, x: float, y: float, size=8):
    t.penup(); t.goto(x, y); t.dot(size); t.pendown()

# ---------- figures ----------
def render_double_rhombuses(t: turtle.Turtle, x_off, y_off):
    """
    Two white rhombuses with black contour only (no interior lines).
    """
    edge = 70
    gap = edge * math.sqrt(2) / 2  # spacing so inner corners meet

    t.pencolor("black")
    t.fillcolor("white")

    for cx in (x_off - gap, x_off + gap):
        t.penup()
        t.goto(cx, y_off)
        t.setheading(45)
        t.begin_fill()
        t.pendown()
        for _ in range(4):
            t.forward(edge)
            t.right(90)
        t.end_fill()
        t.penup()

def render_triangle_with_inset(t: turtle.Turtle, x_off, y_off):
    side = 180
    cx, cy = x_off, y_off
    h = side * math.sqrt(3) / 2
    base_y = cy - h / 2
    top_y  = cy + h / 1.5

    outer = [(cx - side/2, base_y), (cx + side/2, base_y), (cx, top_y)]
    t.penup(); t.goto(outer[0]); t.pendown()
    for pt in outer[1:] + outer[:1]:
        t.goto(pt)

    inner = [(cx - side/2, base_y), (cx + side/2, base_y), (cx, base_y + h/2.2)]
    t.fillcolor("white")
    t.penup(); t.goto(inner[0]); t.pendown()
    t.begin_fill()
    for pt in inner[1:] + inner[:1]:
        t.goto(pt)
    t.end_fill()

def render_prism(t: turtle.Turtle, x_off, y_off):
    """Front face shaded; back edges dashed to suggest depth."""
    side = 110
    dx, dy = 80, -80

    front = [(x_off - side/2, y_off - side/2),
             (x_off - side/2, y_off + side/2),
             (x_off + side/2, y_off + side/2),
             (x_off + side/2, y_off - side/2)]
    back  = [(x + dx, y + dy) for (x, y) in front]

    # back square dashed (hidden)
    t.pencolor("#606060")
    move_to(t, *back[0])
    for pt in back[1:] + back[:1]:
        dashed_to(t, *pt, dash_len=8, gap_len=6)
    for f, b in zip(front, back):
        move_to(t, *b); dashed_to(t, *f, dash_len=8, gap_len=6)

    # front face filled (shaded)
    t.pencolor("black")
    t.fillcolor("#f0f0f0")
    move_to(t, *front[0])
    t.begin_fill()
    for pt in front[1:] + front[:1]:
        t.goto(pt)
    t.end_fill()

    # front diagonals
    move_to(t, *front[0]); t.goto(*front[2])
    move_to(t, *front[1]); t.goto(*front[3])

def render_olympic_rings(t: turtle.Turtle, x_off, y_off):
    r = 30
    spacing = r * 2 + 10
    offsets = [(-spacing, 0), (0, 0), (spacing, 0),
               (-spacing/2, -r), (spacing/2, -r)]
    for dx, dy in offsets:
        t.penup(); t.goto(x_off + dx, y_off + dy - r)
        t.pendown(); t.circle(r)
    t.penup()

def render_compass_rose(t: turtle.Turtle, x_off, y_off):
    """Centered compass rose with light-purple label text."""
    r = 20
    L = 60

    # cross lines
    t.pencolor("black")
    t.penup(); t.goto(x_off - L, y_off); t.pendown(); t.goto(x_off + L, y_off)
    t.penup(); t.goto(x_off, y_off - L); t.pendown(); t.goto(x_off, y_off + L)

    # circle centered
    t.penup(); t.goto(x_off, y_off - r); t.setheading(0); t.pendown(); t.circle(r)

    # labels in light purple
    prev = t.pencolor()
    t.pencolor("#9b7cff")  # light purple
    t.penup()
    t.goto(x_off, y_off + L + 12);    t.write("North", align="center", font=("Arial", 12, "normal"))
    t.goto(x_off + L + 12, y_off - 6); t.write("East",  align="left",   font=("Arial", 12, "normal"))
    t.goto(x_off, y_off - L - 20);    t.write("South", align="center", font=("Arial", 12, "normal"))
    t.goto(x_off - L - 12, y_off - 6); t.write("West",  align="right",  font=("Arial", 12, "normal"))
    t.pencolor(prev)

def render_marked_square(t: turtle.Turtle, x_off, y_off):
    size = 140; half = size / 2
    lx, rx = x_off - half, x_off + half
    by, ty = y_off - half, y_off + half

    # verticals solid
    move_to(t, lx, by); t.goto(lx, ty)
    move_to(t, rx, by); t.goto(rx, ty)

    # top & bottom dashed
    move_to(t, lx, ty); dashed_to(t, rx, ty)
    move_to(t, lx, by); dashed_to(t, rx, by)

    # diagonals
    move_to(t, lx, by); t.goto(rx, ty)
    move_to(t, lx, ty); t.goto(rx, by)

    # dots
    dot_at(t, x_off, y_off, 8)
    for x, y in [(lx, by), (lx, ty), (rx, by), (rx, ty)]:
        dot_at(t, x, y, 8)

# ---------- main ----------
def main():
    screen = turtle.Screen()
    screen.bgcolor("lightblue")
    screen.setup(1100, 800)

    t = turtle.Turtle(visible=False)
    t.speed(0)
    t.pencolor("black")

    # place figures
    render_double_rhombuses(t, -350, 250)
    render_triangle_with_inset(t, 350, 250)
    render_prism(t, -350, 20)
    render_olympic_rings(t, 350, 20)
    render_compass_rose(t, -350, -250)
    render_marked_square(t, 350, -250)

    screen.exitonclick()

if __name__ == "__main__":
    main()

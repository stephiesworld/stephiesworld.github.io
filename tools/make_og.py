#!/usr/bin/env python3
"""Draw og.png, the 1200x630 link-preview card. Needs Pillow; pass Tilt Neon, Doto, and the output path."""
import math, random, sys
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

serif_path, mono_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
W, H = 1200, 630
INK, CREAM, NEON = (5, 5, 7), (239, 228, 214), (255, 45, 74)
random.seed(29)

img = Image.new('RGB', (W, H), INK)

# Red glow rising from the bottom, as on the site
glow = Image.new('RGB', (W, H), INK)
g = ImageDraw.Draw(glow)
g.ellipse((W * 0.18, H * 0.72, W * 0.95, H * 1.55), fill=(70, 8, 18))
img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(120)), 0.9)

# A dotted globe on the right, lit from the front
cx, cy, R = 930, 360, 270
halo = Image.new('RGB', (W, H), (0, 0, 0))
ImageDraw.Draw(halo).ellipse((cx - R - 6, cy - R - 6, cx + R + 6, cy + R + 6), outline=NEON, width=10)
halo = halo.filter(ImageFilter.GaussianBlur(22))
img = Image.composite(Image.blend(img, halo, 0.55), img, halo.convert('L').point(lambda v: min(255, v * 3)))
dots = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(dots)
tilt = math.radians(18)
N = 5200  # evenly spread points (Fibonacci sphere), so no rings bunch up at the poles
golden = math.pi * (3 - math.sqrt(5))
for i in range(N):
    y0 = 1 - 2 * (i + 0.5) / N
    rad = math.sqrt(1 - y0 * y0)
    th = golden * i
    x, y, z = math.cos(th) * rad, y0, math.sin(th) * rad
    y, z = y * math.cos(tilt) - z * math.sin(tilt), y * math.sin(tilt) + z * math.cos(tilt)
    if z <= 0.05: continue
    px, py = cx + x * R, cy - y * R
    a = int(30 + 150 * z ** 1.6)
    col = (255, 177, 92, a) if random.random() < 0.06 else (255, 60, 85, a)
    r = 0.9 + 1.2 * z
    d.ellipse((px - r, py - r, px + r, py + r), fill=col)
img.paste(dots, (0, 0), dots)

# A few rain streaks
rain = ImageDraw.Draw(img, 'RGBA')
for _ in range(60):
    x, y, L = random.uniform(0, W), random.uniform(0, H), random.uniform(10, 26)
    rain.line((x, y, x - L * 0.18, y + L), fill=(239, 228, 214, random.randint(10, 32)), width=1)

# The name as an amber neon tube sign, stacked in two lines, with an LED readout below
AMBER, CORE = (255, 177, 92), (255, 241, 220)
sign = ImageFont.truetype(serif_path, 92)
led = ImageFont.truetype(mono_path, 26)
try: led.set_variation_by_axes([0, 900])  # Doto: roundness, weight
except Exception: pass

def spaced(draw, xy, text, font, fill, track):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + track

lines, tx, ty, lh = ["STEPHIE’S", "WORLD"], 84, 170, 118
def tubes(fill):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for k, line in enumerate(lines):
        spaced(ld, (tx, ty + k * lh), line, sign, fill, 16)
    return layer
src = Image.new('RGB', (W, H), (0, 0, 0))
src.paste(tubes(AMBER + (255,)), (0, 0), tubes(AMBER + (255,)))
for blur, gain in ((50, 1.6), (20, 1.5), (7, 1.2)):  # added light, the way a tube blooms
    b = src.filter(ImageFilter.GaussianBlur(blur)).point(lambda v, g=gain: min(255, int(v * g)))
    img = ImageChops.add(img, b)
core = tubes(CORE + (255,))
img.paste(core, (0, 0), core)

label = "STEPHIESWORLD.COM"
ly = ty + 2 * lh + 34
board = ImageDraw.Draw(img, 'RGBA')
lw = sum(board.textlength(ch, font=led) + 6 for ch in label) - 6
board.rounded_rectangle((tx - 14, ly - 12, tx + lw + 14, ly + 42), radius=4, fill=(18, 9, 4, 200), outline=(255, 177, 92, 45))
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
spaced(ImageDraw.Draw(glow), (tx, ly), label, led, AMBER + (200,), 6)
g2 = glow.filter(ImageFilter.GaussianBlur(6))
img.paste(g2, (0, 0), g2)
spaced(ImageDraw.Draw(img), (tx, ly), label, led, AMBER, 6)

img.save(out, optimize=True)
print('wrote', out)

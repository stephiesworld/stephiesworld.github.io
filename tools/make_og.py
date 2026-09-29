#!/usr/bin/env python3
"""Draw og.png, the 1200x630 link-preview card. Needs Pillow and the two fonts passed in."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

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

# Title with a soft neon bloom behind it
serif = ImageFont.truetype(serif_path, 104)
mono = ImageFont.truetype(mono_path, 22)
tx, ty = 84, 232
bloom = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(bloom).text((tx, ty), "Stephie’s World", font=serif, fill=(255, 45, 74, 110))
img.paste(bloom.filter(ImageFilter.GaussianBlur(18)), (0, 0), bloom.filter(ImageFilter.GaussianBlur(18)))
t = ImageDraw.Draw(img)
t.text((tx, ty), "Stephie’s World", font=serif, fill=CREAM)

label = "STEPHIESWORLD.COM"
x = tx + 4
for ch in label:
    t.text((x, ty + 150), ch, font=mono, fill=NEON)
    x += t.textlength(ch, font=mono) + 5

img.save(out, optimize=True)
print('wrote', out)

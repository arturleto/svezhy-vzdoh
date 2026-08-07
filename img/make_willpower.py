#!/usr/bin/env python3
"""Картинка для слайда «дело не в силе воли»: сто человечков, четверо дошли.

Инфографика вместо декоративной абстракции — цифра читается за секунду.
Палитра сайта: фон --bg-soft, акцент --acc.
"""
import math
from PIL import Image, ImageDraw, ImageFilter

W, H = 860, 480
BG = (13, 21, 35)
ACC = (168, 230, 197)
# цвета сплошные, уже подмешанные к фону: рисование с альфой по RGBA
# заменяет пиксель вместе с прозрачностью, и «тусклые» выходили белыми
DIM = tuple(int(BG[i] + (255 - BG[i]) * 0.26) for i in range(3))
COLS, ROWS = 20, 5
WON = {6, 34, 51, 88}          # четверо из ста — дошли

img = Image.new("RGB", (W, H), BG)
# мягкое свечение фона к центру
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([W * 0.18, H * 0.10, W * 0.82, H * 0.95],
                             fill=ACC + (26,))
img = Image.alpha_composite(img.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(90)))
d = ImageDraw.Draw(img)

pad_x, pad_top = 64, 96
cw = (W - pad_x * 2) / COLS
ch = (H - pad_top - 74) / ROWS
fh = ch * 0.62                    # рост человечка

for i in range(COLS * ROWS):
    cx = pad_x + cw * (i % COLS) + cw / 2
    cy = pad_top + ch * (i // COLS) + ch / 2
    win = i in WON
    col = ACC if win else DIM
    lw = max(2, int(fh * (0.115 if win else 0.095)))
    r = fh * 0.17
    hy = cy - fh * 0.5 + r
    d.ellipse([cx - r, hy - r, cx + r, hy + r], fill=col)
    d.line([cx, hy + r, cx, cy + fh * 0.10], fill=col, width=lw)          # корпус
    d.line([cx - fh * 0.20, cy + fh * 0.50, cx, cy + fh * 0.10],
           fill=col, width=lw)                                            # ноги
    d.line([cx + fh * 0.20, cy + fh * 0.50, cx, cy + fh * 0.10], fill=col, width=lw)
    d.line([cx - fh * 0.22, cy - fh * 0.02, cx + fh * 0.22, cy - fh * 0.02],
           fill=col, width=max(2, int(lw * 0.85)))                        # руки

# подсветка дошедших
hl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(hl)
for i in WON:
    cx = pad_x + cw * (i % COLS) + cw / 2
    cy = pad_top + ch * (i // COLS) + ch / 2
    hd.ellipse([cx - cw * 0.5, cy - ch * 0.5, cx + cw * 0.5, cy + ch * 0.5],
               fill=ACC + (70,))
img = Image.alpha_composite(img, hl.filter(ImageFilter.GaussianBlur(16)))
img.convert("RGB").save("willpower.jpg", quality=90)
print("ok -> willpower.jpg")

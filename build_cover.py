"""Generate 3:4 Xiaohongshu cover images for the job-personality test."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
OUT = os.path.dirname(os.path.abspath(__file__))
NAVY = (31, 56, 100)
ORANGE = (255, 107, 74)
CREAM = (247, 241, 232)
WHITE = (255, 255, 255)
MUTED_D = (255, 255, 255, 190)
MUTED_L = (110, 110, 110)

BOLD = "C:/Windows/Fonts/msyhbd.ttc"
REG = "C:/Windows/Fonts/msyh.ttc"


def font(path, size):
    for p in (path, "C:/Windows/Fonts/simhei.ttf", "C:/Windows/Fonts/arialbd.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def text_w(draw, s, f):
    b = draw.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def cover(path, dark=True):
    bg = NAVY if dark else CREAM
    fg = WHITE if dark else NAVY
    sub = (255, 255, 255, 200) if dark else (90, 90, 90)
    chip_bg = (255, 255, 255, 22) if dark else WHITE
    chip_line = (255, 255, 255, 60) if dark else (215, 205, 190)
    chip_fg = WHITE if dark else NAVY

    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img, "RGBA")

    # decorative rings
    d.ellipse((W - 420, -260, W + 220, 380), outline=(255, 255, 255, 26) if dark else (31, 56, 100, 22), width=3)
    d.ellipse((W - 300, -140, W + 100, 260), outline=(255, 255, 255, 18) if dark else (31, 56, 100, 16), width=2)

    pad = 92

    # kicker
    fk = font(BOLD, 34)
    d.text((pad, 150), "求职干货 · 原创测试", font=fk, fill=ORANGE if dark else ORANGE)

    # title
    ft = font(BOLD, 116)
    lines = ["12 道题", "测出你适合", "什么工作"]
    y = 250
    for i, line in enumerate(lines):
        if i == 2:
            # highlight last line with an underline bar
            w = text_w(d, line, ft)
            d.rectangle((pad - 6, y + 138, pad + w + 6, y + 152), fill=ORANGE)
        d.text((pad, y), line, font=ft, fill=fg)
        y += 158

    # subtitle
    fs = font(REG, 40)
    d.text((pad, 790), "2 分钟  ·  4 种类型  ·  免费", font=fs, fill=sub)

    # chips 2x2
    fchip = font(BOLD, 36)
    names = ["猎手型", "工匠型", "联结型", "守序型"]
    cw, ch, gap = 380, 88, 24
    x0, y0 = pad, 900
    for i, n in enumerate(names):
        cx = x0 + (i % 2) * (cw + gap)
        cy = y0 + (i // 2) * (ch + gap)
        d.rounded_rectangle((cx, cy, cx + cw, cy + ch), radius=20, fill=chip_bg, outline=chip_line, width=2)
        tw = text_w(d, n, fchip)
        d.text((cx + (cw - tw) / 2, cy + (ch - 46) / 2), n, font=fchip, fill=chip_fg)

    # bottom bar
    d.rectangle((0, H - 190, W, H), fill=(0, 0, 0, 40) if dark else (31, 56, 100, 12))
    fb = font(BOLD, 38)
    d.text((pad, H - 130), "凭第一反应选  ·  测完有结果", font=fb, fill=fg)
    fa = font(REG, 30)
    arrow = "→"
    d.text((W - pad - text_w(d, arrow, fa), H - 128), arrow, font=fa, fill=ORANGE)

    img.save(path, quality=95)
    print("saved", path)


if __name__ == "__main__":
    cover(os.path.join(OUT, "cover_dark.png"), dark=True)
    cover(os.path.join(OUT, "cover_light.png"), dark=False)

# render_meme_v2.py — renders the GTA VI Steam-invoice meme (meme v2, Round 8).
#
# Concept: a fake official Steam invoice. The joke is bureaucratic and
# specific — a pre-order placed 17 Sep 2013 (GTA V launch day, when the
# wait for VI began) finally DELIVERED 19 Nov 2026, i.e. 13 years,
# 2 months, 2 days (4,811 days) late, with a $0.00 late fee because
# "your patience was the payment". The top entries on the board win with
# exactly this format (fake official documents); v1 lost with a flat
# "still waiting" line on a beach photo.
#
# Output: meme-v2.png, 1920x1280 (same canvas as v1), PIL only.
# Run: python3 render_meme_v2.py  (writes meme-v2.png next to the script)

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1280
FONT_DIR = "/home/hatch/workspace/makefun/new4/fonts"
DEJAVU = "/usr/share/fonts/truetype/dejavu"

ANTON = f"{FONT_DIR}/Anton-Regular.ttf"
SANS = f"{DEJAVU}/DejaVuSans.ttf"
SANS_BOLD = f"{DEJAVU}/DejaVuSans-Bold.ttf"
MONO = f"{DEJAVU}/DejaVuSansMono.ttf"
MONO_BOLD = f"{DEJAVU}/DejaVuSansMono-Bold.ttf"

DARK = (23, 26, 33)        # Steam dark navy
STEAM_BLUE = (27, 40, 56)  # Steam header blue
INK = (27, 40, 56)         # body ink
GREY = (90, 100, 110)
LIGHT_LINE = (199, 213, 224)
PAPER = (255, 255, 255)
AMBER_BG = (255, 243, 205)  # delivery-status box
AMBER_BORDER = (180, 130, 30)
RED = (192, 57, 43)         # stamp + punchline accent
GREEN = (27, 94, 32)        # DELIVERED

MARGIN = 80
RIGHT = W - MARGIN


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, size, max_w):
    """Largest font size <= `size` whose text fits `max_w`."""
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font(path, 10)


def draw_right(draw, y, text, f, fill):
    draw.text((RIGHT, y), text, font=f, fill=fill, anchor="ra")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header bar: Steam dark -------------------------------------
    d.rectangle([0, 0, W, 150], fill=STEAM_BLUE)
    d.text((MARGIN, 18), "STEAM", font=font(ANTON, 96), fill=(255, 255, 255))
    d.text((RIGHT, 52), "ORDER CONFIRMATION", font=font(SANS_BOLD, 42),
           fill=(199, 213, 224), anchor="ra")
    # thin accent rule under the header
    d.rectangle([0, 150, W, 156], fill=(102, 192, 244))

    # ---- INVOICE title row ------------------------------------------
    d.text((MARGIN, 190), "INVOICE", font=font(ANTON, 76), fill=INK)
    draw_right(d, 205, "INVOICE # GTA6-2013-0917", font(MONO_BOLD, 30), INK)
    draw_right(d, 245, "ISSUED: 19 NOVEMBER 2026", font(MONO, 28), GREY)
    d.line([MARGIN, 300, RIGHT, 300], fill=LIGHT_LINE, width=2)

    # ---- order details: two columns ---------------------------------
    y0 = 330
    d.text((MARGIN, y0), "BILLED TO", font=font(SANS_BOLD, 26), fill=GREY)
    d.text((MARGIN, y0 + 40), "Jason & Lucia", font=font(SANS_BOLD, 44), fill=INK)
    d.text((MARGIN, y0 + 95), "Vice City, Leonida",
           font=font(SANS, 30), fill=INK)
    d.text((MARGIN, y0 + 135), "jason.and.lucia@vicecity.gg",
           font=font(MONO, 26), fill=GREY)

    rx = 1150
    rows = [
        ("ORDER DATE", "17 SEP 2013"),
        ("PAYMENT", "VISA .... 2013"),
        ("AMOUNT PAID", "$59.99"),
        ("STATUS", "PAID IN FULL"),
    ]
    for i, (k, v) in enumerate(rows):
        y = y0 + i * 48
        d.text((rx, y), k, font=font(MONO_BOLD, 28), fill=GREY)
        d.text((rx + 260, y), v, font=font(MONO_BOLD, 28), fill=INK)

    # ---- item table ---------------------------------------------------
    ty = 560
    d.line([MARGIN, ty, RIGHT, ty], fill=LIGHT_LINE, width=2)
    d.text((MARGIN, ty + 18), "ITEM", font=font(SANS_BOLD, 26), fill=GREY)
    d.text((RIGHT - 260, ty + 18), "QTY", font=font(SANS_BOLD, 26), fill=GREY)
    draw_right(d, ty + 18, "PRICE", font(SANS_BOLD, 26), GREY)
    d.text((MARGIN, ty + 58), "Grand Theft Auto VI — Pre-order (PC)",
           font=font(SANS_BOLD, 38), fill=INK)
    d.text((RIGHT - 260, ty + 62), "1", font=font(SANS, 34), fill=INK)
    draw_right(d, ty + 62, "$59.99", font(SANS, 34), INK)
    d.line([MARGIN, ty + 120, RIGHT, ty + 120], fill=LIGHT_LINE, width=2)
    d.text((MARGIN, ty + 138), "TOTAL PAID", font=font(SANS_BOLD, 32), fill=INK)
    draw_right(d, ty + 138, "$59.99", font(SANS_BOLD, 32), INK)

    # ---- delivery status box (the punchline) -------------------------
    bx0, by0, bx1, by1 = MARGIN, 760, RIGHT, 1085
    d.rectangle([bx0, by0, bx1, by1], fill=AMBER_BG,
                outline=AMBER_BORDER, width=4)
    d.text((bx0 + 36, by0 + 18), "DELIVERY STATUS",
           font=font(SANS_BOLD, 28), fill=GREY)
    f = fit(d, "DELIVERED — 19 NOVEMBER 2026", ANTON, 62, bx1 - bx0 - 72)
    d.text((bx0 + 36, by0 + 50), "DELIVERED — 19 NOVEMBER 2026",
           font=f, fill=GREEN)
    d.text((bx0 + 36, by0 + 128), "TIME IN TRANSIT:",
           font=font(SANS_BOLD, 28), fill=INK)
    f2 = fit(d, "13 YEARS, 2 MONTHS, 2 DAYS", ANTON, 90, bx1 - bx0 - 72)
    d.text((bx0 + 36, by0 + 160), "13 YEARS, 2 MONTHS, 2 DAYS",
           font=f2, fill=RED)
    d.text((bx0 + 36, by0 + 262), "(4,811 days — the wait was the hard part)",
           font=font(SANS, 26), fill=INK)

    # ---- red rubber stamp: 13 YEARS LATE ------------------------------
    stamp = Image.new("RGBA", (720, 200), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sf = font(ANTON, 88)
    sd.rectangle([6, 6, 714, 194], outline=RED, width=8)
    sd.text((360, 100), "13 YEARS LATE", font=sf, fill=RED, anchor="mm")
    stamp = stamp.rotate(-11, expand=True, resample=Image.BICUBIC)
    # fade the stamp slightly so it reads as ink, not a solid block
    alpha = stamp.split()[3].point(lambda a: int(a * 0.88))
    stamp.putalpha(alpha)
    img.paste(stamp, (1180, 690), stamp)

    # ---- late fee + footer ---------------------------------------------
    d.text((MARGIN, 1115),
           "Late delivery fee: $0.00 — your patience was the payment.",
           font=font(SANS_BOLD, 34), fill=INK)
    d.text((MARGIN, 1170),
           "Thank you for shopping on Steam. Your 13 years of patience are appreciated.",
           font=font(SANS, 28), fill=GREY)
    d.text((MARGIN, 1225),
           "Parody — not affiliated with Steam, Valve, or Rockstar Games. No refunds on 13 years of waiting.",
           font=font(MONO, 20), fill=GREY)

    img.save("meme-v2.png")
    print("wrote meme-v2.png", img.size)


if __name__ == "__main__":
    main()

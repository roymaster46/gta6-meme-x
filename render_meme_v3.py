# render_meme_v3.py — renders the GTA VI court-subpoena meme (meme v3, Round 9).
#
# Concept: a fake official court SUBPOENA DUCES TECUM from the Leonida
# County Court. The People of Leonida command Rockstar Games to PRODUCE
# one (1) copy of Grand Theft Auto VI, pre-ordered 17 Sep 2013 and never
# delivered — 13 years, 2 months, 2 days (4,811 days) overdue. The second
# punchline is the penalty for non-compliance: thirteen (13) additional
# years of waiting, to be served consecutively.
#
# Why this format: the board's winners are all fake official Leonida
# documents, and a full scan of all 2,850 leaderboard titles on
# 20 Nov 2026 ~19:00 WIB found ZERO entries using a subpoena (jury
# summons exists at #126, court summons at #145/#155, but a subpoena —
# an order to PRODUCE the game — is unused). It is the same winning
# family, a different joke angle, and a different document.
#
# Why v2 failed and what changes here (the #1 priority is CLEAN
# EXECUTION): v2's rotated "13 YEARS LATE" stamp was pasted ON TOP of
# the punchline "13 YEARS, 2 MONTHS, 2 DAYS" and the "(4,811 days...)"
# line, and it jutted outside its box — verified by looking at the
# rendered v2 image. v2 finished 0-12 head-to-head, rank #2,817,
# judge 181.091. In v3 there is NO rotated stamp and NO element overlaps
# any text: every block gets its own reserved rectangle, the court seal
# lives in a dedicated empty footer zone on the right (no text under it),
# and the punchline sits alone inside its own bordered box.
#
# Output: meme-v3.png, 1920x1280, PIL only.
# Run: python3 render_meme_v3.py  (writes meme-v3.png next to the script)

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1280
FONT_DIR = "/home/hatch/workspace/makefun/new4/fonts"
DEJAVU = "/usr/share/fonts/truetype/dejavu"

ANTON = f"{FONT_DIR}/Anton-Regular.ttf"
SANS = f"{DEJAVU}/DejaVuSans.ttf"
SANS_BOLD = f"{DEJAVU}/DejaVuSans-Bold.ttf"
MONO = f"{DEJAVU}/DejaVuSansMono.ttf"
MONO_BOLD = f"{DEJAVU}/DejaVuSansMono-Bold.ttf"

PAPER = (255, 255, 255)
INK = (18, 22, 28)
GREY = (96, 104, 112)
RULE = (150, 158, 166)
RED = (178, 34, 34)          # punchline + court red, used only for text/borders
RED_BG = (253, 238, 238)     # overdue box fill
BLUE_BG = (238, 242, 247)    # item-to-produce box fill
BLUE_LINE = (70, 90, 120)

MARGIN = 90
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


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- court-document double border (frame only, never over text) --
    d.rectangle([26, 26, W - 26, H - 26], outline=INK, width=4)
    d.rectangle([40, 40, W - 40, H - 40], outline=RULE, width=1)

    # ---- header: court name, centred ----------------------------------
    y = 54
    f = fit(d, "STATE OF LEONIDA", MONO_BOLD, 30, W - 2 * MARGIN)
    d.text((W // 2, y), "STATE OF LEONIDA", font=f, fill=GREY, anchor="ma")
    y += 36
    f = fit(d, "LEONIDA COUNTY COURT", ANTON, 78, W - 2 * MARGIN)
    d.text((W // 2, y), "LEONIDA COUNTY COURT", font=f, fill=INK, anchor="ma")
    y += 98
    f = fit(d, "TWELFTH JUDICIAL CIRCUIT  •  VICE CITY DIVISION",
            MONO, 27, W - 2 * MARGIN)
    d.text((W // 2, y), "TWELFTH JUDICIAL CIRCUIT  •  VICE CITY DIVISION",
           font=f, fill=GREY, anchor="ma")
    y += 40
    d.line([MARGIN, y, RIGHT, y], fill=INK, width=3)
    y += 16

    # ---- case row -------------------------------------------------------
    d.text((MARGIN, y), "CASE NO. 2013-0917",
           font=font(MONO_BOLD, 30), fill=INK)
    d.text((RIGHT, y), "FILED: 19 NOVEMBER 2026",
           font=font(MONO_BOLD, 30), fill=INK, anchor="ra")
    y += 44
    d.line([MARGIN, y, RIGHT, y], fill=RULE, width=2)
    y += 16

    # ---- document title -------------------------------------------------
    f = fit(d, "SUBPOENA DUCES TECUM", ANTON, 92, W - 2 * MARGIN)
    d.text((W // 2, y), "SUBPOENA DUCES TECUM", font=f, fill=RED, anchor="ma")
    y += 112
    f = fit(d, "TO PRODUCE EVIDENCE  —  GRAND THEFT AUTO VI",
            MONO_BOLD, 28, W - 2 * MARGIN)
    d.text((W // 2, y), "TO PRODUCE EVIDENCE  —  GRAND THEFT AUTO VI",
           font=f, fill=INK, anchor="ma")
    y += 44

    # ---- parties: two columns, own rows, nothing overlaps --------------
    d.text((MARGIN, y), "PLAINTIFF:", font=font(SANS_BOLD, 28), fill=GREY)
    d.text((MARGIN + 210, y), "The People of Leonida",
           font=font(SANS_BOLD, 30), fill=INK)
    d.text((RIGHT, y), "DEFENDANT:  Rockstar Games",
           font=font(SANS_BOLD, 30), fill=INK, anchor="ra")
    y += 42
    d.text((MARGIN, y), "TO:", font=font(SANS_BOLD, 28), fill=GREY)
    d.text((MARGIN + 210, y), "Rockstar Games, Vice City, Leonida",
           font=font(SANS, 30), fill=INK)
    y += 46

    # ---- the command (wrapped paragraph, full width, clear zone) --------
    cmd = ("YOU ARE HEREBY COMMANDED to appear before this Court and to "
           "PRODUCE the following item, pre-ordered 17 September 2013 "
           "and never delivered:")
    cf = font(SANS, 29)
    for line in wrap(d, cmd, cf, RIGHT - MARGIN):
        d.text((MARGIN, y), line, font=cf, fill=INK)
        y += 38
    y += 10

    # ---- item to be produced (its own bordered box) ---------------------
    bx0, by0, bx1, by1 = MARGIN, y, RIGHT, y + 84
    d.rectangle([bx0, by0, bx1, by1], fill=BLUE_BG,
                outline=BLUE_LINE, width=3)
    d.text((bx0 + 30, by0 + 10), "ITEM TO BE PRODUCED:",
           font=font(SANS_BOLD, 26), fill=GREY)
    d.text((bx0 + 30, by0 + 42),
           "ONE (1) copy of Grand Theft Auto VI  —  $59.99, PAID IN FULL",
           font=font(SANS_BOLD, 32), fill=INK)
    y = by1 + 18

    # ---- THE PUNCHLINE: overdue box, text alone inside it ---------------
    # No stamp, no rotation, no overlay of any kind: the big red line
    # and its sub-line are the only marks inside this box.
    bx0, by0, bx1, by1 = MARGIN, y, RIGHT, y + 196
    d.rectangle([bx0, by0, bx1, by1], fill=RED_BG, outline=RED, width=4)
    d.text((bx0 + 36, by0 + 12), "TIME OVERDUE",
           font=font(SANS_BOLD, 27), fill=GREY)
    f2 = fit(d, "13 YEARS, 2 MONTHS, 2 DAYS", ANTON, 80, bx1 - bx0 - 72)
    d.text((bx0 + 36, by0 + 46), "13 YEARS, 2 MONTHS, 2 DAYS",
           font=f2, fill=RED)
    d.text((bx0 + 36, by0 + 142), "(4,811 days — and counting)",
           font=font(SANS, 29), fill=INK)
    y = by1 + 18

    # ---- penalty: second punchline, its own clear line -------------------
    pen = ("FAILURE TO COMPLY: thirteen (13) additional years of waiting, "
           "to be served consecutively.")
    pf = font(SANS_BOLD, 32)
    for line in wrap(d, pen, pf, RIGHT - MARGIN):
        d.text((MARGIN, y), line, font=pf, fill=INK)
        y += 44
    y += 14
    d.line([MARGIN, y, RIGHT, y], fill=RULE, width=2)
    y += 20

    # ---- footer: signature LEFT, seal RIGHT in its own empty zone -------
    # The seal zone (x 1640..1840, y ~1080..1240) holds no text at all.
    d.text((MARGIN, y), "Issued: 19 November 2026",
           font=font(MONO, 26), fill=GREY)
    d.text((MARGIN, y + 40), "Clerk of the Court, Leonida County",
           font=font(SANS, 28), fill=INK)
    d.line([MARGIN, y + 84, MARGIN + 520, y + 84], fill=INK, width=2)
    d.text((MARGIN, y + 94), "Signature of the Clerk",
           font=font(SANS, 22), fill=GREY)

    # Court seal: two concentric circles + star, drawn only inside the
    # reserved footer-right rectangle. It touches no text by design.
    # Footer must end well above the disclaimer line (H-78); the seal's
    # bottom edge is cy + 64, checked against that bound when rendered.
    cx, cy = 1740, y + 52
    assert cy + 64 < H - 90, f"seal overflows footer: cy={cy}"
    d.ellipse([cx - 64, cy - 64, cx + 64, cy + 64], outline=RED, width=4)
    d.ellipse([cx - 50, cy - 50, cx + 50, cy + 50], outline=RED, width=2)
    d.text((cx, cy - 42), "LEONIDA", font=font(MONO_BOLD, 18),
           fill=RED, anchor="ma")
    d.text((cx, cy - 10), "★", font=font(SANS_BOLD, 38), fill=RED,
           anchor="mm")
    d.text((cx, cy + 24), "COUNTY COURT", font=font(MONO_BOLD, 13),
           fill=RED, anchor="ma")

    # ---- parody disclaimer (bottom, clear of the seal zone) -------------
    d.text((MARGIN, H - 78),
           "Parody — not affiliated with Rockstar Games or Take-Two Interactive. No refunds on 13 years of waiting.",
           font=font(MONO, 19), fill=GREY)

    img.save("meme-v3.png")
    print("wrote meme-v3.png", img.size)


if __name__ == "__main__":
    main()

"""
Regenerate OPPO/HeyTap composite with OnePlus device screenshots
"""
import os
from PIL import Image, ImageDraw, ImageFont

SCREENSHOT_DIR = r'c:\Users\jane.yan\competitive-analysis\screenshots\OPPO\账号注销'
OUTPUT = r'c:\Users\jane.yan\competitive-analysis\reports\oppo_account_deletion_composite.png'

BG_COLOR = (255, 255, 255)
BORDER_COLOR = (210, 210, 215)
CANVAS_W = 2400
PADDING = 40
CARD_PADDING = 16
SCREENSHOT_MAX_W = 360
SCREENSHOT_MAX_H = 640
TITLE_H = 70
SECTION_HEADER_H = 50

def load_font(size):
    font_paths = ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/msyhbd.ttc",
                  "C:/Windows/Fonts/simsun.ttc", "C:/Windows/Fonts/arial.ttf"]
    for fp in font_paths:
        if os.path.exists(fp):
            try: return ImageFont.truetype(fp, size)
            except: pass
    return ImageFont.load_default()

def load_and_resize(path, max_w, max_h):
    img = Image.open(path).convert('RGB')
    w, h = img.size
    ratio = min(max_w / w, max_h / h, 1.0)
    if ratio < 1.0:
        return img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
    return img

def draw_arrow(draw, x1, y1, x2, y2, color, width=3):
    import math
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 12
    ax1 = x2 - arrow_len * math.cos(angle - math.pi/6)
    ay1 = y2 - arrow_len * math.sin(angle - math.pi/6)
    ax2 = x2 - arrow_len * math.cos(angle + math.pi/6)
    ay2 = y2 - arrow_len * math.sin(angle + math.pi/6)
    draw.polygon([(x2, y2), (ax1, ay1), (ax2, ay2)], fill=color)

def create_card(draw, canvas, x, y, img, label, step_num, badge_color):
    img_w, img_h = img.size
    card_w = img_w + CARD_PADDING * 2
    card_h = img_h + CARD_PADDING * 2 + 55
    draw.rectangle([(x, y), (x + card_w, y + card_h)], fill=(255,255,255), outline=BORDER_COLOR, width=2)
    canvas.paste(img, (x + CARD_PADDING, y + CARD_PADDING))
    badge_x, badge_y = x + CARD_PADDING - 4, y + CARD_PADDING - 4
    badge_r = 15
    draw.ellipse([(badge_x, badge_y), (badge_x + badge_r*2, badge_y + badge_r*2)], fill=badge_color)
    draw.text((badge_x + badge_r - 4, badge_y + badge_r - 8), str(step_num), fill=(255,255,255), font=load_font(14))
    label_y = y + CARD_PADDING + img_h + 10
    for j, line in enumerate(label.split('\n')):
        draw.text((x + CARD_PADDING, label_y + j * 18), line, fill=(30,30,35), font=load_font(12))
    return card_w, card_h

def main():
    # Flow: Settings path (OnePlus/OPPO - same HeyTap account system)
    settings_flow = [
        ('step01_settings_home.png', 'Step 1: Settings Home\nOnePlus/OPPO ColorOS', 1),
        ('step02_account_page.png', 'Step 2: Account Center\nTap Avatar at top', 2),
        ('step03_signin_security.png', 'Step 3: Sign-in & Security\nAccount security settings', 3),
        ('step04_scrolled_down.png', 'Step 4: Scroll to Bottom\nFind Delete Account / More Help', 4),
    ]

    # Web path
    web_flow = [
        ('02_heytap_page.png', 'Step 5 (Web): HeyTap Portal\nid.heytap.com/static/', 5),
    ]

    header_bg = (30, 140, 80)
    arrow_color = (30, 140, 80)
    badge_color = (30, 140, 80)
    section_bg = (240, 250, 245)

    # Calculate layout
    flow1_items = settings_flow
    flow2_items = web_flow

    cards_per_row1 = min(4, len(flow1_items))
    spacing_x1 = (CANVAS_W - PADDING * 2 - cards_per_row1 * (SCREENSHOT_MAX_W + 80)) // (cards_per_row1 + 1)
    n_rows1 = (len(flow1_items) + cards_per_row1 - 1) // cards_per_row1
    section1_h = n_rows1 * (SCREENSHOT_MAX_H + 120)

    cards_per_row2 = min(4, len(flow2_items))
    spacing_x2 = (CANVAS_W - PADDING * 2 - cards_per_row2 * (SCREENSHOT_MAX_W + 80)) // (cards_per_row2 + 1)
    n_rows2 = (len(flow2_items) + cards_per_row2 - 1) // cards_per_row2
    section2_h = n_rows2 * (SCREENSHOT_MAX_H + 120)

    notes_h = 380
    total_h = PADDING + TITLE_H + PADDING + SECTION_HEADER_H + PADDING + section1_h + PADDING
    total_h += SECTION_HEADER_H + PADDING + section2_h + PADDING + notes_h + PADDING

    print(f"Canvas: {CANVAS_W} x {total_h}")
    canvas = Image.new('RGB', (CANVAS_W, total_h), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    # Title
    draw.rectangle([(0, 0), (CANVAS_W, TITLE_H)], fill=header_bg)
    draw.text((PADDING, 10), "Competitive Analysis: OPPO / OnePlus HeyTap Account Deletion Flow", fill=(255,255,255), font=load_font(26))
    draw.text((PADDING, TITLE_H - 24), "OnePlus & OPPO share the same HeyTap account system | Captured from OnePlus device (ColorOS) | 2025-06-25", fill=(200, 235, 210), font=load_font(13))

    y = TITLE_H + PADDING * 2

    # ── Section 1: Settings Path ──
    draw.rectangle([(PADDING, y), (CANVAS_W - PADDING, y + SECTION_HEADER_H)], fill=section_bg, outline=BORDER_COLOR, width=1)
    draw.text((PADDING + 16, y + 8), "Section 1: Phone Settings Path — OnePlus/OPPO (ColorOS)", fill=(30,30,35), font=load_font(20))
    draw.text((PADDING + 16, y + 32), "Settings > Avatar > Sign-in & Security > More Help > Delete Personal Account", fill=(120,130,120), font=load_font(13))
    y += SECTION_HEADER_H + PADDING

    for i, (filename, label, step_num) in enumerate(settings_flow):
        col = i % cards_per_row1
        x = PADDING + spacing_x1 + col * (SCREENSHOT_MAX_W + 80 + spacing_x1)
        card_y = y + (i // cards_per_row1) * (SCREENSHOT_MAX_H + 120)

        filepath = os.path.join(SCREENSHOT_DIR, filename)
        if os.path.exists(filepath) and os.path.getsize(filepath) > 50000:
            img = load_and_resize(filepath, SCREENSHOT_MAX_W, SCREENSHOT_MAX_H)
            card_w, card_h = create_card(draw, canvas, x, card_y, img, label, step_num, badge_color)
            if col < cards_per_row1 - 1 and i < len(settings_flow) - 1:
                arrow_x1 = x + card_w
                draw_arrow(draw, arrow_x1, card_y + card_h//2, x + SCREENSHOT_MAX_W + 80 + spacing_x1 - 10, card_y + card_h//2, arrow_color)
        else:
            # Placeholder text card
            ph_w = SCREENSHOT_MAX_W + CARD_PADDING*2
            ph_h = 450
            draw.rectangle([(x, card_y), (x+ph_w, card_y+ph_h)], fill=(250,248,245), outline=(200,200,200))
            draw.text((x+CARD_PADDING, card_y+ph_h//2-20), f"[Screenshot]", fill=(150,150,150), font=load_font(12))
            draw.text((x+CARD_PADDING, card_y+ph_h//2+10), label.replace('\n',' ')[:40], fill=(100,100,100), font=load_font(11))

    y += n_rows1 * (SCREENSHOT_MAX_H + 120) + PADDING

    # ── Section 2: Web Path ──
    draw.rectangle([(PADDING, y), (CANVAS_W - PADDING, y + SECTION_HEADER_H)], fill=section_bg, outline=BORDER_COLOR, width=1)
    draw.text((PADDING + 16, y + 8), "Section 2: Web-Based Path — id.heytap.com", fill=(30,30,35), font=load_font(20))
    draw.text((PADDING + 16, y + 32), "id.heytap.com > Login > Personal Data Management > Delete Account OR Delete Personal Data (partial)", fill=(120,130,120), font=load_font(13))
    y += SECTION_HEADER_H + PADDING

    for i, (filename, label, step_num) in enumerate(web_flow):
        x = PADDING + spacing_x2 + i * (SCREENSHOT_MAX_W + 80 + spacing_x2)
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        if os.path.exists(filepath) and os.path.getsize(filepath) > 20000:
            img = load_and_resize(filepath, SCREENSHOT_MAX_W, SCREENSHOT_MAX_H)
            create_card(draw, canvas, x, y, img, label, step_num, badge_color)
        else:
            ph_w = SCREENSHOT_MAX_W + CARD_PADDING*2
            ph_h = 450
            draw.rectangle([(x, y), (x+ph_w, y+ph_h)], fill=(250,248,245), outline=(200,200,200))
            draw.text((x+CARD_PADDING, y+ph_h//2), "[Web page screenshot]", fill=(150,150,150), font=load_font(12))
            draw.text((x+CARD_PADDING, y+ph_h//2+30), label, fill=(100,100,100), font=load_font(11))

    y += n_rows2 * (SCREENSHOT_MAX_H + 120) + PADDING

    # ── Notes ──
    draw.rectangle([(PADDING, y), (CANVAS_W - PADDING, y + notes_h)], fill=(255,248,240), outline=(240,180,100), width=2)
    notes = [
        "KEY FINDINGS: OPPO / OnePlus (HeyTap Account) Deletion",
        "",
        "1. TWO DELETION PATHS: Native Settings (ColorOS) AND Web (id.heytap.com).",
        "2. UNIQUE PARTIAL DATA DELETE: OPPO is the ONLY Chinese OEM that allows selectively deleting personal data",
        "   (avatar, nickname, activity history) WITHOUT deleting the entire account — via id.heytap.com.",
        "   This is the closest equivalent to Google's 'delete a Google service' among Chinese competitors.",
        "3. Both OnePlus and OPPO use the SAME HeyTap account system — identical deletion flow.",
        "4. Processing time: Up to 10 business days for review. NO cooling-off or recovery period.",
        "5. Phone number CAN be reused to register new account after deletion.",
        "6. Identity verification: Phone verification code + Account password (moderate security).",
        "7. Requirements before deletion: No active subscriptions, no pending orders, devices unlinked.",
    ]
    for j, note in enumerate(notes):
        color = (60, 20, 20) if j == 0 else (80, 60, 40)
        f = load_font(20) if j == 0 else load_font(14)
        draw.text((PADDING + 16, y + 16 + j * 22), note, fill=color, font=f)

    canvas.save(OUTPUT, quality=95)
    print(f"Saved: {OUTPUT}")

if __name__ == '__main__':
    main()

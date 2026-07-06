"""
OPPO/OnePlus HeyTap account deletion composite using user's web_deletion screenshots
"""
import os
from PIL import Image, ImageDraw, ImageFont

INPUT_DIR = r'c:\Users\jane.yan\competitive-analysis\screenshots\OnePlus\web_deletion'
OUTPUT = r'c:\Users\jane.yan\competitive-analysis\reports\oppo_account_deletion_composite.png'

BG_COLOR = (255, 255, 255)
BORDER_COLOR = (210, 210, 215)
CANVAS_W = 2400
PADDING = 40
CARD_PADDING = 16

# These are phone browser screenshots - need bigger display
SCREENSHOT_MAX_W = 320
SCREENSHOT_MAX_H = 600
TITLE_H = 70
SECTION_HEADER_H = 50

def load_font(size):
    for fp in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/msyhbd.ttc",
               "C:/Windows/Fonts/simsun.ttc", "C:/Windows/Fonts/arial.ttf"]:
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

def draw_down_arrow(draw, x1, y1, x2, y2, color, width=3):
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
    draw.text((badge_x + badge_r - 4, badge_y + badge_r - 9), str(step_num), fill=(255,255,255), font=load_font(13))
    label_y = y + CARD_PADDING + img_h + 8
    for j, line in enumerate(label.split('\n')):
        draw.text((x + CARD_PADDING + 2, label_y + j * 16), line, fill=(30,30,35), font=load_font(11))
    return card_w, card_h

def main():
    # OnePlus/OPPO web deletion flow (from user's screenshots, in time order)
    flow = [
        ('img_111536.png', 'Step 1: Account Dashboard\nHeyTap personal data mgmt', 1),
        ('img_111627.png', 'Step 2: Delete Account Entry\nSelect delete account option', 2),
        ('img_111818.png', 'Step 3: Choose Deletion Reason\nSelect reason from dropdown', 3),
        ('img_112015.png', 'Step 4: Read Deletion Notice\nReview terms and conditions', 4),
        ('img_112223.png', 'Step 5: Acknowledge Terms\nCheck confirmation boxes', 5),
        ('img_112311.png', 'Step 6: ID Card Verification\nEnter last 6 digits of ID card (身份证后六位)', 6),
        ('img_112601.png', 'Step 7: Confirm Deletion\nFinal confirmation before submit', 7),
        ('img_112643.png', 'Step 8: Deletion Complete\nAccount permanently deleted', 8),
    ]

    header_bg = (30, 140, 80)
    arrow_color = (30, 140, 80)
    badge_color = (30, 140, 80)
    section_bg = (240, 250, 245)

    cards_per_row = 4  # 4 screenshots per row (2 rows of 4)
    spacing_x = max(10, (CANVAS_W - PADDING * 2 - cards_per_row * (SCREENSHOT_MAX_W + 80)) // (cards_per_row + 1))
    n_rows = (len(flow) + cards_per_row - 1) // cards_per_row
    flow_section_h = n_rows * (SCREENSHOT_MAX_H + 120)

    notes_h = 280
    total_h = PADDING + TITLE_H + PADDING + SECTION_HEADER_H + PADDING + flow_section_h + PADDING
    total_h += notes_h + PADDING

    print(f"Canvas: {CANVAS_W} x {total_h}")
    canvas = Image.new('RGB', (CANVAS_W, total_h), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    # ── Title ──
    draw.rectangle([(0, 0), (CANVAS_W, TITLE_H)], fill=header_bg)
    draw.text((PADDING, 10), "OPPO / OnePlus HeyTap Account Deletion — Complete Web Flow", fill=(255,255,255), font=load_font(26))
    draw.text((PADDING, TITLE_H - 24), "id.heytap.com web-based deletion | OnePlus & OPPO share the same HeyTap account system | User-captured screenshots", fill=(200, 235, 210), font=load_font(13))

    y = TITLE_H + PADDING * 2

    # ── Section 1: Main Flow ──
    draw.rectangle([(PADDING, y), (CANVAS_W - PADDING, y + SECTION_HEADER_H)], fill=section_bg, outline=BORDER_COLOR, width=1)
    draw.text((PADDING + 16, y + 8), "Section 1: Complete Web-Based Account Deletion Flow (id.heytap.com)", fill=(30,30,35), font=load_font(20))
    draw.text((PADDING + 16, y + 32), "Dashboard → Delete Account → Reason → Notice → Acknowledge → ID Card Verify (后六位) → Confirm → Complete (10 working days)", fill=(120,130,120), font=load_font(12))
    y += SECTION_HEADER_H + PADDING

    step_counter = 0
    for i, (filename, label, step_num) in enumerate(flow):
        row = i // cards_per_row
        col = i % cards_per_row
        x = PADDING + spacing_x + col * (SCREENSHOT_MAX_W + 80 + spacing_x)
        card_y = y + row * (SCREENSHOT_MAX_H + 120)

        filepath = os.path.join(INPUT_DIR, filename)
        if os.path.exists(filepath):
            img = load_and_resize(filepath, SCREENSHOT_MAX_W, SCREENSHOT_MAX_H)
            step_counter += 1
            card_w, card_h = create_card(draw, canvas, x, card_y, img, label, step_num, badge_color)
            # Arrow between cards in same row
            if col < cards_per_row - 1 and i < len(flow) - 1:
                next_col = col + 1
                if next_col < cards_per_row:
                    draw_arrow(draw, x + card_w, card_y + card_h // 2,
                              x + SCREENSHOT_MAX_W + 80 + spacing_x - 10, card_y + card_h // 2, arrow_color)
        else:
            print(f"  Missing: {filename}")

    y += n_rows * (SCREENSHOT_MAX_H + 120) + PADDING

    # ── Notes ──
    draw.rectangle([(PADDING, y), (CANVAS_W - PADDING, y + notes_h)], fill=(255,248,240), outline=(240,180,100), width=2)
    notes = [
        "核心发现：OPPO / 一加（HeyTap）网页端账号注销",
        "",
        "1. 简易网页流程：通过 id.heytap.com 进行账号删除，仅需验证身份证后六位——无需短信验证码或密码二次确认。",
        "2. 8 步流程：仪表盘 → 删除账号 → 选择原因 → 阅读须知 → 勾选确认 → 身份证验证 → 最终确认 → 完成。审核最多 10 个工作日。",
        "3. 独特优势：支持选择性删除个人数据（头像、昵称、使用记录）而不删除整个账号——最接近 Google 单业务删除的国产方案。",
        "4. 一加与 OPPO 共用同一 HeyTap 账号体系——两个品牌流程完全一致。",
        "5. 无冷静期/恢复期。账号删除后手机号可重新注册。",
    ]
    for j, note in enumerate(notes):
        color = (60, 20, 20) if j == 0 else (80, 60, 40)
        f = load_font(20) if j == 0 else load_font(14)
        draw.text((PADDING + 16, y + 16 + j * 22), note, fill=color, font=f)

    canvas.save(OUTPUT, quality=95)
    print(f"Saved: {OUTPUT} ({step_counter} screenshots)")

if __name__ == '__main__':
    main()

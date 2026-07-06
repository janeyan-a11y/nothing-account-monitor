"""
Create Huawei account deletion whiteboard composite image
"""
import os
from PIL import Image, ImageDraw, ImageFont

SCREENSHOT_DIR = r'c:\Users\jane.yan\competitive-analysis\screenshots\华为\账号注销'
OUTPUT = r'c:\Users\jane.yan\competitive-analysis\reports\huawei_account_deletion_composite.png'

# Colors
BG_COLOR = (255, 255, 255)
HEADER_BG = (200, 50, 50)       # Huawei red
SECTION_BG = (252, 245, 245)    # light red
BORDER_COLOR = (210, 200, 200)
ARROW_COLOR = (200, 50, 50)
LABEL_COLOR = (60, 20, 20)
STEP_COLOR = (200, 50, 50)
TITLE_COLOR = (255, 255, 255)
WARN_BG = (255, 248, 240)
WARN_BORDER = (240, 180, 100)

CANVAS_W = 2400
PADDING = 40
CARD_PADDING = 16
SCREENSHOT_MAX_W = 350
SCREENSHOT_MAX_H = 620
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

def draw_arrow(draw, x1, y1, x2, y2, color=ARROW_COLOR, width=3):
    import math
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 12
    ax1 = x2 - arrow_len * math.cos(angle - math.pi/6)
    ay1 = y2 - arrow_len * math.sin(angle - math.pi/6)
    ax2 = x2 - arrow_len * math.cos(angle + math.pi/6)
    ay2 = y2 - arrow_len * math.sin(angle + math.pi/6)
    draw.polygon([(x2, y2), (ax1, ay1), (ax2, ay2)], fill=color)

def create_card(draw, canvas, x, y, img, label, step_num):
    img_w, img_h = img.size
    card_w = img_w + CARD_PADDING * 2
    card_h = img_h + CARD_PADDING * 2 + 55

    draw.rectangle([(x, y), (x + card_w, y + card_h)], fill=(255,255,255), outline=BORDER_COLOR, width=2)
    canvas.paste(img, (x + CARD_PADDING, y + CARD_PADDING))

    # Step badge
    badge_x, badge_y = x + CARD_PADDING - 4, y + CARD_PADDING - 4
    badge_r = 16
    draw.ellipse([(badge_x, badge_y), (badge_x + badge_r*2, badge_y + badge_r*2)], fill=STEP_COLOR)
    draw.text((badge_x + badge_r - 4, badge_y + badge_r - 8), str(step_num), fill=(255,255,255), font=load_font(14))

    # Label
    label_y = y + CARD_PADDING + img_h + 10
    for j, line in enumerate(label.split('\n')):
        draw.text((x + CARD_PADDING, label_y + j * 18), line, fill=LABEL_COLOR, font=load_font(12))
    return card_w, card_h

def main():
    # Screenshots for main flow
    flow = [
        ('01_settings_huawei_account.jpg', 'Step 1: Settings\nTap Huawei Account', 1),
        ('02_account_center.jpg', 'Step 2: Account Center\nAccount management page', 2),
        ('03_privacy_center.jpg', 'Step 3: Privacy Center\nOr: Account Security > Security Center', 3),
        ('04_delete_account_button.jpg', 'Step 4: Delete Account\nPermanently delete Huawei ID', 4),
        ('05_enter_password.jpg', 'Step 5: Identity Verification\nEnter account password', 5),
        ('06_confirm_next.jpg', 'Step 6: Confirmation\nReview deletion impact', 6),
        ('07_final_confirm.jpg', 'Step 7: Final Delete\nCheck boxes, confirm', 7),
        ('08_delete_complete.jpg', 'Step 8: Complete\nAccount permanently deleted', 8),
    ]

    # Calculate layout
    cards_per_row = 4
    n_rows = (len(flow) + cards_per_row - 1) // cards_per_row
    spacing_x = (CANVAS_W - PADDING * 2 - cards_per_row * (SCREENSHOT_MAX_W + 80)) // (cards_per_row + 1)

    total_h = PADDING + TITLE_H + PADDING + SECTION_HEADER_H + PADDING
    total_h += n_rows * (SCREENSHOT_MAX_H + 120) + PADDING
    total_h += 400  # for notes section
    total_h += PADDING

    print(f"Canvas: {CANVAS_W} x {total_h}")
    canvas = Image.new('RGB', (CANVAS_W, total_h), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    font_title = load_font(30)
    font_section = load_font(22)
    font_sub = load_font(14)
    font_note = load_font(15)

    # Title bar
    draw.rectangle([(0, 0), (CANVAS_W, TITLE_H)], fill=HEADER_BG)
    draw.text((PADDING, 14), "Competitive Analysis: Huawei Account Deletion Flow", fill=TITLE_COLOR, font=font_title)
    draw.text((PADDING, TITLE_H - 22), "Path: Settings > Huawei Account > Account Center > Privacy/Security Center > Delete Account", fill=(255, 220, 220), font=font_sub)

    y = TITLE_H + PADDING * 2

    # Section header
    draw.rectangle([(PADDING, y), (CANVAS_W - PADDING, y + SECTION_HEADER_H)], fill=SECTION_BG, outline=BORDER_COLOR, width=1)
    draw.text((PADDING + 16, y + 8), "Huawei Account Deletion (销户) — Mobile Flow (EMUI / HarmonyOS)", fill=LABEL_COLOR, font=font_section)
    draw.text((PADDING + 16, y + 32), "Source: Baidu Jingyan / Huawei Official Support — EMUI 8.0+ & HarmonyOS 2.0+", fill=(140,130,130), font=font_sub)
    y += SECTION_HEADER_H + PADDING

    step_counter = 0
    # Layout: 2 rows of 4
    for i, (filename, label, local_step) in enumerate(flow):
        row = i // cards_per_row
        col = i % cards_per_row
        x = PADDING + spacing_x + col * (SCREENSHOT_MAX_W + 80 + spacing_x)
        card_y = y + row * (SCREENSHOT_MAX_H + 130)

        filepath = os.path.join(SCREENSHOT_DIR, filename)
        if os.path.exists(filepath):
            img = load_and_resize(filepath, SCREENSHOT_MAX_W, SCREENSHOT_MAX_H)
            step_counter += 1
            card_w, card_h = create_card(draw, canvas, x, card_y, img, label, step_counter)
            # Arrow between cards in same row
            if col < cards_per_row - 1 and i < len(flow) - 1:
                arrow_x1 = x + card_w
                arrow_y1 = card_y + card_h // 2
                arrow_x2 = x + SCREENSHOT_MAX_W + 80 + spacing_x - 10
                draw_arrow(draw, arrow_x1, arrow_y1, arrow_x2, arrow_y1)
        else:
            print(f"  Missing: {filename}")

    y += n_rows * (SCREENSHOT_MAX_H + 130) + PADDING

    # Notes section
    notes_h = 320
    draw.rectangle([(PADDING, y), (CANVAS_W - PADDING, y + notes_h)], fill=WARN_BG, outline=WARN_BORDER, width=2)
    note_y = y + 16
    notes = [
        "核心发现：华为账号删除（与 Google 对比）",
        "",
        "1. 分散式单业务注销：账号中心无统一「删除单个服务」的入口（如 Google 的 Delete a Google service）。",
        "   各业务独立在 App 内提供注销：华为商城（注销商城账号）、花瓣剪辑（停止服务）等，已确认 2 个，其余待验证。",
        "",
        "2. 无冷静期/恢复期：账号一旦删除，永久消失——无 30 天宽限期（与 Google 不同）。",
        "   但手机号/邮箱可立即用于注册新账号。",
        "",
        "3. 前置条件更严格：须手动解除钱包卡片、未完成订单、自动续费和华为云业务后，",
        "   才能看到「销户」选项。检查项聚合在一个页面上（比 Google 更集中）。",
        "",
        "4. 双入口路径不一致：旧版走「隐私中心」（EMUI 10），新版走「安全中心」（HarmonyOS）——不同系统版本体验不一致。",
        "",
        "5. 无「暂时停用」选项：与 Apple 不同，华为没有暂停/冻结账号功能。",
    ]
    for j, note in enumerate(notes):
        color = LABEL_COLOR if j == 0 else (80, 60, 40)
        font = font_section if j == 0 else font_note
        draw.text((PADDING + 16, note_y + j * 22), note, fill=color, font=font)

    # Footer
    draw.text((PADDING, total_h - 40), "Generated: 2025-06-25 | Source: Baidu Jingyan, Huawei Official Support | 8 screenshots", fill=(150,150,150), font=load_font(12))

    canvas.save(OUTPUT, quality=95)
    print(f"Saved: {OUTPUT}")
    print(f"Placed: {step_counter} screenshots")

if __name__ == '__main__':
    main()

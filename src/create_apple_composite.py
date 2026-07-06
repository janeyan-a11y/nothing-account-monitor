"""
Create Apple Account Deletion & Service Management whiteboard composite
"""
import os
from PIL import Image, ImageDraw, ImageFont

SCREENSHOT_DIR = r'c:\Users\jane.yan\competitive-analysis\screenshots\Apple\账号注销'
OUTPUT = r'c:\Users\jane.yan\competitive-analysis\reports\apple_account_deletion_composite.png'

# Colors - Apple-style
BG_COLOR = (255, 255, 255)
HEADER_BG = (40, 40, 45)       # Apple dark gray
SECTION_BG = (245, 245, 247)   # Apple light gray
BORDER_COLOR = (210, 210, 215)
ARROW_COLOR = (0, 122, 255)    # Apple blue
LABEL_COLOR = (30, 30, 35)
STEP_COLOR = (0, 122, 255)
TITLE_COLOR = (255, 255, 255)
WARN_BG = (255, 248, 240)
WARN_BORDER = (240, 180, 100)
NOTE_BG = (240, 248, 255)
NOTE_BORDER = (150, 200, 230)

CANVAS_W = 2400
PADDING = 40
CARD_PADDING = 16
SCREENSHOT_MAX_W = 380
SCREENSHOT_MAX_H = 560
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

def draw_down_arrow(draw, x1, y1, x2, y2, color=ARROW_COLOR, width=3):
    import math
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 12
    ax1 = x2 - arrow_len * math.cos(angle - math.pi/6)
    ay1 = y2 - arrow_len * math.sin(angle - math.pi/6)
    ax2 = x2 - arrow_len * math.cos(angle + math.pi/6)
    ay2 = y2 - arrow_len * math.sin(angle + math.pi/6)
    draw.polygon([(x2, y2), (ax1, ay1), (ax2, ay2)], fill=color)

def create_card(draw, canvas, x, y, img, label, step_num, badge_color=None):
    if badge_color is None:
        badge_color = STEP_COLOR
    img_w, img_h = img.size
    card_w = img_w + CARD_PADDING * 2
    card_h = img_h + CARD_PADDING * 2 + 55

    draw.rectangle([(x, y), (x + card_w, y + card_h)], fill=(255,255,255), outline=BORDER_COLOR, width=2)
    canvas.paste(img, (x + CARD_PADDING, y + CARD_PADDING))

    # Step badge
    badge_x, badge_y = x + CARD_PADDING - 4, y + CARD_PADDING - 4
    badge_r = 16
    draw.ellipse([(badge_x, badge_y), (badge_x + badge_r*2, badge_y + badge_r*2)], fill=badge_color)
    draw.text((badge_x + badge_r - 4, badge_y + badge_r - 8), str(step_num), fill=(255,255,255), font=load_font(14))

    # Label
    label_y = y + CARD_PADDING + img_h + 10
    for j, line in enumerate(label.split('\n')):
        draw.text((x + CARD_PADDING, label_y + j * 18), line, fill=LABEL_COLOR, font=load_font(12))
    return card_w, card_h

def create_horizontal_flow(draw, canvas, start_x, start_y, screenshots, cards_per_row=3):
    """Layout a horizontal flow row"""
    spacing_x = (CANVAS_W - PADDING * 2 - cards_per_row * (SCREENSHOT_MAX_W + 80)) // (cards_per_row + 1)
    total_w = 0
    max_h = 0

    for i, (filename, label, step_num) in enumerate(screenshots):
        row = i // cards_per_row
        col = i % cards_per_row
        x = PADDING + spacing_x + col * (SCREENSHOT_MAX_W + 80 + spacing_x)
        y = start_y + row * (SCREENSHOT_MAX_H + 120)

        filepath = os.path.join(SCREENSHOT_DIR, filename)
        if os.path.exists(filepath):
            img = load_and_resize(filepath, SCREENSHOT_MAX_W, SCREENSHOT_MAX_H)
            card_w, card_h = create_card(draw, canvas, x, y, img, label, step_num)

            if col < cards_per_row - 1 and i < len(screenshots) - 1:
                arrow_x1 = x + card_w
                arrow_y1 = y + card_h // 2
                arrow_x2 = x + SCREENSHOT_MAX_W + 80 + spacing_x - 10
                draw_arrow(draw, arrow_x1, arrow_y1, arrow_x2, arrow_y1)

            max_h = max(max_h, card_h)
        else:
            print(f"  Missing: {filename}")

    n_rows = (len(screenshots) + cards_per_row - 1) // cards_per_row
    return start_y + n_rows * (SCREENSHOT_MAX_H + 120)

def main():
    # Flow 1: Apple Account Deletion (privacy.apple.com)
    deletion_flow = [
        ('01_privacy_apple_com_login.jpg', 'Step 1: privacy.apple.com\nSign in with Apple Account', 1),
        ('02_select_delete_reason.jpg', 'Step 2: Select Deletion Reason\nChoose from dropdown menu', 2),
        ('03_review_terms.jpg', 'Step 3: Review Terms\nRead deletion consequences', 3),
        ('04_access_code.jpg', 'Step 4: Save Access Code\nUnique 12-digit recovery code', 4),
        ('05_confirm_delete.jpg', 'Step 5: Confirm & Delete\nEnter access code, final confirm', 5),
    ]

    # Flow 2: Apple's "Single Service" management (iCloud toggles)
    # NOTE: Apple does NOT have true single-service deletion
    icloud_flow = [
        ('07_icloud_settings_main.png', 'Step 1: Settings > Apple ID\niCloud management page', 1),
        ('09_icloud_apps_list.png', 'Step 2: iCloud Apps List\nToggle individual services', 2),
        ('10_icloud_toggle_off.png', 'Step 3: Toggle Off Services\nDisable Photos/Mail/etc sync', 3),
        ('11_sign_out_icloud.png', 'Step 4: Sign Out iCloud\nRemove from this device only', 4),
    ]

    # Flow 3: Apple's unique features
    extra_flow = [
        ('06_deactivate_option.jpg', 'Unique: Temporarily Deactivate\nSuspend account without deleting', 1),
        ('08_icloud_manage_storage.png', 'Unique: Manage Storage\nIndividual service data view', 2),
    ]

    # Calculate canvas
    n_rows_deletion = (len(deletion_flow) + 2) // 3  # 3 per row
    n_rows_icloud = (len(icloud_flow) + 1) // 3
    n_rows_extra = (len(extra_flow) + 1) // 2

    section1_h = n_rows_deletion * (SCREENSHOT_MAX_H + 120)
    section2_h = n_rows_icloud * (SCREENSHOT_MAX_H + 120)
    section3_h = n_rows_extra * (SCREENSHOT_MAX_H + 120)

    total_h = PADDING + TITLE_H + PADDING
    total_h += SECTION_HEADER_H + PADDING + section1_h + PADDING  # section 1
    total_h += SECTION_HEADER_H + PADDING + section2_h + PADDING  # section 2
    total_h += SECTION_HEADER_H + PADDING + section3_h + PADDING  # section 3
    total_h += 380  # analysis notes
    total_h += PADDING

    print(f"Canvas: {CANVAS_W} x {total_h}")
    canvas = Image.new('RGB', (CANVAS_W, total_h), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    font_title = load_font(30)
    font_section = load_font(22)
    font_sub = load_font(14)
    font_note = load_font(15)

    # Title
    draw.rectangle([(0, 0), (CANVAS_W, TITLE_H)], fill=HEADER_BG)
    draw.text((PADDING, 14), "Competitive Analysis: Apple Account Deletion Flow", fill=TITLE_COLOR, font=font_title)
    draw.text((PADDING, TITLE_H - 22), "Path: privacy.apple.com > Sign in > Delete your account > 7-day cooling period > Permanent deletion", fill=(200, 200, 210), font=font_sub)

    y = TITLE_H + PADDING * 2

    # ── Section 1: Account Deletion ──
    draw.rectangle([(PADDING, y), (CANVAS_W - PADDING, y + SECTION_HEADER_H)], fill=SECTION_BG, outline=BORDER_COLOR, width=1)
    draw.text((PADDING + 16, y + 8), "Section 1: Apple Account Permanent Deletion — privacy.apple.com Web Flow", fill=LABEL_COLOR, font=font_section)
    draw.text((PADDING + 16, y + 32), "Source: Beebom / Apple Support — 2025 April | ~7 day cooling period with Access Code recovery", fill=(140,130,130), font=font_sub)
    y += SECTION_HEADER_H + PADDING

    y = create_horizontal_flow(draw, canvas, PADDING, y, deletion_flow, cards_per_row=3)
    y += PADDING // 2

    # ── Section 2: Individual Service Management ──
    draw.rectangle([(PADDING, y), (CANVAS_W - PADDING, y + SECTION_HEADER_H)], fill=SECTION_BG, outline=BORDER_COLOR, width=1)
    draw.text((PADDING + 16, y + 8), "Section 2: Apple Individual Service Management — iCloud Toggle (NOT true single-service deletion)", fill=LABEL_COLOR, font=font_section)
    draw.text((PADDING + 16, y + 32), "Source: iphonelife.com | Settings > Apple ID > iCloud > Toggle individual apps ON/OFF", fill=(140,130,130), font=font_sub)
    y += SECTION_HEADER_H + PADDING

    y = create_horizontal_flow(draw, canvas, PADDING, y, icloud_flow, cards_per_row=4)
    y += PADDING // 2

    # ── Section 3: Unique Features ──
    draw.rectangle([(PADDING, y), (CANVAS_W - PADDING, y + SECTION_HEADER_H)], fill=SECTION_BG, outline=BORDER_COLOR, width=1)
    draw.text((PADDING + 16, y + 8), "Section 3: Apple-Exclusive Features — Temporarily Deactivate & Manage Storage", fill=LABEL_COLOR, font=font_section)
    draw.text((PADDING + 16, y + 32), "Apple is the ONLY competitor with a 'temporarily deactivate' option (vs permanent deletion)", fill=(140,130,130), font=font_sub)
    y += SECTION_HEADER_H + PADDING

    # Layout 2 extra items side by side
    spacing_x = (CANVAS_W - PADDING * 2 - 2 * (SCREENSHOT_MAX_W + 80)) // 3
    for i, (filename, label, step_num) in enumerate(extra_flow):
        x = PADDING + spacing_x + i * (SCREENSHOT_MAX_W + 80 + spacing_x)
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        if os.path.exists(filepath):
            img = load_and_resize(filepath, SCREENSHOT_MAX_W, SCREENSHOT_MAX_H)
            create_card(draw, canvas, x, y, img, label, step_num)

    y += max(SCREENSHOT_MAX_H + 120, 600) + PADDING

    # ── Analysis Notes ──
    notes_h = 360
    draw.rectangle([(PADDING, y), (CANVAS_W - PADDING, y + notes_h)], fill=WARN_BG, outline=WARN_BORDER, width=2)
    note_y = y + 16
    notes = [
        "核心发现：Apple 账号删除与单服务管理",
        "",
        "1. 单业务删除能力：Apple 不支持「删除单个服务并保留 Apple ID」（与 Google 不同）。",
        "   - 可以在「设置 > iCloud」中关闭单个 iCloud 服务（照片、邮件、通讯录等）的开关",
        "   - 但这仅是停止同步——并不会从 Apple 服务器删除该服务或数据",
        "   - 无法「删除 iCloud 邮箱，同时保留 Apple ID 用于 App Store 购买」",
        "   - 整个账号是整体性的：要么全删，要么全留",
        "",
        "2. 独家优势：Apple 是所有竞品中唯一提供「暂时停用」选项的。",
        "   - 这会暂停账号而不永久删除——数据仍保留",
        "   - 随时可通过联系 Apple 支持重新激活",
        "",
        "3. 安全性：所有竞品中最强的身份验证机制：",
        "   - 密码 + 双重认证 + 声纹验证（2025 新增）+ Face ID 活体检测",
        "   - 唯一的 12 位访问代码机制，在 7 天冷静期内可用于恢复",
        "",
        "4. 冷静期：永久删除前有 7 天等待期——仅次于 Google 的 30 天，排名第二。",
        "   - 用户可在此期间凭访问代码随时取消删除",
    ]
    for j, note in enumerate(notes):
        color = LABEL_COLOR if j == 0 else (80, 60, 40)
        font = font_section if j == 0 else font_note
        draw.text((PADDING + 16, note_y + j * 21), note, fill=color, font=font)

    # Footer
    draw.text((PADDING, total_h - 40), "Generated: 2025-06-25 | Sources: Beebom, iphonelife.com, Apple Support | 11 screenshots", fill=(150,150,150), font=load_font(12))

    canvas.save(OUTPUT, quality=95)
    print(f"Saved: {OUTPUT}")

if __name__ == '__main__':
    main()

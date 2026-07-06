"""
Xiaomi composite from real device screenshots
"""
import os
from PIL import Image, ImageDraw, ImageFont

INPUT_DIR = r'c:\Users\jane.yan\competitive-analysis\screenshots\小米\账号注销'
OUTPUT = r'c:\Users\jane.yan\competitive-analysis\reports\xiaomi_account_deletion_composite.png'

BG_COLOR = (255, 255, 255)
BORDER_COLOR = (210, 210, 215)
CANVAS_W = 2400
PADDING = 40
CARD_PADDING = 16
SCREENSHOT_MAX_W = 340
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
    # Native Settings path (设置 > 小米账号 > 账号帮助中心 > 注销账号)
    settings_flow = [
        ('mi_01_settings.png', 'Step 1: 设置首页\n点击顶部"小米账号"', 1),
        ('mi_s1_account_page.png', 'Step 2: 小米账号中心\n账号信息与功能管理', 2),
        ('mi_s2_help_center.png', 'Step 3: 账号帮助中心\n点击进入帮助中心', 3),
        ('mi_s3_help_scrolled.png', 'Step 4: 找到「注销账号」\n独立按钮入口', 4),
        ('mi_s5_scrolled_far.png', 'Step 5: 注销账号页面\n阅读注销条款/须知', 5),
        ('mi_s6_after_full_scan.png', 'Step 6: 验证/确认\n后续验证步骤', 6),
    ]

    # Web path (account.xiaomi.com/pass/del)
    web_flow = [
        ('xm_01_web_del_page.png', 'Step 7(Web): 注销页面\naccount.xiaomi.com/pass/del', 7),
        ('xm_02_web_scrolled1.png', 'Step 8(Web): 注销须知\n阅读注销条款', 8),
        ('xm_03_after_tap.png', 'Step 9(Web): 身份验证\n验证手机号/邮箱', 9),
    ]

    header_bg = (255, 105, 0)  # Xiaomi orange
    arrow_color = (255, 105, 0)
    badge_color = (255, 105, 0)
    section_bg = (255, 248, 240)

    cards_per_row1 = 3
    spacing_x1 = (CANVAS_W - PADDING * 2 - cards_per_row1 * (SCREENSHOT_MAX_W + 80)) // (cards_per_row1 + 1)
    n_rows1 = (len(settings_flow) + cards_per_row1 - 1) // cards_per_row1
    section1_h = n_rows1 * (SCREENSHOT_MAX_H + 120)

    cards_per_row2 = 3
    spacing_x2 = (CANVAS_W - PADDING * 2 - cards_per_row2 * (SCREENSHOT_MAX_W + 80)) // (cards_per_row2 + 1)
    n_rows2 = (len(web_flow) + cards_per_row2 - 1) // cards_per_row2
    section2_h = n_rows2 * (SCREENSHOT_MAX_H + 120)

    notes_h = 280
    total_h = PADDING + TITLE_H + PADDING + SECTION_HEADER_H + PADDING + section1_h + PADDING
    total_h += SECTION_HEADER_H + PADDING + section2_h + PADDING + notes_h + PADDING

    print(f"Canvas: {CANVAS_W} x {total_h}")
    canvas = Image.new('RGB', (CANVAS_W, total_h), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    # Title
    draw.rectangle([(0, 0), (CANVAS_W, TITLE_H)], fill=header_bg)
    draw.text((PADDING, 10), "小米账号注销 — 真机实测截图 (Xiaomi Device)", fill=(255,255,255), font=load_font(26))
    draw.text((PADDING, TITLE_H - 24), "访问入口: 设置 → 小米账号 | 网页端: account.xiaomi.com/pass/del | 2025-06-26", fill=(255, 230, 210), font=load_font(13))

    y = TITLE_H + PADDING * 2

    # Section 1: Native Settings
    draw.rectangle([(PADDING, y), (CANVAS_W - PADDING, y + SECTION_HEADER_H)], fill=section_bg, outline=BORDER_COLOR, width=1)
    draw.text((PADDING + 16, y + 8), "Section 1: 手机原生路径 — 设置 → 小米账号 → 账号中心 → 退出/注销", fill=(30,30,35), font=load_font(20))
    draw.text((PADDING + 16, y + 32), "小米真机实测 (MIUI/HyperOS) | 2025-06-26", fill=(140,130,130), font=load_font(13))
    y += SECTION_HEADER_H + PADDING

    for i, (filename, label, step_num) in enumerate(settings_flow):
        col = i % cards_per_row1
        x = PADDING + spacing_x1 + col * (SCREENSHOT_MAX_W + 80 + spacing_x1)
        card_y = y + (i // cards_per_row1) * (SCREENSHOT_MAX_H + 120)
        filepath = os.path.join(INPUT_DIR, filename)
        if os.path.exists(filepath) and os.path.getsize(filepath) > 50000:
            img = load_and_resize(filepath, SCREENSHOT_MAX_W, SCREENSHOT_MAX_H)
            card_w, card_h = create_card(draw, canvas, x, card_y, img, label, step_num, badge_color)
            if col < cards_per_row1 - 1 and i < len(settings_flow) - 1:
                draw_arrow(draw, x + card_w, card_y + card_h//2,
                          x + SCREENSHOT_MAX_W + 80 + spacing_x1 - 10, card_y + card_h//2, arrow_color)
    y += n_rows1 * (SCREENSHOT_MAX_H + 120) + PADDING

    # Section 2: Web
    draw.rectangle([(PADDING, y), (CANVAS_W - PADDING, y + SECTION_HEADER_H)], fill=section_bg, outline=BORDER_COLOR, width=1)
    draw.text((PADDING + 16, y + 8), "Section 2: 网页端路径 — account.xiaomi.com/pass/del", fill=(30,30,35), font=load_font(20))
    draw.text((PADDING + 16, y + 32), "网页版账号注销入口 | 已登录状态可直接进入注销流程", fill=(140,130,130), font=load_font(13))
    y += SECTION_HEADER_H + PADDING

    for i, (filename, label, step_num) in enumerate(web_flow):
        x = PADDING + spacing_x2 + i * (SCREENSHOT_MAX_W + 80 + spacing_x2)
        filepath = os.path.join(INPUT_DIR, filename)
        if os.path.exists(filepath) and os.path.getsize(filepath) > 50000:
            img = load_and_resize(filepath, SCREENSHOT_MAX_W, SCREENSHOT_MAX_H)
            card_w, card_h = create_card(draw, canvas, x, y, img, label, step_num, badge_color)
            if i < len(web_flow) - 1:
                draw_arrow(draw, x + card_w, y + card_h//2,
                          x + SCREENSHOT_MAX_W + 80 + spacing_x2 - 10, y + card_h//2, arrow_color)
    y += n_rows2 * (SCREENSHOT_MAX_H + 120) + PADDING

    # Notes
    draw.rectangle([(PADDING, y), (CANVAS_W - PADDING, y + notes_h)], fill=(255,248,240), outline=(240,180,100), width=2)
    notes = [
        "核心发现：小米账号删除 — 真机实测",
        "",
        "1. 访问入口：设置 → 小米账号 → 账号中心（滚动到底部查找退出/注销选项）",
        "2. 网页端直达：account.xiaomi.com/pass/del（需已登录状态）",
        "3. 无单业务删除：小米云服务可单独开关同步，但无法删除单个业务而保留账号",
        "4. 无冷静期/恢复期：注销后不可恢复，原手机号可重新注册",
        "5. 处理时长：完全删除最多 15 个工作日",
    ]
    for j, note in enumerate(notes):
        color = (60, 20, 20) if j == 0 else (80, 60, 40)
        f = load_font(20) if j == 0 else load_font(14)
        draw.text((PADDING + 16, y + 16 + j * 22), note, fill=color, font=f)

    canvas.save(OUTPUT, quality=95)
    print(f"Saved: {OUTPUT}")

if __name__ == '__main__':
    main()

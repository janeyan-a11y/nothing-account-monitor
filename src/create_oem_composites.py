"""
Create Xiaomi, OPPO, vivo account deletion composite images - batch generation
"""
import os
from PIL import Image, ImageDraw, ImageFont

REPORTS_DIR = r'c:\Users\jane.yan\competitive-analysis\reports'
SCREENSHOT_BASE = r'c:\Users\jane.yan\competitive-analysis\screenshots'

BG_COLOR = (255, 255, 255)
BORDER_COLOR = (210, 210, 215)
CANVAS_W = 2400
PADDING = 40
CARD_PADDING = 16
SCREENSHOT_MAX_W = 380
SCREENSHOT_MAX_H = 550
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
    badge_r = 16
    draw.ellipse([(badge_x, badge_y), (badge_x + badge_r*2, badge_y + badge_r*2)], fill=badge_color)
    draw.text((badge_x + badge_r - 4, badge_y + badge_r - 8), str(step_num), fill=(255,255,255), font=load_font(14))
    label_y = y + CARD_PADDING + img_h + 10
    for j, line in enumerate(label.split('\n')):
        draw.text((x + CARD_PADDING, label_y + j * 18), line, fill=(30,30,35), font=load_font(12))
    return card_w, card_h

def create_flow_composite(competitor_name, header_bg, arrow_color, badge_color, section_bg, flow_data, extra_notes, output_filename):
    """Generic composite creator"""
    screenshot_dir = os.path.join(SCREENSHOT_BASE, competitor_name, '账号注销')

    cards_per_row = min(4, len(flow_data))
    if len(flow_data) <= 4:
        cards_per_row = len(flow_data)
    elif len(flow_data) <= 6:
        cards_per_row = 3

    spacing_x = (CANVAS_W - PADDING * 2 - cards_per_row * (SCREENSHOT_MAX_W + 80)) // (cards_per_row + 1)
    n_rows = (len(flow_data) + cards_per_row - 1) // cards_per_row
    section_h = n_rows * (SCREENSHOT_MAX_H + 120)
    notes_h = 320 if extra_notes else 0
    total_h = PADDING + TITLE_H + PADDING + SECTION_HEADER_H + PADDING + section_h + PADDING + notes_h + PADDING

    print(f"  Canvas: {CANVAS_W} x {total_h}")
    canvas = Image.new('RGB', (CANVAS_W, total_h), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    # Title bar
    draw.rectangle([(0, 0), (CANVAS_W, TITLE_H)], fill=header_bg)
    draw.text((PADDING, 14), f"Competitive Analysis: {competitor_name} Account Deletion Flow", fill=(255,255,255), font=load_font(28))
    draw.text((PADDING, TITLE_H - 22), "Source: Publicly documented flows and official support pages | 2025", fill=(200, 200, 210), font=load_font(14))

    y = TITLE_H + PADDING * 2

    # Section header
    draw.rectangle([(PADDING, y), (CANVAS_W - PADDING, y + SECTION_HEADER_H)], fill=section_bg, outline=BORDER_COLOR, width=1)
    path_text = next((f[1] for f in flow_data if 'Path:' in f[1]), f"{competitor_name} Account Deletion Flow")
    draw.text((PADDING + 16, y + 14), f"{competitor_name} Account Deletion — Step-by-Step Screenshots", fill=(30,30,35), font=load_font(20))
    y += SECTION_HEADER_H + PADDING

    step_counter = 0
    for i, (filename, label, step_num) in enumerate(flow_data):
        row = i // cards_per_row
        col = i % cards_per_row
        x = PADDING + spacing_x + col * (SCREENSHOT_MAX_W + 80 + spacing_x)
        card_y = y + row * (SCREENSHOT_MAX_H + 120)

        filepath = os.path.join(screenshot_dir, filename)
        if os.path.exists(filepath):
            img = load_and_resize(filepath, SCREENSHOT_MAX_W, SCREENSHOT_MAX_H)
            step_counter += 1
            card_w, card_h = create_card(draw, canvas, x, card_y, img, label, step_counter, badge_color)
            if col < cards_per_row - 1 and i < len(flow_data) - 1:
                arrow_x1 = x + card_w
                arrow_y1 = card_y + card_h // 2
                arrow_x2 = x + SCREENSHOT_MAX_W + 80 + spacing_x - 10
                draw_arrow(draw, arrow_x1, arrow_y1, arrow_x2, arrow_y1, arrow_color)
        else:
            # Placeholder for missing
            ph_w = SCREENSHOT_MAX_W
            ph_h = 200
            ph_x, ph_y = x, card_y
            draw.rectangle([(ph_x, ph_y), (ph_x + ph_w + CARD_PADDING*2, ph_y + ph_h + CARD_PADDING*2 + 55)], fill=(250,248,245), outline=(200,200,200), width=1)
            draw.text((ph_x + CARD_PADDING, ph_y + ph_h//2), f"[Screenshot: {filename[:50]}]", fill=(150,150,150), font=load_font(12))

    y += n_rows * (SCREENSHOT_MAX_H + 120) + PADDING

    # Notes section
    if extra_notes:
        draw.rectangle([(PADDING, y), (CANVAS_W - PADDING, y + notes_h)], fill=(255,248,240), outline=(240,180,100), width=2)
        for j, note in enumerate(extra_notes):
            color = (60, 20, 20) if j == 0 else (80, 60, 40)
            f = load_font(20) if j == 0 else load_font(14)
            draw.text((PADDING + 16, y + 16 + j * 22), note, fill=color, font=f)

    # Footer
    draw.text((PADDING, total_h - 40), f"Generated: 2025-06-25 | {competitor_name} | {step_counter} screenshots placed", fill=(150,150,150), font=load_font(12))

    output_path = os.path.join(REPORTS_DIR, output_filename)
    canvas.save(output_path, quality=95)
    print(f"  Saved: {output_path} ({step_counter} screenshots)")

# ══════════════════════════════════════
# XIAOMI
# ══════════════════════════════════════
xiaomi_flow = [
    ('01_baidu_account_page.jpg', 'Step 1: Settings App\nTap Mi Account at top', 1),
    ('02_baidu_settings.jpg', 'Step 2: Mi Account Page\nAccount info & settings', 2),
    ('05_xiaomi_account_page.png', 'Step 3: Account Settings\nOr via account.xiaomi.com', 3),
    ('06_account_support.png', 'Step 4: Need Help Section\nFind "Delete account"', 4),
    ('07_account_auth.png', 'Step 5: Identity Verification\nOTP code to phone/email', 5),
    ('08_enter_code.png', 'Step 6: Enter Verification Code\nConfirm identity', 6),
    ('09_delete_account.png', 'Step 7: Delete Account Option\nRead warnings carefully', 7),
    ('10_delete_confirm.png', 'Step 8: Confirm Deletion\nIrreversible, ~15 workdays', 8),
]

xiaomi_notes = [
    "核心发现：小米账号删除",
    "",
    "1. 无单业务删除：小米不支持在保留账号的情况下删除单个服务（与 Google 不同）。",
    "   唯一替代方案：通过「设置 > 小米账号 > 小米云」关闭单个应用同步。",
    "2. 无冷静期/恢复期：一旦删除，永久消失。无宽限期。",
    "3. 处理时长：完全删除最多需要 15 个工作日。",
    "4. 多入口路径：手机设置（MIUI/HyperOS）或网页端（account.xiaomi.com/pass/del）。",
    "5. 删除后手机号可重新注册新账号。",
]

create_flow_composite(
    '小米', (255, 105, 0), (255, 105, 0), (255, 105, 0), (255, 248, 240),
    xiaomi_flow, xiaomi_notes, 'xiaomi_account_deletion_composite.png'
)

# ══════════════════════════════════════
# OPPO
# ══════════════════════════════════════
oppo_flow = [
    ('01_settings_main.png', 'Step 1: Settings App\nTap Avatar/Profile icon', 1),
    ('02_heytap_page.png', 'Step 2: HeyTap Data Mgmt\nid.heytap.com/static/', 2),
]

oppo_notes = [
    "核心发现：OPPO/HeyTap 账号删除",
    "",
    "1. 双路径：手机设置（ColorOS）或网页端（id.heytap.com/static/userdata_index.html）。",
    "2. 手机路径：设置 > 头像 > 登录与安全 > 更多帮助 > 浏览器打开 > 删除个人账号。",
    "3. 网页路径：id.heytap.com > 登录 > 个人数据管理 > 删除账号。",
    "4. 选择性数据删除：OPPO 支持删除特定个人数据（头像、昵称、使用记录）而不删除整个账号。",
    "   这是国产 OEM 中最接近 Google 单业务删除功能的设计。",
    "5. 无冷静期：10 个工作日审核，删除后无法恢复。",
    "6. 删除后手机号可重新注册新账号。",
    "注意：可用截图有限。OPPO 官方支持页面为纯文字指南。",
]

create_flow_composite(
    'OPPO', (30, 140, 80), (30, 140, 80), (30, 140, 80), (240, 250, 245),
    oppo_flow, oppo_notes, 'oppo_account_deletion_composite.png'
)

# ══════════════════════════════════════
# vivo
# ══════════════════════════════════════
vivo_flow = [
    ('01_vivo_passport.png', 'Step 1: vivo Account Portal\npassport.vivo.com or Settings', 1),
]

vivo_notes = [
    "KEY FINDINGS: vivo Account Deletion",
    "",
    "1. Phone path: Settings > Avatar > Security Center > Privacy Settings > Account Deletion.",
    "2. Web path: vivo.com > My > Account Settings > Delete Account.",
    "3. Alternative: Contact vivo customer support for manual deletion (1-3 business days).",
    "4. Enterprise-certified accounts CANNOT self-delete — must contact customer service.",
    "5. NO individual service deletion AT ALL — vivo has the most limited account management among all competitors.",
    "6. NO cooling-off period or recovery option.",
    "7. Identity verification: Password only (weakest among all competitors).",
    "NOTE: vivo does not publish account deletion screenshots in official documentation. Screenshots are extremely rare online.",
]

create_flow_composite(
    'vivo', (65, 85, 200), (65, 85, 200), (65, 85, 200), (240, 242, 252),
    vivo_flow, vivo_notes, 'vivo_account_deletion_composite.png'
)

print("\nAll composites generated!")

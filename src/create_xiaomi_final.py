"""
Xiaomi final composite - complete real deletion flow (10 steps)
"""
import os
from PIL import Image, ImageDraw, ImageFont

INPUT_DIR = r'c:\Users\jane.yan\competitive-analysis\screenshots\小米\账号注销'
OUTPUT = r'c:\Users\jane.yan\competitive-analysis\reports\xiaomi_account_deletion_composite.png'

BG_COLOR, BORDER_COLOR = (255,255,255), (210,210,215)
CANVAS_W, PADDING, CARD_PADDING = 2400, 40, 16
SCREENSHOT_MAX_W, SCREENSHOT_MAX_H = 320, 580
TITLE_H, SECTION_HEADER_H = 70, 50

def load_font(size):
    for fp in ["C:/Windows/Fonts/msyh.ttc","C:/Windows/Fonts/msyhbd.ttc","C:/Windows/Fonts/simsun.ttc","C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(fp):
            try: return ImageFont.truetype(fp, size)
            except: pass
    return ImageFont.load_default()

def load_and_resize(path, max_w, max_h):
    img = Image.open(path).convert('RGB')
    w, h = img.size
    ratio = min(max_w/w, max_h/h, 1.0)
    if ratio < 1.0: return img.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)
    return img

def draw_arrow(draw, x1, y1, x2, y2, color, width=3):
    import math
    draw.line([(x1,y1),(x2,y2)], fill=color, width=width)
    angle = math.atan2(y2-y1, x2-x1)
    al = 12
    ax1, ay1 = x2-al*math.cos(angle-math.pi/6), y2-al*math.sin(angle-math.pi/6)
    ax2, ay2 = x2-al*math.cos(angle+math.pi/6), y2-al*math.sin(angle+math.pi/6)
    draw.polygon([(x2,y2),(ax1,ay1),(ax2,ay2)], fill=color)

def create_card(draw, canvas, x, y, img, label, step_num, badge_color):
    iw, ih = img.size
    cw, ch = iw+CARD_PADDING*2, ih+CARD_PADDING*2+58
    draw.rectangle([(x,y),(x+cw,y+ch)], fill=(255,255,255), outline=BORDER_COLOR, width=2)
    canvas.paste(img, (x+CARD_PADDING, y+CARD_PADDING))
    bx, by = x+CARD_PADDING-4, y+CARD_PADDING-4
    br = 15
    draw.ellipse([(bx,by),(bx+br*2,by+br*2)], fill=badge_color)
    draw.text((bx+br-5,by+br-10), str(step_num), fill=(255,255,255), font=load_font(13))
    ly = y+CARD_PADDING+ih+8
    for j, line in enumerate(label.split('\n')):
        draw.text((x+CARD_PADDING+2, ly+j*15), line, fill=(30,30,35), font=load_font(10))
    return cw, ch

def main():
    flow = [
        ('mi_01_settings.png', '1. 设置首页\n点击"小米账号"', 1),
        ('mi_s1_account_page.png', '2. 小米账号中心\n账号 134****2070', 2),
        ('mi_s2_help_center.png', '3. 账号帮助中心\n找到注销入口', 3),
        ('del_01_page_top.png', '4. 注销账号页\n警告及后果摘要', 4),
        ('del_04_expanded.png', '5. 展开后果清单\n10+项数据将永久删除', 5),
        ('del_08_verify_code.png', '6. 短信安全验证\n发送验证码到134******70', 6),
        ('del_10_code_entered.png', '7. 输入验证码\n770057 + 25s倒计时', 7),
        ('del_11_result.png', '8. 最终确认页\n勾选接受损失+开始删除', 8),
        ('del_13_deleted_result.png', '9. 设备检查拦截\nPOCO M7 5G仍在登录', 9),
        ('del_14_final_deleted.png', '10. 回到账号中心\n注销被阻止,账号仍存在', 10),
    ]

    header_bg, arrow_color, badge_color, section_bg = (255,105,0),(255,105,0),(255,105,0),(255,248,240)

    cards_per_row, n = 5, len(flow)
    spacing_x = max(8, (CANVAS_W-PADDING*2-cards_per_row*(SCREENSHOT_MAX_W+70))//(cards_per_row+1))
    n_rows = (n+cards_per_row-1)//cards_per_row
    section_h = n_rows*(SCREENSHOT_MAX_H+120)
    notes_h = 280
    total_h = PADDING+TITLE_H+PADDING+SECTION_HEADER_H+PADDING+section_h+PADDING+notes_h+PADDING

    print(f"Canvas: {CANVAS_W} x {total_h}")
    canvas = Image.new('RGB', (CANVAS_W, total_h), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    draw.rectangle([(0,0),(CANVAS_W,TITLE_H)], fill=header_bg)
    draw.text((PADDING,10), "小米账号注销 — 真机实测完整流程 & 关键发现", fill=(255,255,255), font=load_font(26))
    draw.text((PADDING,TITLE_H-24), "路径: 设置 > 小米账号 > 账号帮助中心 > 注销账号 | 验证: SMS (770057) | 结果: 设备检查拦截 | 2025-06-26", fill=(255,230,210), font=load_font(13))

    y = TITLE_H + PADDING*2
    draw.rectangle([(PADDING,y),(CANVAS_W-PADDING,y+SECTION_HEADER_H)], fill=section_bg, outline=BORDER_COLOR, width=1)
    draw.text((PADDING+16,y+8), "小米账号注销完整流程 — 真机实测 10 步（含最终拦截结果）", fill=(30,30,35), font=load_font(20))
    draw.text((PADDING+16,y+32), "关键发现: 无冷却期, 多重确认 (SMS + 勾选 + 设备检查), 设备未退出则无法完成注销", fill=(140,130,130), font=load_font(13))
    y += SECTION_HEADER_H + PADDING

    for i, (filename, label, step_num) in enumerate(flow):
        col, row = i%cards_per_row, i//cards_per_row
        x = PADDING+spacing_x+col*(SCREENSHOT_MAX_W+70+spacing_x)
        card_y = y+row*(SCREENSHOT_MAX_H+120)
        filepath = os.path.join(INPUT_DIR, filename)
        if os.path.exists(filepath) and os.path.getsize(filepath) > 20000:
            img = load_and_resize(filepath, SCREENSHOT_MAX_W, SCREENSHOT_MAX_H)
            cw, ch = create_card(draw, canvas, x, card_y, img, label, step_num, badge_color)
            if col < cards_per_row-1 and i < n-1:
                draw_arrow(draw, x+cw, card_y+ch//2, x+SCREENSHOT_MAX_W+70+spacing_x-10, card_y+ch//2, arrow_color)

    y += n_rows*(SCREENSHOT_MAX_H+120) + PADDING
    draw.rectangle([(PADDING,y),(CANVAS_W-PADDING,y+notes_h)], fill=(255,248,240), outline=(240,180,100), width=2)
    notes = [
        "核心发现：小米账号注销 — 真机实测结论",
        "",
        "1. 无冷却期/恢复期 — 确认后立即执行删除（与 Google 30天 / Apple 7天完全不同）",
        "2. 四重确认机制: SMS验证码 + 勾选接受损失 + 开始删除 + 设备登录检查",
        "3. 设备检查拦截: 检测到仍有设备登录 (本案例: POCO M7 5G + Edge Browser)，系统阻止删除",
        "4. 需先退出所有设备登录后才能完成注销 — 这是实际的安全保护机制",
        "5. 验证方式: 短信验证码到绑定手机号 (134******70)，无密码/生物识别验证",
        "6. 无单业务删除能力 — 仅支持整体注销",
    ]
    for j, note in enumerate(notes):
        color = (60,20,20) if j==0 else (80,60,40)
        f = load_font(20) if j==0 else load_font(14)
        draw.text((PADDING+16, y+16+j*22), note, fill=color, font=f)

    canvas.save(OUTPUT, quality=95)
    print(f"Saved: {OUTPUT}")

if __name__ == '__main__':
    main()

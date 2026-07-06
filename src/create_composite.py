"""
Create a competitive analysis whiteboard composite image
Assembles Google account deletion screenshots into a flowchart layout
"""
import os
from PIL import Image, ImageDraw, ImageFont

DOWNLOADS = r'c:\Users\jane.yan\competitive-analysis\screenshots\Google\账号注销\downloaded'
OUTPUT = r'c:\Users\jane.yan\competitive-analysis\reports\google_account_deletion_composite.png'

# Color scheme (matching whiteboard style)
BG_COLOR = (255, 255, 255)
HEADER_BG = (30, 58, 95)       # dark blue
SECTION_BG = (245, 247, 250)    # light gray-blue
BORDER_COLOR = (200, 210, 220)
ARROW_COLOR = (37, 99, 235)     # blue
LABEL_COLOR = (30, 58, 95)
STEP_COLOR = (37, 99, 235)
TITLE_COLOR = (255, 255, 255)

# Layout constants
CANVAS_W = 2400
PADDING = 40
CARD_PADDING = 16
SCREENSHOT_MAX_W = 380
SCREENSHOT_MAX_H = 600
TITLE_H = 70
SECTION_HEADER_H = 50

def load_font(size, bold=False):
    """Try to load a good font, fallback to default"""
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",        # Microsoft YaHei
        "C:/Windows/Fonts/msyhbd.ttc",       # Microsoft YaHei Bold
        "C:/Windows/Fonts/simsun.ttc",       # SimSun
        "C:/Windows/Fonts/arial.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                pass
    return ImageFont.load_default()

def load_and_resize(path, max_w, max_h):
    """Load image and resize to fit within max dimensions"""
    img = Image.open(path).convert('RGB')
    w, h = img.size
    ratio = min(max_w / w, max_h / h, 1.0)
    if ratio < 1.0:
        new_w, new_h = int(w * ratio), int(h * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)
    return img

def draw_arrow(draw, x1, y1, x2, y2, color=ARROW_COLOR, width=3):
    """Draw an arrow from (x1,y1) to (x2,y2)"""
    import math
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    # Arrow head
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 12
    ax1 = x2 - arrow_len * math.cos(angle - math.pi/6)
    ay1 = y2 - arrow_len * math.sin(angle - math.pi/6)
    ax2 = x2 - arrow_len * math.cos(angle + math.pi/6)
    ay2 = y2 - arrow_len * math.sin(angle + math.pi/6)
    draw.polygon([(x2, y2), (ax1, ay1), (ax2, ay2)], fill=color)

def create_card(draw, canvas, x, y, img, label, step_num=None):
    """Place a screenshot on the canvas with border, label, and optional step number"""
    img_w, img_h = img.size
    card_w = img_w + CARD_PADDING * 2
    card_h = img_h + CARD_PADDING * 2 + 50  # extra for label

    # Card background
    draw.rectangle(
        [(x, y), (x + card_w, y + card_h)],
        fill=(255, 255, 255),
        outline=BORDER_COLOR,
        width=2
    )

    # Screenshot with subtle shadow
    shadow_offset = 3
    draw.rectangle(
        [(x + CARD_PADDING + shadow_offset, y + CARD_PADDING + shadow_offset),
         (x + CARD_PADDING + img_w + shadow_offset, y + CARD_PADDING + img_h + shadow_offset)],
        fill=(220, 220, 225)
    )
    canvas.paste(img, (x + CARD_PADDING, y + CARD_PADDING))

    # Step number badge
    if step_num:
        badge_x = x + CARD_PADDING - 4
        badge_y = y + CARD_PADDING - 4
        badge_r = 16
        draw.ellipse(
            [(badge_x, badge_y), (badge_x + badge_r*2, badge_y + badge_r*2)],
            fill=STEP_COLOR
        )
        font_s = load_font(14)
        draw.text(
            (badge_x + badge_r - 4, badge_y + badge_r - 8),
            str(step_num), fill=(255,255,255), font=font_s
        )

    # Label text
    font_label = load_font(13)
    label_y = y + CARD_PADDING + img_h + 12
    draw.text((x + CARD_PADDING, label_y), label, fill=LABEL_COLOR, font=font_label)

    return card_w, card_h

def get_screenshot_files():
    """Get available screenshots organized by flow"""
    files = {}
    for f in os.listdir(DOWNLOADS):
        if f.endswith(('.png', '.jpg', '.jpeg')):
            files[f] = os.path.join(DOWNLOADS, f)
    return files

def main():
    files = get_screenshot_files()
    print(f"Found {len(files)} screenshot files")

    # Define the layout: which screenshots to use for each section
    # (filename, label, step_num)
    desktop_flow = [
        ('01_desktop_data_privacy.png', 'Step 1: myaccount.google.com\nData & Privacy page', 1),
        ('08_desktop_delete_account_1.png', 'Step 2: "Delete your\nGoogle Account" section', 2),
        ('11_desktop_enter_password.png', 'Step 3: Re-enter password\nfor identity verification', 3),
        ('12_desktop_confirm_checkboxes.png', 'Step 4: Review deletion\nimpact list, confirm', 4),
        ('09_desktop_delete_account_2.png', 'Step 5: Account enters\n~30 day recovery period', 5),
    ]

    single_service_flow = [
        ('19_delete_google_service_page.png', 'Step 1: Data & privacy \n"Delete a Google service"', 1),
        ('20_gmail_trash_icon.png', 'Step 2: Click trash icon\nnext to Gmail/YouTube/etc', 2),
        ('21_alternate_email.png', 'Step 3: Provide alternate\nnon-Gmail email address', 3),
        ('02_desktop_delete_gmail.png', 'Step 4: Verify alternate\nemail via confirmation link', 4),
        ('03_desktop_confirm.png', 'Step 5: Confirm deletion\nservice removed, account stays', 5),
    ]

    mobile_flow = [
        ('13_android_chrome_account.png', 'Step 1: Open Chrome\ntap profile icon', 1),
        ('15_android_manage_account.png', 'Step 2: "Manage your\nGoogle Account"', 2),
        ('16_android_data_privacy.png', 'Step 3: Data & Privacy tab\nin account settings', 3),
        ('17_android_scroll_delete.png', 'Step 4: Scroll to bottom\n"Delete your Google Account"', 4),
        ('18_android_confirm.png', 'Step 5: Read warning\ncheck boxes, confirm', 5),
    ]

    backup_flow = [
        ('22_takeout_select.png', 'Google Takeout:\nSelect data to export', 1),
        ('23_takeout_options.png', 'Choose export format\n.zip or .tgz', 2),
        ('24_security_third_party.png', 'Security Checkup:\nReview third-party access', 3),
        ('25_subscriptions.png', 'Cancel active\nsubscriptions first', 4),
    ]

    all_sections = [
        ("Google Account Deletion — Desktop Flow", desktop_flow, "Delete entire Google Account via myaccount.google.com"),
        ("Google Individual Service Deletion", single_service_flow, "Delete single services (Gmail/YouTube) without losing entire account"),
        ("Google Account Deletion — Android Mobile Flow", mobile_flow, "Delete via Android Settings > Google > Manage Account"),
        ("Pre-Deletion Checklist & Backup", backup_flow, "Essential steps before account deletion"),
    ]

    # Calculate canvas height
    rows_per_section = []
    total_h = PADDING + TITLE_H + PADDING
    for section_title, flow, subtitle in all_sections:
        # Layout: 5 screenshots per row, wrap to next row if more
        n = len(flow)
        # Estimate: each card roughly SCREENSHOT_MAX_W + 80 wide, SCREENSHOT_MAX_H + 80 tall
        cards_per_row = max(1, (CANVAS_W - PADDING * 2) // (SCREENSHOT_MAX_W + 120))
        n_rows = (n + cards_per_row - 1) // cards_per_row
        section_h = SECTION_HEADER_H + PADDING + n_rows * (SCREENSHOT_MAX_H + 120) + PADDING
        rows_per_section.append((n_rows, cards_per_row, n))
        total_h += section_h

    total_h += PADDING
    total_h = max(total_h, 4000)

    print(f"Canvas: {CANVAS_W} x {total_h}")
    canvas = Image.new('RGB', (CANVAS_W, total_h), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    # Draw main title
    font_title = load_font(32)
    font_subtitle = load_font(16)
    font_section = load_font(22)
    font_sub = load_font(14)

    # Title bar
    draw.rectangle([(0, 0), (CANVAS_W, TITLE_H)], fill=HEADER_BG)
    draw.text((PADDING, 15), "账号注销竞品分析详情 — Google", fill=TITLE_COLOR, font=font_title)
    draw.text((PADDING, TITLE_H - 22), "Source: Google Account (myaccount.google.com) — Screenshots from publicly documented flows", fill=(180, 200, 220), font=font_sub)

    y_offset = TITLE_H + PADDING * 2

    step_counter = 0

    for section_idx, (section_title, flow, subtitle) in enumerate(all_sections):
        section_start_y = y_offset

        # Section header
        draw.rectangle(
            [(PADDING, y_offset), (CANVAS_W - PADDING, y_offset + SECTION_HEADER_H)],
            fill=SECTION_BG,
            outline=BORDER_COLOR,
            width=1
        )
        draw.text((PADDING + 16, y_offset + 8), section_title, fill=LABEL_COLOR, font=font_section)
        draw.text((PADDING + 16, y_offset + 32), subtitle, fill=(120, 130, 140), font=font_sub)

        y_offset += SECTION_HEADER_H + PADDING

        # Layout screenshots in rows
        cards_per_row = max(1, (CANVAS_W - PADDING * 2) // (SCREENSHOT_MAX_W + 120))
        spacing_x = (CANVAS_W - PADDING * 2 - cards_per_row * (SCREENSHOT_MAX_W + 100)) // (cards_per_row + 1)

        for i, (filename, label, local_step) in enumerate(flow):
            row = i // cards_per_row
            col = i % cards_per_row

            x = PADDING + spacing_x + col * (SCREENSHOT_MAX_W + 100 + spacing_x)
            y = y_offset + row * (SCREENSHOT_MAX_H + 130)

            if filename in files:
                img = load_and_resize(files[filename], SCREENSHOT_MAX_W, SCREENSHOT_MAX_H)
                step_counter += 1
                card_w, card_h = create_card(draw, canvas, x, y, img, label, step_counter)

                # Draw right arrow (except last in row and last overall)
                if col < cards_per_row - 1 and i < len(flow) - 1:
                    arrow_start_x = x + card_w
                    arrow_start_y = y + card_h // 2
                    next_x = x + SCREENSHOT_MAX_W + 100 + spacing_x
                    arrow_end_x = next_x - 10
                    arrow_end_y = y + card_h // 2
                    draw_arrow(draw, arrow_start_x, arrow_start_y, arrow_end_x, arrow_end_y)
            else:
                # Placeholder for missing screenshot
                ph_w, ph_h = SCREENSHOT_MAX_W, 200
                draw.rectangle(
                    [(x, y), (x + ph_w + CARD_PADDING*2, y + ph_h + CARD_PADDING*2 + 50)],
                    fill=(250, 248, 245),
                    outline=(200, 200, 200),
                    width=1
                )
                font_ph = load_font(12)
                draw.text((x + CARD_PADDING, y + ph_h//2), f"[Screenshot: {filename[:40]}]", fill=(150,150,150), font=font_ph)
                draw.text((x + CARD_PADDING, y + ph_h + 20), label, fill=LABEL_COLOR, font=load_font(13))

        # Move to next section
        n_rows = (len(flow) + cards_per_row - 1) // cards_per_row
        y_offset += n_rows * (SCREENSHOT_MAX_H + 130) + PADDING

        # Draw section divider line
        if section_idx < len(all_sections) - 1:
            draw.line(
                [(PADDING * 2, y_offset), (CANVAS_W - PADDING * 2, y_offset)],
                fill=(220, 225, 230),
                width=2
            )
            y_offset += PADDING // 2

    # Footer
    footer_y = total_h - 40
    draw.text((PADDING, footer_y), "Generated: 2025-06-25 | Analysis: Google Account & Individual Service Deletion Flow", fill=(150,150,150), font=load_font(12))

    # Save
    canvas.save(OUTPUT, quality=95)
    print(f"Saved: {OUTPUT}")
    print(f"Final canvas: {CANVAS_W} x {total_h}")
    print(f"Screenshots placed: {step_counter}")

if __name__ == '__main__':
    main()

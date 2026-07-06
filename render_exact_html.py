import sys, json, re, html as html_mod
sys.stdout.reconfigure(encoding='utf-8')
from xml.etree import ElementTree as ET

json_path = r'C:\Users\jane.yan\.claude\projects\c--Users-jane-yan-competitive-analysis\c5bbbae7-0778-4920-b9ae-fb15912ad9a6\tool-results\bb8vl5msu.txt'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

xml_content = data['data']['xml_presentation']['content']
root = ET.fromstring(xml_content)

NS = '/sml/2.0'
W = 960  # slide width
H = 540  # slide height
SCALE = 1.4  # scale for display

def get_slides():
    slides = []
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'slide':
            slides.append(elem)
    return slides

def parse_color(c):
    """Parse rgba color string"""
    if not c:
        return None
    if c.startswith('rgba('):
        parts = c[5:-1].split(',')
        r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
        a = float(parts[3]) if len(parts) > 3 else 1
        return f'rgba({r},{g},{b},{a})'
    if c.startswith('rgb('):
        return c
    return c

def get_style_attrs(elem):
    """Extract common style attributes"""
    attrs = {}
    for attr in ['fontSize', 'fontFamily', 'color', 'bold', 'italic', 'underline', 'strikethrough', 'textAlign', 'lineSpacing']:
        val = elem.get(attr)
        if val:
            attrs[attr] = val
    return attrs

def render_text_content(elem, parent_style=None):
    """Render <content> element to HTML"""
    if elem is None:
        return ''
    padding_top = elem.get('paddingTop', '0')
    padding_bottom = elem.get('paddingBottom', '0')
    padding_left = elem.get('paddingLeft', '0')
    padding_right = elem.get('paddingRight', '0')

    base_font_size = elem.get('fontSize', '16')
    base_font_family = elem.get('fontFamily', '')
    base_color = parse_color(elem.get('color', 'rgba(31,35,41,1)'))

    html_parts = []
    for p in elem.findall(f'{{{NS}}}p'):
        p_style = get_style_attrs(p)
        text_align = p_style.get('textAlign', 'left')
        line_spacing = p_style.get('lineSpacing', '1.5')

        p_html = []
        # Process children in order
        children = list(p)
        if not children:
            # Just text
            txt = p.text or ''
            if txt.strip():
                p_html.append(html_mod.escape(txt))
        else:
            for child in children:
                ctag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if ctag == 'span':
                    s_style = get_style_attrs(child)
                    s_font_size = s_style.get('fontSize', base_font_size)
                    s_font_family = s_style.get('fontFamily', base_font_family)
                    s_color = parse_color(s_style.get('color', elem.get('color', 'rgba(31,35,41,1)')))
                    s_bold = s_style.get('bold', 'false') == 'true'
                    s_italic = s_style.get('italic', 'false') == 'true'
                    s_underline = s_style.get('underline', 'false') == 'true'

                    styles = [f'font-size:{s_font_size}pt']
                    if s_font_family:
                        styles.append(f'font-family:"{s_font_family}",sans-serif')
                    if s_color:
                        styles.append(f'color:{s_color}')
                    if s_bold:
                        styles.append('font-weight:bold')
                    if s_italic:
                        styles.append('font-style:italic')
                    if s_underline:
                        styles.append('text-decoration:underline')

                    txt = child.text or ''
                    if txt.strip():
                        p_html.append(f'<span style="{";".join(styles)}">{html_mod.escape(txt)}</span>')

                elif ctag == 'br':
                    p_html.append('<br>')

                if child.tail:
                    p_html.append(html_mod.escape(child.tail))

        if p_html:
            line_h = '1.5'
            if line_spacing and 'multiple:' in line_spacing:
                line_h = line_spacing.split(':')[1]
            p_style_str = f'text-align:{text_align};line-height:{line_h};margin:0;'
            html_parts.append(f'<p style="{p_style_str}">{"".join(p_html)}</p>')

    return ''.join(html_parts)

def render_shape(shape):
    """Render a shape to HTML"""
    tl_x = float(shape.get('topLeftX', 0))
    tl_y = float(shape.get('topLeftY', 0))
    w = float(shape.get('width', 0))
    h = float(shape.get('height', 0))
    shape_type = shape.get('type', 'rect')

    fill_html = ''
    fill_elem = shape.find(f'{{{NS}}}fill')
    if fill_elem is not None:
        fill_color = fill_elem.find(f'{{{NS}}}fillColor')
        fill_img = fill_elem.find(f'{{{NS}}}fillImg')
        if fill_color is not None:
            c = parse_color(fill_color.get('color'))
            if c:
                fill_html = f'background:{c};'
        elif fill_img is not None:
            src = fill_img.get('src', '')
            fill_html = f'background:#eee;'

    border_radius = '0'
    if shape_type == 'circle' or shape_type == 'ellipse':
        border_radius = '50%'

    # Get content
    content_elem = shape.find(f'{{{NS}}}content')
    text_html = render_text_content(content_elem) if content_elem is not None else ''

    opacity = 1
    style = f'position:absolute;left:{tl_x*SCALE}px;top:{tl_y*SCALE}px;width:{w*SCALE}px;height:{h*SCALE}px;{fill_html}border-radius:{border_radius};overflow:hidden;'
    if text_html:
        style += f'display:flex;align-items:flex-start;'

    # Get padding from content
    padding = '0'
    if content_elem is not None:
        pt = content_elem.get('paddingTop', '0')
        pb = content_elem.get('paddingBottom', '0')
        pl = content_elem.get('paddingLeft', '0')
        pr = content_elem.get('paddingRight', '0')
        padding = f'{float(pt)*SCALE}px {float(pr)*SCALE}px {float(pb)*SCALE}px {float(pl)*SCALE}px'

    inner_html = f'<div style="padding:{padding};width:100%;box-sizing:border-box;">{text_html}</div>' if text_html else ''

    return f'<div style="{style}">{inner_html}</div>'

def render_img(img_elem):
    """Render an image element"""
    tl_x = float(img_elem.get('topLeftX', 0))
    tl_y = float(img_elem.get('topLeftY', 0))
    w = float(img_elem.get('width', 0))
    h = float(img_elem.get('height', 0))

    # Images from Lark need file_token but we can't display them directly
    # Show a placeholder with the token
    src = img_elem.get('src', '')
    style = f'position:absolute;left:{tl_x*SCALE}px;top:{tl_y*SCALE}px;width:{w*SCALE}px;height:{h*SCALE}px;'
    style += 'background:#e8e8e8;border:1px dashed #ccc;display:flex;align-items:center;justify-content:center;'
    style += 'color:#aaa;font-size:11px;overflow:hidden;'
    return f'<div style="{style}">[img]</div>'

def render_slide(slide, index):
    """Render a complete slide to HTML"""
    # Get background from style
    bg_color = '#fff'
    style_elem = slide.find(f'{{{NS}}}style')
    if style_elem is not None:
        fill_elem = style_elem.find(f'{{{NS}}}fill')
        if fill_elem is not None:
            fc = fill_elem.find(f'{{{NS}}}fillColor')
            if fc is not None:
                bg_color = parse_color(fc.get('color', 'rgba(244,244,243,1)')) or bg_color
            fi = fill_elem.find(f'{{{NS}}}fillImg')
            if fi is not None:
                bg_color = '#f4f4f3'  # fallback for bg images

    # Get slide data
    data_elem = slide.find(f'{{{NS}}}data')
    if data_elem is None:
        return ''

    children_html = []
    for child in data_elem:
        ctag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if ctag == 'shape':
            children_html.append(render_shape(child))
        elif ctag == 'img':
            children_html.append(render_img(child))
        elif ctag == 'line':
            pass  # skip lines for now
        elif ctag == 'table':
            pass  # skip tables for now
        elif ctag == 'chart':
            pass
        elif ctag == 'whiteboard':
            pass

    slide_style = f'width:{W*SCALE}px;height:{H*SCALE}px;background:{bg_color};position:relative;overflow:hidden;margin:0 auto 24px;box-shadow:0 2px 16px rgba(0,0,0,0.15);border-radius:4px;'

    return f'''
<div style="{slide_style}">
  {''.join(children_html)}
  <div style="position:absolute;bottom:4px;right:8px;font-size:10px;color:#aaa;">{index+1}/7</div>
</div>'''

# Generate HTML
slides = get_slides()

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nothing Account 2026年上半年进展汇报</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  font-family: "PingFang SC","Microsoft YaHei","思源黑体",Arial,sans-serif;
  background: #e8e8e8;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}}
.slide-wrapper {{
  margin-bottom: 16px;
}}
@media (max-width: {W*SCALE+40}px) {{
  body {{ padding: 4px; }}
}}
</style>
</head>
<body>
'''

for i, slide in enumerate(slides):
    html += f'<div class="slide-wrapper">\n{render_slide(slide, i)}\n</div>\n'

html += '''
</body>
</html>'''

output_path = r'C:\Users\jane.yan\competitive-analysis\ppt_export\nothing_account_report.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated: {output_path}")
print(f"Size: {len(html)} bytes")
print(f"Slides: {len(slides)}")

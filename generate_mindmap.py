import sys, json, re, hashlib, os

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r'c:\Users\jane.yan\competitive-analysis'

with open(os.path.join(BASE_DIR, 'nothing_account_baseline.md'), 'r', encoding='utf-8') as f:
    md = f.read()

lines = md.split('\n')

def make_id(topic, counter):
    h = hashlib.md5(f"{topic}{counter}".encode()).hexdigest()[:8]
    return f"n_{h}"

# Parse markdown to tree
root = None
stack = []
counter = [0]
ID_MAP = {}  # id -> node

for line in lines:
    stripped = line.strip()
    if not stripped:
        continue
    m = re.match(r'^(#{1,5})\s+(.+)$', stripped)
    if m:
        level = len(m.group(1))
        topic = m.group(2).strip()
        topic = re.sub(r'\*\*([^*]+)\*\*', r'\1', topic)
        topic = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', topic)
        topic = re.sub(r'`([^`]+)`', r'\1', topic)

        if level == 1:
            nid = make_id(topic, counter[0]); counter[0] += 1
            root = {"id": nid, "topic": topic, "children": []}
            stack = [(1, root)]
            ID_MAP[nid] = root
        else:
            while stack and stack[-1][0] >= level:
                stack.pop()
            if stack:
                parent = stack[-1][1]
                nid = make_id(topic, counter[0]); counter[0] += 1
                node = {"id": nid, "topic": topic, "children": []}
                parent.setdefault("children", []).append(node)
                stack.append((level, node))
                ID_MAP[nid] = node
    elif stripped.startswith('- '):
        topic = stripped[2:].strip()
        topic = re.sub(r'\*\*([^*]+)\*\*', r'\1', topic)
        topic = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', topic)
        topic = re.sub(r'`([^`]+)`', r'\1', topic)
        topic = re.sub(r'^[├└]\s*', '', topic)
        if stack:
            parent = stack[-1][1]
            nid = make_id(topic, counter[0]); counter[0] += 1
            node = {"id": nid, "topic": topic, "children": []}
            parent.setdefault("children", []).append(node)
            ID_MAP[nid] = node

if root is None:
    print("ERROR: No root heading found")
    sys.exit(1)

# Assign directions: CN -> left, others -> right
for child in root.get("children", []):
    topic = child.get("topic", "")
    if "中国区" in topic:
        child["side"] = "left"
    else:
        child["side"] = "right"

# Generate HTML for a node recursively
def gen_node_html(node, depth=0, max_children_per_row=3):
    """Generate HTML for a tree node and its children using CSS grid rows"""
    children = node.get("children", [])
    nid = node["id"]
    topic = node.get("topic", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    side = node.get("side", "")

    # Determine if this node has the "new section" marker (for CN/Intl)
    is_section = depth <= 1

    children_html = ""
    if children:
        # Split children into rows if many
        child_items = []
        for c in children:
            child_items.append(gen_node_html(c, depth + 1))

        if len(children) <= 4:
            # Single row
            children_html = f'''<div class="children-row">{"".join(child_items)}</div>'''
        else:
            # Multiple rows
            rows = []
            row_size = 3
            for i in range(0, len(children), row_size):
                chunk = child_items[i:i+row_size]
                rows.append(f'''<div class="children-row">{"".join(chunk)}</div>''')
            children_html = "".join(rows)

    topic_class = "root-topic" if depth == 0 else ("section-topic" if depth <= 1 else ("sub-topic" if depth <= 2 else "leaf-topic"))
    side_class = f"side-{side}" if side else ""

    return f'''<div class="tree-node {side_class} depth-{depth}" data-id="{nid}" data-depth="{depth}">
    <div class="node-content {topic_class}">
        <span class="toggle-btn" onclick="toggleNode(this)" data-id="{nid}">−</span>
        <span class="topic-text">{topic}</span>
    </div>
    {children_html}
</div>'''

# Actually, let me use a different approach. Instead of complex CSS tree, let me use
# a simple recursive details/summary with CSS styling.

# Generate the mind map as nested collapsible sections
# Left side: CN, Right side: Intl + 通用 + 速查表

body_html_parts = []
left_children = []
right_children = []

for child in root.get("children", []):
    side = child.get("side", "right")
    if side == "left":
        left_children.append(child)
    else:
        right_children.append(child)

def gen_tree_html(node, depth=0, max_depth=99):
    """Generate semantic HTML tree with details/summary"""
    children = node.get("children", [])
    topic = node.get("topic", "")
    topic_esc = topic.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    nid = node.get("id", "")
    side = node.get("side", "")

    # Truncate long topics for display
    display_topic = topic_esc
    if len(display_topic) > 80:
        display_topic = display_topic[:77] + "..."

    # Determine icon based on topic content
    icon = ""
    if "二期" in topic:
        icon = '<span class="badge badge-future">🔄二期</span> '
    elif "❌" in topic or "不支持" in topic:
        icon = ""
    elif "✅" in topic:
        icon = ""

    classes = []
    if depth == 0:
        classes.append("root-node")
    elif depth == 1:
        classes.append("section-node")
    elif depth == 2:
        classes.append("category-node")
    elif depth <= 3:
        classes.append("sub-node")
    else:
        classes.append("leaf-node")

    if side:
        classes.append(f"side-{side}")

    # Build children HTML
    children_html = ""
    if children and depth < max_depth:
        child_parts = []
        for c in children:
            child_parts.append(gen_tree_html(c, depth + 1, max_depth))
        children_html = f'<ul class="tree-children">{"".join(child_parts)}</ul>'

    return f'''<li class="tree-item {" ".join(classes)}" data-id="{nid}" data-depth="{depth}">
    <details {"open" if depth < 3 else ""}>
        <summary class="tree-label" title="{topic_esc}">{icon}{display_topic}</summary>
        {children_html}
    </details>
</li>'''

# Build the complete HTML
columns = []

for child in root.get("children", []):
    side = child.get("side", "right")
    col_html = gen_tree_html(child, depth=1)
    columns.append((side, child["topic"], col_html))

# Render
tree_sections = ""
for side, title, html in columns:
    tree_sections += f'''<div class="column column-{side}">
    <h2 class="column-title">{title}</h2>
    <ul class="tree-root">{html}</ul>
</div>'''

root_html = f'''<div class="root-center">
    <div class="root-label">{root["topic"]}</div>
    <div class="root-subtitle">{sum(1 for _ in ID_MAP)} 个节点 | v1.0 + v2.0 PRD</div>
</div>'''

total_nodes = len(ID_MAP)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nothing Account 账号基线 — 思维导图</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: "Microsoft YaHei", "PingFang SC", -apple-system, "Segoe UI", Roboto, sans-serif;
    background: #f0f2f5; color: #333; min-height: 100vh;
  }}

  /* Header */
  .header {{
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: #fff; padding: 16px 24px; display: flex; align-items: center;
    justify-content: space-between; position: sticky; top: 0; z-index: 100;
    box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  }}
  .header h1 {{ font-size: 20px; font-weight: 600; }}
  .header .meta {{ font-size: 12px; opacity: 0.7; }}
  .header input {{
    padding: 8px 16px; border: 1px solid rgba(255,255,255,0.2); border-radius: 20px;
    background: rgba(255,255,255,0.1); color: #fff; font-size: 14px; width: 240px;
    outline: none; transition: border-color 0.2s;
  }}
  .header input:focus {{ border-color: rgba(255,255,255,0.5); }}
  .header input::placeholder {{ color: rgba(255,255,255,0.4); }}
  .header .btn-group {{ display: flex; gap: 8px; }}
  .header button {{
    background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2);
    border-radius: 6px; padding: 6px 14px; cursor: pointer; font-size: 13px;
    transition: background 0.2s;
  }}
  .header button:hover {{ background: rgba(255,255,255,0.2); }}

  /* Mind Map Container */
  .mindmap-container {{
    display: flex; align-items: flex-start; justify-content: center;
    padding: 40px 20px; gap: 0; min-height: calc(100vh - 64px);
    overflow-x: auto;
  }}

  /* Root Center */
  .root-center {{
    flex-shrink: 0; display: flex; flex-direction: column;
    align-items: center; justify-content: flex-start;
    padding-top: 60px; width: 220px; text-align: center;
  }}
  .root-label {{
    background: linear-gradient(135deg, #1a1a2e, #0f3460);
    color: #fff; font-size: 18px; font-weight: 700; padding: 18px 24px;
    border-radius: 12px; box-shadow: 0 4px 20px rgba(15,52,96,0.3);
    cursor: default; white-space: nowrap;
  }}
  .root-subtitle {{ font-size: 11px; color: #999; margin-top: 8px; }}

  /* Columns */
  .column {{ flex-shrink: 0; padding: 0 20px; }}
  .column-left {{ text-align: right; }}
  .column-right {{ text-align: left; }}
  .column-title {{
    font-size: 16px; font-weight: 700; color: #1a1a2e; margin-bottom: 16px;
    padding-bottom: 8px; border-bottom: 2px solid #e0e0e0;
  }}
  .column-left .column-title {{ text-align: right; }}

  /* Tree */
  .tree-root {{ list-style: none; }}
  .tree-item {{ list-style: none; margin: 0; padding: 0; }}

  details > summary {{
    cursor: pointer; list-style: none; display: flex; align-items: center;
    gap: 6px; padding: 5px 10px; margin: 2px 0; border-radius: 6px;
    transition: background 0.15s; white-space: nowrap;
  }}
  details > summary::-webkit-details-marker {{ display: none; }}
  details > summary:hover {{ background: #e8ecf1; }}
  details[open] > summary {{ font-weight: 600; }}

  .tree-label {{
    font-size: 13px; line-height: 1.5; color: #333;
  }}
  .tree-children {{
    list-style: none; margin-left: 24px; border-left: 2px solid #d0d5dd;
    padding-left: 12px;
  }}

  /* Node styles by depth */
  .root-node {{ }}
  .section-node > .tree-label {{
    font-size: 15px; font-weight: 700; color: #1a1a2e;
    background: linear-gradient(135deg, #f0f4ff, #e8ecf5);
    padding: 8px 14px; border-radius: 8px;
  }}
  .category-node > .tree-label {{
    font-size: 14px; font-weight: 600; color: #2d3a4a;
  }}
  .sub-node > .tree-label {{
    font-size: 13px; color: #444;
  }}
  .leaf-node > .tree-label {{
    font-size: 12px; color: #666;
  }}

  /* Badges */
  .badge {{
    font-size: 11px; padding: 1px 6px; border-radius: 10px; margin-right: 4px;
    display: inline-block; font-weight: 500;
  }}
  .badge-future {{ background: #fff3cd; color: #856404; }}

  /* Highlight search matches */
  .tree-label.highlight {{
    background: #fff9c4 !important; border-radius: 4px;
  }}
  .tree-label.dim {{
    opacity: 0.3;
  }}

  /* Responsive */
  @media (max-width: 768px) {{
    .mindmap-container {{ flex-direction: column; align-items: center; }}
    .root-center {{ padding-top: 20px; }}
    .header input {{ width: 140px; }}

    .tree-children {{ margin-left: 12px; padding-left: 8px; }}
  }}

  /* Print */
  @media print {{
    .header {{ position: static; }}
    body {{ font-size: 11px; }}
  }}

  /* Scrollbar */
  ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
  ::-webkit-scrollbar-track {{ background: #f0f2f5; }}
  ::-webkit-scrollbar-thumb {{ background: #c0c0c0; border-radius: 3px; }}

  /* Connector lines on the left side */
  .column-left .tree-children {{
    border-left: none; border-right: 2px solid #d0d5dd;
    padding-left: 0; padding-right: 12px; margin-left: 0; margin-right: 24px;
  }}
  .column-left .tree-label {{
    direction: rtl; text-align: right;
  }}
</style>
</head>
<body>

<div class="header">
    <div>
        <h1>🧠 Nothing Account 账号基线</h1>
        <div class="meta">{total_nodes} 节点 · 合并 v1.0 + v2.0 PRD · 已区分中国区/海外/APP/Web/出端 · 🔄标记=二期规划</div>
    </div>
    <div class="btn-group">
        <input type="text" id="search" placeholder="🔍 搜索节点…" oninput="doSearch()">
        <button onclick="expandAll()">⬇ 全部展开</button>
        <button onclick="collapseAll()">⬆ 折叠到一级</button>
        <button onclick="resetView()">🔄 重置</button>
    </div>
</div>

<div class="mindmap-container" id="mindmap">
    {root_html}
    {tree_sections}
</div>

<script>
// --- Search ---
function doSearch() {{
    const q = document.getElementById('search').value.trim().toLowerCase();
    const labels = document.querySelectorAll('.tree-label');
    if (!q) {{
        labels.forEach(l => {{ l.classList.remove('highlight', 'dim'); }});
        return;
    }}
    labels.forEach(l => {{
        if (l.textContent.toLowerCase().includes(q)) {{
            l.classList.add('highlight');
            l.classList.remove('dim');
            // Expand ancestors
            let el = l.closest('details');
            while (el) {{
                el.open = true;
                el = el.parentElement.closest('details');
            }}
            // Scroll into view
            l.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        }} else {{
            l.classList.remove('highlight');
            l.classList.add('dim');
        }}
    }});
}}

// --- Expand/Collapse all ---
function expandAll() {{
    document.querySelectorAll('details').forEach(d => d.open = true);
}}
function collapseAll() {{
    document.querySelectorAll('details').forEach(d => {{
        const depth = parseInt(d.closest('.tree-item')?.dataset?.depth || '0');
        if (depth >= 1) d.open = false;
    }});
}}
function resetView() {{
    document.getElementById('search').value = '';
    document.querySelectorAll('.tree-label').forEach(l => l.classList.remove('highlight', 'dim'));
    // Collapse deeper nodes, expand shallow
    document.querySelectorAll('details').forEach(d => {{
        const depth = parseInt(d.closest('.tree-item')?.dataset?.depth || '0');
        d.open = depth < 2;
    }});
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

// --- Keyboard shortcuts ---
document.addEventListener('keydown', e => {{
    if ((e.key === 'f' || e.key === 'F') && (e.ctrlKey || e.metaKey)) {{
        e.preventDefault();
        document.getElementById('search').focus();
    }}
    if (e.key === 'Escape') {{
        resetView();
    }}
}});

console.log('✅ Nothing Account 账号基线思维导图已就绪');
console.log('   节点总数: {total_nodes}');
console.log('   💡 点击 ▶ 展开/折叠 | Ctrl+F 搜索 | 全部展开/折叠按钮');
</script>
</body>
</html>'''

with open(os.path.join(BASE_DIR, 'nothing_account_baseline.html'), 'w', encoding='utf-8') as f:
    f.write(html)

print(f'✅ HTML file created: {len(html)} chars')
print(f'   Total nodes: {total_nodes}')

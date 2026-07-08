import sys, re, os

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r'c:\Users\jane.yan\competitive-analysis'

with open(os.path.join(BASE_DIR, 'nothing_account_baseline.md'), 'r', encoding='utf-8') as f:
    md = f.read()

lines = md.split('\n')

# Parse markdown to tree
root = None
stack = []
counter = [0]

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
        topic = topic.replace('(', '（').replace(')', '）')
        topic = topic.replace('[', '【').replace(']', '】')
        topic = topic.replace(':', '：')
        topic = topic.replace('"', "'")
        if len(topic) > 40:
            topic = topic[:37] + "..."

        if level == 1:
            root = {"topic": topic, "children": [], "depth": 0}
            stack = [(1, root)]
            counter[0] += 1
        else:
            while stack and stack[-1][0] >= level:
                stack.pop()
            if stack:
                parent = stack[-1][1]
                node = {"topic": topic, "children": [], "depth": parent["depth"] + 1}
                parent["children"].append(node)
                stack.append((level, node))
                counter[0] += 1
    elif stripped.startswith('- ') and len(stack) > 0 and stack[-1][1]["depth"] < 6:
        topic = stripped[2:].strip()
        topic = re.sub(r'\*\*([^*]+)\*\*', r'\1', topic)
        topic = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', topic)
        topic = re.sub(r'`([^`]+)`', r'\1', topic)
        topic = re.sub(r'^[├└]\s*', '', topic)
        topic = topic.replace('(', '（').replace(')', '）')
        topic = topic.replace('[', '【').replace(']', '】')
        topic = topic.replace(':', '：')
        topic = topic.replace('"', "'")
        if len(topic) > 60:
            topic = topic[:57] + "..."
        parent = stack[-1][1]
        if parent["depth"] < 7:
            node = {"topic": topic, "children": [], "depth": parent["depth"] + 1}
            parent["children"].append(node)

if root is None:
    print("ERROR: No root")
    sys.exit(1)

MAX_DEPTH = 4

def gen_mermaid(node, indent_level, skip_errors=False):
    """Generate Mermaid mindmap lines recursively"""
    lines = []
    topic = node["topic"]
    depth = node.get("depth", 0)

    # Skip error/exception/badge nodes for flow mind map
    if skip_errors and depth >= 3:
        stripped_topic = topic.strip()
        if (stripped_topic.startswith("异常") or stripped_topic.startswith("异常处理")
            or "小红点" in stripped_topic):
            return lines  # skip this node and its children

    if depth == 0:
        lines.append("mindmap")
        lines.append(f"  root(({topic}))")
        for child in node.get("children", []):
            lines.extend(gen_mermaid(child, 2, skip_errors))
    else:
        indent = "    " * indent_level
        lines.append(f"{indent}{topic}")
        if depth < MAX_DEPTH:
            for child in node.get("children", []):
                lines.extend(gen_mermaid(child, indent_level + 1, skip_errors))
    return lines

# Split root children into groups:
# Group A (用户体验流程): 中国区 + 海外
# Group B (规则与策略): 通用 + 验证码异常场景速查表
children = root.get("children", [])
flow_children = []
rule_children = []

for child in children:
    topic = child.get("topic", "")
    if "中国区" in topic or "海外" in topic:
        flow_children.append(child)
    else:
        rule_children.append(child)

# Create virtual roots
virtual_flow = {"topic": "用户体验流程", "children": flow_children, "depth": 0}
virtual_rules = {"topic": "规则与策略", "children": rule_children, "depth": 0}

# Generate mermaid for each
mermaid_flow_lines = gen_mermaid(virtual_flow, 0, skip_errors=True)
mermaid_rules_lines = gen_mermaid(virtual_rules, 0, skip_errors=False)

mermaid_flow = "\n".join(mermaid_flow_lines)
mermaid_rules = "\n".join(mermaid_rules_lines)

print(f"思维导图1 (用户体验流程): {len(mermaid_flow_lines)} lines, {len(mermaid_flow)} chars")
print(f"思维导图2 (规则与策略): {len(mermaid_rules_lines)} lines, {len(mermaid_rules)} chars")

# Create XML files
for name, mermaid_code in [("flow", mermaid_flow), ("rules", mermaid_rules)]:
    xml = f'<whiteboard type="mermaid">\n{mermaid_code}\n</whiteboard>'
    with open(os.path.join(BASE_DIR, f'whiteboard_{name}.xml'), 'w', encoding='utf-8') as f:
        f.write(xml)

print("Files written: whiteboard_flow.xml, whiteboard_rules.xml")

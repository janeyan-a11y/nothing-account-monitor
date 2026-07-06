# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

海外手机系统账号竞品分析项目。产品经理（Jane Yan）对标 Google/Apple/华为/小米/OPPO/vivo 等手机系统账号的注册、登录、安全、注销等流程，生成结构化分析报告。输出物包括 Mermaid 流程图、Markdown 对比表格、带截图的 HTML 报告。

## Key Workflows

### 1. ADB 设备操作（核心工作流）

通过 MCP `android-adb` server 操作 Android 设备：

- `mcp__android-adb__adb_devices` — 列出已连接设备
- `mcp__android-adb__take_screenshot_and_save` — 截图并保存到指定路径
- `mcp__android-adb__adb_shell` — 执行 shell 命令（`input tap x y` 点击、`input swipe` 滑动、`input text` 输入文字）
- `mcp__android-adb__adb_pull` — 拉取文件（注意 Windows 路径问题，报错时仍可能成功）

**重要技巧：** 当页面是 WebView 无法通过 `uiautomator dump` 读元素时，先 dump 看是否 `android.webkit.WebView`，如果是则 web 内容可被 dump 出来（如小米账号页面的 WebView 可读）。

**导航模式：**
1. `uiautomator dump /sdcard/ui.xml` → `cat /sdcard/ui.xml` 读 UI 树
2. 找到目标元素的 `bounds="[x1,y1][x2,y2]"`，计算中心点 `((x1+x2)/2, (y1+y2)/2)`
3. `input tap <cx> <cy>` 点击
4. 截图确认页面变化

### 2. HTML 报告生成与部署

报告文件在 `reports/` 目录：

- 源文件：`reports/report_账号注销_2025-06-25.html`（编辑此文件）
- 部署文件：`reports/account-deletion-analysis.html`（含 base64 嵌入图片的自包含版本）

**生成部署文件的命令：**
```bash
python3 -c "
import base64, re, os
rd = r'c:\Users\jane.yan\competitive-analysis\reports'
with open(os.path.join(rd, 'report_账号注销_2025-06-25.html'), encoding='utf-8') as f:
    html = f.read()
for n in set(re.findall(r'src=\"([^\"]+_composite\.png)\"', html)):
    ip = os.path.join(rd, n)
    if os.path.exists(ip):
        with open(ip, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('ascii')
        html = html.replace(f'src=\"{n}\"', f'src=\"data:image/png;base64,{b64}\"')
        html = html.replace(f'href=\"{n}\"', 'href=\"#\"')
with open(os.path.join(rd, 'account-deletion-analysis.html'), 'w', encoding='utf-8') as f:
    f.write(html)
"
```

**部署到 hub：**
```bash
curl -s -F "file=@c:\Users\jane.yan\competitive-analysis\reports\account-deletion-analysis.html" -F "folder=jane" "http://172.30.5.62:3100/api/upload"
```
> Hub 地址：`http://172.30.5.62:3100/pages/jane/<filename>`，仅接受 `.html` 文件。图片需 base64 嵌入。

### 3. 复合截图生成

`src/` 下有多个 Python 脚本，用 Pillow 将零散截图拼合为带标注的复合图：

| 脚本 | 输出 |
|------|------|
| `src/create_composite.py` | Google 复合图 |
| `src/create_apple_composite.py` | Apple 复合图 |
| `src/create_huawei_composite.py` | 华为复合图 |
| `src/create_xiaomi_final.py` | 小米复合图（真机实测版） |
| `src/create_oppo_from_user_screenshots.py` | OPPO/一加复合图（用户截图版） |
| `src/create_oem_composites.py` | 旧版批量生成（已被上述替代，仅 vivo 从这出） |

运行：`python3 src/create_<name>.py`，输出到 `reports/<name>_account_deletion_composite.png`。

## Directory Structure

```
competitive-analysis/
├── data/accounts.json           # 竞品账号矩阵（已注册/未注册）
├── screenshots/
│   ├── Google/账号注销/downloaded/  # 网页下载的截图
│   ├── Apple/账号注销/
│   ├── 华为/账号注销/
│   ├── 小米/账号注销/                  # 真机实测截图
│   ├── OPPO/账号注销/                  # 真机+网页截图
│   └── OnePlus/web_deletion/         # 一加网页版注销（同 OPPO 体系）
├── reports/
│   ├── report_账号注销_2025-06-25.html  # 编辑源文件
│   ├── account-deletion-analysis.html  # 部署版（base64 嵌入）
│   └── *_account_deletion_composite.png  # 复合截图
├── src/
│   ├── generate_report.js          # 旧版报告生成（已不用，直接操作 HTML）
│   └── create_*_composite.py       # 复合图生成脚本
├── prompt_template.md              # 分析 Prompt 模板
├── CLAUDE_PROJECT_KNOWLEDGE.md     # 项目背景知识（竞品列表、分析维度）
└── .mcp.json                       # MCP 配置（android-adb, mcp-vision, agents-html-hub）
```

## 核心纪律：反幻觉规则

**所有输出必须有依据，禁止编造。不明确的地方必须向用户确认。**

1. **截图即证据**：流程步骤、UI 文字、交互行为必须来自截图或真机操作记录。无截图不写入分析。
2. **实测优先**：优先 ADB 真机实测。网页截图次之。纯文字描述只能标为「待验证」。
3. **不确定就问**：对截图内容、流程分支、功能是否存在存疑时，**必须向用户发问确认**，严禁猜测。
4. **标注来源**：每条信息注明出处——「真机实测」「网页截图（URL）」「官方文档」「待验证」。
5. **错误即改**：用户指出的错误立即修正，并同步更新所有引用处（复合图、HTML、对比表）。

## 关键注意事项

1. **Git Bash / PowerShell 混用**：Windows 环境，Bash 工具用的是 Git Bash（POSIX sh），部分命令如 `grep`/`head` 不可用，需用 Python 替代。`copy` 是 PowerShell 命令，Bash 中要用 `cp`。

2. **Python 编码**：print 中文需 `sys.stdout.reconfigure(encoding='utf-8')`，否则在 Git Bash 中会 `UnicodeEncodeError`。

3. **真机实测 > 网页下载**：优先使用 ADB 操控真机截图。网页下载的截图可能有水印、低分辨率或版本不匹配。

4. **HTML 编辑时注意顺序**：报告章节按「总结→设计建议→结论→详情分析→竞品对比」排列，Mermaid 流程图放在对应竞品的小节内，不要错位到其他竞品下。

5. **复合图标题注意**：复合图内部有标题文字（如 "核心发现：..."），修改流程文字需同时改 Python 脚本重新生成 PNG；修改 HTML 文本只需改 HTML。

6. **adb 设备识别**：多设备连接时用 `adb -s <serial>` 指定。当前常用设备：OnePlus `2715c13b`、Xiaomi `9a9d526e`。

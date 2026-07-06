# 竞品分析工作流工具集

> 海外手机系统账号竞品分析——从体验到报告的 AI 辅助流水线

## 三种使用方式

本工具支持三种分发和使用方式，按需选择：

| 方式 | 适用场景 | 命令 |
|------|----------|------|
| **npm CLI** | 命令行直接使用，独立于 Claude Code | `competitive-analysis account list` |
| **Claude Code Skill** | 在 Claude Code 中使用 slash commands | `/analyze-competitor` 等 |
| **MCP Server** | 通过 MCP 协议在 Claude Code 中调用 Tools | `check_device`, `capture_screenshot` 等 |

---

## 方式一：npm CLI 全局安装

### 安装

```bash
# 从本目录直接安装（开发）
npm install -g .

# 或发布到 npm 后
npm install -g competitive-analysis
```

### 使用

```bash
# 账号管理
competitive-analysis account list                    # 列出所有账号
competitive-analysis account add                     # 交互式添加账号
competitive-analysis account push Google             # 推送 Google 账号到手机
competitive-analysis account search --type unregistered  # 搜索未注册邮箱

# 截图
competitive-analysis screenshot capture Google "注册" "点击设置→账号→注册"
competitive-analysis screenshot batch Google "注册"  # 交互式连续截图
competitive-analysis screenshot list                 # 列出所有截图
competitive-analysis screenshot list Google          # 按竞品筛选

# 报告
competitive-analysis report "第三方账号绑定"                  # 模板模式
competitive-analysis report "邮箱注册" --competitors "Google,Apple" --ai  # AI 模式
competitive-analysis report "注销账号" --all --ai            # 全量 AI 分析

# 工具
competitive-analysis device                           # 检测设备连接
competitive-analysis web                              # 启动 Web 控制台
competitive-analysis templates                        # 输出 Prompt 模板
competitive-analysis --help                           # 查看帮助
```

### 环境变量

- `ANTHROPIC_API_KEY` — Claude API key（AI 命名和分析需要）
- `ADB_DEVICE` — 指定 ADB 设备序列号（多设备时使用）

---

## 方式二：Claude Code Skill

### 安装

将 `skills/competitive-analysis/` 目录复制到你的 Claude Code 项目的 `.claude/skills/` 目录：

```bash
# 从 npm 包复制
cp -r node_modules/competitive-analysis/skills/competitive-analysis .claude/skills/

# 或从源码复制
cp -r skills/competitive-analysis .claude/skills/
```

### 可用命令

- `/analyze-competitor <competitor> <feature>` — 分析单个竞品的指定功能
- `/compare-all <feature>` — 生成全量竞品对比报告
- `/screenshot <competitor> <feature>` — 截图并归档
- `/accounts` — 列出账号矩阵
- `/push-account <competitor>` — 推送账号到手机
- `/report <feature>` — 生成报告模板

### 在 Claude Code 中使用

安装后，在对话中直接输入 `/analyze-competitor Google 第三方账号绑定` 等命令即可。

---

## 方式三：MCP Server

### 配置

在项目 `.mcp.json` 中添加：

```json
{
  "mcpServers": {
    "competitive-analysis": {
      "command": "node",
      "args": ["src/mcp-server.js"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

如果通过 npm 全局安装，使用绝对路径：

```json
{
  "mcpServers": {
    "competitive-analysis": {
      "command": "node",
      "args": ["C:/Users/<username>/AppData/Roaming/npm/node_modules/competitive-analysis/src/mcp-server.js"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

### 可用 Tools (8个)

| Tool | 描述 | 参数 |
|------|------|------|
| `check_device` | 检测 ADB 设备连接 | 无 |
| `list_accounts` | 列出所有竞品账号 | `category?` (system/consumer) |
| `search_accounts` | 按类型/竞品搜索账号 | `type?`, `competitor?` |
| `push_account` | 推送账号到手机剪贴板 | `competitor` (必填) |
| `capture_screenshot` | 截图并归档 | `competitor`, `feature`, `step?` |
| `list_screenshots` | 列出已有截图 | `competitor?`, `feature?` |
| `generate_report` | 生成分析报告 | `feature` (必填), `competitors?`, `ai_mode?` |
| `get_prompt_template` | 获取 Prompt 模板 | `template_id` (1-4) |

### 在 Claude Code 中使用

配置完成后，MCP Tools 自动出现在 Claude Code 的 Tool 列表中。例如：

> "帮我检测设备是否连接，然后列出所有截图"

Claude 会自动调用 `check_device` 和 `list_screenshots` 两个 Tool。

---

## 项目结构

```
competitive-analysis/
├── README.md
├── package.json
├── prompt_template.md         # 可复用 Prompt 模板
├── .mcp.json                  # MCP Server 配置
├── bin/
│   └── competitive-analysis.js  # npm CLI 入口
├── src/
│   ├── index.js               # 库入口 (barrel export)
│   ├── mcp-server.js          # MCP stdio server
│   ├── lib/                   # 核心库
│   │   ├── config.js          # 统一配置
│   │   ├── adb.js             # ADB 操作
│   │   ├── accounts.js        # 账号管理
│   │   ├── screenshots.js     # 截图管理
│   │   └── reports.js         # 报告生成
│   ├── account_manager.js     # 账号 CLI (兼容层)
│   ├── screenshot_helper.js   # 截图 CLI (兼容层)
│   └── generate_report.js     # 报告 CLI (兼容层)
├── skills/
│   └── competitive-analysis/
│       └── SKILL.md           # Claude Code Skill 定义
├── server.js                  # Web 控制台服务器
├── start.js                   # 交互式菜单
├── agent.html                 # Web 控制台前端
├── templates.html             # Prompt 模板浏览器
├── data/                      # 账号数据
├── screenshots/               # 截图存档
└── reports/                   # 生成的报告
```

---

## 整体工作流

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  1. 体验截图   │ →  │  2. AI 整理   │ →  │  3. 生成报告  │ →  │  4. 设计决策   │
│  (你 + 手机)  │    │  (Claude)    │    │  (Claude)    │    │  (你拍板)    │
├──────────────┤    ├──────────────┤    ├──────────────┤    ├──────────────┤
│ scrcpy 投屏  │    │ 截图自动命名 │    │ 单竞品分析   │    │ 对比表+结论  │
│ adb 快捷截图 │    │ 分支路径串联 │    │ 流程图生成   │    │ 推荐设计     │
│ 账号快捷输入 │    │ 步骤说明生成 │    │ 对比表生成   │    │ 差异点分析   │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
        30 min/竞品         10 min/竞品         10 竞品全量        15 min
```

## 环境准备

### 1. 安装 Node.js 依赖

```bash
cd competitive-analysis
npm install
```

### 2. 安装手机投屏工具

**Android**:
```bash
# 下载 scrcpy: https://github.com/Genymobile/scrcpy
# 或通过包管理器: winget install Genymobile.scrcpy

# 验证 adb 可用
adb devices
```

**iPhone** (macOS):
```
用系统自带的 iPhone 镜像功能（macOS Sequoia+）
或通过 QuickTime Player → 新建影片录制 → 选择 iPhone
```

### 3. (可选) 设置 Claude API Key

```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# 或创建 .env 文件
```

---

## 快速参考

### 账号管理 (三种方式等效)
```bash
# npm CLI
competitive-analysis account list
# 或 legacy CLI
node src/account_manager.js list
# 或 MCP Tool
mcp: list_accounts
```

### 截图
```bash
# npm CLI
competitive-analysis screenshot capture Google "注册" "点击设置"
# 或 legacy CLI
node src/screenshot_helper.js --competitor Google --feature "注册" --step "点击设置"
# 或 MCP Tool
mcp: capture_screenshot { competitor: "Google", feature: "注册", step: "点击设置" }
```

### 报告
```bash
# npm CLI
competitive-analysis report "第三方账号绑定" --ai
# 或 legacy CLI
node src/generate_report.js --feature "第三方账号绑定" --ai
# 或 MCP Tool
mcp: generate_report { feature: "第三方账号绑定", ai_mode: true }
```

---

## 竞品列表

| # | 竞品 | 分类 | 账号类型 |
|---|------|------|----------|
| 1 | Google Account | 系统账号 | Google 账号 |
| 2 | Apple ID | 系统账号 | Apple ID |
| 3 | OPPO HeyTap | 系统账号 | 手机号 |
| 4 | 华为账号 | 系统账号 | 手机号/邮箱 |
| 5 | 小米账号 | 系统账号 | 手机号/邮箱 |
| 6 | vivo账号 | 系统账号 | 手机号/邮箱 |
| 7 | Trip.com | C端账号 | 邮箱 |
| 8 | Instagram | C端账号 | 邮箱/用户名 |
| 9 | RedNote | C端账号 | 手机号 |
| 10 | WeChat | C端账号 | 手机号 |

---

## FAQ

### Q: 发布到 npm 后别人怎么用？
**A:** `npm install -g competitive-analysis`，然后 `competitive-analysis --help` 查看所有子命令。

### Q: 三种方式怎么选？
**A:** 简单来说：习惯命令行的用 npm CLI，在 Claude Code 里用的用 MCP Server，需要快捷模板的就装 Skill。三者可以同时使用。

### Q: 如何给其他团队成员使用？
**A:** 
1. `npm publish` 发布到 npm（或私有 registry），团队成员 `npm install -g` 即可
2. 或者把整个项目文件夹复制给别人，`npm install && npm link` 就能用
3. `.mcp.json` 和 `skills/` 目录也可以直接复制到别人的项目中

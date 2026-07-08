# 竞品分析 Skill

分析分 3 个阶段，按顺序读取子文件：

## Phase Map

```
用户说"分析XX的YY功能"
  │
  ├─→ 阶段 1: 读取 init.md  → 确认目标+体验方式（4选1）
  │     ├─ 选 2(搜索): 读取 research.md   → 搜索截图→整理流程→标注来源
  │     └─ 选 3/4(AI截图): 读取 screenshot.md → 强制截图日志
  ├─→ 阶段 3: 读取 report.md       → 总-分报告+零幻觉
  └─→ 输出前: 读取 quality-gates.md → 5道门禁（必须输出可见证据）
```

## 竞品列表

| # | 竞品 | 类型 |
|---|------|------|
| 1 | Google Account | 系统账号 |
| 2 | Apple ID | 系统账号 |
| 3 | 华为账号 | 系统账号 |
| 4 | 小米账号 | 系统账号（`9a9d526e`）|
| 5 | OPPO/OnePlus | 系统账号（`2715c13b`）|
| 6 | vivo账号 | 系统账号 |

## 环境

Win11 + Python3 + Node.js | ADB + MCP: `android-adb` `mcp-vision`

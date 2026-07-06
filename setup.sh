#!/usr/bin/env bash
set -e

echo ""
echo "╔══════════════════════════════════╗"
echo "║   📱 竞品分析工具集 - 安装向导  ║"
echo "╚══════════════════════════════════╝"
echo ""

echo "[1/3] 安装 Node.js 依赖..."
npm install
echo "✅ 依赖安装完成"
echo ""

echo "[2/3] 注册全局命令..."
npm link
echo "✅ 全局命令已注册"
echo ""

echo "[3/3] 创建必要目录..."
mkdir -p screenshots reports data
echo "✅ 目录结构已创建"
echo ""

echo "══════════════════════════════════"
echo "  🎉 安装完成！"
echo "══════════════════════════════════"
echo ""
echo "  📋 快速开始:"
echo "    competitive-analysis --help"
echo "    competitive-analysis device"
echo "    competitive-analysis account list"
echo ""
echo "  🌐 启动 Web 控制台:"
echo "    competitive-analysis web"
echo "    → 浏览器打开 http://localhost:3456"
echo ""
echo "  🤖 Claude Code MCP 配置:"
echo "    已将 MCP Server 信息写入 .mcp.json"
echo "    在 Claude Code 项目中引用即可"
echo ""

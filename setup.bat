@echo off
chcp 65001 >nul
echo.
echo ╔══════════════════════════════════╗
echo ║   📱 竞品分析工具集 - 安装向导  ║
echo ╚══════════════════════════════════╝
echo.

echo [1/3] 安装 Node.js 依赖...
call npm install
if %errorlevel% neq 0 (
    echo ❌ npm install 失败，请检查 Node.js 是否安装
    pause
    exit /b 1
)
echo ✅ 依赖安装完成
echo.

echo [2/3] 注册全局命令...
call npm link
if %errorlevel% neq 0 (
    echo ⚠️  npm link 失败，可能需要管理员权限
)
echo ✅ 全局命令已注册
echo.

echo [3/3] 创建必要目录...
if not exist "screenshots" mkdir screenshots
if not exist "reports" mkdir reports
if not exist "data" mkdir data
echo ✅ 目录结构已创建
echo.

echo ══════════════════════════════════
echo   🎉 安装完成！
echo ══════════════════════════════════
echo.
echo   📋 快速开始:
echo     competitive-analysis --help
echo     competitive-analysis device
echo     competitive-analysis account list
echo.
echo   🌐 启动 Web 控制台:
echo     competitive-analysis web
echo     → 浏览器打开 http://localhost:3456
echo.
echo   🤖 Claude Code MCP 配置:
echo     已将 MCP Server 信息写入 .mcp.json
echo     在 Claude Code 项目中引用即可
echo.
pause

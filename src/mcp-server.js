/**
 * 竞品分析工具 - MCP Server (JSON-RPC over stdio)
 *
 * 不依赖 @modelcontextprotocol/sdk（它是 ESM-only）。
 * 直接实现 MCP stdio 传输协议的 JSON-RPC 2.0 子集。
 *
 * 暴露 8 个 Tools 供 Claude Code 调用：
 *   check_device, list_accounts, search_accounts, push_account,
 *   capture_screenshot, list_screenshots, generate_report, get_prompt_template
 *
 * 用法: node src/mcp-server.js
 * 在 .mcp.json 中配置:
 *   { "mcpServers": { "competitive-analysis": { "command": "node", "args": ["src/mcp-server.js"] } } }
 */

const readline = require('readline');
const fs = require('fs');
const path = require('path');

// ============================================================
// MCP 协议常量
// ============================================================

const PROTOCOL_VERSION = '2024-11-05';
const SERVER_NAME = 'competitive-analysis';
const SERVER_VERSION = '1.0.0';

// ============================================================
// Tool 定义
// ============================================================

const TOOLS = [
  {
    name: 'check_device',
    description: '检测 Android 设备是否通过 ADB 连接',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'list_accounts',
    description: '列出所有竞品测试账号',
    inputSchema: {
      type: 'object',
      properties: {
        category: {
          type: 'string',
          enum: ['system', 'consumer'],
          description: '按分类筛选：system=系统账号类, consumer=C端账号类',
        },
      },
      required: [],
    },
  },
  {
    name: 'search_accounts',
    description: '按类型或竞品名搜索账号',
    inputSchema: {
      type: 'object',
      properties: {
        type: {
          type: 'string',
          enum: ['registered', 'unregistered'],
          description: '按注册状态筛选',
        },
        competitor: {
          type: 'string',
          description: '按竞品名模糊搜索',
        },
      },
      required: [],
    },
  },
  {
    name: 'push_account',
    description: '将指定竞品的账号密码推送到手机剪贴板',
    inputSchema: {
      type: 'object',
      properties: {
        competitor: {
          type: 'string',
          description: '竞品名，如 Google, Apple, Instagram',
        },
      },
      required: ['competitor'],
    },
  },
  {
    name: 'capture_screenshot',
    description: '从已连接的 Android 设备截图并归档到对应竞品/功能目录',
    inputSchema: {
      type: 'object',
      properties: {
        competitor: {
          type: 'string',
          description: '竞品名',
        },
        feature: {
          type: 'string',
          description: '功能名，如 "注册", "第三方绑定"',
        },
        step: {
          type: 'string',
          description: '步骤描述（可选）',
        },
      },
      required: ['competitor', 'feature'],
    },
  },
  {
    name: 'list_screenshots',
    description: '列出已有的竞品截图',
    inputSchema: {
      type: 'object',
      properties: {
        competitor: {
          type: 'string',
          description: '按竞品筛选（可选）',
        },
        feature: {
          type: 'string',
          description: '按功能筛选（可选）',
        },
      },
      required: [],
    },
  },
  {
    name: 'generate_report',
    description: '根据截图生成竞品分析报告模板（本地模式）或 AI 模式报告',
    inputSchema: {
      type: 'object',
      properties: {
        feature: {
          type: 'string',
          description: '功能名，如 "第三方账号绑定"',
        },
        competitors: {
          type: 'string',
          description: '指定竞品，逗号分隔。不指定则包含所有有截图的竞品',
        },
        ai_mode: {
          type: 'boolean',
          description: '是否使用 AI 模式（需 ANTHROPIC_API_KEY）',
        },
      },
      required: ['feature'],
    },
  },
  {
    name: 'get_prompt_template',
    description: '获取竞品分析的 Prompt 模板，用于在 Claude Code 中指导分析',
    inputSchema: {
      type: 'object',
      properties: {
        template_id: {
          type: 'string',
          enum: ['1', '2', '3', '4'],
          description: '模板编号：1=单竞品分析, 2=全量对比, 3=截图整理, 4=快速分析',
        },
      },
      required: ['template_id'],
    },
  },
];

// ============================================================
// Tool 执行器
// ============================================================

async function executeTool(name, args) {
  switch (name) {
    case 'check_device': {
      const { checkDevice } = require('./lib/adb');
      const result = checkDevice();
      if (result.connected) {
        return `✅ 设备已连接: ${result.device}\n所有设备: ${result.devices.join(', ')}`;
      }
      return `❌ 未检测到 Android 设备。请确保：\n1. 手机已用 USB 连接电脑\n2. 手机已开启 USB 调试\n3. adb devices 能看到设备`;
    }

    case 'list_accounts': {
      const { loadAccounts, listAccounts } = require('./lib/accounts');
      const data = loadAccounts();
      let all = listAccounts(data);

      if (args.category) {
        all = all.filter(a => a.category === args.category);
      }

      const lines = [`共 ${all.length} 个账号：`];
      for (const a of all) {
        const tag = a.type === 'unregistered' ? '🆕' : '✅';
        lines.push(`  ${tag} [${a.competitor}] ${a.display} (${a.type})${a.note ? ' — ' + a.note : ''}${a.has2FA ? ' ⚠️2FA' : ''}`);
      }
      return lines.join('\n');
    }

    case 'search_accounts': {
      const { loadAccounts, searchAccounts } = require('./lib/accounts');
      const data = loadAccounts();
      const results = searchAccounts(data, {
        type: args.type,
        competitor: args.competitor,
      });

      if (results.length === 0) return '未找到匹配的账号';
      const lines = [`找到 ${results.length} 个账号：`];
      for (const a of results) {
        lines.push(`  [${a.competitor}] ${a.display} (${a.type})${a.note ? ' — ' + a.note : ''}`);
      }
      return lines.join('\n');
    }

    case 'push_account': {
      const { pushAccount } = require('./lib/accounts');
      const result = pushAccount(args.competitor);

      if (!result.success) return `❌ ${result.error}`;

      let msg = `✅ 已推送 ${result.competitor} 账号到手机\n`;
      msg += `📋 账号: ${result.account}\n`;
      msg += `🔐 密码: ${result.password}\n`;
      if (result.clipboardOk) {
        msg += `📋 账号已复制到剪贴板，可直接粘贴\n`;
      }
      msg += `💡 完整信息在手机 sdcard/account_cred.txt`;
      return msg;
    }

    case 'capture_screenshot': {
      const { captureScreenshot } = require('./lib/adb');
      const { aiRename, archiveScreenshot } = require('./lib/screenshots');

      // 1. 截图
      const shot = captureScreenshot();
      if (!shot.success) return `❌ ${shot.error}`;

      // 2. AI 命名
      const context = `竞品=${args.competitor} 功能=${args.feature} 步骤=${args.step || '操作截图'}`;
      const filename = await aiRename(shot.path, context);

      // 3. 归档
      const archived = archiveScreenshot(shot.path, filename, args.competitor, args.feature);
      if (!archived.success) return `❌ ${archived.error}`;

      return `✅ 截图完成\n📸 文件: ${archived.relativePath}\n📁 竞品: ${args.competitor}\n🏷️  功能: ${args.feature}`;
    }

    case 'list_screenshots': {
      const { listScreenshots } = require('./lib/screenshots');
      const files = listScreenshots(args.competitor, args.feature);

      if (files.length === 0) return '暂无截图';

      const lines = [`共 ${files.length} 张截图：`];
      for (const f of files) {
        lines.push(`  📸 ${f}`);
      }
      return lines.join('\n');
    }

    case 'generate_report': {
      const { collectScreenshots, generateMarkdownReport, saveReport, generateAIReport } = require('./lib/reports');
      const { CONFIG } = require('./lib/config');

      let competitorFilter = null;
      if (args.competitors) {
        competitorFilter = args.competitors.split(',').map(s => s.trim());
      }

      if (args.ai_mode && CONFIG.anthropicApiKey) {
        try {
          const result = await generateAIReport(args.feature, competitorFilter);
          return `✅ AI 报告已生成\n📄 文件: ${result.path}\n\n前 500 字预览:\n${result.report.substring(0, 500)}...`;
        } catch (e) {
          return `❌ AI 分析失败: ${e.message}`;
        }
      }

      const screenshots = collectScreenshots(args.feature, competitorFilter);
      const report = generateMarkdownReport(args.feature, screenshots);
      const filepath = saveReport(args.feature, report);

      const total = Object.values(screenshots).flat().length;
      const withShots = Object.keys(screenshots).filter(k => screenshots[k].length > 0);

      return [
        `✅ 报告模板已生成`,
        `📄 文件: ${filepath}`,
        `📸 截图: ${total} 张，覆盖 ${withShots.length} 个竞品`,
        `💡 使用 report 命令配合 ai_mode=true 可获得 AI 分析`,
      ].join('\n');
    }

    case 'get_prompt_template': {
      const templateFile = path.join(__dirname, '..', 'prompt_template.md');
      if (!fs.existsSync(templateFile)) return '⚠️ prompt_template.md 不存在';

      const content = fs.readFileSync(templateFile, 'utf-8');
      const sections = content.split(/(?=^## 模板)/m);

      const id = parseInt(args.template_id, 10);
      if (id >= 1 && id <= 4 && sections[id]) {
        return sections[id].trim();
      }

      // 返回全部模板概览
      return content.substring(0, 2000);
    }

    default:
      return `未知工具: ${name}`;
  }
}

// ============================================================
// MCP JSON-RPC 消息处理
// ============================================================

function handleInitialize(id) {
  return {
    jsonrpc: '2.0',
    id,
    result: {
      protocolVersion: PROTOCOL_VERSION,
      capabilities: { tools: {} },
      serverInfo: {
        name: SERVER_NAME,
        version: SERVER_VERSION,
      },
    },
  };
}

function handleToolsList(id) {
  return {
    jsonrpc: '2.0',
    id,
    result: { tools: TOOLS },
  };
}

async function handleToolsCall(id, params) {
  const { name, arguments: args } = params;

  try {
    const text = await executeTool(name, args || {});
    return {
      jsonrpc: '2.0',
      id,
      result: {
        content: [{ type: 'text', text }],
      },
    };
  } catch (e) {
    return {
      jsonrpc: '2.0',
      id,
      result: {
        content: [{ type: 'text', text: `执行 ${name} 时出错: ${e.message}` }],
        isError: true,
      },
    };
  }
}

// ============================================================
// Stdio 主循环
// ============================================================

function main() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false,
  });

  // 将 stderr 重定向到日志文件，避免干扰 stdio 协议
  const logStream = fs.createWriteStream(
    path.join(__dirname, '..', 'mcp-server.log'),
    { flags: 'a' }
  );

  function log(msg) {
    logStream.write(`[${new Date().toISOString()}] ${msg}\n`);
  }

  log('MCP Server started');

  rl.on('line', async (line) => {
    if (!line.trim()) return;

    let msg;
    try {
      msg = JSON.parse(line);
    } catch {
      log(`Failed to parse: ${line}`);
      return;
    }

    log(`Received: ${msg.method || 'response'}`);

    let response = null;

    try {
      if (msg.method === 'initialize') {
        response = handleInitialize(msg.id);
      } else if (msg.method === 'tools/list') {
        response = handleToolsList(msg.id);
      } else if (msg.method === 'tools/call') {
        response = await handleToolsCall(msg.id, msg.params);
      } else if (msg.method === 'notifications/initialized') {
        // 通知不需要响应
        log('Client initialized');
      } else if (msg.id === undefined || msg.method?.startsWith('notifications/')) {
        // 其他通知，忽略
      } else {
        response = {
          jsonrpc: '2.0',
          id: msg.id,
          error: {
            code: -32601,
            message: `Method not found: ${msg.method}`,
          },
        };
      }
    } catch (e) {
      log(`Error handling ${msg.method}: ${e.message}`);
      response = {
        jsonrpc: '2.0',
        id: msg.id,
        error: {
          code: -32603,
          message: `Internal error: ${e.message}`,
        },
      };
    }

    if (response) {
      const json = JSON.stringify(response);
      process.stdout.write(json + '\n');
      log(`Sent: ${json.substring(0, 200)}`);
    }
  });

  rl.on('close', () => {
    log('MCP Server stopped');
    logStream.end();
    process.exit(0);
  });

  process.on('SIGTERM', () => {
    log('SIGTERM received');
    rl.close();
  });

  process.on('SIGINT', () => {
    log('SIGINT received');
    rl.close();
  });
}

main();

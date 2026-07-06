/**
 * 竞品分析工具 - 后端服务
 * 用法: node server.js
 * 浏览器打开: http://localhost:3456
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { checkDevice } = require('./src/lib/adb');
const { listAccounts, pushAccount } = require('./src/lib/accounts');
const { listScreenshots } = require('./src/lib/screenshots');
const { countScreenshots, generateMarkdownReport, saveReport } = require('./src/lib/reports');
const { CONFIG, ALL_COMPETITORS } = require('./src/lib/config');

const PORT = CONFIG.serverPort;

// ==================== API 处理函数 ====================

function handleDevice() {
  return checkDevice();
}

function handleAccountsList() {
  const accounts = listAccounts();
  return { accounts, output: `共 ${accounts.length} 个账号` };
}

function handleAccountsPush(data) {
  const result = pushAccount(data.competitor);
  return {
    ...result,
    output: result.success
      ? `✅ 已推送 ${result.competitor} 账号到手机`
      : `❌ ${result.error}`,
  };
}

function handleScreenshot(data) {
  try {
    const { captureAndArchive } = require('./src/lib/screenshots');
    // 注意：这是异步的，但 HTTP handler 中我们 await
    return { _async: true, _fn: 'captureAndArchive', _args: [data] };
  } catch (e) {
    return { error: e.message, output: `❌ 截图失败: ${e.message}` };
  }
}

function handleScreenshotsList() {
  const files = listScreenshots();
  return { files, output: `共 ${files.length} 张截图` };
}

function handleReport(data) {
  const feature = data.feature || 'passkey';
  const screenshots = countScreenshots(feature);
  const report = generateMarkdownReport(feature,
    Object.fromEntries(Object.entries(screenshots).map(([k, v]) => [k, Array(v).fill('')]))
  );
  const filepath = saveReport(feature, report);
  return { success: true, output: `✅ 报告已生成: ${filepath}`, path: filepath, feature };
}

function handleScrcpy() {
  const { exec } = require('child_process');
  exec('scrcpy --window-title "竞品分析"', { stdio: 'ignore' });
  return { success: true, output: '✅ scrcpy 投屏已启动' };
}

// ==================== HTTP 服务 ====================

const server = http.createServer(async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  // 静态文件
  if (req.method === 'GET' && req.url === '/') {
    const html = fs.readFileSync(path.join(__dirname, 'agent.html'), 'utf-8');
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(html);
    return;
  }

  // API 路由
  if (req.method === 'POST' || req.method === 'GET') {
    const body = await new Promise((resolve) => {
      let b = '';
      req.on('data', c => b += c);
      req.on('end', () => resolve(b));
    });

    let data = {};
    try { data = JSON.parse(body); } catch {}

    const url = req.url.split('?')[0];
    let result;

    switch (url) {
      case '/device':
        result = handleDevice();
        break;
      case '/accounts/list':
        result = handleAccountsList();
        break;
      case '/accounts/push':
        result = handleAccountsPush(data);
        break;
      case '/screenshot': {
        // 截图是异步的，需要特殊处理
        try {
          const { captureScreenshot: cap } = require('./src/lib/adb');
          const { aiRename, archiveScreenshot } = require('./src/lib/screenshots');
          const competitor = data.competitor || 'Google';
          const feature = data.feature || 'passkey';

          const shot = cap();
          if (!shot.success) {
            result = { error: shot.error, output: `❌ ${shot.error}` };
          } else {
            const context = `竞品=${competitor} 功能=${feature} 步骤=操作截图`;
            const filename = await aiRename(shot.path, context);
            const archived = archiveScreenshot(shot.path, filename, competitor, feature);
            result = {
              success: archived.success,
              output: archived.success ? `✅ 截图已保存: ${archived.relativePath}` : `❌ ${archived.error}`,
              ...archived,
            };
          }
        } catch (e) {
          result = { error: e.message, output: `❌ 截图失败: ${e.message}` };
        }
        break;
      }
      case '/screenshots':
        result = handleScreenshotsList();
        break;
      case '/report':
        result = handleReport(data);
        break;
      case '/scrcpy':
        result = handleScrcpy();
        break;
      default:
        res.writeHead(404);
        res.end('404');
        return;
    }

    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify(result));
    return;
  }

  res.writeHead(404);
  res.end('404');
});

server.listen(PORT, () => {
  console.log(`\n╔══════════════════════════════════════╗`);
  console.log(`║  📱 竞品分析工具 - 已启动             ║`);
  console.log(`╠══════════════════════════════════════╣`);
  console.log(`║  浏览器打开: http://localhost:${PORT}   ║`);
  console.log(`╚══════════════════════════════════════╝\n`);
});

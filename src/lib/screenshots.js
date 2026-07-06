/**
 * 竞品分析工具 - 截图管理核心
 *
 * 纯函数，不含 CLI 参数解析和交互式 readline 循环。
 */

const fs = require('fs');
const path = require('path');
const { CONFIG } = require('./config');
const { captureScreenshot } = require('./adb');

/**
 * 规则引擎命名（无 AI 时的后备方案）
 * @param {string} context - 上下文描述
 * @returns {string} 文件名
 */
function ruleBasedRename(context) {
  const parts = {};
  (context || '').split(/\s+/).forEach(p => {
    const eqIdx = p.indexOf('=');
    if (eqIdx > 0) {
      parts[p.slice(0, eqIdx)] = p.slice(eqIdx + 1);
    }
  });

  const competitor = parts['竞品'] || parts['competitor'] || 'Unknown';
  const feature = parts['功能'] || parts['feature'] || 'Unknown';
  const step = parts['步骤'] || parts['step'] || Date.now();

  const safeName = (str) => {
    return String(str).replace(/[^a-zA-Z0-9一-鿿_-]/g, '_')
      .replace(/\s+/g, '_')
      .substring(0, 50);
  };

  return `${safeName(competitor)}_${safeName(feature)}_${safeName(step)}.png`;
}

/**
 * 使用 Claude API 智能命名截图
 * @param {string} imagePath - 截图本地路径
 * @param {string} context - 上下文（竞品、功能、步骤描述）
 * @param {string} [apiKey] - Claude API key
 * @returns {Promise<string>} AI 建议的文件名
 */
async function aiRename(imagePath, context, apiKey) {
  const key = apiKey || CONFIG.anthropicApiKey;

  if (!key) {
    return ruleBasedRename(context);
  }

  try {
    const Anthropic = require('@anthropic-ai/sdk');
    const anthropic = new Anthropic({ apiKey: key });

    const imageBuffer = fs.readFileSync(imagePath);
    const base64Image = imageBuffer.toString('base64');

    const response = await anthropic.messages.create({
      model: CONFIG.model,
      max_tokens: 100,
      messages: [{
        role: 'user',
        content: [
          {
            type: 'text',
            text: `这是手机竞品分析的截图。上下文：${context}。\n请根据截图内容和上下文，生成一个英文文件名（用下划线连接），格式：Competitor_Feature_Step.png。\n只输出文件名，不要其他内容。例如：Google_Register_EmailError.png`
          },
          {
            type: 'image',
            source: {
              type: 'base64',
              media_type: 'image/png',
              data: base64Image,
            }
          }
        ]
      }]
    });

    const filename = response.content[0].text.trim();
    return filename.endsWith('.png') ? filename : filename + '.png';
  } catch {
    return ruleBasedRename(context);
  }
}

/**
 * 归档截图到目标文件夹
 * @param {string} sourcePath - 源文件路径
 * @param {string} filename - 目标文件名
 * @param {string} competitor - 竞品名
 * @param {string} feature - 功能名
 * @returns {{ success: bool, path?: string, error?: string }}
 */
function archiveScreenshot(sourcePath, filename, competitor, feature) {
  try {
    const targetDir = path.join(CONFIG.screenshotDir, competitor, feature);
    if (!fs.existsSync(targetDir)) {
      fs.mkdirSync(targetDir, { recursive: true });
    }

    const targetPath = path.join(targetDir, filename);
    fs.copyFileSync(sourcePath, targetPath);

    // 删除临时文件
    if (sourcePath.includes('_tmp')) {
      try { fs.unlinkSync(sourcePath); } catch {}
    }

    const relativePath = path.relative(CONFIG.screenshotDir, targetPath);
    return { success: true, path: targetPath, relativePath };
  } catch (e) {
    return { success: false, error: `归档失败: ${e.message}` };
  }
}

/**
 * 单次截图 → AI命名 → 归档
 * @param {object} opts - { competitor, feature, step?, apiKey? }
 * @returns {Promise<{ success: bool, path?: string, filename?: string, error?: string }>}
 */
async function captureAndArchive(opts) {
  const { competitor, feature, step, apiKey } = opts;

  // 1. 截图
  const shot = captureScreenshot();
  if (!shot.success) return shot;

  // 2. AI 命名
  const context = `竞品=${competitor} 功能=${feature} 步骤=${step || '操作截图'}`;
  const filename = await aiRename(shot.path, context, apiKey);

  // 3. 归档
  const archived = archiveScreenshot(shot.path, filename, competitor, feature);
  if (!archived.success) return archived;

  return { success: true, path: archived.path, filename: archived.relativePath };
}

/**
 * 列出截图文件
 * @param {string} [competitor] - 按竞品筛选
 * @param {string} [feature] - 按功能筛选
 * @returns {string[]} 相对路径列表
 */
function listScreenshots(competitor, feature) {
  const files = [];
  const baseDir = CONFIG.screenshotDir;

  if (!fs.existsSync(baseDir)) return files;

  const walk = (dir, prefix) => {
    if (!fs.existsSync(dir)) return;
    for (const entry of fs.readdirSync(dir)) {
      const full = path.join(dir, entry);
      if (fs.statSync(full).isDirectory()) {
        walk(full, path.join(prefix, entry));
      } else if (/\.(png|jpg|jpeg)$/i.test(entry)) {
        files.push(path.join(prefix, entry).replace(/\\/g, '/'));
      }
    }
  };

  if (competitor && feature) {
    walk(path.join(baseDir, competitor, feature), path.join(competitor, feature));
  } else if (competitor) {
    walk(path.join(baseDir, competitor), competitor);
  } else {
    walk(baseDir, '');
  }

  return files;
}

/**
 * 统计截图数量（按竞品+功能）
 * @param {string} feature - 功能名
 * @param {string[]} [competitorFilter] - 竞品筛选
 * @returns {object} { [competitor]: number }
 */
function countScreenshots(feature, competitorFilter) {
  const { ALL_COMPETITORS } = require('./config');
  const counts = {};

  for (const cat of ['system', 'consumer']) {
    for (const comp of ALL_COMPETITORS[cat]) {
      if (competitorFilter && !competitorFilter.includes(comp)) continue;
      const dir = path.join(CONFIG.screenshotDir, comp, feature);
      counts[comp] = (fs.existsSync(dir))
        ? fs.readdirSync(dir).filter(f => /\.(png|jpg|jpeg)$/i.test(f)).length
        : 0;
    }
  }

  return counts;
}

module.exports = {
  ruleBasedRename,
  aiRename,
  archiveScreenshot,
  captureAndArchive,
  listScreenshots,
  countScreenshots,
};

/**
 * 截图分析脚本 —— 把截图文件夹发给 Claude API 分析
 *
 * 用法：
 *   node src/analyze_screenshots.js --competitor Google --feature passkey
 */

const fs = require('fs');
const path = require('path');

const SCREENSHOT_DIR = path.join(__dirname, '..', 'screenshots');

async function main() {
  const args = process.argv.slice(2);
  const getArg = (name) => {
    const idx = args.indexOf(`--${name}`);
    return idx >= 0 ? args[idx + 1] : null;
  };

  const competitor = getArg('--competitor') || 'Google';
  const feature = getArg('--feature') || 'passkey';

  const dir = path.join(SCREENSHOT_DIR, competitor, feature);

  if (!fs.existsSync(dir)) {
    console.log(`❌ 文件夹不存在: ${dir}`);
    return;
  }

  const files = fs.readdirSync(dir)
    .filter(f => /\.png$/i.test(f))
    .sort()
    .map(f => path.join(dir, f));

  if (files.length === 0) {
    console.log('❌ 没有截图文件');
    return;
  }

  console.log(`📸 找到 ${files.length} 张截图\n`);

  // 输出每张截图的信息，方便后续 AI 分析
  for (let i = 0; i < files.length; i++) {
    const stats = fs.statSync(files[i]);
    const kb = (stats.size / 1024).toFixed(1);
    console.log(`  [${i + 1}] ${path.basename(files[i])}  (${kb} KB)`);
  }

  console.log(`\n---`);
  console.log(`截图路径: ${dir}`);
  console.log(`\n💡 接下来的步骤：`);
  console.log(`   1. 在 Finder/资源管理器中打开: ${dir}`);
  console.log(`   2. 把这 ${files.length} 张截图按顺序拖到 Claude Code 对话中`);
  console.log(`   3. 输入: "请分析 ${competitor} 的 ${feature} 功能，按 prompt_template.md 模板一输出"`);
}

main().catch(console.error);

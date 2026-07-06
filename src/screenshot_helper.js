/**
 * 截图自动命名工具
 *
 * 使用方法：
 *   node src/screenshot_helper.js --competitor "Google" --feature "注册" --step "输入邮箱后报错"
 *   node src/screenshot_helper.js --batch         # 连续截图模式
 *   node src/screenshot_helper.js --rename-all    # 批量重命名已有的截图文件夹
 */

const readline = require('readline');
const fs = require('fs');
const path = require('path');
const { CONFIG } = require('./lib/config');
const { captureScreenshot } = require('./lib/adb');
const { aiRename, ruleBasedRename, archiveScreenshot, listScreenshots } = require('./lib/screenshots');

// ============================================================
// 连续截图模式（交互式）
// ============================================================

async function batchMode(competitor, feature) {
  console.log('\n📱 连续截图模式已启动');
  console.log(`   竞品: ${competitor || '待指定'}`);
  console.log(`   功能: ${feature || '待指定'}`);
  console.log('   每次截图后，在下方输入当前步骤描述，回车继续下一张');
  console.log('   输入 "done" 退出\n');

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  let stepNum = 1;
  let currentCompetitor = competitor || '';
  let currentFeature = feature || '';

  const askStep = () => {
    return new Promise((resolve) => {
      rl.question(`🔹 步骤 ${stepNum} 描述（如"点击设置→账号→注册"）：`, (answer) => {
        resolve(answer);
      });
    });
  };

  while (true) {
    const stepDesc = await askStep();

    if (stepDesc.toLowerCase() === 'done' || stepDesc.toLowerCase() === 'q') {
      break;
    }

    if (!stepDesc.trim()) continue;

    // 如果输入中包含 "竞品=XXX 功能=XXX"，则更新上下文
    const compMatch = stepDesc.match(/竞品=(\S+)/);
    const featMatch = stepDesc.match(/功能=(\S+)/);
    if (compMatch) currentCompetitor = compMatch[1];
    if (featMatch) currentFeature = featMatch[1];

    // 截图
    console.log('📸 正在截图...');
    const shot = captureScreenshot();
    if (!shot.success) {
      console.log(`❌ ${shot.error}`);
      continue;
    }
    console.log(`   ✅ 截图已保存: ${shot.path}`);

    // AI 命名
    const context = `竞品=${currentCompetitor || 'Unknown'} 功能=${currentFeature || 'Unknown'} 步骤=${stepDesc}`;
    const filename = await aiRename(shot.path, context);

    // 归档
    const archived = archiveScreenshot(
      shot.path,
      filename,
      currentCompetitor || 'Unknown',
      currentFeature || 'Unknown'
    );
    if (archived.success) {
      console.log(`   📁 归档: ${archived.relativePath}`);
    }

    stepNum++;
  }

  rl.close();
  console.log(`\n✅ 共完成 ${stepNum - 1} 张截图`);
}

// ============================================================
// 批量重命名模式
// ============================================================

function batchRename(dirPath, competitor, feature) {
  if (!fs.existsSync(dirPath)) {
    console.error(`❌ 目录不存在: ${dirPath}`);
    return;
  }

  const files = fs.readdirSync(dirPath)
    .filter(f => /\.(png|jpg|jpeg)$/i.test(f))
    .sort();

  console.log(`📂 找到 ${files.length} 张图片，开始重命名...\n`);

  for (let i = 0; i < files.length; i++) {
    const oldPath = path.join(dirPath, files[i]);
    console.log(`[${i + 1}/${files.length}] ${files[i]}`);

    const context = `竞品=${competitor || 'Unknown'} 功能=${feature || 'Unknown'} 步骤=第${i + 1}步`;
    const newName = `${String(i + 1).padStart(2, '0')}_${ruleBasedRename(context)}`;
    const newPath = path.join(dirPath, newName);

    fs.renameSync(oldPath, newPath);
    console.log(`   → ${path.basename(newPath)}`);
  }

  console.log(`\n✅ 重命名完成`);
}

// ============================================================
// CLI 入口
// ============================================================

async function main() {
  const args = process.argv.slice(2);

  const getArg = (name) => {
    const idx = args.indexOf(`--${name}`);
    return idx >= 0 ? args[idx + 1] : null;
  };

  const mode = args.includes('--batch') ? 'batch'
    : args.includes('--rename-all') ? 'rename'
    : 'single';

  const competitor = getArg('competitor');
  const feature = getArg('feature');
  const step = getArg('step');
  const dir = getArg('dir');

  console.log('═══════════════════════════════════════');
  console.log('  竞品分析截图助手');
  console.log('═══════════════════════════════════════\n');

  switch (mode) {
    case 'batch':
      await batchMode(competitor || '', feature || '');
      break;

    case 'rename':
      if (!dir) {
        console.log('用法: node screenshot_helper.js --rename-all --dir <截图文件夹路径> --competitor <竞品名> --feature <功能名>');
        break;
      }
      batchRename(dir, competitor || 'Unknown', feature || 'Unknown');
      break;

    case 'single': {
      if (!competitor || !feature) {
        console.log('用法: node screenshot_helper.js --competitor <竞品名> --feature <功能名> [--step <步骤描述>]');
        console.log('      node screenshot_helper.js --batch --competitor <竞品名> --feature <功能名>');
        console.log('      node screenshot_helper.js --rename-all --dir <文件夹> --competitor <竞品名> --feature <功能名>');
        break;
      }
      const { captureAndArchive } = require('./lib/screenshots');
      const result = await captureAndArchive({ competitor, feature, step: step || '操作截图' });
      if (result.success) {
        console.log(`✅ 截图完成: ${result.filename}`);
      } else {
        console.log(`❌ ${result.error}`);
      }
      break;
    }
  }
}

main().catch(console.error);

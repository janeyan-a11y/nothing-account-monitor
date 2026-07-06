#!/usr/bin/env node

/**
 * 竞品分析工具集 - npm CLI 入口
 *
 * 安装: npm install -g competitive-analysis
 * 使用: competitive-analysis <command>
 *
 * 子命令:
 *   account list                    列出所有账号
 *   account add                     交互式添加账号
 *   account push <competitor>       推送账号到手机
 *   account search [--type] [--competitor]  搜索账号
 *   screenshot <competitor> <feature> [step]  单次截图
 *   screenshot batch <competitor> <feature>  连续截图
 *   screenshot list [competitor] [feature]    列出截图
 *   report <feature> [--ai] [--all] [--competitors]  生成报告
 *   device                          检测设备
 *   web                             启动 Web 控制台
 *   templates                       输出 Prompt 模板
 */

const { Command } = require('commander');
const path = require('path');

const program = new Command();

program
  .name('competitive-analysis')
  .description('海外手机系统账号竞品分析工具集')
  .version('1.0.0');

// ==================== account 命令组 ====================

const accountCmd = program.command('account')
  .description('账号矩阵管理');

accountCmd.command('list')
  .description('列出所有竞品账号')
  .action(() => {
    const { loadAccounts, listAccounts } = require('../src/lib/accounts');
    const data = loadAccounts();
    const all = listAccounts(data);

    console.log('\n📋 账号矩阵\n');
    console.log('── 系统账号类 ──');
    all.filter(a => a.category === 'system').forEach(a => {
      const tag = a.type === 'unregistered' ? '🆕' : '✅';
      console.log(`  ${tag} [${a.competitor}] ${a.display}`);
      if (a.note) console.log(`     ${a.note}${a.has2FA ? ' | ⚠️ 2FA' : ''}`);
    });

    console.log('\n── C端账号类 ──');
    all.filter(a => a.category === 'consumer').forEach(a => {
      console.log(`  ✅ [${a.competitor}] ${a.display}`);
      if (a.note) console.log(`     ${a.note}`);
    });

    const registered = all.filter(a => a.type === 'registered');
    const unregistered = all.filter(a => a.type === 'unregistered');
    console.log(`\n── 总计 ${all.length} 个账号 (已注册: ${registered.length}, 未注册: ${unregistered.length}) ──\n`);
  });

accountCmd.command('add')
  .description('交互式添加账号')
  .action(async () => {
    const readline = require('readline');
    const { loadAccounts, addAccount } = require('../src/lib/accounts');

    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    const q = (p) => new Promise(resolve => rl.question(p, resolve));

    console.log('\n➕ 添加新账号\n');
    const category = await q('类别 (system/consumer): ');
    if (!['system', 'consumer'].includes(category)) {
      console.log('❌ 类别必须为 system 或 consumer');
      rl.close();
      return;
    }

    const competitor = await q('竞品名 (如 Google): ');
    const type = await q('类型 (registered/unregistered): ');
    const email = await q('邮箱/用户名 (留空跳过): ');
    const password = await q('密码 (留空跳过): ');
    const phone = await q('手机号 (留空跳过): ');
    const note = await q('备注: ');
    const has2FAInput = category === 'system' ? await q('是否有2FA? (y/n): ') : 'n';

    const data = loadAccounts();
    addAccount(data, {
      category,
      competitor,
      type: type || 'registered',
      email: email || undefined,
      password: password || undefined,
      phone: phone || undefined,
      note,
      has2FA: has2FAInput.toLowerCase() === 'y',
    });

    console.log(`✅ 已添加 ${competitor} 账号`);
    rl.close();
  });

accountCmd.command('push')
  .description('推送账号到手机剪贴板')
  .argument('<competitor>', '竞品名 (如 Google)')
  .action((competitor) => {
    const { pushAccount } = require('../src/lib/accounts');
    const result = pushAccount(competitor);

    if (!result.success) {
      console.log(`❌ ${result.error}`);
      return;
    }
    console.log(`📱 已推送 ${result.competitor} 账号到手机`);
    console.log(`   账号: ${result.account}`);
    console.log(`   密码: ${result.password}`);
    if (result.clipboardOk) {
      console.log('   ✅ 账号已复制到手机剪贴板（可直接粘贴）');
    }
    console.log(`\n📋 ${result.content}`);
  });

accountCmd.command('search')
  .description('搜索账号')
  .option('--type <type>', '按类型筛选 (registered/unregistered)')
  .option('--competitor <name>', '按竞品名模糊搜索')
  .action((opts) => {
    const { loadAccounts, searchAccounts } = require('../src/lib/accounts');
    const data = loadAccounts();
    const results = searchAccounts(data, { type: opts.type, competitor: opts.competitor });

    console.log(`\n🔍 搜索结果 (${results.length} 个):\n`);
    results.forEach(a => {
      console.log(`  [${a.competitor}] ${a.display} (${a.type})`);
      if (a.note) console.log(`     ${a.note}`);
    });
    console.log('');
  });

// ==================== screenshot 命令组 ====================

const shotCmd = program.command('screenshot')
  .description('截图管理');

shotCmd.command('capture')
  .description('单次截图 → AI命名 → 归档')
  .argument('<competitor>', '竞品名')
  .argument('<feature>', '功能名')
  .argument('[step]', '步骤描述', '操作截图')
  .action(async (competitor, feature, step) => {
    const { captureAndArchive } = require('../src/lib/screenshots');
    console.log('📸 正在截图...');
    const result = await captureAndArchive({ competitor, feature, step });
    if (result.success) {
      console.log(`✅ 截图完成: ${result.filename}`);
    } else {
      console.log(`❌ ${result.error}`);
    }
  });

shotCmd.command('batch')
  .description('连续截图模式（交互式）')
  .argument('<competitor>', '竞品名')
  .argument('<feature>', '功能名')
  .action(async (competitor, feature) => {
    const readline = require('readline');
    const { captureScreenshot } = require('../src/lib/adb');
    const { aiRename, archiveScreenshot } = require('../src/lib/screenshots');

    console.log('\n📱 连续截图模式');
    console.log(`   竞品: ${competitor}`);
    console.log(`   功能: ${feature}`);
    console.log('   输入步骤描述后回车截图，输入 "done" 退出\n');

    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    const ask = () => new Promise(resolve => rl.question(`🔹 步骤描述: `, resolve));

    let stepNum = 1;
    while (true) {
      const desc = await ask();
      if (!desc || desc.toLowerCase() === 'done' || desc.toLowerCase() === 'q') break;
      if (!desc.trim()) continue;

      console.log('   📸 截图...');
      const shot = captureScreenshot();
      if (!shot.success) {
        console.log(`   ❌ ${shot.error}`);
        continue;
      }

      const context = `竞品=${competitor} 功能=${feature} 步骤=${desc}`;
      const filename = await aiRename(shot.path, context);
      const archived = archiveScreenshot(shot.path, filename, competitor, feature);
      if (archived.success) {
        console.log(`   ✅ ${archived.relativePath}`);
      }
      stepNum++;
    }
    rl.close();
    console.log(`\n✅ 共完成 ${stepNum - 1} 张截图\n`);
  });

shotCmd.command('list')
  .description('列出已有截图')
  .argument('[competitor]', '按竞品筛选')
  .argument('[feature]', '按功能筛选')
  .action((competitor, feature) => {
    const { listScreenshots } = require('../src/lib/screenshots');
    const files = listScreenshots(competitor, feature);

    if (files.length === 0) {
      console.log('暂无截图');
    } else {
      console.log(`\n📸 共 ${files.length} 张截图:\n`);
      files.forEach(f => console.log(`  📸 ${f}`));
      console.log('');
    }
  });

// ==================== report 命令 ====================

program.command('report')
  .description('生成竞品分析报告')
  .argument('<feature>', '功能名 (如 "第三方账号绑定")')
  .option('--ai', '使用 AI 模式（需 ANTHROPIC_API_KEY）')
  .option('--all', '分析全部竞品')
  .option('--competitors <list>', '指定竞品，逗号分隔 (如 "Google,Apple")')
  .action(async (feature, opts) => {
    const { collectScreenshots, generateMarkdownReport, generateAIReport, saveReport } = require('../src/lib/reports');
    const { CONFIG } = require('../src/lib/config');

    let competitorFilter = null;
    if (!opts.all && opts.competitors) {
      competitorFilter = opts.competitors.split(',').map(s => s.trim());
    }

    const screenshots = collectScreenshots(feature, competitorFilter);
    const total = Object.values(screenshots).flat().length;
    const withShots = Object.keys(screenshots).filter(k => screenshots[k].length > 0);
    console.log(`\n📸 截图统计: ${total} 张，覆盖 ${withShots.length} 个竞品\n`);

    if (opts.ai && CONFIG.anthropicApiKey) {
      console.log('🤖 AI 分析模式...\n');
      try {
        const result = await generateAIReport(feature, competitorFilter);
        console.log(`\n✅ 报告已保存: ${result.path}`);
      } catch (e) {
        console.error(`❌ AI 分析失败: ${e.message}`);
      }
    } else if (opts.ai) {
      console.log('❌ 未设置 ANTHROPIC_API_KEY 环境变量，回退到模板模式\n');
      const report = generateMarkdownReport(feature, screenshots);
      const filepath = saveReport(feature, report);
      console.log(`✅ 报告模板已保存: ${filepath}`);
    } else {
      console.log('📝 模板模式\n');
      const report = generateMarkdownReport(feature, screenshots);
      const filepath = saveReport(feature, report);
      console.log(`✅ 报告模板已保存: ${filepath}`);
      console.log('💡 添加 --ai 可使用 Claude API 自动分析');
    }
  });

// ==================== 工具命令 ====================

program.command('device')
  .description('检测 Android 设备连接状态')
  .action(() => {
    const { checkDevice } = require('../src/lib/adb');
    const result = checkDevice();

    if (result.connected) {
      console.log(`✅ 设备已连接: ${result.device}`);
      if (result.devices.length > 1) {
        console.log(`   所有设备: ${result.devices.join(', ')}`);
      }
    } else {
      console.log('❌ 未检测到 Android 设备');
      if (result.error) console.log(`   ${result.error}`);
    }
  });

program.command('web')
  .description('启动 Web 控制台 (HTTP 服务)')
  .action(() => {
    const { CONFIG } = require('../src/lib/config');
    console.log(`启动 Web 控制台: http://localhost:${CONFIG.serverPort}`);
    require(path.join(__dirname, '..', 'server.js'));
  });

program.command('templates')
  .description('输出 Prompt 模板')
  .action(() => {
    const fs = require('fs');
    const templatePath = path.join(__dirname, '..', 'prompt_template.md');
    if (fs.existsSync(templatePath)) {
      console.log(fs.readFileSync(templatePath, 'utf-8'));
    } else {
      console.log('⚠️  prompt_template.md 不存在');
    }
  });

// ==================== 启动 ====================

program.parse();

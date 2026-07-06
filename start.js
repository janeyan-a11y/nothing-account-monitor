/**
 * 竞品分析工具 - 交互式菜单入口
 * 用法: node start.js
 */

const readline = require('readline');
const fs = require('fs');
const path = require('path');
const { CONFIG } = require('./src/lib/config');
const { checkDevice, captureScreenshot } = require('./src/lib/adb');
const { listAccounts, pushAccount, loadAccounts } = require('./src/lib/accounts');
const { listScreenshots } = require('./src/lib/screenshots');
const { generateMarkdownReport, collectScreenshots, saveReport } = require('./src/lib/reports');

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const q = (p) => new Promise(r => rl.question(p, r));

async function main() {
  while (true) {
    console.log('\n');
    console.log('╔══════════════════════════════════╗');
    console.log('║    📱 竞品分析工具集             ║');
    console.log('╠══════════════════════════════════╣');
    console.log('║  1. 📋 查看所有账号              ║');
    console.log('║  2. 📲 推送账号到手机            ║');
    console.log('║  3. 📸 截图 (当前页面)           ║');
    console.log('║  4. 📁 查看已有截图              ║');
    console.log('║  5. 📄 生成报告模板              ║');
    console.log('║  6. 📱 启动投屏 (scrcpy)         ║');
    console.log('║  7. ❌ 退出                      ║');
    console.log('╚══════════════════════════════════╝');

    const choice = await q('\n👉 选择 (1-7): ');

    switch (choice) {
      case '1': {
        // 查看所有账号
        const data = loadAccounts();
        const all = listAccounts(data);
        console.log(`\n📋 共 ${all.length} 个账号:\n`);
        all.forEach(a => {
          const tag = a.type === 'unregistered' ? '🆕' : '✅';
          console.log(`  ${tag} [${a.competitor}] ${a.display}`);
          if (a.note) console.log(`     ${a.note}${a.has2FA ? ' | ⚠️ 2FA' : ''}`);
        });
        break;
      }

      case '2': {
        const comp = await q('竞品名 (如 Google): ');
        const result = pushAccount(comp);
        if (result.success) {
          console.log(`✅ 已推送 ${result.competitor} 到手机`);
          console.log(`   账号: ${result.account}`);
          if (result.clipboardOk) console.log('   📋 已复制到剪贴板');
        } else {
          console.log(`❌ ${result.error}`);
        }
        break;
      }

      case '3': {
        const comp = await q('竞品名: ');
        const feat = await q('功能名 (如 passkey): ');

        // 计算序号
        const dir = path.join(CONFIG.screenshotDir, comp, feat);
        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
        const n = fs.readdirSync(dir).filter(f => f.endsWith('.png')).length + 1;
        const num = String(n).padStart(2, '0');

        const shot = captureScreenshot();
        if (shot.success) {
          const targetPath = path.join(dir, `${num}.png`);
          fs.copyFileSync(shot.path, targetPath);
          console.log(`✅ 截图已保存: screenshots/${comp}/${feat}/${num}.png`);
        } else {
          console.log(`❌ ${shot.error}`);
        }
        break;
      }

      case '4': {
        const files = listScreenshots();
        if (files.length === 0) {
          console.log('暂无截图');
        } else {
          console.log(`共 ${files.length} 张截图:`);
          files.forEach(f => console.log(`  📸 ${f}`));
        }
        break;
      }

      case '5': {
        const feat = await q('功能名 (如 passkey): ');
        const screenshots = collectScreenshots(feat);
        const report = generateMarkdownReport(feat, screenshots);
        const filepath = saveReport(feat, report);
        console.log(`✅ 报告已生成: ${filepath}`);
        break;
      }

      case '6':
        try {
          const { exec } = require('child_process');
          exec('scrcpy --window-title "竞品分析"', { stdio: 'ignore' });
          console.log('✅ scrcpy 投屏已启动');
        } catch (e) {
          console.log(`❌ 启动失败: ${e.message}`);
        }
        break;

      case '7':
        console.log('👋 再见');
        rl.close();
        return;

      default:
        console.log('选 1-7');
    }
  }
}

main().catch(console.error);

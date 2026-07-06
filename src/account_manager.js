/**
 * 账号矩阵管理工具
 *
 * 使用方法：
 *   node src/account_manager.js list                          # 列出所有账号
 *   node src/account_manager.js add                           # 交互式添加账号
 *   node src/account_manager.js push --competitor Google      # 推送账号到手机
 *   node src/account_manager.js search --type unregistered    # 查找未注册邮箱
 */

const readline = require('readline');
const { loadAccounts, saveAccounts, listAccounts, searchAccounts, addAccount, pushAccount } = require('./lib/accounts');

// ============================================================
// 功能：交互式添加账号
// ============================================================

async function interactiveAddAccount(data) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  const q = (prompt) => new Promise(resolve => rl.question(prompt, resolve));

  console.log('\n➕ 添加新账号\n');

  const category = await q('类别 (system/consumer): ');
  if (!['system', 'consumer'].includes(category)) {
    console.log('❌ 类别必须为 system 或 consumer');
    rl.close();
    return;
  }

  const competitor = await q('竞品名 (如 Google/Instagram): ');
  const type = await q('类型 (registered/unregistered): ');
  const email = await q('邮箱/用户名 (留空跳过): ');
  const password = await q('密码 (留空跳过): ');
  const phone = await q('手机号 (留空跳过): ');
  const note = await q('备注: ');
  const has2FAInput = category === 'system' ? await q('是否有2FA? (y/n): ') : 'n';

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
}

// ============================================================
// 输出辅助
// ============================================================

function printAccountList(data) {
  console.log('\n═══════════════════════════════════════');
  console.log('  📋 账号矩阵');
  console.log('═══════════════════════════════════════\n');

  console.log('── 系统账号类 ──');
  for (const acc of data.accounts.system) {
    const tag = acc.type === 'unregistered' ? '🆕' : '✅';
    const id = acc.email || acc.phone || acc.appleId || '(未填写)';
    console.log(`  ${tag} [${acc.competitor}] ${id}`);
    console.log(`     类型: ${acc.type}${acc.note ? ` | ${acc.note}` : ''}${acc.has2FA ? ' | ⚠️ 2FA' : ''}\n`);
  }

  console.log('── 海外 C 端账号 ──');
  for (const acc of data.accounts.consumer) {
    const id = acc.email || acc.phone || acc.username || '(未填写)';
    console.log(`  ✅ [${acc.competitor}] ${id}`);
    console.log(`     ${acc.note || ''}\n`);
  }

  const all = listAccounts(data);
  const registered = all.filter(a => a.type === 'registered');
  const unregistered = all.filter(a => a.type === 'unregistered');

  console.log('═══════════════════════════════════════');
  console.log(`  总计 ${all.length} 个账号`);
  console.log(`  已注册: ${registered.length} | 未注册: ${unregistered.length}`);
  console.log('═══════════════════════════════════════');
}

function printSearchResults(results) {
  console.log(`\n🔍 搜索结果 (${results.length} 个):\n`);
  results.forEach(a => {
    console.log(`  [${a.competitor}] ${a.display} (${a.type})`);
    if (a.note) console.log(`     ${a.note}`);
  });
}

function printPushResult(result) {
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
  console.log('\n📋 账号信息:');
  console.log(result.content);
  console.log('\n💡 提示：如果剪贴板推送失败，可以在手机上打开 sdcard/account_cred.txt 查看');
}

// ============================================================
// CLI 入口
// ============================================================

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  const getArg = (name) => {
    const idx = args.indexOf(`--${name}`);
    return idx >= 0 ? args[idx + 1] : null;
  };

  const data = loadAccounts();

  switch (command) {
    case 'list':
      printAccountList(data);
      break;

    case 'add':
      await interactiveAddAccount(data);
      break;

    case 'push': {
      const competitor = getArg('competitor') || getArg('c');
      if (!competitor) {
        console.log('用法: node account_manager.js push --competitor <竞品名>');
        console.log('示例: node account_manager.js push -c Google');
      } else {
        const result = pushAccount(competitor, data);
        printPushResult(result);
      }
      break;
    }

    case 'search': {
      const type = getArg('type');
      const competitor = getArg('competitor');
      const results = searchAccounts(data, { type, competitor });
      printSearchResults(results);
      break;
    }

    default:
      console.log('═══════════════════════════════════════');
      console.log('  🔐 竞品分析 - 账号矩阵管理');
      console.log('═══════════════════════════════════════\n');
      console.log('用法:');
      console.log('  node src/account_manager.js list                       列出所有账号');
      console.log('  node src/account_manager.js add                        添加新账号');
      console.log('  node src/account_manager.js push -c <竞品名>           推送账号到手机');
      console.log('  node src/account_manager.js search --type unregistered 查找未注册邮箱');
      console.log('\n💡 首次使用请编辑 data/accounts.json 填入真实账号密码');
  }
}

main().catch(console.error);

/**
 * 竞品分析工具 - 账号管理核心
 *
 * 纯函数，无 CLI 解析逻辑，无交互式 readline。
 * 交互式逻辑保留在 account_manager.js CLI 层。
 */

const fs = require('fs');
const path = require('path');
const { CONFIG, DEFAULT_ACCOUNTS_DATA } = require('./config');
const { getAdbCommand } = require('./adb');

/**
 * 加载账号数据，文件不存在时自动创建模板
 * @returns {object} 账号数据对象
 */
function loadAccounts() {
  const dataFile = CONFIG.dataFile;

  if (!fs.existsSync(dataFile)) {
    const dir = path.dirname(dataFile);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(dataFile, JSON.stringify(DEFAULT_ACCOUNTS_DATA, null, 2));
    return JSON.parse(JSON.stringify(DEFAULT_ACCOUNTS_DATA));
  }

  return JSON.parse(fs.readFileSync(dataFile, 'utf-8'));
}

/**
 * 保存账号数据
 * @param {object} data - 账号数据对象
 */
function saveAccounts(data) {
  const dataFile = CONFIG.dataFile;
  const dir = path.dirname(dataFile);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  data.updated = new Date().toISOString();
  fs.writeFileSync(dataFile, JSON.stringify(data, null, 2));
}

/**
 * 获取所有账号的扁平列表
 * @param {object} [data] - 账号数据，不传则自动加载
 * @returns {Array<{competitor, type, display, note, has2FA, category}>}
 */
function listAccounts(data) {
  const accountsData = data || loadAccounts();
  const all = [];

  for (const cat of ['system', 'consumer']) {
    for (const a of accountsData.accounts[cat]) {
      all.push({
        competitor: a.competitor,
        type: a.type,
        display: a.email || a.phone || a.appleId || a.username || '(未填写)',
        password: a.password || '',
        note: a.note || '',
        has2FA: a.has2FA || false,
        category: cat,
      });
    }
  }

  return all;
}

/**
 * 搜索账号
 * @param {object} data - 账号数据
 * @param {object} filter - 过滤条件 { type?, competitor? }
 * @returns {Array} 匹配的账号列表
 */
function searchAccounts(data, filter) {
  const all = listAccounts(data);

  let results = all;
  if (filter.type) {
    results = results.filter(a => a.type === filter.type);
  }
  if (filter.competitor) {
    results = results.filter(a =>
      a.competitor.toLowerCase().includes(filter.competitor.toLowerCase())
    );
  }

  return results;
}

/**
 * 添加账号（非交互式）
 * @param {object} data - 账号数据
 * @param {object} fields - { category, competitor, type, email?, password?, phone?, note?, has2FA? }
 * @returns {object} 更新后的 data
 */
function addAccount(data, fields) {
  const newAccount = {
    competitor: fields.competitor,
    type: fields.type || 'registered',
    note: fields.note || '',
  };

  if (fields.email) newAccount.email = fields.email;
  if (fields.password) newAccount.password = fields.password;
  if (fields.phone) newAccount.phone = fields.phone;
  if (fields.username) newAccount.username = fields.username;
  if (fields.appleId) newAccount.appleId = fields.appleId;
  if (fields.has2FA !== undefined) newAccount.has2FA = fields.has2FA;

  const category = fields.category === 'consumer' ? 'consumer' : 'system';
  data.accounts[category].push(newAccount);

  saveAccounts(data);
  return data;
}

/**
 * 查找并推送账号到手机
 * @param {string} competitor - 竞品名
 * @param {object} [data] - 账号数据
 * @returns {{ success: bool, account?: string, password?: string, error?: string }}
 */
function pushAccount(competitor, data) {
  const accountsData = data || loadAccounts();
  const all = listAccounts(accountsData);
  const acc = all.find(a => a.competitor.toLowerCase() === competitor.toLowerCase());

  if (!acc) {
    const available = [...new Set(all.map(a => a.competitor))].join(', ');
    return { success: false, error: `未找到竞品 "${competitor}" 的账号。可用竞品: ${available}` };
  }

  if (!acc.display || acc.display === '(未填写)') {
    return { success: false, error: `${competitor} 账号信息为空，请先编辑 data/accounts.json` };
  }

  const content = `账号: ${acc.display}\n密码: ${acc.password || '(未填写)'}`;

  try {
    const adb = getAdbCommand();
    const { execSync } = require('child_process');

    // 推送到 sdcard
    const escapedContent = content.replace(/'/g, "\\'").replace(/\n/g, '\\n');
    execSync(`${adb} shell "echo '${escapedContent}' > /sdcard/account_cred.txt"`, { stdio: 'pipe' });

    // 尝试推送剪贴板
    let clipboardOk = false;
    try {
      const escapedId = acc.display.replace(/'/g, "'\\''");
      execSync(`${adb} shell "cmd clipboard set '${escapedId}'"`, { stdio: 'pipe' });
      clipboardOk = true;
    } catch {
      // clipboard 不可用
    }

    return {
      success: true,
      account: acc.display,
      password: acc.password ? '***已加载***' : '无密码',
      competitor: acc.competitor,
      clipboardOk,
      content,
    };
  } catch (e) {
    return { success: false, error: `推送失败: ${e.message}` };
  }
}

module.exports = {
  loadAccounts,
  saveAccounts,
  listAccounts,
  searchAccounts,
  addAccount,
  pushAccount,
};

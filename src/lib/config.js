/**
 * 竞品分析工具 - 统一配置
 *
 * 集中管理所有环境变量、路径常量和竞品列表。
 * 所有其他模块从这里获取配置，避免散落各处。
 */

const path = require('path');

const ROOT_DIR = path.join(__dirname, '..', '..');

const CONFIG = Object.freeze({
  // 目录路径
  rootDir: ROOT_DIR,
  screenshotDir: path.join(ROOT_DIR, 'screenshots'),
  reportDir: path.join(ROOT_DIR, 'reports'),
  dataFile: path.join(ROOT_DIR, 'data', 'accounts.json'),

  // Claude API 配置
  anthropicApiKey: process.env.ANTHROPIC_API_KEY || '',
  model: process.env.CLAUDE_MODEL || 'claude-sonnet-4-20250514',

  // ADB 配置
  adbDevice: process.env.ADB_DEVICE || '',

  // 服务器配置
  serverPort: parseInt(process.env.SERVER_PORT || '3456', 10),

  // 分析限制
  maxScreenshotsPerCompetitor: 15,
});

// 竞品列表
const ALL_COMPETITORS = Object.freeze({
  system: ['Google', 'Apple', 'OPPO', '华为', '小米', 'vivo'],
  consumer: ['Trip.com', 'Instagram', 'RedNote', 'WeChat'],
});

// 竞品分类中文名
const CATEGORY_NAMES = {
  system: '系统账号类',
  consumer: '海外C端账号类',
};

// 报告对比维度
const COMPARISON_DIMENSIONS = [
  '入口路径',
  '是否支持关闭',
  '注册/登录门槛',
  '分支场景数量',
  '隐私设置粒度',
  '异常/错误处理',
  '体验亮点',
  '体验痛点',
];

// 账号数据模板
const DEFAULT_ACCOUNTS_DATA = {
  version: '1.0',
  updated: '',
  accounts: {
    system: [
      { competitor: 'Google', type: 'registered', email: '', password: '', phone: '', note: '美区账号，已开启2FA', has2FA: true, recoveryEmail: '' },
      { competitor: 'Apple', type: 'registered', appleId: '', password: '', phone: '', note: '美区Apple ID', has2FA: true },
      { competitor: 'OPPO', type: 'registered', phone: '', password: '', note: 'HeyTap账号' },
      { competitor: '华为', type: 'registered', email: '', password: '', phone: '', note: '华为账号' },
      { competitor: '小米', type: 'registered', phone: '', password: '', note: '小米账号' },
      { competitor: 'vivo', type: 'registered', phone: '', password: '', note: 'vivo账号' },
      { competitor: 'Generic', type: 'unregistered', email: '', note: '未注册过的Outlook邮箱', usage: '注册流程测试' },
      { competitor: 'Generic', type: 'unregistered', email: '', note: '未注册过的Gmail邮箱', usage: '注册流程测试-备用' },
    ],
    consumer: [
      { competitor: 'Trip.com', type: 'registered', email: '', password: '', note: '' },
      { competitor: 'Instagram', type: 'registered', username: '', password: '', email: '', note: '' },
      { competitor: 'RedNote', type: 'registered', phone: '', password: '', note: '小红书国际版' },
      { competitor: 'WeChat', type: 'registered', phone: '', password: '', wechatId: '', note: '已实名' },
    ],
  },
};

/**
 * 获取合并后的配置（允许运行时覆盖）
 */
function getConfig(overrides) {
  return Object.assign({}, CONFIG, overrides);
}

module.exports = {
  CONFIG,
  ALL_COMPETITORS,
  CATEGORY_NAMES,
  COMPARISON_DIMENSIONS,
  DEFAULT_ACCOUNTS_DATA,
  getConfig,
};

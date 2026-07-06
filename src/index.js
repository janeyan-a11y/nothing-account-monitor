/**
 * 竞品分析工具集 - 统一入口
 *
 * 三种使用方式：
 * 1. npm CLI:    competitive-analysis account list
 * 2. MCP Server: node src/mcp-server.js
 * 3. Claude Code Skill: skills/competitive-analysis/
 *
 * 也支持编程调用：const { accounts, screenshots, reports } = require('competitive-analysis');
 */

const accounts = require('./lib/accounts');
const screenshots = require('./lib/screenshots');
const reports = require('./lib/reports');
const adb = require('./lib/adb');
const config = require('./lib/config');

module.exports = {
  accounts,
  screenshots,
  reports,
  adb,
  config,
};

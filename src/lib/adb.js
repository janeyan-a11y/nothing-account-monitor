/**
 * 竞品分析工具 - ADB 操作封装
 *
 * 统一封装所有 adb 命令调用。
 * 所有函数返回 { success: bool, error?: string, ... } 格式，
 * 不抛异常，由调用方决定如何处理失败。
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const { CONFIG } = require('./config');

/**
 * 获取 adb 命令前缀
 */
function getAdbCommand() {
  const device = CONFIG.adbDevice;
  return device ? `adb -s ${device}` : 'adb';
}

/**
 * 检测 Android 设备连接状态
 * @returns {{ connected: boolean, devices: string[], device?: string, error?: string }}
 */
function checkDevice() {
  try {
    const adb = getAdbCommand();
    const out = execSync(`${adb} devices`, { encoding: 'utf8', timeout: 10000 });
    const lines = out.trim().split('\n').slice(1);
    const devices = lines
      .filter(l => l.includes('\tdevice'))
      .map(l => l.split('\t')[0]);

    return {
      success: true,
      connected: devices.length > 0,
      devices,
      device: devices[0] || null,
    };
  } catch (e) {
    return {
      success: false,
      connected: false,
      devices: [],
      error: `ADB 命令执行失败: ${e.message}`,
    };
  }
}

/**
 * 从 Android 设备截图并拉取到本地
 * @param {string} [localDir] - 本地保存目录，默认临时目录
 * @returns {{ success: bool, path?: string, error?: string }}
 */
function captureScreenshot(localDir) {
  const tmpPath = '/sdcard/comp_analysis_tmp.png';
  const targetDir = localDir || path.join(CONFIG.screenshotDir, '_tmp');

  try {
    const adb = getAdbCommand();

    // 确保本地目录存在
    if (!fs.existsSync(targetDir)) {
      fs.mkdirSync(targetDir, { recursive: true });
    }

    const timestamp = Date.now();
    const localPath = path.join(targetDir, `tmp_${timestamp}.png`);

    // 截屏 → 拉取 → 清理
    execSync(`${adb} shell screencap -p ${tmpPath}`, { stdio: 'pipe', timeout: 15000 });
    execSync(`${adb} pull "${tmpPath}" "${localPath}"`, { stdio: 'pipe', timeout: 15000 });
    execSync(`${adb} shell rm ${tmpPath}`, { stdio: 'pipe', timeout: 5000 });

    return { success: true, path: localPath };
  } catch (e) {
    return { success: false, error: `截图失败: ${e.message}` };
  }
}

/**
 * 推送文本到 Android 设备剪贴板
 * @param {string} text - 要推送到剪贴板的文本
 * @returns {{ success: bool, method?: string, error?: string }}
 */
function pushToClipboard(text) {
  try {
    const adb = getAdbCommand();
    const escaped = text.replace(/'/g, "'\\''");

    // 方式1: cmd clipboard (Android 10+)
    try {
      execSync(`${adb} shell "cmd clipboard set '${escaped}'"`, { stdio: 'pipe', timeout: 5000 });
      return { success: true, method: 'cmd_clipboard' };
    } catch {
      // 方式1 失败，继续尝试方式2
    }

    // 方式2: service call clipboard (需 root)
    try {
      execSync(`${adb} shell "service call clipboard 1 i32 1 s16 '${escaped}'"`, { stdio: 'pipe', timeout: 5000 });
      return { success: true, method: 'service_call' };
    } catch {
      return { success: false, error: '所有剪贴板推送方式均失败' };
    }
  } catch (e) {
    return { success: false, error: `剪贴板推送失败: ${e.message}` };
  }
}

/**
 * 写入内容到设备 sdcard
 * @param {string} content - 要写入的内容
 * @param {string} [filename] - 文件名，默认 account_cred.txt
 * @returns {{ success: bool, path?: string, error?: string }}
 */
function writeToSdcard(content, filename) {
  const fname = filename || 'account_cred.txt';
  const remotePath = `/sdcard/${fname}`;

  try {
    const adb = getAdbCommand();
    const escaped = content.replace(/'/g, "\\'").replace(/\n/g, '\\n');
    execSync(`${adb} shell "echo '${escaped}' > ${remotePath}"`, { stdio: 'pipe', timeout: 5000 });
    return { success: true, path: remotePath };
  } catch (e) {
    return { success: false, error: `写入 sdcard 失败: ${e.message}` };
  }
}

module.exports = {
  getAdbCommand,
  checkDevice,
  captureScreenshot,
  pushToClipboard,
  writeToSdcard,
};

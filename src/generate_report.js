/**
 * 一键生成竞品报告脚本
 *
 * 使用方法：
 *   node src/generate_report.js --feature "第三方账号绑定"
 *   node src/generate_report.js --feature "邮箱注册" --competitors "Google,Apple"
 *   node src/generate_report.js --feature "注销账号" --all --ai
 */

const {
  collectScreenshots,
  generateMarkdownReport,
  saveReport,
  generateAIReport,
} = require('./lib/reports');
const { CONFIG, ALL_COMPETITORS } = require('./lib/config');

// ============================================================
// CLI 入口
// ============================================================

async function main() {
  const args = process.argv.slice(2);
  const getArg = (name) => {
    const idx = args.indexOf(`--${name}`);
    return idx >= 0 ? args[idx + 1] : null;
  };

  const feature = getArg('feature');
  if (!feature) {
    console.log('═══════════════════════════════════════');
    console.log('  📄 竞品分析报告生成器');
    console.log('═══════════════════════════════════════\n');
    console.log('用法:');
    console.log('  node src/generate_report.js --feature "第三方账号绑定"');
    console.log('  node src/generate_report.js --feature "邮箱注册" --competitors "Google,Apple"');
    console.log('  node src/generate_report.js --feature "注销账号" --all --ai');
    console.log('');
    console.log('工作模式:');
    console.log('  1. 本地模式（默认）：生成报告模板到 reports/ 目录');
    console.log('  2. AI 模式：设置 ANTHROPIC_API_KEY 后自动调用 Claude 分析截图');
    console.log('');
    console.log('💡 推荐：将截图拖入 Claude Code 对话中，使用 prompt_template.md 提示词');
    return;
  }

  const competitorsStr = getArg('competitors');
  const useAll = args.includes('--all');
  const useAI = args.includes('--ai');

  let competitorFilter = null;
  if (!useAll && competitorsStr) {
    competitorFilter = competitorsStr.split(',').map(s => s.trim());
  }

  console.log('═══════════════════════════════════════');
  console.log(`  竞品分析: ${feature}`);
  console.log('═══════════════════════════════════════\n');

  // 收集截图
  const screenshots = collectScreenshots(feature, competitorFilter);

  // 统计
  const totalScreenshots = Object.values(screenshots).flat().length;
  const competitorsWithScreenshots = Object.keys(screenshots).filter(k => screenshots[k].length > 0);

  console.log(`📸 截图统计: ${totalScreenshots} 张，覆盖 ${competitorsWithScreenshots.length} 个竞品\n`);

  if (useAI && CONFIG.anthropicApiKey) {
    // AI 模式：调用 Claude API 分析
    console.log('🤖 AI 分析模式启动...\n');

    try {
      const result = await generateAIReport(feature, competitorFilter);
      console.log(`\n✅ 报告已保存: ${result.path}`);
    } catch (e) {
      console.error(`❌ AI 分析失败: ${e.message}`);
      console.log('   回退到本地模板模式...');
      const report = generateMarkdownReport(feature, screenshots);
      const filepath = saveReport(feature, report);
      console.log(`✅ 报告模板已保存: ${filepath}`);
    }
  } else {
    // 本地模式：生成报告模板
    console.log('📝 本地模式：生成报告模板\n');
    const report = generateMarkdownReport(feature, screenshots);
    const filepath = saveReport(feature, report);
    console.log(`✅ 报告已保存: ${filepath}`);

    console.log('\n💡 提示：');
    console.log('   1. 设置环境变量 ANTHROPIC_API_KEY 后加 --ai 可自动调用 AI 分析');
    console.log('   2. 或使用 prompt_template.md 模板在 Claude Code 中分析');
    console.log('   3. 也可将截图逐一拖入 Claude Code 对话中分析');
  }
}

main().catch(console.error);

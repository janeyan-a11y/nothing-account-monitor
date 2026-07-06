/**
 * 竞品分析工具 - 报告生成核心
 *
 * 纯函数，不含 CLI 参数解析。
 */

const fs = require('fs');
const path = require('path');
const { CONFIG, ALL_COMPETITORS, COMPARISON_DIMENSIONS } = require('./config');

/**
 * 收集指定功能的截图（按竞品分组）
 * @param {string} feature - 功能名
 * @param {string[]} [competitorFilter] - 竞品白名单
 * @returns {object} { [competitor]: string[] } 各竞品的截图完整路径列表
 */
function collectScreenshots(feature, competitorFilter) {
  const screenshots = {};

  for (const category of ['system', 'consumer']) {
    for (const competitor of ALL_COMPETITORS[category]) {
      if (competitorFilter && !competitorFilter.includes(competitor)) continue;

      const dir = path.join(CONFIG.screenshotDir, competitor, feature);
      if (!fs.existsSync(dir)) {
        screenshots[competitor] = [];
        continue;
      }

      screenshots[competitor] = fs.readdirSync(dir)
        .filter(f => /\.(png|jpg|jpeg)$/i.test(f))
        .sort()
        .map(f => path.join(dir, f));
    }
  }

  return screenshots;
}

/**
 * 构建主流程报告 Prompt
 * @param {string} feature - 功能名
 * @param {object} screenshots - collectScreenshots 的输出
 * @returns {string} prompt 文本
 */
function buildReportPrompt(feature, screenshots) {
  const competitorList = Object.keys(screenshots).filter(k => screenshots[k].length > 0);
  const emptyList = Object.keys(screenshots).filter(k => screenshots[k].length === 0);
  const allCompetitors = [...ALL_COMPETITORS.system, ...ALL_COMPETITORS.consumer];

  return [
    `# 竞品分析任务`,
    ``,
    `## 分析对象`,
    `- **分析能力**: ${feature}`,
    `- **有截图的竞品**: ${competitorList.join('、') || '无'}`,
    `- **尚未截图的竞品**: ${emptyList.join('、') || '无'}`,
    ``,
    `## 竞品分类`,
    `- **系统账号类**: ${ALL_COMPETITORS.system.join('、')}`,
    `- **海外C端账号类**: ${ALL_COMPETITORS.consumer.join('、')}`,
    ``,
    `## 输出要求`,
    ``,
    `### 一、各竞品逐项分析`,
    `1. **入口路径**：记录从主页/设置页开始，到达该功能的最短路径`,
    `2. **开启流程**：逐步说明如何开启该能力，附截图说明`,
    `3. **关闭流程**：是否支持关闭？路径是什么？`,
    `4. **使用流程**：开启后如何使用？触发条件是什么？`,
    `5. **分支场景**：是否有分支？分支的触发条件和处理方式`,
    `6. **流程图**：用 Mermaid flowchart 格式画出该竞品的完整流程`,
    ``,
    `### 二、跨竞品功能对比表`,
    `| 维度 | ${allCompetitors.join(' | ')} |`,
    `|------|${allCompetitors.map(() => '---').join('|')} |`,
    ...COMPARISON_DIMENSIONS.map(d => `| ${d} | ${allCompetitors.map(() => '').join(' | ')} |`),
    ``,
    `### 三、横向对比总结`,
    `- 系统账号类的共性做法`,
    `- C端账号类的共性做法`,
    `- 两类的差异化分析`,
    ``,
    `### 四、设计建议`,
    `- 推荐流程图（Mermaid flowchart）`,
    `- 设计理由`,
    `- 与竞品的差异化点`,
  ].join('\n');
}

/**
 * 构建单个竞品分析 Prompt
 * @param {string} competitor - 竞品名
 * @param {string} feature - 功能名
 * @param {string[]} screenshotPaths - 截图路径列表
 * @returns {string} prompt 文本
 */
function buildCompetitorAnalysisPrompt(competitor, feature, screenshotPaths) {
  const category = ALL_COMPETITORS.system.includes(competitor) ? '系统账号类' : '海外C端账号类';

  return [
    `## 竞品分析：${competitor} - ${feature}`,
    ``,
    `**竞品分类**: ${category}`,
    `**分析能力**: ${feature}`,
    ``,
    `以下是按操作顺序排列的截图。请根据截图内容进行分析：`,
  ].join('\n');
}

/**
 * 生成纯 Markdown 报告模板（不调用 AI）
 * @param {string} feature - 功能名
 * @param {object} screenshots - collectScreenshots 的输出
 * @returns {string} 完整的 markdown 报告
 */
function generateMarkdownReport(feature, screenshots) {
  const timestamp = new Date().toISOString().split('T')[0];
  const competitors = Object.keys(screenshots);
  let md = '';

  md += `# 竞品分析报告：${feature}\n\n`;
  md += `> 生成日期：${timestamp}\n\n---\n\n`;

  // 截图清单
  md += `## 📸 截图清单\n\n`;
  for (const [competitor, files] of Object.entries(screenshots)) {
    md += `### ${competitor}\n\n`;
    if (files.length === 0) {
      md += `- ⚠️ 暂无截图\n\n`;
    } else {
      md += `| 序号 | 截图 | 步骤说明 | 分支 |\n`;
      md += `|------|------|----------|------|\n`;
      files.forEach((f, i) => {
        const name = path.basename(f, path.extname(f));
        md += `| ${i + 1} | ${name} | *(待填写)* | *(待填写)* |\n`;
      });
      md += '\n';
    }
  }

  // 对比表格
  md += `## 📊 功能对比总表\n\n`;
  md += `| 维度 | ${competitors.join(' | ')} |\n`;
  md += `|------|${competitors.map(() => '---').join('|')}|\n`;
  COMPARISON_DIMENSIONS.forEach(d => {
    md += `| ${d} | ${competitors.map(() => '*(待填写)*').join(' | ')} |\n`;
  });
  md += '\n';

  // 总结
  md += `## 📝 横向对比总结\n\n`;
  md += `### 系统账号类共性\n\n*(待分析)*\n\n`;
  md += `### C端账号类共性\n\n*(待分析)*\n\n`;
  md += `### 两类差异化\n\n*(待分析)*\n\n`;

  // 设计建议
  md += `## 🎯 设计建议\n\n`;
  md += `### 推荐流程图\n\n*(待生成)*\n\n`;
  md += `### 设计理由\n\n*(待分析)*\n\n`;
  md += `### 与竞品的差异化\n\n*(待分析)*\n\n`;

  return md;
}

/**
 * 保存报告到文件
 * @param {string} feature - 功能名
 * @param {string} content - 报告内容
 * @returns {string} 保存路径
 */
function saveReport(feature, content) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0];
  const safeFeature = feature.replace(/\s+/g, '_');
  const filename = `report_${safeFeature}_${timestamp}.md`;
  const filepath = path.join(CONFIG.reportDir, filename);

  if (!fs.existsSync(CONFIG.reportDir)) {
    fs.mkdirSync(CONFIG.reportDir, { recursive: true });
  }

  fs.writeFileSync(filepath, content, 'utf-8');
  return filepath;
}

/**
 * 使用 Claude API 分析单个竞品
 * @param {object} anthropic - Anthropic SDK 实例
 * @param {string} competitor - 竞品名
 * @param {string} feature - 功能名
 * @param {string[]} screenshotPaths - 截图路径
 * @returns {Promise<string>} 分析结果 markdown
 */
async function analyzeCompetitor(anthropic, competitor, feature, screenshotPaths) {
  if (screenshotPaths.length === 0) {
    return `### ${competitor}\n\n⚠️ 暂无截图，请先体验并截图。\n`;
  }

  const content = [];

  // 上下文说明
  content.push({
    type: 'text',
    text: buildCompetitorAnalysisPrompt(competitor, feature, screenshotPaths),
  });

  // 截图（最多15张）
  const imagesToSend = screenshotPaths.slice(0, CONFIG.maxScreenshotsPerCompetitor);
  for (const imgPath of imagesToSend) {
    const buffer = fs.readFileSync(imgPath);
    content.push({
      type: 'image',
      source: {
        type: 'base64',
        media_type: 'image/png',
        data: buffer.toString('base64'),
      }
    });
    content.push({
      type: 'text',
      text: `（截图：${path.basename(imgPath)}）`,
    });
  }

  // 分析指令
  content.push({
    type: 'text',
    text: [
      ``,
      `请根据以上截图，分析 ${competitor} 的「${feature}」功能：`,
      ``,
      `### 分析维度`,
      `1. **入口路径**：从哪进入这个功能？`,
      `2. **开启流程**：如何开启？（逐步说明，引用对应截图编号）`,
      `3. **关闭流程**：是否可以关闭？如何关闭？`,
      `4. **使用流程**：开启后如何触发使用？`,
      `5. **分支场景**：是否有分支？每个分支的处理方式？`,
      `6. **流程图**：用 Mermaid flowchart 格式，画出包含所有分支场景的完整流程`,
      ``,
      `请用中文输出，结构清晰。每个步骤标注对应的截图文件名。`,
    ].join('\n'),
  });

  const response = await anthropic.messages.create({
    model: CONFIG.model,
    max_tokens: 4096,
    messages: [{ role: 'user', content }],
  });

  return `### ${competitor}\n\n${response.content[0].text}\n`;
}

/**
 * 生成 AI 对比总结
 * @param {object} anthropic - Anthropic SDK 实例
 * @param {string} feature - 功能名
 * @param {string} allAnalyses - 所有竞品分析的拼接
 * @returns {Promise<string>} 对比总结 markdown
 */
async function generateComparison(anthropic, feature, allAnalyses) {
  const response = await anthropic.messages.create({
    model: CONFIG.model,
    max_tokens: 4096,
    messages: [{
      role: 'user',
      content: [
        `以下是「${feature}」功能各竞品的分析结果。请生成：`,
        ``,
        `### 一、功能对比总表`,
        `生成 Markdown 表格，行=对比维度，列=各竞品。`,
        ``,
        `### 二、横向对比总结`,
        `1. 系统账号类的共性做法`,
        `2. C端账号类的共性做法`,
        `3. 两类的差异点和各自优劣`,
        ``,
        `### 三、设计建议`,
        `1. 推荐流程图（Mermaid flowchart，包含分支）`,
        `2. 设计理由`,
        `3. 与竞品的差异化建议`,
        ``,
        `---`,
        `以下是各竞品分析：`,
        allAnalyses,
      ].join('\n'),
    }],
  });

  return response.content[0].text;
}

/**
 * 一键 AI 报告生成
 * @param {string} feature - 功能名
 * @param {string[]} [competitorFilter] - 竞品筛选
 * @param {string} [apiKey] - Claude API key
 * @returns {Promise<{ report: string, path: string }>}
 */
async function generateAIReport(feature, competitorFilter, apiKey) {
  const key = apiKey || CONFIG.anthropicApiKey;
  if (!key) {
    throw new Error('未设置 ANTHROPIC_API_KEY，无法使用 AI 模式');
  }

  const Anthropic = require('@anthropic-ai/sdk');
  const anthropic = new Anthropic({ apiKey: key });

  const screenshots = collectScreenshots(feature, competitorFilter);
  const competitorsWithShots = Object.keys(screenshots).filter(k => screenshots[k].length > 0);

  let fullReport = `# 竞品分析报告：${feature}\n\n`;
  fullReport += `> 生成日期：${new Date().toISOString().split('T')[0]}\n\n---\n\n`;

  // 逐个竞品分析
  let allAnalyses = '';
  for (const competitor of competitorsWithShots) {
    const analysis = await analyzeCompetitor(anthropic, competitor, feature, screenshots[competitor]);
    fullReport += analysis + '\n---\n\n';
    allAnalyses += analysis + '\n';
  }

  // 对比总结
  const comparison = await generateComparison(anthropic, feature, allAnalyses);
  fullReport += `## 📊 对比总结与设计建议\n\n${comparison}\n`;

  // 无截图的竞品
  const emptyCompetitors = Object.keys(screenshots).filter(k => screenshots[k].length === 0);
  if (emptyCompetitors.length > 0) {
    fullReport += `\n## ⚠️ 待补充\n\n以下竞品暂无截图：${emptyCompetitors.join('、')}\n`;
  }

  const filepath = saveReport(feature, fullReport);
  return { report: fullReport, path: filepath };
}

module.exports = {
  collectScreenshots,
  buildReportPrompt,
  buildCompetitorAnalysisPrompt,
  generateMarkdownReport,
  saveReport,
  analyzeCompetitor,
  generateComparison,
  generateAIReport,
};

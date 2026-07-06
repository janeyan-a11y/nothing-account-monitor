"""
社媒舆情监控 — 全局配置
"""

import os

# ============================================================
# 搜索关键词（支持 X API v2 搜索语法，OR 连接，最多 512 字符）
# ============================================================
SEARCH_KEYWORDS = [
    # 核心品牌词
    '"Nothing Account"',
    '"Nothing Phone" account',
    "NothingOS account",
    "Nothing login",
    "Nothing sign in",
    # 问题/负面相关
    '"Nothing" account problem',
    '"Nothing" can\'t login',
    '"Nothing Phone" login issue',
    # 竞品对比语境
    '"Nothing" account vs',
]

# 拼成 X API 搜索 query（OR 连接）
SEARCH_QUERY = " OR ".join(SEARCH_KEYWORDS)

# 每次搜索最大结果数 (X API free tier: 10-100)
MAX_RESULTS = 50

# ============================================================
# X API 凭证（从环境变量读取，不硬编码）
# ============================================================
X_BEARER_TOKEN = os.environ.get("X_BEARER_TOKEN", "")
X_API_KEY = os.environ.get("X_API_KEY", "")

# 备用：从 .env 文件加载
def _load_env_file():
    """尝试从 social-monitor/.env 加载环境变量"""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    if key not in os.environ:
                        os.environ[key] = val

_load_env_file()

# 重新读取（.env 加载后）
X_BEARER_TOKEN = os.environ.get("X_BEARER_TOKEN", "")
X_API_KEY = os.environ.get("X_API_KEY", "")

# twikit 登录凭证（免 API 额度方案）
X_EMAIL = os.environ.get("X_EMAIL", "")
X_PASSWORD = os.environ.get("X_PASSWORD", "")

# ============================================================
# 数据路径
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "mentions.json")
DASHBOARD_OUTPUT = os.path.join(BASE_DIR, "..", "docs", "index.html")

# ============================================================
# 通知配置（后期接飞书/邮件）
# ============================================================
ENABLE_NOTIFICATION = False

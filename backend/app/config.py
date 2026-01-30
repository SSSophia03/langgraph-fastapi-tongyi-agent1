import os
import logging
from dotenv import load_dotenv

# 加载 .env 文件
# 这里的逻辑是：先找当前目录，如果找不到去上一级找（防止路径问题）
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir)) # 项目根目录
backend_dir = os.path.dirname(current_dir) # backend 目录

# 尝试加载多个位置的 .env，确保万无一失
load_dotenv(os.path.join(backend_dir, ".env"))
load_dotenv(os.path.join(parent_dir, ".env"))

# 读取 DeepSeek Key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not DEEPSEEK_API_KEY:
    print("Warning: DEEPSEEK_API_KEY not found in env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent_backend")
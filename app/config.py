import os
import logging
from dotenv import load_dotenv

load_dotenv()

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise ValueError("请在.env文件中配置DASHSCOPE_API_KEY！")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import logging
import sys
from pathlib import Path
import contextvars

# 日志目录
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

request_id_var = contextvars.ContextVar("request_id", default="-")
task_id_var = contextvars.ContextVar("task_id", default="-")


class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # 将上下文中的 request_id 与 task_id 注入日志
        record.request_id = request_id_var.get("-")
        record.task_id = task_id_var.get("-")
        return True


context_filter = ContextFilter()

# 日志格式（包含 request_id 与 task_id）
formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] [req=%(request_id)s task=%(task_id)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 控制台输出
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.addFilter(context_filter)

# 文件输出
file_handler = logging.FileHandler(LOG_DIR / "app.log", encoding="utf-8")
file_handler.setFormatter(formatter)
file_handler.addFilter(context_filter)

# 获取日志器

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.propagate = False
    return logger

# 提供上下文 setter，便于在中间件/任务阶段设置
def set_request_id(request_id: str):
    request_id_var.set(request_id or "-")


def set_task_id(task_id: str):
    task_id_var.set(task_id or "-")

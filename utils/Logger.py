import logging
import logging.config
import json
import os
from typing import Optional
from logging.handlers import TimedRotatingFileHandler
import datetime
import threading

class Logger:
    """增强版日志类，提供更详细的日志记录功能"""
    _initialized = False
    _lock = threading.Lock()
    
    @classmethod
    def initialize(cls):
        """初始化日志系统"""
        with cls._lock:
            if cls._initialized:
                return
                
            # 创建日志目录
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
                
            # 加载日志配置
            config_path = "logging_config.json"
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    logging.config.dictConfig(config)
                except Exception as e:
                    logging.error(f"Failed to load logging config: {str(e)}")
                    raise
            else:
                # 默认配置
                logging.basicConfig(
                    level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    handlers=[
                        logging.StreamHandler(),
                        TimedRotatingFileHandler(
                            filename=os.path.join(log_dir, "application.log"),
                            when="midnight",
                            interval=1,
                            backupCount=7,
                            encoding="utf-8"
                        )
                    ]
                )
                
            cls._initialized = True
            logging.info("Logger system initialized successfully")

    def __init__(self, name: str):
        """初始化日志实例"""
        Logger.initialize()
        self.logger = logging.getLogger(name)
        self.logger.debug(f"Logger instance created for {name}")
        
    def set_level(self, level: str) -> None:
        """设置日志级别"""
        try:
            level = level.upper()
            if level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
                self.logger.setLevel(getattr(logging, level))
                self.logger.info(f"Log level changed to {level}")
            else:
                self.logger.warning(f"Invalid log level: {level}")
        except Exception as e:
            self.logger.error(f"Failed to set log level: {str(e)}", exc_info=True)

    def debug(self, message: str, **kwargs) -> None:
        """记录调试信息"""
        self.logger.debug(message, **kwargs)

    def info(self, message: str, **kwargs) -> None:
        """记录常规信息"""
        self.logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """记录警告信息"""
        self.logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        """记录错误信息"""
        self.logger.error(message, **kwargs)

    def critical(self, message: str, **kwargs) -> None:
        """记录严重错误信息"""
        self.logger.critical(message, **kwargs)

    def exception(self, message: str, **kwargs) -> None:
        """记录异常信息"""
        self.logger.exception(message, **kwargs)

    @staticmethod
    def cleanup_logs(max_days: int = 7) -> None:
        """清理过期日志文件"""
        try:
            log_dir = "logs"
            if not os.path.exists(log_dir):
                return
                
            now = datetime.datetime.now()
            for filename in os.listdir(log_dir):
                file_path = os.path.join(log_dir, filename)
                if os.path.isfile(file_path):
                    file_time = datetime.datetime.fromtimestamp(
                        os.path.getmtime(file_path)
                    )
                    if (now - file_time).days > max_days:
                        try:
                            os.remove(file_path)
                            logging.info(f"Deleted old log file: {file_path}")
                        except Exception as e:
                            logging.error(f"Failed to delete log file {file_path}: {e}")
        except Exception as e:
            logging.error(f"Failed to cleanup logs: {str(e)}", exc_info=True)

import sys
from utils.Logger import Logger
from core.FileManager import FileManager
import json
from typing import Any, Dict, Optional
import os

class Config:
    """配置管理类"""

    def __init__(self, config_file: str = "config.json"):
        """初始化配置管理器"""
        self.logger = Logger(__name__)
        self.file_manager = FileManager()

        if not config_file:
            raise ValueError("Config file path cannot be empty")

        # 确保路径是绝对路径
        if not os.path.isabs(config_file):
            # 如果是打包后的应用程序，使用sys._MEIPASS获取临时目录
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.getcwd()
            config_file = os.path.join(base_path, config_file)

        # 确保目录存在
        os.makedirs(os.path.dirname(config_file), exist_ok=True)

        self.config_file = config_file
        self.config = self._load_config()
        self.logger.info(f"Config initialized with file: {self.config_file}")

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            config = self.file_manager.read_json(self.config_file)
            self.logger.info(f"Successfully loaded config from {self.config_file}")
            return config
        except FileNotFoundError:
            self.logger.warning(f"Config file {self.config_file} not found, creating default")
            return self._create_default_config()
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config file: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to load config: {str(e)}")
            raise

    def _create_default_config(self) -> Dict[str, Any]:
        """创建默认配置"""
        default_config = {
            "provider": "deepseek",
            "api_keys": {
                "deepseek": "",
                "zhipu": "",
                "qwen": ""
            },
            "model_id": {
                "deepseek": "deepseek-chat",
                "zhipu": "glm-4-flash",
                "qwen": "qwen-turbo"
            },
            "temperature": 0.7,
            "max_tokens": 1000,
            "top_p": 0.9,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0,
            "stream": True,
            "font_family": "Arial",
            "font_size": 18,
            "log_level": "INFO"
        }
        try:
            self.file_manager.write_json(self.config_file, default_config)
            self.logger.info(f"Created default config at {self.config_file}")
            return default_config
        except Exception as e:
            self.logger.error(f"Failed to create default config: {str(e)}")
            raise

    def get(self, key: str, default=None) -> Any:
        """获取配置项"""
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                if isinstance(value, dict):
                    value = value[k]
                else:
                    return default
            return value
        except KeyError:
            return default

    def get_current_provider(self) -> str:
        """获取当前使用的AI服务提供商"""
        provider = self.get("provider", "deepseek")
        self.logger.debug(f"Current provider: {provider}")
        return provider

    def _validate_provider(self, provider: str) -> str:
        """验证并规范化provider名称"""
        provider = provider.lower()
        if provider not in ["deepseek", "zhipu", "qwen"]:
            raise ValueError(f"Invalid provider: {provider}")
        return provider

    def set_current_provider(self, provider: str) -> None:
        """设置当前使用的AI服务提供商"""
        provider = self._validate_provider(provider)
        self.set("provider", provider)
        self.logger.info(f"Changed provider to: {provider}")
        # 设置默认模型ID
        self.set(f"model_id.{provider}", f"{provider}-chat")
        self.logger.info(f"Set default model ID for provider: {provider}")

    def set_api_key(self, provider: str, api_key: str) -> None:
        """设置指定provider的API key"""
        provider = self._validate_provider(provider)
        self.set(f"api_keys.{provider}", api_key)
        self.logger.info(f"Updated API key for provider: {provider}")

    def set_model_id(self, provider: str, model_id: str) -> None:
        """设置指定provider的模型ID"""
        provider = self._validate_provider(provider)
        self.set(f"model_id.{provider}", model_id)
        self.logger.info(f"Changed model ID to: {model_id}")

    def get_api_key(self, provider: Optional[str] = None) -> str:
        """获取指定provider的API key"""
        if provider is None:
            provider = self.get_current_provider()
        api_key = self.get(f"api_keys.{provider}", "")
        self.logger.debug(f"Retrieved API key for provider: {provider}")
        return api_key

    def set(self, key: str, value: Any) -> None:
        """设置配置项"""
        keys = key.split('.')
        current = self.config
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
        self.logger.info(f"Updated config key: {key} = {value}")
        self.save()  # 调用 save 方法保存配置

    def save(self) -> None:
        """保存配置到文件"""
        try:
            self.file_manager.write_json(self.config_file, self.config)
            self.logger.info(f"Successfully saved config to {self.config_file}")
        except Exception as e:
            self.logger.error(f"Failed to save config: {str(e)}")
            raise
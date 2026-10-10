from utils.Logger import Logger
import os
import json
from typing import Optional

class FileManager:
    def __init__(self):
        self.logger = Logger(__name__)
        self.logger.info("FileManager initialized")

    def read_file(self, file_path: str) -> Optional[str]:
        """读取文件内容"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.logger.info(f"Successfully read file: {file_path}")
                return content
        except Exception as e:
            self.logger.error(f"Failed to read file {file_path}: {str(e)}")
            return None

    def write_file(self, file_path: str, content: str) -> bool:
        """写入文件内容"""
        try:
            # 创建目录（如果不存在）
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
                self.logger.info(f"Successfully wrote to file: {file_path}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to write file {file_path}: {str(e)}")
            return False

    def read_json(self, file_path: str) -> Optional[dict]:
        """读取JSON文件"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.logger.info(f"Successfully read JSON file: {file_path}")
                return data
        except Exception as e:
            self.logger.error(f"Failed to read JSON file {file_path}: {str(e)}")
            return None

    def write_json(self, file_path: str, data: dict) -> bool:
        """写入JSON文件"""
        try:
            # 创建目录（如果不存在）
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                self.logger.info(f"Successfully wrote JSON file: {file_path}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to write JSON file {file_path}: {str(e)}")
            return False

    def file_exists(self, file_path: str) -> bool:
        """检查文件是否存在"""
        exists = os.path.exists(file_path)
        self.logger.info(f"File {file_path} exists: {exists}")
        return exists

    def delete_file(self, file_path: str) -> bool:
        """删除文件"""
        try:
            os.remove(file_path)
            self.logger.info(f"Successfully deleted file: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete file {file_path}: {str(e)}")
            return False

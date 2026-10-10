from utils.Logger import Logger
import re
from typing import Optional

class FormatManager:
    def __init__(self):
        self.logger = Logger(__name__)
        self.logger.info("FormatManager initialized")

    def format_text(self, text: str, max_line_length: int = 80) -> str:
        """格式化文本"""
        try:
            # 去除多余空行
            text = re.sub(r'\n{3,}', '\n\n', text)
            
            # 格式化段落
            formatted_lines = []
            for paragraph in text.split('\n\n'):
                lines = self._wrap_paragraph(paragraph, max_line_length)
                formatted_lines.extend(lines)
                formatted_lines.append('')  # 添加空行分隔段落
            
            # 去除最后一个多余的空行
            if formatted_lines and formatted_lines[-1] == '':
                formatted_lines.pop()
            
            formatted_text = '\n'.join(formatted_lines)
            self.logger.info("Text formatted successfully")
            return formatted_text
        except Exception as e:
            self.logger.error(f"Failed to format text: {str(e)}")
            return text

    def _wrap_paragraph(self, text: str, max_length: int) -> list:
        """包装单个段落"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            # 如果当前行加上新单词不超过最大长度
            if current_length + word_length + len(current_line) <= max_length:
                current_line.append(word)
                current_length += word_length
            else:
                # 添加当前行并开始新行
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
        
        # 添加最后一行
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

    def format_json(self, json_str: str) -> Optional[str]:
        """格式化JSON字符串"""
        try:
            import json
            parsed = json.loads(json_str)
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
            self.logger.info("JSON formatted successfully")
            return formatted
        except Exception as e:
            self.logger.error(f"Failed to format JSON: {str(e)}")
            return None

    def format_code(self, code: str, language: str) -> Optional[str]:
        """格式化代码"""
        try:
            # 这里可以扩展支持更多语言的格式化
            if language.lower() == "python":
                import autopep8
                formatted = autopep8.fix_code(code)
                self.logger.info(f"Python code formatted successfully")
                return formatted
            else:
                self.logger.warning(f"Unsupported language for formatting: {language}")
                return code
        except Exception as e:
            self.logger.error(f"Failed to format {language} code: {str(e)}")
            return None

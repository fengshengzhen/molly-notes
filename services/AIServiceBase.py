from abc import ABC, abstractmethod  #用于创建抽象的基类
from typing import  Optional, Dict, Any, List
import json
from utils.Logger import Logger

class AIServiceBase(ABC):
    def __init__(self, api_key:str,config:Dict = None):
        self.logger = Logger(self.__class__.__name__)
        self.api_key = api_key
        self.config = config or {}

        self.logger.info(f"{self.__class__.__name__} initialized")

    def get_model_params(self) -> Dict[str, Any]:
        """
        获取
        :return:
        """
        return {
            "temperature": self.config.get("temperature",0.7),
            "top_p": self.config.get("top_p",0.9),
            "max_tokens": self.config.get("max_tokens",1000),

        }
    @abstractmethod
    async def generate_text(self,prompt:str) -> Optional[str]:
           """
           根据提示词生成文本
           :param prompt:用于生成文本的提示词
           :return:
           """
           pass



    @abstractmethod
    async def continue_writing(self,text:str) -> Optional[str]:
        """
        根据已有的文本进行续写
        :param text:需要续写的文本
        :return:
        """
        pass

    @abstractmethod
    async def ask_question(self,question:str) -> Optional[str]:
        """
        回答用户的问题
        :param question:用户提出的问题
        :return:
        """
        pass

    @abstractmethod
    async def  expand_text(self,text:str) -> Optional[str]:
        """
        对现有的文本进行扩展和补充
        :param text:
        :return:
        """
        pass

    @abstractmethod
    async  def analyze_code(self,code:str) -> Optional[Dict[str,Any]]:
        """
        分析并评估提供给的代码
        :param code:需要分析的代码
        :return:
        """
        pass

    @abstractmethod
    async def summarize_text(self,text:str,max_length:int =150) -> Optional[str]:
        """
        生成文本摘要
        :param text:需要摘要的原始文本
        :param max_length:摘要的最大长度
        :return:
        """
        pass

    @abstractmethod
    async  def translate_text(self,text:str,target_language:str = "en") -> Optional[str]:
        """
        将文本翻译到目标语言
        :param text:
        :param target_language:目标语言
        :return:
        """
        pass

    @abstractmethod
    async def convert_style(self,text:str,target_style:str = "informal") -> Optional[str]:
        """
        转换文本
        :param text:
        :param target_style:
        :return:
        """
        pass


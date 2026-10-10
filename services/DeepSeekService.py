# 导入所需模块
from services.AIServiceBase import AIServiceBase  # 从自定义模块导入基类
from typing import Optional, Dict, Any  # 类型提示相关
import json  # JSON处理模块
from openai import OpenAI  # OpenAI官方库
import asyncio  # 异步IO库


class DeepSeekService(AIServiceBase):
    def __init__(self, api_key: str, config: Dict = None):
        # 调用父类的初始化方法
        super().__init__(api_key, config)

        # 创建DeepSeek客户端实例
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

        self.config = config if isinstance(config, dict) else {}

    async def generate_text(self, prompt: str) -> Optional[str]:
        """核心文本生成"""
        try:
            model_params = {
                "temperature": self.config.get("temperature", 0.7),
                "top_p": self.config.get("top_p", 0.9),
                "max_tokens": self.config.get("max_tokens", 1000)
            }

            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                **model_params  # 注入模型参数
            )

            return response.choices[0].message.content
        except Exception as e:
            # 记录错误日志（包含完整异步信息）
            self.logger.error(f"DeepSeek text  generation failed: {str(e)}", exc_info=True)
            return None

    async def continue_writing(self, text: str) -> Optional[str]:
        """文本续写功能"""
        self.logger.info("Starting text continuation")

        # 构建提示词模板
        prompt = f"""请续写以下内容
        {text}

        续写要求：
        1.保持原有的风格和语气
        2.续写200-300字
        3.确保内容连贯
        """
        self.logger.debug(f"Continue writing prompt: {prompt}")
        result = await self.generate_text(prompt)
        self.logger.info(f"Text continuation completed")

        return result

    async def ask_question(self, question: str) -> Optional[str]:
        """问答功能实现"""
        self.logger.info(f"Starting to answer question: {question[:100]}...")

        prompt = f"""请回答以下问题
        {question}

        回答要求：
        1.提供详细解释
        2.必要时给出示例
        3.保持专业性
        """

        self.logger.debug(f"Question answering prompt: {prompt}")
        result = await self.generate_text(prompt)
        self.logger.info(f"Question answered")

        return result

    async def expand_text(self, text: str) -> Optional[str]:
        """文本扩展功能实现"""
        self.logger.info(f"Starting text expansion")

        prompt = f"""请扩写以下内容
        {text}

        扩写要求：
        1.保持核心内容不变
        2.添加细节和解释
        3.使内容更丰富完整
        """

        self.logger.debug(f"Text expansion prompt: {prompt}")
        result = await self.generate_text(prompt)
        self.logger.info("Text expansion completed")

        return result

    async  def analyze_code(self,code:str) -> Optional[Dict[str,Any]]:
        """代码分析功能实现"""
        self.logger.info("Starting code analysis")

        prompt = f"""请分析以下代码并返回JSON格式的分析结果
        {code}
        1.代码质量评分(0-100)
        2.潜在问题列表
        3.改进建议
        
        代码：
        {code}
        
        返回格式:
        {{
            "quality_score":0-100
            "issues":["问题1","问题2"
            "suggestions":["建议1","建议2"] 
        }}
        """

        self.logger.debug(f"Code analysis prompt: {prompt}")

        result = await self.generate_text(prompt)

        if result:
            try:
                return  json.loads(result)
            except json.JSONDecodeError:
                #处理格式错误
                self.logger.warning("Code analysis  returned no result")
                return None

    async  def summarize_text(self,text:str,max_length:int =150) -> Optional[str]:
        """文本摘要功能实现"""
        prompt = f"""请对以下文本进行摘要，摘要长度不超过{max_length}字:{text}"""


        return  await self.generate_text(prompt)

    async  def  translate_text(self,text:str,target_language:str = "en") -> Optional[str]:
        """文本翻译功能实现"""
        prompt =  f"""请将以下文本翻译成{target_language}: {text}"""


        return await self.generate_text(prompt)

    async def convert_style(self,text:str,target_style:str = "informal") -> Optional[str]:
        """文本风格"""
        prompt = f"""请对将以下文本的风格转换成{f"target_style"}:{text}"""

        return await self.generate_text(prompt)
from services.AIServiceBase import AIServiceBase
from openai import AsyncOpenAI
import os

class ZhipuService(AIServiceBase):
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv("ZHIPU_API_KEY"),
            base_url="https://open.bigmodel.cn/api/paas/v4/"
        )
        self.model = "glm-4-flash"

    async def generate(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
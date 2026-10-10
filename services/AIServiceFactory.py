#导入所需模块
from services.DeepSeekService import DeepSeekService
from services.ZhipuService import ZhipuService
from utils.Logger import Logger #自定义日志记录工具
#from services.DeepSeekService import DeepSeekService
#from services.ZhipuService import ZhipuService
#from services.QwenService import Qwenservice
from config import Config

class AIServiceFactory:

    @staticmethod
    def create_service(config:Config,loop:None):
        """
        根据配置创建对应的AI服务的实例
        :param config:
        :param loop:
        :return:具体的AI服务实例
        """
        logger = Logger(__name__)
        provider = config.get_current_provider()
        logger.debug(f"Creating AI service for  provider: {provider}")

        #根据服务商的名称创建对应实例
        if provider == 'deepseek':
            logger.info("Initializing Deepseek service")
            return  DeepSeekService(config.get_api_key("deepseek"),loop)
        elif provider == 'zhipu':
            logger.info("Initializing Zhipu service")
            return ZhipuService(config.get_api_key("zhipu"),loop)
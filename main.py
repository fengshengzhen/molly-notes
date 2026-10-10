import  asyncio
import  threading #线程
import time
import tkinter as tk
from config  import  Config
from services.AIServiceFactory import AIServiceFactory
from utils.Logger import Logger
from sys import  exc_info
from anyio import  sleep
from ui.MainWindow import MainWindow
from services.AIServiceFactory import AIServiceFactory
def async_loop(loop):
    """

    :param loop: 要运行的事件循环对象
    :return:
    """
    asyncio.set_event_loop(loop)
    #启动事件循环
    loop.run_forever()

def main():
    """启用程序主入口"""
    logger = Logger(__name__)
    logger.info("开始启动程序——————")

    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    threading.Thread(target=async_loop, args=(loop,),daemon=True).start()

    while not loop.is_running():
        time.sleep(0.1)

    try:


        config = Config()

        root = tk.Tk()
        root.title("AI魔力笔记")
        root.geometry("900x600")

        #初始化AI服务
        ai_service = AIServiceFactory.create_service(config,loop)

        logger.info("初始化主窗口组件")

        MainWindow(root, ai_service,config)

        root.mainloop()
    except Exception as e:
        logger.critical(f"程序出现错误:{str(e)}",exc_info=True)
        raise #重新抛出异常

    finally:
        logger.info("关闭程序")
        Logger.cleanup_logs(7)

if __name__ == "__main__":
    main()

import asyncio
from gettext import translation
from sys import exc_info
from tkhtmlview import  HTMLLabel  #第三方库组件,用于TKinter显示HTML内容标签组件
import tkinter as tk
from tkinter import ttk, scrolledtext,filedialog
from utils.Logger import Logger
from ui.SettingsWindow import SettingsWindow

class MainWindow:
    def __init__(self,root,ai_service,config):
        #tkinter 根窗口对象
        self.root = root
        self.logger = Logger(__name__)
        self.config = config
        self.ai_service = ai_service
        self.settings_window = SettingsWindow(config)

        try:
            self.logger.info("初始化窗口————————")

            self.setup_ui()

            self.logger.info("主窗口初始化成功")
        except Exception as e:
            self.logger.critical(f"主窗口初始化失败{str(e)}",exc_info=True)

    def setup_ui(self):
            main_frame = ttk.Frame(self.root)

            main_frame.pack(fill=tk.BOTH, expand=True,padx=10,pady=10)

            self.editor = scrolledtext.ScrolledText(
                main_frame,
                wrap= tk.WORD,
                font =("Consolas",16),
                undo=True,
                maxundo=50
            )
            self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.logger.debug("编辑区域已经初始化")


            #创建HTML预览区域
            self.preview = HTMLLabel(main_frame)
            self.preview.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            self.logger.debug("预览区域已经初始化")

            #创建菜单栏
            menubar = tk.Menu(self.root)
            self.root.config(menu=menubar)

            #创建文件菜单及其选项
            file_menu = tk.Menu(menubar, tearoff=0)
            file_menu.add_command(label='打开',command=self.open_file)
            file_menu.add_command(label='保存',command=self.save_file)
            menubar.add_cascade(label='文件',menu=file_menu)

            # 创建编辑菜单及其选项
            edit_menu = tk.Menu(menubar, tearoff=0)
            edit_menu.add_command(label='撤销',command=lambda:self.editor.event_generate("<<Undo>>"))
            edit_menu.add_command(label='重做', command=lambda: self.editor.event_generate("<<Redo>>"))
            edit_menu.add_separator()
            edit_menu.add_command(label='剪切', command=lambda: self.editor.event_generate("<<cut>>"))
            edit_menu.add_command(label='复制', command=lambda: self.editor.event_generate("<<copy>>"))
            edit_menu.add_command(label='粘贴', command=lambda: self.editor.event_generate("<<Paste>>"))
            edit_menu.add_separator()
            edit_menu.add_command(label='全选', command=lambda: self.editor.tag_add("sel","1.0","end"))
            menubar.add_cascade(label="编辑",menu=edit_menu)

            #创建AI功能的菜单
            ai_menu = tk.Menu(menubar, tearoff=0)
            ai_menu.add_command(label="续写",command=self.continue_writing)
            ai_menu.add_command(label="提问",command=self.ask_question)
            ai_menu.add_command(label="扩写", command=self.expand_text)
            ai_menu.add_command(label="文本摘要",command=self.summarize_text)
            ai_menu.add_command(label="文本翻译", command=self.translate_text)
            ai_menu.add_command(label="风格转换", command=self.convert_style)
            ai_menu.add_command(label="分析代码", command=self.analyze_code)
            menubar.add_cascade(label="AI功能",menu=ai_menu)

            settings_menu = tk.Menu(menubar, tearoff=0)
            settings_menu.add_command(label="设置",command=self.show_settings)
            menubar.add_cascade(label="设置",menu=settings_menu)

            self.editor.bind("<KeyRelease>",self.on_editor_change)

            self.root.bind("<Control-o>",lambda e:self.open_file())
            self.root.bind("<Control-s>",lambda e:self.save_file())
            self.root.bind("<Control-z>",lambda e:self.editor.event_generate("<<Undo>>"))
            self.root.bind("<Control-y>", lambda e: self.editor.event_generate("<<Redo>>"))
            self.root.bind("<Control-x>", lambda e: self.editor.event_generate("<<Cut>>"))
            self.root.bind("<Control-c>", lambda e: self.editor.event_generate("<<Copy>>"))
            self.root.bind("<Control-v>", lambda e: self.editor.event_generate("<<Paste>>"))
            self.root.bind("<Control-a>", lambda e: self.editor.tag_add("sel","1.0","end"))


            self.root.bind("<Control-r>", lambda e: self.continue_writing())
            self.root.bind("<Control-q>", lambda e: self.ask_question())
            self.root.bind("<Control-e>", lambda e: self.expand_text())
            self.root.bind("<Control-t>", lambda e: self.translate_text())
            self.root.bind("<Control-m>", lambda e: self.summarize_text())
            self.root.bind("<Control-b>", lambda e: self.convert_style())


            file_menu.entryconfig("打开",accelerator="Ctrl+o")
            file_menu.entryconfig("保存", accelerator="Ctrl+s")
            edit_menu.entryconfig("撤销", accelerator="Ctrl+z")
            edit_menu.entryconfig("重做", accelerator="Ctrl+y")
            edit_menu.entryconfig("剪切", accelerator="Ctrl+x")
            edit_menu.entryconfig("复制", accelerator="Ctrl+c")
            edit_menu.entryconfig("粘贴", accelerator="Ctrl+v")
            edit_menu.entryconfig("全选", accelerator="Ctrl+a")

            ai_menu.entryconfig("续写", accelerator="Ctrl+r")
            ai_menu.entryconfig("提问", accelerator="Ctrl+q")
            ai_menu.entryconfig("扩写", accelerator="Ctrl+e")
            ai_menu.entryconfig("文本摘要", accelerator="Ctrl+m")
            ai_menu.entryconfig("文本翻译", accelerator="Ctrl+t")
            ai_menu.entryconfig("风格转换", accelerator="Ctrl+b")

    def refresh_preview(self, event=None):
        try:
            markdown_str = self.editor.get("1.0", tk.END)
            preview_str = self.get_preview(markdown_str)  # 调用自己的get_preview方法
            self.preview.set_html(preview_str)
        except Exception as e:
            self.logger.error(f"刷新预览失败: {str(e)}", exc_info=True)
    def on_editor_change(self,event:None):
        self.refresh_preview()

    def get_preview(self,markdown):
        try:
            self.logger.debug("生成预览")
            import markdown2

            html = markdown2.markdown(
                markdown,
                extras=['fenced-code-blocks','tables','code-friendly'],
            )
            return html
        except Exception as e:
            self.logger.error(f"生成预览失败,文本内容是:{markdown}",exc_info=True)
            return  f"<pre>{markdown}</pre>"

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Markdown","*.md"),("文本文件","*.txt"),("所有文件","*.*")]
        )
        print("******************:",file_path)
        if file_path:
            try:
                with open(file_path,"r",encoding="UTF-8") as f:
                    content = f.read()
                    self.editor.delete("1.0",tk.END)
                    self.editor.insert(tk.END,content)
                    self.logger.info(f"文件{file_path}打开成功")
            except Exception as e:
                self.logger.critical(f"文件{file_path}=打开失败",exc_info=True)
                raise

    def save_file(self):
        file_path = filedialog.asksaveasfile(
            defaultextension=".md",
            filetypes=[("Markdown","*.md"),("文本文件","*.txt"),("所有文件","*.*")]
        )
        if file_path:
            try:
                with open(file_path.name,"w",encoding="UTF-8") as f:
                    content = self.editor.get(1.0,tk.END)
                    f.write(content)
                    self.logger.info(f"文件{file_path}保存成功")
            except Exception as e:
                self.logger.info(f"文件{file_path}保存失败")
                raise
    def show_settings(self):
        self.logger.info("显示设置窗口")
        try:
            self.settings_window.show(self.root)
            self.logger.info("设置窗口显示成功")
        except:
            self.logger.info("打开设置窗口错误")

    def continue_writing(self):
        """续写文本功能的方法"""
        self.logger.info("Initiating text continuation")

        try:
            text = self.editor.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            self.logger.warning("No text selected for continuation")
            return  # 直接返回 不执行后续操作

        def callback(future):
            continuation = future.result()
            try:
                continuation = future.result()

                if continuation:
                    self.editor.replace(tk.SEL_FIRST, tk.SEL_LAST, continuation)
                    self.logger.info("Text continuation completed successfully")
            except Exception as e:
                self.logger.error(f"Failed to continue text: {str(e)}", exc_info=True)

        future = asyncio.run_coroutine_threadsafe(
            self.ai_service.continue_writing(text),
            asyncio.get_event_loop()
        )

        future.add_done_callback(callback)


    def ask_question(self):
        self.logger.info("ask question")

        try:
            text = self.editor.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            text = self.editor.get("1.0", tk.END).strip()
            if not text:
             self.logger.warning("No text selected for continuation")
            return  # 直接返回 不执行后续操作

        def callback(future):
            try:
                continuation = future.result()
                try:
                    # 尝试替换选中的文字
                    self.editor.replace(tk.SEL_FIRST, tk.SEL_LAST, continuation)
                except tk.TclError:
                    # 如果用户中途取消选中，直接插入到光标位置
                    self.editor.insert(tk.INSERT, continuation)

                self.logger.info("Text continuation completed successfully")
            except Exception as e:
                self.logger.error(f"Failed to continue text: {str(e)}", exc_info=True)
        future = asyncio.run_coroutine_threadsafe(
            self.ai_service.ask_question(text),
            asyncio.get_event_loop()
        )

        future.add_done_callback(callback)

    def show_analysis_result(self,analysis):
        try:
            self.logger.info("Showing analysis result")
            #
            result_window = tk.Toplevel(self.root)
            result_window.title("问题结果")

            result_text = scrolledtext.ScrolledText(result_window,wrap=tk.WORD)
            result_text.pack(fill=tk.BOTH,expand=True)

            result_text.insert(tk.END,str(analysis))
            self.logger.debug("Analysis result window shown")
        except Exception as e:
            self.logger.error(f"Failed to show analysis result: {str(e)}", exc_info=True)


    def expand_text(self):
        self.logger.info("expanding text")

        try:
            text = self.editor.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            self.logger.warning("No text selected for continuation")
            return  # 直接返回 不执行后续操作

        def callback(future):
            continuation = future.result()
            try:
                continuation = future.result()

                if continuation:
                    self.editor.replace(tk.SEL_FIRST, tk.SEL_LAST, continuation)
                    self.logger.info("Text continuation completed successfully")
            except Exception as e:
                self.logger.error(f"Failed to continue text: {str(e)}", exc_info=True)

        future = asyncio.run_coroutine_threadsafe(
            self.ai_service.expand_text(text),
            asyncio.get_event_loop()
        )

        future.add_done_callback(callback)

    def summarize_text(self):
        self.logger.info("Initiating text summarization")

        try:
            text = self.editor.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            self.logger.warning("No text selected for continuation")
            return

        def callback(future):
            try:
                summary = future.result()
                if summary:
                    self.show_analysis_result(summary)
                    self.logger.info("Text summary completed successfully")
            except Exception as e:
                self.logger.error(f"Failed to summarize text: {str(e)}", exc_info=True)

        future = asyncio.run_coroutine_threadsafe(
            self.ai_service.summarize_text(text),
            asyncio.get_event_loop()
        )
        future.add_done_callback(callback)


    def translate_text(self):
        self.logger.info("Initiating text translation")
        try:
            #
            text = self.editor.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            self.logger.warning("No text selected for continuation")
            return

        #
        translation_window = tk.Toplevel(self.root)
        translation_window.title("翻译选项")

        ttk.Label(translation_window,text="目标语言")

        #
        self.target_language_var = tk.StringVar(value="英语(English)")
        language_options = {
            "en": "英语(English)",
            "zh": "中文(Chinese)",
            "ja": "日语(Japanese)",
            "fr": "法语(French)",
            "de": "德语(German)",
            "es": "西班牙语(Spanish)"
        }

        language_combobox = ttk.Combobox(
            translation_window,
            textvariable=self.target_language_var,
            values=list(language_options.values()),
            state="readonly",
        )
        language_combobox.grid(row=0, column=0, padx=5, pady=5)
        def start_translation():
            translation_window.destroy()
            selected_language = self.target_language_var.get()
            target_language = {v: k for k, v in language_options.items()}[selected_language]

            def callback(future):
                try:
                    translation = future.result()
                    if translation:
                        self.show_analysis_result(translation)
                        self.logger.info("Text translation completed successfully")
                except Exception as e:
                    self.logger.error(f"Failed to translate text: {str(e)}", exc_info=True)

            future = asyncio.run_coroutine_threadsafe(
                self.ai_service.translate_text(text,target_language),
                asyncio.get_event_loop()
            )

            future.add_done_callback(callback)

        ttk.Button(translation_window,text="开始翻译",command=start_translation).grid(row=1, column=0, padx=2, pady=5)


    def convert_style(self):
        self.logger.info("Initiating style conversion")
        try:
            text = self.editor.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            self.logger.warning("No text selected for continuation")
            return

        style_window = tk.Toplevel(self.root)
        style_window.title("风格转换选项")

        ttk.Label(style_window,text="风格目标:").grid(row=0, column=0, padx=5, pady=5)

        self.target_style_var = tk.StringVar(value="正式风格")
        style_options = {
            "formal":"正式风格",
            "casual":"日常口语",
            "professional":"专业技术",
            "literary":"文学风格",
            "business":"商务风格",
        }
        style_combobox = ttk.Combobox(
            style_window,
            textvariable=self.target_style_var,
            values=list(style_options.values()),
            state="readonly",
        )
        def start_conversion():
            style_window.destroy()
            selected_style = self.target_style_var.get()
            #
            target_style = {v:k for k, v in style_options.items()}[selected_style]
            def callback(future):
                try:
                    converted = future.result()
                    if converted:
                        self.editor.replace(tk.SEL_FIRST, tk.SEL_LAST, converted)
                        self.logger.info("Text converted successfully")
                except Exception as e:
                    self.logger.error(f"Failed to convert text: {str(e)}", exc_info=True)
                    future = asyncio.run_coroutine_threadsafe(
                        self.ai_service.convert_style(text,target_style),
                        asyncio.get_event_loop()
                    )
                    future.add_done_callback(callback)

                    style_combobox.grid(row=0, column=1, padx=5, pady=5)

                    ttk.Button(style_window,text="开始转换",command=start_conversion).grid(row=1, column=0, columnspan=2, pady=5)

    def analyze_code(self):
            """处理代码分析功能"""
            self.logger.info("Initiating code analysis")
            try:
                code = self.editor.get(tk.SEL_FIRST, tk.SEL_LAST)
            except tk.TclError:
                self.logger.warning("No text selected for code analysis")
                return

            def callback(future):
                try:
                    # 获取代码分析结果
                    analysis = future.result()
                    if analysis:  # 这里开始缩进
                        self.show_analysis_result(analysis)  # 缩进 4 个空格
                        self.logger.info("Code analysis completed successfully")
                except Exception as e:
                    self.logger.error(f"Failed to analyze code: {str(e)}", exc_info=True)

            future = asyncio.run_coroutine_threadsafe(
                self.ai_service.analyze_code(code),
                asyncio.get_event_loop()
            )
            future.add_done_callback(callback)













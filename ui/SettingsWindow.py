from tkinter import Toplevel, ttk, Canvas, BooleanVar, StringVar, DoubleVar, IntVar, messagebox
from utils.Logger import Logger
from typing import Dict, Optional, Any

class SettingsWindow:
    def __init__(self, config):
        self.logger = Logger(__name__)
        self.config = config
        self.logger.info("初始化设置窗口")
        self.model_options = {
            "deepseek": ["deepseek-chat", "deepseek-reasoner"],
            "zhipu": ["glm-4-flash", "glm-4-v-flash"],
            "qwen": ["qwen-turbo", "qwen-plus"],
        }
        self.original_api_key = ""  # 初始化 original_api_key

    def show(self, parent):
        try:
            self.logger.debug("创建设置窗口")
            self.window = Toplevel(parent)
            self.window.title("设置")
            self.window.geometry("600x400")

            tab_control = ttk.Notebook(self.window)

            ai_tab = ttk.Frame(tab_control)
            tab_control.add(ai_tab, text="AI服务")

            ai_canvas = Canvas(ai_tab)
            ai_scrollbar = ttk.Scrollbar(ai_tab, orient="vertical", command=ai_canvas.yview)
            ai_scrollable_frame = ttk.Frame(ai_canvas)

            ai_scrollable_frame.bind(
                "<Configure>",
                lambda e: ai_canvas.configure(
                    scrollregion=ai_canvas.bbox("all")
                )
            )

            ai_canvas.create_window((0, 0), window=ai_scrollable_frame, anchor="nw")
            ai_canvas.configure(yscrollcommand=ai_scrollbar.set)

            ai_canvas.pack(side="left", fill="both", expand=True)
            ai_scrollbar.pack(side="right", fill="y")

            ai_frame = ttk.LabelFrame(ai_scrollable_frame, text="AI服务设置")
            ai_frame.pack(fill="x", padx=5, pady=5)

            ttk.Label(ai_frame, text="服务提供商:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
            self.provider_var = StringVar()
            self.provider_combobox = ttk.Combobox(
                ai_frame,
                textvariable=self.provider_var,
                values=["Deepseek", "Zhipu", "Qwen"],
                state="readonly",
                width=37
            )
            self.provider_combobox.grid(row=0, column=1, padx=5, pady=2)
            self.provider_combobox.set(self.config.get_current_provider())
            self.provider_combobox.bind("<<ComboboxSelected>>", self._update_provider_settings)

            ttk.Label(ai_frame, text="模型ID:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
            self.model_id_var = StringVar()
            self.model_id_combobox = ttk.Combobox(
                ai_frame,
                textvariable=self.model_id_var,
                state="readonly",
                width=37
            )
            self.model_id_combobox.grid(row=1, column=1, padx=5, pady=2)

            ttk.Label(ai_frame, text="API Key:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
            self.api_key_var = StringVar()
            self.api_key_entry = ttk.Entry(ai_frame, textvariable=self.api_key_var, width=37)
            self.api_key_entry.grid(row=2, column=1, padx=5, pady=2)
            self.api_key_entry.bind("<FocusIn>", self._show_full_api_key)
            self.api_key_entry.bind("<FocusOut>", self._hide_api_key)

            self._update_provider_settings()  # 初始化时更新设置

            model_frame = ttk.LabelFrame(ai_scrollable_frame, text="模型参数")
            model_frame.pack(fill="x", padx=5, pady=5)

            ttk.Label(model_frame, text="温度(0-1):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
            self.temperature_var = DoubleVar(value=self.config.get("temperature", 0.7))
            self.temperature_scale = ttk.Scale(model_frame, from_=0, to=1, variable=self.temperature_var, length=200)
            self.temperature_scale.grid(row=0, column=1, padx=5, pady=2)
            self.temperature_entry = ttk.Entry(model_frame, textvariable=self.temperature_var, width=10)
            self.temperature_entry.grid(row=0, column=2, padx=5, pady=2)

            ttk.Label(model_frame, text="最大token数:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
            self.max_tokens_var = IntVar(value=self.config.get("max_tokens", 1000))
            self.max_tokens_scale = ttk.Scale(model_frame, from_=100, to=4000, variable=self.max_tokens_var, length=200)
            self.max_tokens_scale.grid(row=1, column=1, padx=5, pady=2)
            self.max_tokens_entry = ttk.Entry(model_frame, textvariable=self.max_tokens_var, width=10)
            self.max_tokens_entry.grid(row=1, column=2, padx=5, pady=2)

            ttk.Label(model_frame, text="Top P (0-1):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
            self.top_p_var = DoubleVar(value=self.config.get("top_p", 0.9))
            self.top_p_scale = ttk.Scale(model_frame, from_=0, to=1, variable=self.top_p_var, length=200)
            self.top_p_scale.grid(row=2, column=1, padx=5, pady=2)
            self.top_p_entry = ttk.Entry(model_frame, textvariable=self.top_p_var, width=10)
            self.top_p_entry.grid(row=2, column=2, padx=5, pady=2)

            self.stream_var = BooleanVar(value=self.config.get("stream", True))
            ttk.Checkbutton(model_frame, text="流式输出", variable=self.stream_var).grid(row=3, column=0, sticky="w", columnspan=3, padx=5, pady=2)

            editor_tab = ttk.Frame(tab_control)
            tab_control.add(editor_tab, text='编辑器')

            editor_frame = ttk.LabelFrame(editor_tab, text="编辑器设置")
            editor_frame.pack(fill="x", padx=5, pady=5)

            ttk.Label(editor_frame, text="字体:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
            self.font_family_entry = ttk.Entry(editor_frame, width=20)
            self.font_family_entry.grid(row=0, column=1, padx=5, pady=2)
            self.font_family_entry.insert(0, self.config.get("font_family", "Arial"))

            ttk.Label(editor_frame, text="字体大小:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
            self.font_size_entry = ttk.Entry(editor_frame, width=10)
            self.font_size_entry.grid(row=1, column=1, padx=5, pady=2)
            self.font_size_entry.insert(0, str(self.config.get("font_size", 18)))

            ttk.Label(editor_frame, text="日志级别:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
            self.log_level_var = StringVar()
            self.log_level_combobox = ttk.Combobox(editor_frame,
                                                   textvariable=self.log_level_var,
                                                   values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                                                   state="readonly",
                                                   width=10)
            self.log_level_combobox.grid(row=2, column=1, padx=5, pady=2)
            self.log_level_combobox.set(self.config.get("log_level", "INFO"))

            tab_control.pack(expand=1, fill="both", pady=10, ipady=10)

            save_button = ttk.Button(self.window, text="保存设置", command=self._save_settings)
            save_button.pack(side="bottom", padx=10)

            self.logger.debug("设置窗口初始化完成")
        except Exception as e:
            self.logger.critical(f"显示窗口异常: {str(e)}", exc_info=True)

    def _update_provider_settings(self, event=None):
        try:
            provider = self.provider_var.get().lower()
            self.logger.debug(f"Updating provider settings for: {provider}")

            model_options = self.model_options.get(provider, [])
            self.model_id_combobox['values'] = model_options
            current_model = self.config.get(f"model_id.{provider}", "")
            if current_model in model_options:
                self.model_id_combobox.set(current_model)
            elif model_options:
                self.model_id_combobox.set(model_options[0])

            api_key = self.config.get(f"api_keys.{provider}", "")
            self.original_api_key = api_key
            self.api_key_var.set(self._format_api_key(api_key))

            self.logger.debug(f"Successfully updated settings for provider: {provider}")
        except Exception as e:
            self.logger.error(f"Failed to update provider settings: {str(e)}", exc_info=True)

    def _format_api_key(self, api_key: str) -> str:
        if len(api_key) <= 20:
            return api_key
        return f"{api_key[:8]}*****{api_key[-8:]}"

    def _show_full_api_key(self, event=None):
        try:
            current_provider = self.provider_var.get().lower()
            api_key = self.config.get(f"api_keys.{current_provider}", "")
            self.original_api_key = api_key
            self.api_key_var.set(api_key)
        except Exception as e:
            self.logger.error(f"Failed to show full API key: {str(e)}")

    def _hide_api_key(self, event=None):
        try:
            if hasattr(self, 'original_api_key'):
                self.api_key_var.set(self._format_api_key(self.original_api_key))
        except Exception as e:
            self.logger.error(f"Failed to hide API key: {str(e)}")

    def _save_settings(self):
        try:
            provider = self.provider_var.get().lower()
            if not hasattr(self, 'original_api_key'):
                self.logger.error("original_api_key is not initialized")
                messagebox.showerror("错误", "API Key 未正确初始化")
                return

            self.config.set(f"api_keys.{provider}", self.original_api_key)
            self.config.set(f"model_id.{provider}", self.model_id_var.get())
            self.config.set("temperature", self.temperature_var.get())
            self.config.set("max_tokens", self.max_tokens_var.get())
            self.config.set("top_p", self.top_p_var.get())
            self.config.set("stream", self.stream_var.get())
            self.config.set("font_family", self.font_family_entry.get())
            self.config.set("font_size", self.font_size_entry.get())
            self.config.set("log_level", self.log_level_var.get())
            self.config.save()
            messagebox.showinfo("成功", "设置已保存")
        except ValueError as e:
            self.logger.error(f"Invalid setting value: {str(e)}", exc_info=True)
            messagebox.showerror("错误", f"设置值格式错误: {str(e)}")
        except Exception as e:
            self.logger.critical(f"保存设置失败: {str(e)}", exc_info=True)
            messagebox.showerror("错误", f"保存设置失败: {str(e)}")
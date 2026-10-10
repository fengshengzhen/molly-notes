# AI 魔力笔记 (Molly Notes)

基于 Python + Tkinter + DeepSeek 的桌面端 AI 智能 Markdown 编辑器。

## ✨ 功能特性
- 实时 Markdown 预览
- AI 续写、AI 问答、AI 扩写
- 多模型接入（DeepSeek、通义千问、智谱AI），采用工厂模式一键切换
- asyncio 异步请求，解决 GUI 卡顿
- 分层解耦架构，代码高内聚低耦合

## 🚀 运行步骤
1. 克隆代码到本地：
   `git clone https://github.com/fengshengzhen/molly-notes.git`
2. 安装依赖：
   `pip install -r requirements.txt`
3. 配置 API Key：
   把 `config.example.json` 复制一份并重命名为 `config.json`，把里面的占位符换成你自己的 API Key。
4. 启动项目：
   `python main.py`

## 📷 运行截图
<img width="1920" height="1027" alt="AI魔力笔记运行截图" src="https://github.com/user-attachments/assets/f69b6215-30f8-4365-a758-1ad213171ebd" />


## 📝 注意事项
本项目仅供学习与展示，API Key 请自行在对应平台申请，不要将 `config.json` 上传至公开仓库。

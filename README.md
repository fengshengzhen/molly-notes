# AI 魔力笔记 (Molly Notes)

基于 Python + Tkinter + DeepSeek 的桌面端 AI 智能 Markdown 编辑器。

## ✨ 功能特性
- 实时 Markdown 预览
- AI 续写、AI 问答、AI 扩写
- 多模型接入（DeepSeek、通义千问、智谱AI），采用工厂模式一键切换
- asyncio 异步请求，解决 GUI 卡顿
- 分层解耦架构，代码高内聚低耦合

## 🚀 运行步骤

1. 克隆代码：
   `git clone https://github.com/fengshengzhen/molly-notes.git`

2. 安装依赖（建议使用 Python 3.11 虚拟环境）：
   `pip install -r requirements.txt`

3. 配置 API Key：
   - 把 `config.example.json` 复制一份并重命名为 `config.json`。
   - 填入你自己的 API Key（支持 DeepSeek、通义千问、智谱）。
   - **注意：千万不要把 `config.json` 提交到 Git！**

4. 启动程序：
   `python main.py`

## 📷 运行截图
<img width="1920" height="1027" alt="AI魔力笔记运行截图" src="https://github.com/user-attachments/assets/f69b6215-30f8-4365-a758-1ad213171ebd" />


## 📝 个人备注
- 开发过程中遇到的最大坑是 `config.json` 的泄露防范，所以我特地写了一个 `.gitignore` 来屏蔽它。
- 如果遇到网络请求超时，可以尝试使用加速工具或者更换第三方 API 代理。
- 本项目是我的个人练习与简历展示作品，欢迎交流指正。

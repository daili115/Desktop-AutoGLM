# Desktop-AutoGLM

Desktop-AutoGLM 是一个基于 [Open-AutoGLM](https://github.com/zai-org/Open-AutoGLM) 理念开发的桌面端 AI 自动操作助手。它能够通过视觉感知屏幕内容，并自动执行鼠标和键盘操作来完成用户指定的任务。

## 特性

- **视觉感知**：使用多模态大模型（如 GPT-4o, GLM-4V）直接理解屏幕截图。
- **跨平台支持**：基于 `pyautogui`，支持 Windows, macOS 和 Linux。
- **自然语言交互**：用户只需输入自然语言指令，AI 即可规划并执行操作。
- **灵活扩展**：易于添加新的操作指令或适配不同的模型。

## 安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/YOUR_USERNAME/Desktop-AutoGLM.git
   cd Desktop-AutoGLM
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

设置你的 API 密钥：
```bash
export OPENAI_API_KEY="your-api-key"
```

运行程序：
```bash
python main.py "在浏览器中搜索最新的 AI 新闻并总结"
```

### 参数说明

- `task`: 要执行的任务描述。
- `--model`: 使用的模型名称（默认: `gpt-4o`）。
- `--base-url`: API 基础地址（默认: `https://api.openai.com/v1`）。
- `--api-key`: API 密钥（也可以通过环境变量设置）。

## 可用操作

AI 可以执行以下操作：
- `Tap(x, y)`: 点击
- `DoubleTap(x, y)`: 双击
- `Type(text)`: 输入文本
- `Press(key)`: 按下按键
- `Scroll(clicks)`: 滚动
- `Drag(x1, y1, x2, y2)`: 拖拽
- `Wait(seconds)`: 等待

## 免责声明

本项目仅供研究和学习使用。在使用过程中，请确保 AI 的操作不会造成数据丢失或违反相关服务条款。

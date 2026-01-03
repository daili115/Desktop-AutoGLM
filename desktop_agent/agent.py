import os
import json
from typing import Optional, List, Dict, Any
from .model.client import ModelClient, ModelConfig, MessageBuilder
from .executor.controller import DesktopController

class DesktopAgent:
    def __init__(self, model_config: Optional[ModelConfig] = None):
        self.model_client = ModelClient(model_config)
        self.controller = DesktopController()
        self.history: List[Dict[str, Any]] = []
        self.system_prompt = """你是一个桌面操作助手。你可以通过查看屏幕截图并执行鼠标键盘操作来帮助用户完成任务。
可用操作：
- do(action="Tap", x=int, y=int): 点击坐标 (x, y)
- do(action="DoubleTap", x=int, y=int): 双击坐标 (x, y)
- do(action="Type", text=str): 输入文本
- do(action="Press", key=str): 按下按键 (如 'enter', 'esc', 'backspace')
- do(action="Scroll", clicks=int): 滚动鼠标 (正数向上，负数向下)
- do(action="Drag", x1=int, y1=int, x2=int, y2=int): 拖拽
- do(action="Wait", seconds=float): 等待
- finish(message=str): 任务完成并返回消息

请在回复中先使用 <think> 标签描述你的思考过程，然后给出具体的 do(...) 或 finish(...) 指令。
"""

    def run(self, task: str, max_steps: int = 20):
        print(f"开始任务: {task}")
        self.history = [MessageBuilder.create_system_message(self.system_prompt)]
        
        for step in range(max_steps):
            print(f"\n--- 步骤 {step + 1} ---")
            
            # 1. 获取当前屏幕截图
            screenshot_path = "current_screen.png"
            self.controller.get_screenshot(screenshot_path)
            
            # 2. 构建消息
            user_msg = f"当前任务: {task}\n请根据当前屏幕截图决定下一步操作。"
            if step == 0:
                self.history.append(MessageBuilder.create_user_message(user_msg, screenshot_path))
            else:
                # 为了节省上下文，可以只保留最近几张图，或者只传文字描述
                self.history.append(MessageBuilder.create_user_message("下一步？", screenshot_path))
            
            # 3. 请求模型
            response = self.model_client.request(self.history)
            print(f"思考: {response.thinking}")
            print(f"动作: {response.action}")
            
            self.history.append({"role": "assistant", "content": response.raw_content})
            
            # 4. 执行动作
            if "finish(" in response.action:
                message = response.action.split('message="')[1].split('"')[0]
                print(f"任务完成: {message}")
                return message
            
            try:
                self._execute_action(response.action)
            except Exception as e:
                print(f"执行动作出错: {e}")
                self.history.append(MessageBuilder.create_user_message(f"执行出错: {e}，请重试。"))
                
        print("达到最大步数，任务停止。")
        return "Failed to complete task within max steps."

    def _execute_action(self, action_str: str):
        # 简单的解析逻辑，实际应用中可以使用更严谨的解析
        if "action=\"Tap\"" in action_str:
            x = int(action_str.split("x=")[1].split(",")[0])
            y = int(action_str.split("y=")[1].split(")")[0])
            self.controller.tap(x, y)
        elif "action=\"DoubleTap\"" in action_str:
            x = int(action_str.split("x=")[1].split(",")[0])
            y = int(action_str.split("y=")[1].split(")")[0])
            self.controller.double_tap(x, y)
        elif "action=\"Type\"" in action_str:
            text = action_str.split('text="')[1].split('"')[0]
            self.controller.type_text(text)
        elif "action=\"Press\"" in action_str:
            key = action_str.split('key="')[1].split('"')[0]
            self.controller.press_key(key)
        elif "action=\"Scroll\"" in action_str:
            clicks = int(action_str.split("clicks=")[1].split(")")[0])
            self.controller.scroll(clicks)
        elif "action=\"Wait\"" in action_str:
            seconds = float(action_str.split("seconds=")[1].split(")")[0])
            self.controller.wait(seconds)
        elif "action=\"Drag\"" in action_str:
            x1 = int(action_str.split("x1=")[1].split(",")[0])
            y1 = int(action_str.split("y1=")[1].split(",")[0])
            x2 = int(action_str.split("x2=")[1].split(",")[0])
            y2 = int(action_str.split("y2=")[1].split(")")[0])
            self.controller.drag(x1, y1, x2, y2)

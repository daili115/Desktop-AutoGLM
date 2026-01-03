import os
import json
import re
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
            try:
                self.controller.get_screenshot(screenshot_path)
            except Exception as e:
                print(f"截图失败: {e}")
                # 在某些无头环境下可能会失败，这里记录但不中断
            
            # 2. 构建消息
            user_msg = f"当前任务: {task}\n请根据当前屏幕截图决定下一步操作。"
            if step == 0:
                self.history.append(MessageBuilder.create_user_message(user_msg, screenshot_path if os.path.exists(screenshot_path) else None))
            else:
                self.history.append(MessageBuilder.create_user_message("下一步？", screenshot_path if os.path.exists(screenshot_path) else None))
            
            # 3. 请求模型
            try:
                response = self.model_client.request(self.history)
                print(f"思考: {response.thinking}")
                print(f"动作: {response.action}")
                self.history.append({"role": "assistant", "content": response.raw_content})
            except Exception as e:
                print(f"模型请求失败: {e}")
                return f"Error: {e}"
            
            # 4. 执行动作
            if "finish(" in response.action:
                match = re.search(r'finish\(message=["\'](.*?)["\']\)', response.action)
                message = match.group(1) if match else "任务完成"
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
        # 使用正则表达式进行更健壮的解析
        if "action=\"Tap\"" in action_str or "action='Tap'" in action_str:
            match = re.search(r'x=(\d+),\s*y=(\d+)', action_str)
            if match:
                self.controller.tap(int(match.group(1)), int(match.group(2)))
        elif "action=\"DoubleTap\"" in action_str or "action='DoubleTap'" in action_str:
            match = re.search(r'x=(\d+),\s*y=(\d+)', action_str)
            if match:
                self.controller.double_tap(int(match.group(1)), int(match.group(2)))
        elif "action=\"Type\"" in action_str or "action='Type'" in action_str:
            match = re.search(r'text=["\'](.*?)["\']', action_str)
            if match:
                self.controller.type_text(match.group(1))
        elif "action=\"Press\"" in action_str or "action='Press'" in action_str:
            match = re.search(r'key=["\'](.*?)["\']', action_str)
            if match:
                self.controller.press_key(match.group(1))
        elif "action=\"Scroll\"" in action_str or "action='Scroll'" in action_str:
            match = re.search(r'clicks=(-?\d+)', action_str)
            if match:
                self.controller.scroll(int(match.group(1)))
        elif "action=\"Wait\"" in action_str or "action='Wait'" in action_str:
            match = re.search(r'seconds=(\d+\.?\d*)', action_str)
            if match:
                self.controller.wait(float(match.group(1)))
        elif "action=\"Drag\"" in action_str or "action='Drag'" in action_str:
            match = re.search(r'x1=(\d+),\s*y1=(\d+),\s*x2=(\d+),\s*y2=(\d+)', action_str)
            if match:
                self.controller.drag(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)))

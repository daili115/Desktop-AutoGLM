import os
import json
from desktop_agent.model.client import ModelClient, ModelConfig
from desktop_agent.executor.controller import DesktopController

def test_config_loading():
    print("测试配置加载...")
    config_path = "config.json"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            print(f"成功加载配置，默认提供商: {config.get('default_provider')}")
            return True
    print("未找到 config.json")
    return False

def test_controller_init():
    print("测试控制器初始化...")
    try:
        controller = DesktopController()
        print(f"屏幕尺寸: {controller.screen_width}x{controller.screen_height}")
        return True
    except Exception as e:
        print(f"控制器初始化失败 (可能是无头环境): {e}")
        return False

def test_model_parsing():
    print("测试模型响应解析...")
    client = ModelClient()
    test_content = "<think>我需要点击开始按钮</think>do(action=\"Tap\", x=100, y=200)"
    thinking, action = client._parse_response(test_content)
    print(f"解析思考: {thinking}")
    print(f"解析动作: {action}")
    assert thinking == "我需要点击开始按钮"
    assert "Tap" in action
    return True

if __name__ == "__main__":
    test_config_loading()
    test_controller_init()
    test_model_parsing()
    print("\n组件测试完成。")

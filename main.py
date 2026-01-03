import argparse
import os
from desktop_agent.agent import DesktopAgent
from desktop_agent.model.client import ModelConfig

import json

def load_config(config_path="config.json"):
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return None

def main():
    parser = argparse.ArgumentParser(description="Desktop-AutoGLM: AI 自动操作电脑助手")
    parser.add_argument("task", type=str, nargs='?', help="要执行的任务描述")
    parser.add_argument("--provider", type=str, help="使用的提供商名称 (从 config.json 中读取)")
    parser.add_argument("--model", type=str, help="使用的模型名称")
    parser.add_argument("--base-url", type=str, help="API 基础地址")
    parser.add_argument("--api-key", type=str, help="API 密钥")
    
    args = parser.parse_args()
    
    if not args.task:
        args.task = input("请输入您想让 AI 执行的任务: ")
    
    # 默认配置
    base_url = args.base_url or "https://api.openai.com/v1"
    model_name = args.model or "gpt-4o"
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")

    # 尝试从 config.json 加载
    file_config = load_config()
    if file_config:
        provider_name = args.provider or file_config.get("default_provider")
        providers = {p["name"]: p for p in file_config.get("providers", [])}
        
        if provider_name in providers:
            p = providers[provider_name]
            base_url = args.base_url or p.get("base_url", base_url)
            model_name = args.model or p.get("model", model_name)
            api_key = args.api_key or p.get("api_key") or api_key
            print(f"使用提供商配置: {provider_name}")

    if not api_key or api_key.startswith("YOUR_"):
        print("错误: 请提供有效的 API 密钥 (通过 config.json, --api-key 或环境变量 OPENAI_API_KEY)")
        return

    config = ModelConfig(
        base_url=base_url,
        api_key=api_key,
        model_name=model_name
    )
    
    agent = DesktopAgent(model_config=config)
    agent.run(args.task)

if __name__ == "__main__":
    main()

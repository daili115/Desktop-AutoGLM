import argparse
import os
from desktop_agent.agent import DesktopAgent
from desktop_agent.model.client import ModelConfig

def main():
    parser = argparse.ArgumentParser(description="Desktop-AutoGLM: AI 自动操作电脑助手")
    parser.add_argument("task", type=str, nargs='?', help="要执行的任务描述")
    parser.add_argument("--model", type=str, default="gpt-4o", help="使用的模型名称")
    parser.add_argument("--base-url", type=str, default="https://api.openai.com/v1", help="API 基础地址")
    parser.add_argument("--api-key", type=str, help="API 密钥")
    
    args = parser.parse_args()
    
    if not args.task:
        args.task = input("请输入您想让 AI 执行的任务: ")
    
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("错误: 请提供 API 密钥 (通过 --api-key 或环境变量 OPENAI_API_KEY)")
        return

    config = ModelConfig(
        base_url=args.base_url,
        api_key=api_key,
        model_name=args.model
    )
    
    agent = DesktopAgent(model_config=config)
    agent.run(args.task)

if __name__ == "__main__":
    main()

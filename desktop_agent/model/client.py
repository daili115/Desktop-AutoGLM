import json
import base64
from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from openai import OpenAI

@dataclass
class ModelConfig:
    base_url: str = "https://api.openai.com/v1"
    api_key: str = ""
    model_name: str = "gpt-4o"
    max_tokens: int = 2048
    temperature: float = 0.0

@dataclass
class ModelResponse:
    thinking: str
    action: str
    raw_content: str

class ModelClient:
    def __init__(self, config: Optional[ModelConfig] = None):
        self.config = config or ModelConfig()
        self.client = OpenAI(base_url=self.config.base_url, api_key=self.config.api_key)

    def request(self, messages: List[dict]) -> ModelResponse:
        response = self.client.chat.completions.create(
            model=self.config.model_name,
            messages=messages,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
        )
        raw_content = response.choices[0].message.content
        thinking, action = self._parse_response(raw_content)
        return ModelResponse(thinking=thinking, action=action, raw_content=raw_content)

    def _parse_response(self, content: str) -> Tuple[str, str]:
        if "<think>" in content and "</think>" in content:
            thinking = content.split("<think>")[1].split("</think>")[0].strip()
            action = content.split("</think>")[1].strip()
            return thinking, action
        
        if "do(" in content:
            parts = content.split("do(", 1)
            thinking = parts[0].strip()
            action = "do(" + parts[1]
            return thinking, action
            
        return "", content

class MessageBuilder:
    @staticmethod
    def create_system_message(content: str) -> dict:
        return {"role": "system", "content": content}

    @staticmethod
    def create_user_message(text: str, image_path: Optional[str] = None) -> dict:
        content = [{"type": "text", "text": text}]
        if image_path:
            with open(image_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode("utf-8")
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image_base64}"}
            })
        return {"role": "user", "content": content}

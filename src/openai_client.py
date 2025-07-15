import openai
import json
from typing import Dict, Any, Optional


class OpenAIClient:
    def __init__(self, api_key: str):
        """OpenAI APIクライアントを初期化"""
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate_scene_prompt(self, word: str, character_description: str = "仲の良い猫とねずみ", context: str = "") -> Dict[str, Any]:
        """
        英単語からシーンとイラスト作成プロンプトを生成
        
        Args:
            word: 対象の英単語
            character_description: キャラクターの説明
            
        Returns:
            シーン内容とプロンプトを含む辞書
        """
        system_prompt = f"""あなたは英語教育のためのイラスト作成を支援するAIです。
英単語の意味を視覚的に表現するシーンを考案し、イラスト作成用のプロンプトを生成してください。

キャラクター: {character_description}

以下の形式で回答してください：
```json
{{
    "word": "英単語",
    "scene_description": "シーンの詳細な説明（日本語）。キャラクターの表情、動作、背景要素まで具体的に描写する",
    "core_image": "この英単語のコアイメージ（日本語）。単語の本質的な意味や使用場面、感情的ニュアンスを説明する。シーンの説明ではなく、単語そのものの意味を表現する",
    "illustration_prompt": "イラスト作成用プロンプト（英語）。キャラクターの詳細な外見、表情、動作、背景要素を具体的に描写し、必ず最後に'No text, no words, no dialogue.'を含めること"
}}
```

重要な制約:
- セリフや文字は一切使用しない
- 視覚的なシーンだけで単語の意味を表現
- 子どもにも理解できるシンプルな構図
- キャラクターの表情や動作で感情を表現
- core_imageは英単語の辞書的意味や概念を説明し、シーンの要約にしない
- scene_descriptionは視覚的詳細を豊富に含める
- illustration_promptは具体的で詳細な英語描写にする"""

        user_prompt = f"英単語: {word}"
        if context:
            user_prompt += f"\n補足情報: {context}"
        user_prompt += f"\n\nこの単語のコアイメージを表現するシーンを考案してください。"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            # 使用量情報を取得
            usage = response.usage
            
            # JSONブロックを抽出
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_content = content[json_start:json_end].strip()
            else:
                json_content = content
            
            result = json.loads(json_content)
            
            # 使用量情報を結果に追加
            result["usage"] = {
                "model": "gpt-4o-mini",
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"シーン生成中にエラーが発生しました: {str(e)}")
    
    def create_image_edit(self, image_path: str, prompt: str, size: str = "1024x1024", quality: str = "auto") -> str:
        """
        gpt-image-1で画像編集を実行
        
        Args:
            image_path: ベース画像のパス
            prompt: 生成用プロンプト
            size: 画像サイズ
            quality: 画像品質（auto, low, medium, high）
            
        Returns:
            生成された画像のbase64データ
        """
        try:
            with open(image_path, "rb") as image_file:
                response = self.client.images.edit(
                    model="gpt-image-1",
                    image=image_file,
                    prompt=prompt,
                    size=size,
                    quality=quality,
                    n=1
                )
            
            # gpt-image-1は常にbase64形式で返す
            result = {
                "image_data": response.data[0].b64_json,
                "usage": {
                    "total_tokens": response.usage.total_tokens,
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "input_tokens_details": {
                        "text_tokens": response.usage.input_tokens_details.text_tokens,
                        "image_tokens": response.usage.input_tokens_details.image_tokens
                    }
                }
            }
            return result
            
        except Exception as e:
            raise Exception(f"画像生成中にエラーが発生しました: {str(e)}")
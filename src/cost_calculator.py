"""
OpenAI APIの使用量とコストを計算するユーティリティ
"""

from typing import Dict, Any


class CostCalculator:
    def __init__(self):
        """コスト計算機を初期化"""
        # OpenAI API料金表 (2025年7月11日時点)
        self.pricing = {
            "gpt-4o-mini": {
                "input": 0.000600,   # $0.60 per 1M tokens
                "output": 0.002400   # $2.40 per 1M tokens
            },
            "gpt-4o": {
                "input": 0.005000,   # $5.00 per 1M tokens
                "output": 0.020000   # $20.00 per 1M tokens
            },
            "gpt-4": {
                "input": 0.030000,   # $30.00 per 1M tokens
                "output": 0.060000   # $60.00 per 1M tokens
            },
            "gpt-image-1": {
                "text_input": 0.005000,   # $5.00 per 1M tokens (テキストプロンプト)
                "image_input": 0.010000,  # $10.00 per 1M tokens (ベース画像)
                "output": {
                    "1024x1024": {
                        "low": 0.011,
                        "medium": 0.042,
                        "high": 0.167,
                        "auto": 0.042  # 推定中品質
                    },
                    "1024x1536": {
                        "low": 0.016,
                        "medium": 0.063,
                        "high": 0.25,
                        "auto": 0.063
                    },
                    "1536x1024": {
                        "low": 0.016,
                        "medium": 0.063,
                        "high": 0.25,
                        "auto": 0.063
                    }
                }
            }
        }
    
    def calculate_chat_cost(self, usage: Dict[str, Any]) -> Dict[str, Any]:
        """
        Chat Completions APIのコストを計算
        
        Args:
            usage: 使用量情報
            
        Returns:
            コスト情報の辞書
        """
        model = usage["model"]
        prompt_tokens = usage["prompt_tokens"]
        completion_tokens = usage["completion_tokens"]
        total_tokens = usage["total_tokens"]
        
        if model not in self.pricing:
            return {
                "model": model,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "input_cost": 0.0,
                "output_cost": 0.0,
                "total_cost": 0.0,
                "error": f"Unknown model: {model}"
            }
        
        # コスト計算 (1Mトークンあたりの料金)
        input_cost = (prompt_tokens / 1_000_000) * self.pricing[model]["input"]
        output_cost = (completion_tokens / 1_000_000) * self.pricing[model]["output"]
        total_cost = input_cost + output_cost
        
        return {
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost
        }
    
    def calculate_image_cost(self, model: str = "gpt-image-1", quality: str = "auto", 
                           size: str = "1024x1024", count: int = 1, 
                           prompt_tokens: int = 0, image_tokens: int = 0, 
                           output_tokens: int = 0) -> Dict[str, Any]:
        """
        Image Generation APIのコストを計算
        
        Args:
            model: 使用モデル
            quality: 品質設定
            size: 画像サイズ
            count: 生成枚数
            prompt_tokens: テキストプロンプトのトークン数
            image_tokens: ベース画像のトークン数
            output_tokens: 出力トークン数
            
        Returns:
            コスト情報の辞書
        """
        if model not in self.pricing:
            return {
                "model": model,
                "quality": quality,
                "size": size,
                "count": count,
                "input_cost": 0.0,
                "output_cost": 0.0,
                "total_cost": 0.0,
                "error": f"Unknown model: {model}"
            }
        
        # 入力コスト（トークンベース）
        text_input_cost = (prompt_tokens / 1_000_000) * self.pricing[model]["text_input"]
        image_input_cost = (image_tokens / 1_000_000) * self.pricing[model]["image_input"]
        input_cost = text_input_cost + image_input_cost
        
        # 出力コスト（トークンベース + 品質推定）
        if model == "gpt-image-1":
            # $40.00 per 1M output tokens
            token_based_cost = (output_tokens / 1_000_000) * 40.0
            
            # 実際の品質を推定（トークンベースコストと品質別料金を比較）
            actual_quality = self._estimate_quality_from_cost(token_based_cost, size)
            
            output_cost = token_based_cost
            quality = actual_quality  # 推定された品質に更新
        else:
            # 他のモデル用のフォールバック
            if size in self.pricing[model]["output"] and quality in self.pricing[model]["output"][size]:
                cost_per_image = self.pricing[model]["output"][size][quality]
            else:
                cost_per_image = self.pricing[model]["output"]["1024x1024"]["auto"]
            output_cost = cost_per_image * count
        
        total_cost = input_cost + output_cost
        
        return {
            "model": model,
            "quality": quality,
            "size": size,
            "count": count,
            "prompt_tokens": prompt_tokens,
            "image_tokens": image_tokens,
            "output_tokens": output_tokens,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost
        }
    
    def _estimate_quality_from_cost(self, token_cost: float, size: str = "1024x1024") -> str:
        """
        トークンベースコストから品質を推定
        
        Args:
            token_cost: 実際のトークンベースコスト
            size: 画像サイズ
            
        Returns:
            推定された品質
        """
        if size not in self.pricing["gpt-image-1"]["output"]:
            size = "1024x1024"  # デフォルト
            
        quality_costs = self.pricing["gpt-image-1"]["output"][size]
        
        # 最も近い品質を見つける
        min_diff = float('inf')
        estimated_quality = "auto"
        
        for quality, expected_cost in quality_costs.items():
            diff = abs(token_cost - expected_cost)
            if diff < min_diff:
                min_diff = diff
                estimated_quality = quality
        
        return estimated_quality
    
    def calculate_total_cost(self, chat_cost: Dict[str, Any], 
                           image_cost: Dict[str, Any]) -> Dict[str, Any]:
        """
        総コストを計算
        
        Args:
            chat_cost: Chat APIのコスト情報
            image_cost: Image APIのコスト情報
            
        Returns:
            総コスト情報の辞書
        """
        chat_total = chat_cost.get("total_cost", 0.0)
        image_total = image_cost.get("total_cost", 0.0)
        total_cost = chat_total + image_total
        
        return {
            "chat_cost": chat_cost,
            "image_cost": image_cost,
            "total_cost": total_cost
        }
    
    def format_cost_display(self, cost_info: Dict[str, Any]) -> str:
        """
        コスト情報を表示用にフォーマット
        
        Args:
            cost_info: コスト情報
            
        Returns:
            フォーマットされた文字列
        """
        if "error" in cost_info:
            return f"コスト計算エラー: {cost_info['error']}"
        
        total_usd = cost_info.get("total_cost", 0.0)
        
        chat_cost = cost_info.get("chat_cost", {})
        image_cost = cost_info.get("image_cost", {})
        
        format_str = f"""
💰 生成コスト詳細
・チャット生成: ${chat_cost.get('total_cost', 0.0):.6f} ({chat_cost.get('total_tokens', 0)} tokens)
・画像生成入力: ${image_cost.get('input_cost', 0.0):.6f} ({image_cost.get('prompt_tokens', 0)} prompt + {image_cost.get('image_tokens', 0)} image tokens)
・画像生成出力: ${image_cost.get('output_cost', 0.0):.6f} ({image_cost.get('output_tokens', 0)} tokens → {image_cost.get('quality', 'auto')} quality, {image_cost.get('size', '1024x1024')})
・総コスト: ${total_usd:.6f}
        """.strip()
        
        return format_str
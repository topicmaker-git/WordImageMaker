import os
import requests
from datetime import datetime
from typing import Dict, Any
from .openai_client import OpenAIClient
from .cost_calculator import CostCalculator


class ImageGenerator:
    def __init__(self, openai_client: OpenAIClient, output_dir: str = "output/images"):
        """イメージ生成器を初期化"""
        self.openai_client = openai_client
        self.output_dir = output_dir
        self.cost_calculator = CostCalculator()
        
        # 出力ディレクトリが存在しない場合は作成
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_image(self, base_image_path: str, scene_data: Dict[str, Any], quality: str = "auto") -> str:
        """
        シーンデータを基にイラストを生成
        
        Args:
            base_image_path: ベースとなるキャラクター画像のパス（参考用）
            scene_data: シーンデータ
            quality: 画像品質（auto, low, medium, high）
            
        Returns:
            生成された画像のローカルパス
        """
        word = scene_data["word"]
        prompt = scene_data["illustration_prompt"]
        
        print(f"'{word}' のイラスト生成中...")
        print(f"プロンプト: {prompt}")
        print(f"品質設定: {quality}")
        
        try:
            # gpt-image-1でベース画像を編集
            image_result = self.openai_client.create_image_edit(
                image_path=base_image_path,
                prompt=prompt,
                size="1024x1024",
                quality=quality
            )
            
            # 生成された画像をbase64から保存
            image_path = self._save_image_from_base64(image_result["image_data"], word)
            
            # コスト計算を追加
            chat_cost = self.cost_calculator.calculate_chat_cost(scene_data.get("usage", {}))
            
            # APIレスポンスから正確なトークン数を取得
            image_usage = image_result.get("usage", {})
            text_tokens = image_usage.get("input_tokens_details", {}).get("text_tokens", 0)
            image_tokens = image_usage.get("input_tokens_details", {}).get("image_tokens", 0)
            output_tokens = image_usage.get("output_tokens", 0)
            
            image_cost = self.cost_calculator.calculate_image_cost(
                model="gpt-image-1", 
                quality=quality,
                size="1024x1024",
                count=1,
                prompt_tokens=text_tokens,
                image_tokens=image_tokens,
                output_tokens=output_tokens
            )
            total_cost = self.cost_calculator.calculate_total_cost(chat_cost, image_cost)
            
            print(f"イラスト生成完了: {image_path}")
            return image_path, total_cost
            
        except Exception as e:
            raise Exception(f"イラスト生成中にエラーが発生しました: {str(e)}")
    
    def _download_image(self, image_url: str, word: str) -> str:
        """
        画像URLから画像をダウンロードして保存
        
        Args:
            image_url: 画像のURL
            word: 英単語（ファイル名用）
            
        Returns:
            保存された画像のパス
        """
        try:
            # ファイル名を生成（タイムスタンプ付き）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{word}_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            
            # 画像をダウンロード
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # ファイルに保存
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return filepath
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"画像のダウンロード中にエラーが発生しました: {str(e)}")
        except Exception as e:
            raise Exception(f"画像の保存中にエラーが発生しました: {str(e)}")
    
    def _save_image_from_base64(self, image_b64: str, word: str) -> str:
        """
        base64データから画像を保存
        
        Args:
            image_b64: base64エンコードされた画像データ
            word: 英単語（ファイル名用）
            
        Returns:
            保存された画像のパス
        """
        try:
            import base64
            from datetime import datetime
            
            # ファイル名を生成（タイムスタンプ付き）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{word}_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            
            # base64データをデコードして保存
            image_data = base64.b64decode(image_b64)
            
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            return filepath
            
        except Exception as e:
            raise Exception(f"base64画像の保存中にエラーが発生しました: {str(e)}")
    
    def get_image_info(self, image_path: str) -> Dict[str, Any]:
        """
        画像の情報を取得
        
        Args:
            image_path: 画像のパス
            
        Returns:
            画像情報の辞書
        """
        try:
            from PIL import Image
            
            with Image.open(image_path) as img:
                width, height = img.size
                format_name = img.format
                mode = img.mode
            
            file_size = os.path.getsize(image_path)
            
            return {
                "path": image_path,
                "width": width,
                "height": height,
                "format": format_name,
                "mode": mode,
                "file_size": file_size
            }
            
        except Exception as e:
            raise Exception(f"画像情報の取得中にエラーが発生しました: {str(e)}")
    
    def display_image_info(self, image_path: str):
        """
        画像情報を表示
        
        Args:
            image_path: 画像のパス
        """
        try:
            info = self.get_image_info(image_path)
            print("\n=== 生成画像情報 ===")
            print(f"パス: {info['path']}")
            print(f"サイズ: {info['width']}x{info['height']}")
            print(f"フォーマット: {info['format']}")
            print(f"モード: {info['mode']}")
            print(f"ファイルサイズ: {info['file_size']} bytes")
            print("==================\n")
        except Exception as e:
            print(f"画像情報の表示中にエラーが発生しました: {str(e)}")
import json
from typing import Dict, Any
from .openai_client import OpenAIClient


class SceneGenerator:
    def __init__(self, openai_client: OpenAIClient):
        """シーン生成器を初期化"""
        self.openai_client = openai_client
    
    def generate_scene_data(self, word: str, character_description: str = '仲の良い猫とねずみ', context: str = '') -> Dict[str, Any]:
        """
        英単語からシーンデータを生成
        
        Args:
            word: 対象の英単語
            
        Returns:
            シーン情報を含む辞書
        """
        print(f"英単語 '{word}' のシーン生成中...")
        
        # OpenAI APIでシーンとプロンプトを生成
        scene_data = self.openai_client.generate_scene_prompt(word, character_description, context)
        
        # 生成結果を検証
        required_keys = ["word", "scene_description", "core_image", "illustration_prompt"]
        missing_keys = [key for key in required_keys if key not in scene_data]
        
        if missing_keys:
            raise ValueError(f"生成されたシーンデータに必要なキーが不足しています: {missing_keys}")
        
        # プロンプトに制約条件が含まれているか確認
        if "No text, no words, no dialogue" not in scene_data["illustration_prompt"]:
            scene_data["illustration_prompt"] += "\nNo text, no words, no dialogue."
        
        print(f"シーン生成完了: {scene_data['scene_description']}")
        return scene_data
    
    def save_scene_data(self, scene_data: Dict[str, Any], output_path: str):
        """
        シーンデータをJSONファイルに保存
        
        Args:
            scene_data: シーンデータ
            output_path: 保存先パス
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(scene_data, f, ensure_ascii=False, indent=2)
            print(f"シーンデータを保存しました: {output_path}")
        except Exception as e:
            raise Exception(f"シーンデータの保存中にエラーが発生しました: {str(e)}")
    
    def load_scene_data(self, file_path: str) -> Dict[str, Any]:
        """
        JSONファイルからシーンデータを読み込み
        
        Args:
            file_path: シーンデータファイルのパス
            
        Returns:
            シーンデータの辞書
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                scene_data = json.load(f)
            return scene_data
        except Exception as e:
            raise Exception(f"シーンデータの読み込み中にエラーが発生しました: {str(e)}")
    
    def display_scene_info(self, scene_data: Dict[str, Any]):
        """
        シーン情報を表示
        
        Args:
            scene_data: シーンデータ
        """
        print("\n=== シーン情報 ===")
        print(f"英単語: {scene_data['word']}")
        print(f"シーン: {scene_data['scene_description']}")
        print(f"コアイメージ: {scene_data['core_image']}")
        print(f"イラストプロンプト: {scene_data['illustration_prompt']}")
        print("==================\n")
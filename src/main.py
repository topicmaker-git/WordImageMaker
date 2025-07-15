#!/usr/bin/env python3
"""
Word Image Maker - 英単語イメージイラスト生成ツール

英単語のコアイメージを視覚的に表現するイラストを生成します。
"""

import os
import sys
import argparse
import traceback
from typing import Optional

# src/ ディレクトリを Python パスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .openai_client import OpenAIClient
from .scene_generator import SceneGenerator
from .image_generator import ImageGenerator
from .html_generator import HTMLGenerator


class WordImageMaker:
    def __init__(self, api_key: str, base_image_path: str):
        """Word Image Maker を初期化"""
        self.api_key = api_key
        self.base_image_path = base_image_path
        
        # コンポーネントを初期化
        self.openai_client = OpenAIClient(api_key)
        self.scene_generator = SceneGenerator(self.openai_client)
        self.image_generator = ImageGenerator(self.openai_client)
        self.html_generator = HTMLGenerator()
        
        # 生成した単語のリストを記録
        self.generated_words = []
    
    def generate_word_image(self, word: str, open_browser: bool = True) -> dict:
        """
        英単語のイメージイラストを生成
        
        Args:
            word: 対象の英単語
            open_browser: 生成後にブラウザで開くか
            
        Returns:
            生成結果の辞書
        """
        try:
            print(f"\\n=== '{word}' のイメージイラスト生成を開始 ===")
            
            # 1. シーンデータを生成
            scene_data = self.scene_generator.generate_scene_data(word)
            self.scene_generator.display_scene_info(scene_data)
            
            # 2. イラストを生成
            image_path, cost_info = self.image_generator.generate_image(self.base_image_path, scene_data, quality="auto")
            self.image_generator.display_image_info(image_path)
            
            # 3. HTMLファイルを生成
            html_path = self.html_generator.generate_viewer_html(scene_data, image_path, cost_info, quality="auto")
            
            # 4. ブラウザで開く
            if open_browser:
                self.html_generator.open_html_file(html_path)
            
            # 5. 生成した単語を記録
            self.generated_words.append(word)
            
            result = {
                "word": word,
                "scene_data": scene_data,
                "image_path": image_path,
                "html_path": html_path,
                "cost_info": cost_info,
                "success": True
            }
            
            print(f"\\n=== '{word}' のイラスト生成完了 ===")
            return result
            
        except Exception as e:
            error_msg = f"'{word}' のイラスト生成中にエラーが発生しました: {str(e)}"
            print(f"\\nエラー: {error_msg}")
            print(f"詳細: {traceback.format_exc()}")
            
            return {
                "word": word,
                "error": error_msg,
                "success": False
            }
    
    def generate_multiple_words(self, words: list, open_browser: bool = True) -> list:
        """
        複数の英単語のイメージイラストを生成
        
        Args:
            words: 対象の英単語リスト
            open_browser: 生成後にブラウザで開くか
            
        Returns:
            生成結果のリスト
        """
        results = []
        
        for i, word in enumerate(words, 1):
            print(f"\\n{'='*50}")
            print(f"進捗: {i}/{len(words)} - '{word}'")
            print(f"{'='*50}")
            
            result = self.generate_word_image(word, open_browser=False)
            results.append(result)
            
            if not result["success"]:
                print(f"'{word}' の生成に失敗しました。次の単語に進みます...")
                continue
        
        # インデックスHTMLを生成
        if self.generated_words:
            try:
                index_path = self.html_generator.generate_index_html(self.generated_words)
                if open_browser:
                    self.html_generator.open_html_file(index_path)
            except Exception as e:
                print(f"インデックスHTML生成中にエラーが発生しました: {str(e)}")
        
        return results
    
    def print_summary(self, results: list):
        """生成結果のサマリーを表示"""
        total = len(results)
        successful = sum(1 for r in results if r["success"])
        failed = total - successful
        
        print(f"\\n{'='*50}")
        print("生成結果サマリー")
        print(f"{'='*50}")
        print(f"総数: {total}")
        print(f"成功: {successful}")
        print(f"失敗: {failed}")
        
        if failed > 0:
            print("\\n失敗した単語:")
            for result in results:
                if not result["success"]:
                    print(f"  - {result['word']}: {result['error']}")
        
        if successful > 0:
            print("\\n成功した単語:")
            for result in results:
                if result["success"]:
                    print(f"  - {result['word']}")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="Word Image Maker - 英単語イメージイラスト生成ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python main.py beg                    # 単語 'beg' のイラストを生成
  python main.py hello world           # 複数の単語を生成
  python main.py --words words.txt     # ファイルから単語を読み込み
  python main.py --no-browser beg      # ブラウザを開かずに生成
        """
    )
    
    parser.add_argument(
        "words",
        nargs="*",
        help="生成する英単語（複数指定可能）"
    )
    
    parser.add_argument(
        "--words-file",
        type=str,
        help="英単語リストファイル（1行1単語）"
    )
    
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="生成後にブラウザで開かない"
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        help="OpenAI API キー（環境変数 OPENAI_API_KEY でも設定可能）"
    )
    
    parser.add_argument(
        "--base-image",
        type=str,
        default="image/cat_and_mouse.jpeg",
        help="ベースキャラクター画像のパス"
    )
    
    args = parser.parse_args()
    
    # 単語リストを構築
    words = []
    
    if args.words:
        words.extend(args.words)
    
    if args.words_file:
        try:
            with open(args.words_file, 'r', encoding='utf-8') as f:
                file_words = [line.strip() for line in f if line.strip()]
                words.extend(file_words)
        except FileNotFoundError:
            print(f"エラー: ファイル '{args.words_file}' が見つかりません")
            sys.exit(1)
        except Exception as e:
            print(f"エラー: ファイル読み込み中にエラーが発生しました: {str(e)}")
            sys.exit(1)
    
    if not words:
        print("エラー: 生成する英単語が指定されていません")
        parser.print_help()
        sys.exit(1)
    
    # API キーを取得
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("エラー: OpenAI API キーが設定されていません")
        print("以下のいずれかの方法で API キーを設定してください:")
        print("1. 環境変数: export OPENAI_API_KEY=your_api_key")
        print("2. コマンドライン引数: --api-key your_api_key")
        print("3. OpenAI API キーの取得: https://platform.openai.com/api-keys")
        sys.exit(1)
    
    # ベース画像の存在確認
    if not os.path.exists(args.base_image):
        print(f"エラー: ベース画像 '{args.base_image}' が見つかりません")
        sys.exit(1)
    
    try:
        # Word Image Maker を初期化
        maker = WordImageMaker(api_key, args.base_image)
        
        # 生成実行
        if len(words) == 1:
            result = maker.generate_word_image(words[0], open_browser=not args.no_browser)
            results = [result]
        else:
            results = maker.generate_multiple_words(words, open_browser=not args.no_browser)
        
        # サマリーを表示
        maker.print_summary(results)
        
    except KeyboardInterrupt:
        print("\\n\\n処理が中断されました")
        sys.exit(1)
    except Exception as e:
        print(f"\\n予期しないエラーが発生しました: {str(e)}")
        print(f"詳細: {traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
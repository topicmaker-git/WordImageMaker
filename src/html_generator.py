import os
from typing import Dict, Any
from .cost_calculator import CostCalculator


class HTMLGenerator:
    def __init__(self, output_dir: str = "output"):
        """HTML生成器を初期化"""
        self.output_dir = output_dir
        self.cost_calculator = CostCalculator()
        
        # 出力ディレクトリが存在しない場合は作成
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_viewer_html(self, scene_data: Dict[str, Any], image_path: str, cost_info: Dict[str, Any] = None) -> str:
        """
        画像確認用のHTMLファイルを生成
        
        Args:
            scene_data: シーンデータ
            image_path: 生成された画像のパス
            cost_info: コスト情報（オプション）
            
        Returns:
            生成されたHTMLファイルのパス
        """
        word = scene_data["word"]
        html_filename = f"{word}_viewer.html"
        html_path = os.path.join(self.output_dir, html_filename)
        
        # 画像パスを相対パスに変換
        relative_image_path = os.path.relpath(image_path, self.output_dir)
        
        html_content = self._create_html_content(scene_data, relative_image_path, cost_info)
        
        try:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"HTML確認用ファイルを生成しました: {html_path}")
            return html_path
            
        except Exception as e:
            raise Exception(f"HTMLファイルの生成中にエラーが発生しました: {str(e)}")
    
    def _create_html_content(self, scene_data: Dict[str, Any], image_path: str, cost_info: Dict[str, Any] = None) -> str:
        """
        HTML内容を生成
        
        Args:
            scene_data: シーンデータ
            image_path: 画像の相対パス
            cost_info: コスト情報（オプション）
            
        Returns:
            HTML内容の文字列
        """
        html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Word Image Maker - {scene_data['word']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        
        .container {{
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin-bottom: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .word-title {{
            font-size: 3em;
            color: #2c3e50;
            margin: 0;
            font-weight: bold;
        }}
        
        .subtitle {{
            font-size: 1.2em;
            color: #7f8c8d;
            margin-top: 10px;
        }}
        
        .content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            align-items: start;
        }}
        
        .image-section {{
            text-align: center;
        }}
        
        .generated-image {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            border: 3px solid #3498db;
        }}
        
        .info-section {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }}
        
        .info-item {{
            margin-bottom: 20px;
        }}
        
        .info-label {{
            font-weight: bold;
            color: #2c3e50;
            font-size: 1.1em;
            margin-bottom: 8px;
            display: block;
        }}
        
        .info-content {{
            color: #34495e;
            line-height: 1.6;
            font-size: 1em;
        }}
        
        .scene-description {{
            background-color: #e8f5e8;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #27ae60;
        }}
        
        .core-image {{
            background-color: #fff3cd;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #ffc107;
        }}
        
        .prompt {{
            background-color: #e7f3ff;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #007bff;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        
        .cost-info {{
            background-color: #f0f8ff;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #20a5ff;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
        }}
        
        .cost-info pre {{
            margin: 0;
            white-space: pre-wrap;
            color: #1e3a8a;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #dee2e6;
            color: #6c757d;
        }}
        
        @media (max-width: 768px) {{
            .content {{
                grid-template-columns: 1fr;
            }}
            
            .word-title {{
                font-size: 2.5em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="word-title">{scene_data['word']}</h1>
            <p class="subtitle">英単語イメージイラスト</p>
        </div>
        
        <div class="content">
            <div class="image-section">
                <img src="{image_path}" alt="{scene_data['word']} illustration" class="generated-image">
                <p style="margin-top: 15px; color: #6c757d; font-style: italic;">
                    生成されたイラスト
                </p>
            </div>
            
            <div class="info-section">
                <div class="info-item">
                    <span class="info-label">🎬 シーンの内容</span>
                    <div class="info-content scene-description">
                        {scene_data['scene_description']}
                    </div>
                </div>
                
                <div class="info-item">
                    <span class="info-label">🎯 表すコアイメージ</span>
                    <div class="info-content core-image">
                        {scene_data['core_image']}
                    </div>
                </div>
                
                <div class="info-item">
                    <span class="info-label">🤖 生成プロンプト</span>
                    <div class="info-content prompt">
                        {scene_data['illustration_prompt']}
                    </div>
                </div>
                
                {self._generate_cost_section(cost_info)}
            </div>
        </div>
        
        <div class="footer">
            <p>Word Image Maker - 英単語学習支援ツール</p>
            <p>Generated on: {self._get_current_timestamp()}</p>
        </div>
    </div>
</body>
</html>"""
        
        return html_template
    
    def _generate_cost_section(self, cost_info: Dict[str, Any] = None) -> str:
        """
        コスト情報のHTMLセクションを生成
        
        Args:
            cost_info: コスト情報
            
        Returns:
            HTML文字列
        """
        if not cost_info:
            return ""
        
        cost_display = self.cost_calculator.format_cost_display(cost_info)
        
        return f"""
                <div class="info-item">
                    <span class="info-label">💰 生成コスト</span>
                    <div class="info-content cost-info">
                        <pre>{cost_display}</pre>
                    </div>
                </div>
        """
    
    def _get_current_timestamp(self) -> str:
        """現在の日時を文字列で取得"""
        from datetime import datetime
        return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    
    def open_html_file(self, html_path: str):
        """
        HTMLファイルをブラウザで開く
        
        Args:
            html_path: HTMLファイルのパス
        """
        try:
            import webbrowser
            file_url = f"file://{os.path.abspath(html_path)}"
            webbrowser.open(file_url)
            print(f"ブラウザでHTMLファイルを開きました: {file_url}")
        except Exception as e:
            print(f"HTMLファイルを開けませんでした: {str(e)}")
            print(f"手動で開いてください: file://{os.path.abspath(html_path)}")
    
    def generate_index_html(self, generated_words: list) -> str:
        """
        生成した全ての単語のインデックスHTMLを生成
        
        Args:
            generated_words: 生成した単語のリスト
            
        Returns:
            インデックスHTMLファイルのパス
        """
        html_path = os.path.join(self.output_dir, "index.html")
        
        word_links = ""
        for word in generated_words:
            word_links += f'<li><a href="{word}_viewer.html">{word}</a></li>\\n'
        
        html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Word Image Maker - 単語一覧</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        
        .container {{
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 30px;
        }}
        
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }}
        
        ul {{
            list-style-type: none;
            padding: 0;
        }}
        
        li {{
            margin-bottom: 10px;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 6px;
            border-left: 4px solid #3498db;
        }}
        
        a {{
            text-decoration: none;
            color: #2c3e50;
            font-weight: bold;
            font-size: 1.1em;
        }}
        
        a:hover {{
            color: #3498db;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Word Image Maker - 生成した単語一覧</h1>
        <ul>
            {word_links}
        </ul>
    </div>
</body>
</html>"""
        
        try:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"インデックスHTMLファイルを生成しました: {html_path}")
            return html_path
            
        except Exception as e:
            raise Exception(f"インデックスHTMLファイルの生成中にエラーが発生しました: {str(e)}")
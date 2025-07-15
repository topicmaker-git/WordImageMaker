#!/usr/bin/env python3
"""
Word Image Maker Ver.2 - Web Application
Flask-based web interface for generating word images
"""

import os
import json
import asyncio
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import glob

# Import Ver.1 core modules
from src.openai_client import OpenAIClient
from src.scene_generator import SceneGenerator
from src.image_generator import ImageGenerator
from src.html_generator import HTMLGenerator
from src.cost_calculator import CostCalculator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'word-image-maker-v2'
app.config['UPLOAD_FOLDER'] = 'image'
app.config['OUTPUT_FOLDER'] = 'output'

# Global variables for configuration
current_config = {
    'api_key': '',
    'character_image': 'cat_and_mouse.png',
    'character_description': '仲の良い猫とねずみ',
    'quality': 'auto'
}

@app.route('/')
def index():
    """Main page with input form"""
    # Get list of existing output HTML files
    output_files = get_output_files()
    return render_template('index.html', 
                         config=current_config,
                         output_files=output_files)

@app.route('/generate', methods=['POST'])
def generate_images():
    """Generate images for multiple words"""
    try:
        # Get form data
        api_key = request.form.get('api_key', '').strip()
        words_text = request.form.get('words', '').strip()
        quality = request.form.get('quality', 'auto')
        character_image = request.form.get('character_image', 'cat_and_mouse.png')
        character_description = request.form.get('character_description', '仲の良い猫とねずみ')
        
        if not api_key:
            return jsonify({'error': 'API Key is required'}), 400
        
        if not words_text:
            return jsonify({'error': 'Words are required'}), 400
        
        # Update global config
        current_config.update({
            'api_key': api_key,
            'character_image': character_image,
            'character_description': character_description,
            'quality': quality
        })
        
        # Parse words (handle # notation for disambiguation)
        words = parse_words(words_text)
        
        # Initialize components
        client = OpenAIClient(api_key)
        scene_generator = SceneGenerator(client)
        image_generator = ImageGenerator(client)
        html_generator = HTMLGenerator()
        cost_calculator = CostCalculator()
        
        # Generate images for each word
        results = []
        total_cost = 0.0
        
        for word_info in words:
            word = word_info['word']
            context = word_info.get('context', '')
            
            try:
                # Generate scene
                scene_data = scene_generator.generate_scene_data(
                    word, 
                    character_description,
                    context
                )
                
                # Generate image
                image_path, cost_info = image_generator.generate_image(
                    f"image/{character_image}",
                    scene_data,
                    quality
                )
                
                # Generate HTML viewer
                html_path = html_generator.generate_viewer_html(
                    scene_data, 
                    image_path,
                    cost_info,
                    quality
                )
                
                # Calculate cost (already calculated in image generation)
                word_cost = cost_info.get('total_cost', 0.0)
                total_cost += word_cost
                
                results.append({
                    'word': word,
                    'context': context,
                    'status': 'success',
                    'image_path': image_path,
                    'html_path': html_path,
                    'html_filename': os.path.basename(html_path),
                    'cost': word_cost
                })
                
            except Exception as e:
                results.append({
                    'word': word,
                    'context': context,
                    'status': 'error',
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'results': results,
            'total_cost': total_cost,
            'output_files': get_output_files()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/outputs')
def list_outputs():
    """Get list of output files"""
    return jsonify({'output_files': get_output_files()})

@app.route('/view/<filename>')
def view_output(filename):
    """Serve output HTML files"""
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return "File not found", 404

@app.route('/view/images/<filename>')
def view_image(filename):
    """Serve generated images"""
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'images', secure_filename(filename))
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return "Image not found", 404

def parse_words(words_text):
    """Parse words from text input, handling # notation for context"""
    words = []
    for line in words_text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        
        if '#' in line:
            word, context = line.split('#', 1)
            words.append({
                'word': word.strip(),
                'context': context.strip()
            })
        else:
            words.append({
                'word': line.strip(),
                'context': ''
            })
    
    return words

def get_output_files():
    """Get list of output HTML files with metadata"""
    output_files = []
    pattern = os.path.join(app.config['OUTPUT_FOLDER'], '*_viewer.html')
    
    for file_path in glob.glob(pattern):
        filename = os.path.basename(file_path)
        word = filename.replace('_viewer.html', '')
        mtime = os.path.getmtime(file_path)
        
        output_files.append({
            'filename': filename,
            'word': word,
            'modified': datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'url': url_for('view_output', filename=filename)
        })
    
    # Sort by modification time (newest first)
    output_files.sort(key=lambda x: x['modified'], reverse=True)
    return output_files

if __name__ == '__main__':
    # Ensure output directories exist
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['OUTPUT_FOLDER'], 'images'), exist_ok=True)
    
    print("🚀 Word Image Maker Ver.2 - Web Application")
    print("📡 Starting server at http://localhost:5000")
    print("🎨 Ready to generate word images!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
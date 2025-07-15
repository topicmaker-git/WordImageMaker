// Word Image Maker Ver.2 - JavaScript Functions

document.addEventListener('DOMContentLoaded', function() {
    const generateForm = document.getElementById('generateForm');
    const generateBtn = document.getElementById('generateBtn');
    const progressArea = document.getElementById('progressArea');
    const resultsArea = document.getElementById('resultsArea');
    const errorArea = document.getElementById('errorArea');
    
    // Load saved API key from localStorage
    loadSavedApiKey();
    
    generateForm.addEventListener('submit', function(e) {
        e.preventDefault();
        generateImages();
    });
    
    // Save API key when it changes
    document.getElementById('apiKey').addEventListener('input', function() {
        saveApiKey();
    });
});

async function generateImages() {
    const generateBtn = document.getElementById('generateBtn');
    const progressArea = document.getElementById('progressArea');
    const resultsArea = document.getElementById('resultsArea');
    const errorArea = document.getElementById('errorArea');
    
    // Reset UI
    hideAllAreas();
    showProgressArea();
    
    // Disable form
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<div class="loading"></div> 生成中...';
    
    // Get form data
    const formData = new FormData(document.getElementById('generateForm'));
    const words = formData.get('words').trim().split('\n').filter(w => w.trim());
    
    try {
        updateProgress(0, '準備中...');
        
        // Submit to server
        const response = await fetch('/generate', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResults(data);
            refreshOutputs();
        } else {
            showError(data.error || '生成に失敗しました');
        }
        
    } catch (error) {
        showError('エラーが発生しました: ' + error.message);
    } finally {
        // Re-enable form
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-magic"></i> イラスト生成開始';
    }
}

function hideAllAreas() {
    document.getElementById('progressArea').classList.add('d-none');
    document.getElementById('resultsArea').classList.add('d-none');
    document.getElementById('errorArea').classList.add('d-none');
}

function showProgressArea() {
    document.getElementById('progressArea').classList.remove('d-none');
}

function updateProgress(percent, text) {
    const progressBar = document.querySelector('.progress-bar');
    const progressText = document.getElementById('progressText');
    
    progressBar.style.width = percent + '%';
    progressText.textContent = text;
}

function showResults(data) {
    hideAllAreas();
    
    const resultsArea = document.getElementById('resultsArea');
    const resultsContent = document.getElementById('resultsContent');
    
    let html = `
        <div class="cost-display">
            <i class="fas fa-dollar-sign"></i> 総コスト: $${data.total_cost.toFixed(4)}
        </div>
        <div class="mt-3">
    `;
    
    data.results.forEach(result => {
        if (result.status === 'success') {
            html += `
                <div class="result-card success card mb-2">
                    <div class="card-body">
                        <h5 class="card-title">
                            <i class="fas fa-check-circle text-success"></i> ${result.word}
                        </h5>
                        ${result.context ? `<p class="card-text"><small class="text-muted">補足: ${result.context}</small></p>` : ''}
                        <p class="card-text">
                            コスト: $${result.cost.toFixed(4)}
                        </p>
                        <a href="/view/${result.html_filename}" target="_blank" class="btn btn-outline-primary btn-sm">
                            <i class="fas fa-eye"></i> 表示
                        </a>
                    </div>
                </div>
            `;
        } else {
            html += `
                <div class="result-card error card mb-2">
                    <div class="card-body">
                        <h5 class="card-title">
                            <i class="fas fa-exclamation-circle text-danger"></i> ${result.word}
                        </h5>
                        ${result.context ? `<p class="card-text"><small class="text-muted">補足: ${result.context}</small></p>` : ''}
                        <p class="card-text text-danger">
                            エラー: ${result.error}
                        </p>
                    </div>
                </div>
            `;
        }
    });
    
    html += '</div>';
    
    resultsContent.innerHTML = html;
    resultsArea.classList.remove('d-none');
}

function showError(message) {
    hideAllAreas();
    
    const errorArea = document.getElementById('errorArea');
    const errorContent = document.getElementById('errorContent');
    
    errorContent.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i> ${message}
    `;
    
    errorArea.classList.remove('d-none');
}

async function refreshOutputs() {
    try {
        const response = await fetch('/outputs');
        const data = await response.json();
        
        const outputsList = document.getElementById('outputsList');
        
        if (data.output_files && data.output_files.length > 0) {
            let html = '<ul class="list-group">';
            
            data.output_files.forEach(file => {
                html += `
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <strong>${file.word}</strong>
                            <small class="text-muted d-block">${file.modified}</small>
                        </div>
                        <a href="${file.url}" target="_blank" class="btn btn-outline-primary btn-sm">
                            <i class="fas fa-eye"></i> 表示
                        </a>
                    </li>
                `;
            });
            
            html += '</ul>';
            outputsList.innerHTML = html;
        } else {
            outputsList.innerHTML = '<p class="text-muted">まだ生成されたファイルがありません</p>';
        }
        
    } catch (error) {
        console.error('Failed to refresh outputs:', error);
    }
}

// Auto-refresh outputs every 30 seconds
setInterval(refreshOutputs, 30000);

// Toggle API key visibility
function toggleApiKeyVisibility() {
    const apiKeyInput = document.getElementById('apiKey');
    const toggleIcon = document.getElementById('apiKeyToggleIcon');
    
    if (apiKeyInput.type === 'password') {
        apiKeyInput.type = 'text';
        toggleIcon.className = 'fas fa-eye-slash';
    } else {
        apiKeyInput.type = 'password';
        toggleIcon.className = 'fas fa-eye';
    }
}

// Form validation
document.getElementById('generateForm').addEventListener('input', function() {
    const apiKey = document.getElementById('apiKey').value.trim();
    const words = document.getElementById('words').value.trim();
    const generateBtn = document.getElementById('generateBtn');
    
    if (apiKey && words) {
        generateBtn.disabled = false;
        generateBtn.classList.remove('btn-secondary');
        generateBtn.classList.add('btn-primary');
    } else {
        generateBtn.disabled = true;
        generateBtn.classList.remove('btn-primary');
        generateBtn.classList.add('btn-secondary');
    }
});

// API Key management functions
function saveApiKey() {
    const apiKey = document.getElementById('apiKey').value.trim();
    if (apiKey) {
        localStorage.setItem('wordImageMaker_apiKey', apiKey);
        console.log('API Key saved to localStorage');
    }
}

function loadSavedApiKey() {
    const savedApiKey = localStorage.getItem('wordImageMaker_apiKey');
    if (savedApiKey) {
        document.getElementById('apiKey').value = savedApiKey;
        console.log('API Key loaded from localStorage');
    }
}

function clearApiKey() {
    localStorage.removeItem('wordImageMaker_apiKey');
    document.getElementById('apiKey').value = '';
    console.log('API Key cleared from localStorage');
}

function showApiKeyManager() {
    const currentKey = localStorage.getItem('wordImageMaker_apiKey') || '';
    const maskedKey = currentKey ? currentKey.substring(0, 10) + '...' : 'なし';
    
    const newKey = prompt(
        `現在のAPI Key: ${maskedKey}\n\n新しいAPI Keyを入力してください（キャンセルで変更なし）:`,
        ''
    );
    
    if (newKey !== null && newKey.trim() !== '') {
        document.getElementById('apiKey').value = newKey.trim();
        saveApiKey();
        alert('API Keyが更新されました');
    }
}

// Initialize form validation
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('generateForm').dispatchEvent(new Event('input'));
});
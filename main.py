# from data_collectors.wb_collector import get_wb_product_data
# from data_collectors.ozon_collector import get_ozon_product_data
# from data_collectors.sber_collector import get_sber_product_data
# from data_collectors.yandex_collector import get_yandex_product_data
# from llm_analyzer import analyze_product_data
# import config

from flask import Flask, request, render_template_string
import os
import base64

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# HTML template with inline CSS and JS for beauty and accessibility
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛒 Помощник по покупкам</title>
    <style>
        :root {
            --bg-color: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --container-bg: white;
            --text-color: #333;
            --accent-color: #2E86AB;
            --button-bg: linear-gradient(45deg, #4CAF50, #45a049);
            --card-bg: #f9f9f9;
            --error-bg: #ffebee;
            --success-bg: #e8f5e8;
        }
        [data-theme="dark"] {
            --bg-color: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            --container-bg: #2c3e50;
            --text-color: #ecf0f1;
            --accent-color: #3498db;
            --button-bg: linear-gradient(45deg, #27ae60, #2ecc71);
            --card-bg: #34495e;
            --error-bg: #e74c3c;
            --success-bg: #27ae60;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-color);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            color: var(--text-color);
            transition: background 0.3s, color 0.3s;
        }
        .skip-link {
            position: absolute;
            top: -40px;
            left: 6px;
            background: #000;
            color: #fff;
            padding: 8px;
            text-decoration: none;
            z-index: 100;
        }
        .skip-link:focus {
            top: 6px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: var(--container-bg);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: background 0.3s;
        }
        h1 {
            color: var(--accent-color);
            text-align: center;
            margin-bottom: 30px;
        }
        .theme-toggle {
            position: absolute;
            top: 20px;
            right: 20px;
            background: var(--button-bg);
            color: white;
            border: none;
            padding: 10px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: var(--text-color);
        }
        textarea, input[type="text"], input[type="file"] {
            width: 100%;
            padding: 10px;
            border: 2px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
            background: var(--container-bg);
            color: var(--text-color);
        }
        textarea:focus, input:focus {
            outline: none;
            border-color: var(--accent-color);
        }
        button {
            background: var(--button-bg);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px 5px;
            transition: background 0.3s;
        }
        button:hover {
            opacity: 0.9;
        }
        .record-btn {
            background: linear-gradient(45deg, #e74c3c, #c0392b);
        }
        .results {
            margin-top: 30px;
            padding: 20px;
            background: var(--success-bg);
            border-radius: 10px;
            border-left: 5px solid #4CAF50;
        }
        .error {
            background: var(--error-bg);
            border-left-color: #f44336;
            color: white;
        }
        .product-card {
            display: inline-block;
            width: 30%;
            margin: 1%;
            background: var(--card-bg);
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            vertical-align: top;
            transition: background 0.3s;
        }
        .product-card img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 5px;
        }
        .product-card h3 {
            margin: 10px 0;
            color: var(--text-color);
        }
        .product-card p {
            margin: 5px 0;
            color: var(--text-color);
        }
        .price {
            font-weight: bold;
            color: #4CAF50;
        }
        .source {
            font-style: italic;
            color: #666;
        }
        .reason {
            font-size: 14px;
            color: var(--text-color);
            margin-top: 10px;
        }
        .buy-btn {
            background: #2196F3;
            width: 100%;
            margin-top: 10px;
        }
        .buy-btn:hover {
            background: #1976D2;
        }
        @media (max-width: 768px) {
            .product-card {
                width: 100%;
                margin: 10px 0;
            }
        }
        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }
    </style>
</head>
<body>
    <a href="#results" class="skip-link">Перейти к результатам</a>
    <button class="theme-toggle" id="themeToggle" aria-label="Переключить тему">🌙</button>
    <div class="container">
        <h1>🛒 Помощник по покупкам</h1>
        <p>Опишите товар, прикрепите фото или запишите голос, и получите предложения с маркетплейсов!</p>
        
        <form method="POST" enctype="multipart/form-data" role="search">
            <fieldset>
                <legend class="sr-only">Форма поиска товаров</legend>
                <div class="form-group">
                    <label for="query">Свободный запрос (описание товара):</label>
                    <textarea id="query" name="query" rows="4" placeholder="Например: красный смартфон Samsung с хорошей камерой" required aria-describedby="query-help"></textarea>
                    <span id="query-help" class="sr-only">Введите описание товара для поиска предложений</span>
                </div>
                
                <div class="form-group">
                    <label for="photo">Прикрепить фото товара:</label>
                    <input type="file" id="photo" name="photo" accept="image/*" aria-describedby="photo-help">
                    <span id="photo-help" class="sr-only">Загрузите изображение товара для уточнения поиска</span>
                </div>
                
                <div class="form-group">
                    <label for="audio">Запись голоса:</label>
                    <button type="button" id="recordBtn" class="record-btn" aria-label="Начать запись голоса">🎤 Начать запись</button>
                    <button type="button" id="stopBtn" class="record-btn" style="display:none;" aria-label="Остановить запись голоса">⏹ Остановить запись</button>
                    <audio id="audioPlayback" controls style="display:none; margin-top:10px;" aria-label="Прослушать записанный голос"></audio>
                    <input type="hidden" name="audio_data" id="audioData">
                    <span class="sr-only" id="audio-help">Запишите голосовое описание товара</span>
                </div>
                
                <button type="submit" aria-describedby="submit-help">🔍 Найти товары</button>
                <span id="submit-help" class="sr-only">Отправить запрос для поиска товаров</span>
            </fieldset>
        </form>
        
        <div id="results" aria-live="polite" aria-atomic="true">
            {% if products %}
            <section class="results" aria-labelledby="results-heading">
                <h2 id="results-heading">📦 Найденные товары</h2>
                {% for product in products %}
                <article class="product-card" role="article">
                    <header>
                        <img src="{{ product.image }}" alt="Изображение товара {{ product.name }}">
                        <h3>{{ product.name }}</h3>
                    </header>
                    <p class="price">{{ product.price }} руб.</p>
                    <p class="source">Источник: {{ product.source }}</p>
                    <p class="reason">{{ product.reason }}</p>
                    <button class="buy-btn" aria-label="Купить {{ product.name }}">Купить</button>
                </article>
                {% endfor %}
            </section>
            {% endif %}
            
            {% if error %}
            <div class="results error" role="alert" aria-live="assertive">
                <p>{{ error }}</p>
            </div>
            {% endif %}
        </div>
    </div>

    <script>
        // Theme toggle with localStorage
        const themeToggle = document.getElementById('themeToggle');
        const body = document.body;

        // Load theme from localStorage
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            body.setAttribute('data-theme', 'dark');
            themeToggle.textContent = '☀️';
            themeToggle.setAttribute('aria-label', 'Переключить на светлую тему');
        } else {
            themeToggle.textContent = '🌙';
            themeToggle.setAttribute('aria-label', 'Переключить на тёмную тему');
        }

        themeToggle.addEventListener('click', () => {
            const currentTheme = body.getAttribute('data-theme');
            if (currentTheme === 'dark') {
                body.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                themeToggle.textContent = '🌙';
                themeToggle.setAttribute('aria-label', 'Переключить на тёмную тему');
            } else {
                body.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                themeToggle.textContent = '☀️';
                themeToggle.setAttribute('aria-label', 'Переключить на светлую тему');
            }
        });

        // Audio recording
        let mediaRecorder;
        let audioChunks = [];
        let isRecording = false;

        document.getElementById('recordBtn').addEventListener('click', async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    document.getElementById('audioPlayback').src = audioUrl;
                    document.getElementById('audioPlayback').style.display = 'block';
                    
                    // Convert to base64 for sending
                    const reader = new FileReader();
                    reader.onload = () => {
                        document.getElementById('audioData').value = reader.result;
                    };
                    reader.readAsDataURL(audioBlob);
                };

                mediaRecorder.start();
                isRecording = true;
                document.getElementById('recordBtn').style.display = 'none';
                document.getElementById('stopBtn').style.display = 'inline-block';
            } catch (error) {
                alert('Ошибка доступа к микрофону: ' + error.message);
            }
        });

        document.getElementById('stopBtn').addEventListener('click', () => {
            if (mediaRecorder && isRecording) {
                mediaRecorder.stop();
                isRecording = false;
                document.getElementById('recordBtn').style.display = 'inline-block';
                document.getElementById('stopBtn').style.display = 'none';
            }
        });
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query')
        photo = request.files.get('photo')
        audio_data = request.form.get('audio_data')
        
        if not query:
            return render_template_string(HTML_TEMPLATE, error="Пожалуйста, введите запрос.")
        
        # Save files if provided
        photo_path = None
        if photo and photo.filename:
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
            photo.save(photo_path)
        
        audio_path = None
        if audio_data:
            # Save audio (base64 to file)
            audio_data = audio_data.split(',')[1]  # Remove data:audio/wav;base64,
            audio_bytes = base64.b64decode(audio_data)
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'voice.wav')
            with open(audio_path, 'wb') as f:
                f.write(audio_bytes)
        
        # Simulate product search based on query
        products = generate_mock_products(query)
        
        return render_template_string(HTML_TEMPLATE, products=products, query=query)
    
    return render_template_string(HTML_TEMPLATE)

def generate_mock_products(query):
    # Mock products based on query keywords
    base_products = [
        {
            'name': f'{query} - Модель 1',
            'price': '15000',
            'source': 'Wildberries',
            'image': 'https://via.placeholder.com/200x150?text=Product+1',
            'reason': 'Этот товар выбран из-за оптимального соотношения цены и качества, а также высокой оценки пользователей.'
        },
        {
            'name': f'{query} - Модель 2',
            'price': '18000',
            'source': 'Ozon',
            'image': 'https://via.placeholder.com/200x150?text=Product+2',
            'reason': 'Рекомендуется за наличие дополнительных аксессуаров в комплекте и быструю доставку.'
        },
        {
            'name': f'{query} - Модель 3',
            'price': '12000',
            'source': 'СберМегаМаркет',
            'image': 'https://via.placeholder.com/200x150?text=Product+3',
            'reason': 'Самый бюджетный вариант с хорошими отзывами и гарантией производителя.'
        },
        {
            'name': f'{query} - Модель 4',
            'price': '20000',
            'source': 'Яндекс Маркет',
            'image': 'https://via.placeholder.com/200x150?text=Product+4',
            'reason': 'Премиум-вариант с расширенной гарантией и эксклюзивными функциями.'
        }
    ]
    return base_products[:4]  # Return up to 4 products

if __name__ == '__main__':
    app.run(debug=True)
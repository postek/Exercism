from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Konfiguracja API (ustaw klucz jako zmienną środowiskową)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_story():
    data = request.json
    
    prompt = f"""Napisz krótkie opowiadanie w 5 rozdziałach po polsku.

Parametry:
- Gatunek: {data.get('genre', 'fantasy')}
- Główny bohater: {data.get('protagonist', 'młody podróżnik')}
- Miejsce akcji: {data.get('setting', 'średniowieczne królestwo')}
- Nastrój: {data.get('mood', 'przygodowy')}
- Motyw przewodni: {data.get('theme', 'przyjaźń')}

Każdy rozdział powinien mieć tytuł i 2-3 akapity. 
Formatuj używając ## dla tytułów rozdziałów."""

    try:
        response = model.generate_content(prompt)
        return jsonify({'story': response.text, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

if __name__ == '__main__':
    app.run(debug=True)

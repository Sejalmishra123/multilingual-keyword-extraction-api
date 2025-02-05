# Import required libraries
import stanza  # For NLP
from collections import Counter  # For counting keyword frequency
from flask import Flask, request, jsonify  # For Flask web API
from flask_ngrok import run_with_ngrok  # To run Flask with ngrok
import langid  # For language identification
import requests  # For making HTTP requests

# Download language models for English and Hindi
stanza.download('en')  # English model
stanza.download('hi')  # Hindi model

# Load Stanza pipelines for English and Hindi
nlp_en = stanza.Pipeline('en', processors='tokenize,pos')
nlp_hi = stanza.Pipeline('hi', processors='tokenize,pos')

# Initialize Flask app
app = Flask(__name__)
run_with_ngrok(app)

# Variable to store ngrok URL
ngrok_url = ""

# Route to get ngrok URL
@app.route('/get_ngrok_url', methods=['GET'])
def get_ngrok_url():
    return jsonify({'ngrok_url': ngrok_url})

# Function to extract top N keywords from the paragraph
def get_top_keywords(paragraph, top_n=10):
    lang, _ = langid.classify(paragraph)

    if lang == 'en':
        doc = nlp_en(paragraph)
    elif lang == 'hi':
        doc = nlp_hi(paragraph)
    else:
        # Default to English for other languages
        doc = nlp_en(paragraph)

    # Extracting keywords (nouns and adjectives)
    keywords = [word.text for sent in doc.sentences for word in sent.words if word.upos in ['NOUN', 'ADJ']]

    # Counting keyword frequencies
    keyword_counts = Counter(keywords)

    # Getting top N keywords
    top_keywords = [keyword for keyword, count in keyword_counts.most_common(top_n)]

    return top_keywords

# API endpoint to extract top keywords
@app.route('/get_top_keywords', methods=['POST'])
def get_top_keywords_api():
    global ngrok_url

    # Extract the paragraph from the incoming request
    data = request.get_json()
    paragraph = data.get('paragraph', '')

    # Get ngrok URL if not already obtained
    if not ngrok_url:
        ngrok_url_api = "http://localhost:4040/api/tunnels"
        ngrok_response = requests.get(ngrok_url_api)
        ngrok_data = ngrok_response.json()
        ngrok_url = ngrok_data['tunnels'][0]['public_url']

    # Extract top keywords from the paragraph
    top_keywords = get_top_keywords(paragraph, top_n=20)

    # Return the result as a JSON response
    return jsonify({'top_keywords': top_keywords})

if __name__ == '__main__':
    app.run()

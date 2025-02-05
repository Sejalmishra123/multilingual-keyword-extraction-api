# Multilingual Keyword Extraction API using Stanza and Flask

This project is a **Natural Language Processing (NLP) API** for extracting **top keywords** from paragraphs in multiple languages (English and Hindi) using **Flask** and **Stanza**.

## Features

- Extracts top keywords (nouns and adjectives) from text in **English** and **Hindi**.
- Automatically detects the language of the input text using **langid**.
- Provides a RESTful API to receive text input and return the top keywords.

## Requirements

To run this project, you need to install the following Python libraries:

- **Flask** - For building the web API.
- **Flask-Ngrok** - For running Flask with Ngrok for public URL exposure.
- **Stanza** - For NLP processing and keyword extraction.
- **Langid** - For language detection.
- **Requests** - For making HTTP requests.

You can install these dependencies by running:

```bash
pip install -r requirements.txt

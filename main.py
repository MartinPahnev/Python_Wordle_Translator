"""
This module contains the main application logic for the Flask web app.
It integrates Wordle game and translation functionalities.
"""

import os
from googletrans import Translator
from flask import Flask, render_template, request, session

from src.wordle_game import wordle_game, reset_wordle, clear_session
from src.translation import translate_file, translate_text

app = Flask(__name__)
app.secret_key = os.urandom(24)

translator = Translator()

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    """Handle translation of text."""
    return translate_text(request, translator)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle file upload and translation."""
    return translate_file(request, translator)

@app.route('/wordle', methods=['GET', 'POST'])
def wordle_game_caller():
    """Handle Wordle game logic."""
    return wordle_game(request, session)

@app.route('/reset_wordle')
def reset():
    """Reset the Wordle game state."""
    return reset_wordle(session)

@app.route('/clear_session')
def clear():
    """Clear the session data."""
    return clear_session(session)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=4242, debug=True)

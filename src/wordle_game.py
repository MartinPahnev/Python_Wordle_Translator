"""
This module contains the Wordle game logic. It provides functionality to play 
the Wordle game through a Flask-based web interface.
"""

import random
import requests
from flask import render_template, request, redirect, url_for

def get_word_list():
    """Retrieve a list of words for the Wordle game."""
    url = 'https://api.datamuse.com/words'
    params = {'sp': '?????', 'max': 1000}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        words = [word['word'] for word in response.json()]
        return words
    else:
        return []

def is_valid_word(word):
    """Check if the word is a valid word."""
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    response = requests.get(url)
    return response.status_code == 200

def wordle_game(request, session):
    """Play the Wordle game."""
    
    max_attempts = 6  

    if 'target_word' not in session:
        word_list = get_word_list()
        session['target_word'] = random.choice(word_list) if word_list else ""
        session['attempts'] = []

    target_word = session.get('target_word')
    attempts = session.get('attempts', [])
    message = ""

    if len(attempts) == max_attempts - 1:
        if request.method == 'POST':
            guess = request.form.get('guess', '').lower().strip()
            if len(guess) != len(target_word):
                message = f"Думата трябва да бъде с {len(target_word)} букви."
            elif not is_valid_word(guess):
                return render_template('wordle.html', attempts=attempts, message=message,
                                        error="Невалидна дума!", word_length=len(target_word))

            feedback = ["absent"] * len(target_word)
            target_word_list = list(target_word)

            for i in range(len(guess)):
                if guess[i] == target_word[i]:
                    feedback[i] = "correct"
                    target_word_list[i] = None  

            for i in range(len(guess)):
                if feedback[i] == "correct":
                    continue
                if guess[i] in target_word_list:
                    feedback[i] = "present"
                    target_word_list[target_word_list.index(guess[i])] = None  

            attempts.append({"guess": guess, "feedback": feedback})
            session['attempts'] = attempts

            if guess == target_word:
                message = "Поздравления! Познахте думата!"
            else:
                message = f"Играта е приключила. Правилната дума беше {target_word}."

            return render_template('wordle.html', attempts=attempts, message=message, word_length=len(target_word))

    if request.method == 'POST' and len(attempts) < max_attempts - 1:
        guess = request.form.get('guess', '').lower().strip()
        if len(guess) != len(target_word):
            message = f"Думата трябва да бъде с {len(target_word)} букви."
        elif not is_valid_word(guess):
            return render_template('wordle.html', attempts=attempts, message=message, error="Невалидна дума!", word_length=len(target_word))

        feedback = ["absent"] * len(target_word)
        target_word_list = list(target_word)

        for i in range(len(guess)):
            if guess[i] == target_word[i]:
                feedback[i] = "correct"
                target_word_list[i] = None  

        for i in range(len(guess)):
            if feedback[i] == "correct":
                continue
            if guess[i] in target_word_list:
                feedback[i] = "present"
                target_word_list[target_word_list.index(guess[i])] = None  

        attempts.append({"guess": guess, "feedback": feedback})
        session['attempts'] = attempts

    return render_template('wordle.html', attempts=attempts, message=message, word_length=len(target_word))

def reset_wordle(session):
    """Reset the Wordle game state."""
    session.pop('target_word', None)
    session.pop('attempts', None)
    return redirect(url_for('wordle_game_caller'))

def clear_session(session):
    """Clear session data."""
    session.clear()
    return "Session cleared."

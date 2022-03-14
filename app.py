from boggle import Boggle
from flask import Flask, jsonify, request, render_template, redirect, session, flash
# from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secretsecret'
# debug = DebugToolbarExtension(app)
CORS(app)

boggle_game = Boggle()

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/new-game')
def show_board():
    board = boggle_game.make_board()
    session['board'] = board
    session['game_count'] = session.get('game_count', 0) + 1
    session['high_score'] = session.get('high_score', 0)
    return render_template('board.html', board=board)

@app.route('/guess')
def handle_guess():
    board = session['board']
    guess = request.args['guess'].lower()
    response = boggle_game.check_valid_word(board, guess)
    return jsonify({"result": response, 'wordLength': len(guess)})

@app.route('/score', methods=['POST'])
def set_scores():
    new_score = request.args['newScore']
    if int(new_score) > int(session['high_score']):
        session['high_score'] = new_score
    return redirect('/score-page')

@app.route('/score-page')
def show_scores():
    high_score = session['high_score']
    game_count = session['game_count']
    return render_template('scores.html', high_score=high_score, game_count=game_count)
    

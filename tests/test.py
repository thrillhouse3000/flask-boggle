from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True

boggle = Boggle()

class FlaskTests(TestCase):
   
    def test_home(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Welcome to Boggle!</h1>', html)

    def test_new_game(self):
        with app.test_client() as client:
            res = client.get('/new-game')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<li class="text-decoration-underline">Instructions:</li>', html)
            self.assertIsInstance(session['board'], list)
            self.assertEqual(session['game_count'], 1)
            self.assertEqual(session['high_score'], 0)
    
    def test_guess(self):
        board = boggle.make_board()
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['board'] = board
            res = client.get('/guess?guess=asdasdasd')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json['result'], 'not-word')

    def test_scores(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['high_score'] = 5
            res = client.post('/score?newScore=10')
            self.assertEqual(res.status_code, 302)

    def test_score_page(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['high_score'] = 5
                session['game_count'] = 2
            res = client.get('/score-page')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("<p>You've played 2 games!</p>", html)
            




#     # TODO -- write tests for every view function / feature!


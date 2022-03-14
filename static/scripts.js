let $guessInput = $('#guess')
let $guessSubmitBtn = $('#guessSubmit')
let $boardSection = $('#board')
let $messageSection = $('#message')
let $scoreSection = $('#score')
let $timer = $('#time')
let $endSection = $('#end') 

class Game {
    constructor() {
        this.score = 0;
        this.timeLimit = 60;
        this.guessed = [];
    }

    timer() {
        $timer.text(this.timeLimit)
        let timeInterval = setInterval(() => {
            if (this.timeLimit > 0) {
                this.timeLimit -= 1;
                $timer.text(this.timeLimit)
            } else {
                $guessSubmitBtn.attr('disabled', 'disabled')
                $messageSection.text(`Time's Up!`)
                clearInterval(timeInterval)
                this.sendScore()
                $endSection.html("<a href='/score-page' class='btn btn-info'>See Your Stats</a> <a href='/new-game' class='btn btn-success'>Play Again?</a>")
            }
        }, 1000) 
    }

    async checkGuess() {
        let $guess = $guessInput.val().toUpperCase()
        let response = await axios({
            url: '/guess',
            method: 'GET',
            params: {guess: $guess}
        });
        
        if (response.data.result === "not-word") {
            $messageSection.text(`That's not a word`)
        } else if (this.guessed.indexOf($guess) !== -1) {
            $messageSection.text(`You've already guessed that`)
        } else if (response.data.result === "ok") {
            $messageSection.text('Nice!');
            this.score += response.data.wordLength
            $scoreSection.text(`Current Score: ${this.score}`)
        } else if (response.data.result === "not-on-board") {
            $messageSection.text(`That's not on the board`)
        }
        this.guessed.push($guess)
    }

    async sendScore() {
        await axios({
            url: '/score',
            method: 'POST',
            params: {newScore: this.score}
        });
    }
}

let myGame = new Game()

window.onload = myGame.timer()

$guessSubmitBtn.on('click', function guessHandler(evt) {
    evt.preventDefault()
    myGame.checkGuess()
    $guessInput.val('')
})



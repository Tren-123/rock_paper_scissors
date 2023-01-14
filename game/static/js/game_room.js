const gameStatus = JSON.parse(document.getElementById('game-status').textContent); // true of false status is game end (true == game end) - upload from db
const plgrg = document.querySelector('.playground') // div class playground
const weapons = document.querySelector('.weapons') // div for weapons buttons inside playground
const choosingText = document.querySelector('#choosing-text') // para for insertion of text with choosing offer
const owner = document.querySelector('#owner-field') // div with owner field (childs owner-name, owner-weapon)
const opponent = document.querySelector('#opponent-field') // div with opponent field (childs opponent-name, opponent-weapon)
const winner = document.querySelector('#winner') // string with winer results
const endGameString = document.querySelector('#end-game-str') // string with end game frase - appears in the end of the game
const wpnDict = { // dictionary with {1st letter of weapon : full name of weapon}
    r : 'Rock',
    p : 'Paper',
    s : 'Scissors'
}
let rockButton = document.querySelector('#rock') // var for Rock button
let paperButton = document.querySelector('#paper') // var for Paper button
let scissorsButton = document.querySelector('#scissors') // var for Scissors button
let resetButton // var for button to reset game after check results
let reultOfGame // var for store result of the game and send it to sever after

if (gameStatus != true){
let socket = new WebSocket('ws://' + window.location.host + '/ws' + window.location.pathname) // var for WebSocket object 
console.log('ws://' + window.location.host + '/ws' + window.location.pathname)

for (weapon of weapons.childNodes) { // listen for weapon buttons click event
    weapon.addEventListener('click', function() { // send message to server if event happend
        socket.send(JSON.stringify({
            'message':  'weapon_choose',
            'weapon':  this.innerText
        }));
        console.log(`weapon of this user ${this.innerText}`)
        
    })
}

socket.onmessage = function(e){ // listen messages from server
    const data = JSON.parse(e.data);
        console.log(data);
        switch (data.type) {
            case "send_result": // if message with result set customer view based on results
                owner.childNodes[2].innerText = wpnDict[data.owner_weapon];
                opponent.childNodes[2].innerText = wpnDict[data.opponent_weapon];
                if (data.winner != false ){
                winner.innerText = 'Winner ' + data.winner
                endGame(socket)
            }
                else{
                    winner.innerText = 'Draw'
                }
                break;
            default:
                console.error("Unknown message type!");
                break;
        }
    }
}

function endGame(socket){ // if winner determinated freeze buttons, show endGameString and close websocket connection
for (weapon of weapons.childNodes) {
    weapon.disabled = true
    endGameString.innerText = 'GAME IS END. PLEASE START NEW GAME'
    socket.close()
}
}
const plgrg = document.querySelector('.playground') // div class playground
const weapons = document.querySelector('.weapons') // div for weapons buttons inside playground
const choosingText = document.querySelector('#choosing-text') // para for insertion of text with choosing offer
const startGamePara = document.querySelector('#start-game-para')
const userWeapon = document.querySelector('#user-weapon') // string with user weapon 
const opponentWeapon = document.querySelector('#opponent-weapon') // string with opponent weapon 
const winner = document.querySelector('#winner') // string with winer results
const wpnDict = { // dictionary with {myWeapon : [win if opp have this weapon, lose if opp have this weapon, draw if opp have this weapon]}
    rock : ['scissors', 'paper', 'rock'],
    paper : ['rock', 'scissors', 'paper'],
    scissors : ['paper', 'rock', 'scissors']
}
const startGame = document.querySelector('#start-game') // button to start the game
let joinGame
let rockButton // var for Rock button
let paperButton // var for Paper button
let scissorsButton // var for Scissors button
let resetButton // var for button to reset game after check results
let reultOfGame // var for store result of the game and send it to sever after
let socket // var for WebSocket object 
let participants = []


startGame.addEventListener('click', waitOpponent)


// function for create button
function createButton(varaible, textContent, parent) {
    varaible = document.createElement('button')
    varaible.textContent = textContent
    varaible.setAttribute('id', textContent.toLowerCase())
    parent.appendChild(varaible)
}

// create socket, send message about user join to server
function waitOpponent(){
    socket = new WebSocket('ws://localhost:8000/ws/game_online/')
    socket.addEventListener("open", (ev) => {
        socket.send(JSON.stringify({
            'user_join':  true,
            'message': ''
        }))
        });
    
    startGame.parentNode.removeChild(startGame)
    createButton(joinGame, 'Join the game', startGamePara)
    startGamePara.childNodes[0].addEventListener('click', Game)
}

// main function
function Game(){
    startGamePara.removeChild(startGamePara.lastChild)
    choosingText.innerText = 'Choose your weapon!'
    createButton(rockButton, 'Rock', weapons)
    createButton(paperButton, 'Paper', weapons)
    createButton(scissorsButton, 'Scissors', weapons)
    for (weapon of weapons.childNodes) {
        
        weapon.addEventListener('click', function() {
            //userWeapon.innerText = `Your weapon - ${this.innerText}`
            socket.send(JSON.stringify({
                'user_join':  false,
                'message':  this.innerText
            }));
            console.log(`it is one ${this.innerText}`)
            
        })
    }

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data.message);
        winner.innerText = data.message
    };
}


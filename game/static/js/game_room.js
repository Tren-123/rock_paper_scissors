const plgrg = document.querySelector('.playground') // div class playground
const weapons = document.querySelector('.weapons') // div for weapons buttons inside playground
const choosingText = document.querySelector('#choosing-text') // para for insertion of text with choosing offer
const userWeapon = document.querySelector('#user-weapon') // string with user weapon 
const opponentWeapon = document.querySelector('#opponent-weapon') // string with opponent weapon 
const winner = document.querySelector('#winner') // string with winer results
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


let socket = new WebSocket('ws://' + window.location.host + '/ws' + window.location.pathname) // var for WebSocket object 
// const owner
// const opponent
console.log('ws://' + window.location.host + '/ws' + window.location.pathname)


for (weapon of weapons.childNodes) {
        
    weapon.addEventListener('click', function() {
        socket.send(JSON.stringify({
            'message':  'weapon_choose',
            'weapon':  this.innerText
        }));
        console.log(`weapon of this user ${this.innerText}`)
        
    })
}

socket.onmessage = function(e){
    let djangoData = JSON.parse(e.data);
    console.log(djangoData);
    if (djangoData.type = 'send_result'){
        userWeapon.innerText = wpnDict[djangoData.owner_weapon];
        opponentWeapon.innerText = wpnDict[djangoData.opponent_weapon];
        if (djangoData.winner){
        winner.innerText = djangoData.winner}
        else{
            winner.innerText = 'Draw'
        }
    }
}
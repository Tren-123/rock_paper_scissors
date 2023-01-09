const plgrg = document.querySelector('.playground') // div class playground
const weapons = document.querySelector('.weapons') // div for weapons buttons inside playground
const choosingText = document.querySelector('#choosing-text') // para for insertion of text with choosing offer
const userWeapon = document.querySelector('#user-weapon') // string with user weapon 
const opponentWeapon = document.querySelector('#opponent-weapon') // string with opponent weapon 
const winner = document.querySelector('#winner') // string with winer results
const wpnDict = { // dictionary with {myWeapon : [win if opp have this weapon, lose if opp have this weapon, draw if opp have this weapon]}
    rock : ['scissors', 'paper', 'rock'],
    paper : ['rock', 'scissors', 'paper'],
    scissors : ['paper', 'rock', 'scissors']
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
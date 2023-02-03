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
const chatLog = document.querySelector('#chatLog'); // const for chat box
const chatMessageInput = document.querySelector('#chatMessageInput'); // const for input message text box
const chatMessageSend = document.querySelector('#chatMessageSend'); // const for button of send message to chat
let returnToIndex = document.createElement('button'); // var for button to return to index page after game ending
returnToIndex.innerText = 'Return to index page';
returnToIndex.setAttribute("id", "return-to-index");
returnToIndex.setAttribute("class", "btn btn-success btn-sm join-buttons");


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
                owner.childNodes[2].innerText = `Choosed weapon - ${wpnDict[data.owner_weapon]}`;
                opponent.childNodes[2].innerText = `Choosed weapon - ${wpnDict[data.opponent_weapon]}`;
                if (data.winner != false ){
                winner.innerText = 'Winner: ' + data.winner
                if (data.winner === data.owner[0]) {
                    console.log(data.winner, data.owner)
                    owner.style.backgroundColor = 'darkseagreen'
                }else{
                    console.log(data.winner, data.opponent)
                    opponent.style.backgroundColor = 'darkseagreen'
                }
                endGame(socket)
            }
                else{
                    winner.innerText = 'Draw'
                }
                break;
            case "chat_send_message_to_room_chat": // show message from user in chat chatLog
                chatLog.value += `${data.user}: ${data.message_body}\n`;
                chatLog.scrollTop = chatLog.scrollHeight;
                console.log(`body message ${data.message_body} recived`)
                break;
            default:
                console.error("Unknown message type!");
                break;
        }
    }


function endGame(socket){ // if winner determinated freeze buttons, show endGameString and close websocket connection
for (weapon of weapons.childNodes) {
    weapon.disabled = true}
endGameString.innerText = 'GAME IS END. TO START NEW GAME:'
endGameString.appendChild(returnToIndex);
returnToIndex.onclick = function(){
    window.location.href = window.location.protocol + '//' + window.location.host + '/index/'
};
socket.close()
};

chatMessageSend.addEventListener("click", function() { // send message to server with chat message
    if (chatMessageInput.value.length === 0) return;
    socket.send(JSON.stringify({
        'message':  'send_message_to_room_chat',
        'message_body':  chatMessageInput.value
    }));
    chatMessageInput.value = "";
});
}
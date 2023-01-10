let socket = new WebSocket('ws://127.0.0.1:8000/ws/index/')
const availableGame = document.querySelector('#available-game') // ul for list of available game for joing
const createGame = document.querySelector('#create-game') // const for create-game button
const createGameInput = document.querySelector('#create-game-input') // const for create-game input text box
// Make the list item
let li = document.createElement('li');
let joinButton = document.createElement('button');
joinButton.innerText = 'Join'

socket.onmessage = function(e){
    let djangoData = JSON.parse(e.data);
    console.log(djangoData.message)
    if (djangoData.message === 'update'){
    availableGame.innerHTML = ''
    djangoData.list_of_game.forEach((item) => {
    // Add the item text
    li.innerHTML += item[0];
    joinButton.setAttribute("id", item[1])
    joinButton.setAttribute("class", "join-buttons")
    li.appendChild(joinButton)
    // Add li to the ul
    availableGame.appendChild(li);
    // Reset the list item
    li = document.createElement('li');
    joinButton = document.createElement('button');
    joinButton.innerText = 'Join';
    
});
    Array.from(document.getElementsByClassName("join-buttons"))
    .forEach(function(element){
        element.addEventListener("click", function(){
            socket.send(JSON.stringify({'message' : 'opponent_connected', 'game_id' : element.id}))
            window.location.href = 'http://' + window.location.host + '/index/game/' + element.id + '/';
        });
})
} else if (djangoData.message === 'new_game'){
        window.location.href = 'http://' + window.location.host + '/index/game/' + djangoData.id + '/';
        }
}

setInterval(requestUpdates, 2000)

function requestUpdates(){
    socket.send(JSON.stringify({'message' : 'update'}))
}

createGame.addEventListener("click", createGameRequest)

function createGameRequest(){
    socket.send(JSON.stringify({'message' : 'create_game', 'game_name' : createGameInput.value}))
}


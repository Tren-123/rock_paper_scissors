let socket = new WebSocket('ws://127.0.0.1:8000/ws/index/')
const availableGame = document.querySelector('#available-game') // ul for list of available game for joing
const createGame = document.querySelector('#create-game') // const for create-game button
const createGameInput = document.querySelector('#create-game-input') // const for create-game input text box
// Make the list item
let li = document.createElement('li');
let joinButton = document.createElement('button');
joinButton.innerText = 'Join'

socket.onmessage = function(e){ // listen messages from server
    let djangoData = JSON.parse(e.data);
    console.log(djangoData.message)
    if (djangoData.message === 'update'){ // update list of available games on web page
    availableGame.innerHTML = ''
    djangoData.list_of_game.forEach((item) => { // add button to join game to each game from list
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
    Array.from(document.getElementsByClassName("join-buttons")) // add event listner to joinButtons
    .forEach(function(element){
        element.addEventListener("click", function(){ // send message to server whan user click join button
            socket.send(JSON.stringify({'message' : 'opponent_connected', 'game_id' : element.id}))
            window.location.href = 'http://' + window.location.host + '/index/game/' + element.id + '/'; // redirect user to game room
        });
})
} else if (djangoData.message === 'new_game'){ // redirect user to waiting opponent web page
        window.location.href = 'http://' + window.location.host + '/index/game/waiting/' + djangoData.id + '/';
        }
}

setInterval(requestUpdates, 2000) // sending request each 2 sec

function requestUpdates(){ // send request for updates list of available games to server
    socket.send(JSON.stringify({'message' : 'update'}))
}

createGame.addEventListener("click", createGameRequest) // event listener for createGame button

function createGameRequest(){ // send create_game message with game name to server
    socket.send(JSON.stringify({'message' : 'create_game', 'game_name' : createGameInput.value}))
}


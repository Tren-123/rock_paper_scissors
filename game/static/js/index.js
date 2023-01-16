let socket = new WebSocket('ws://127.0.0.1:8000/ws/index/');
const availableGameTbl = document.querySelector('#available-game');
const tblBody = document.querySelector("#available-game-tbody");
const createGame = document.querySelector('#create-game'); // const for create-game button
const createGameInput = document.querySelector('#create-game-input'); // const for create-game input text box
let joinButton = document.createElement('button');
joinButton.innerText = 'Join';

socket.onmessage = function(e){ // listen messages from server
    let djangoData = JSON.parse(e.data);
    console.log(djangoData.message);
    if (djangoData.message === 'update'){ // update list of available games on web page
    tblBody.innerHTML = '';
    djangoData.list_of_game.forEach((item) => { // add button to join game to each game from list
    // creates a table row
    let row = document.createElement("tr");
    let cell = document.createElement("td");
    let cellText = document.createTextNode(item[0]);
    cell.appendChild(cellText);
    row.appendChild(cell);
    row.appendChild(cell);
    cell = document.createElement("td");
    cellText = document.createTextNode(item[2]);
    cell.appendChild(cellText);
    row.appendChild(cell);
    cell = document.createElement("td");
    joinButton.setAttribute("id", item[1]);
    joinButton.setAttribute("class", "btn btn-success btn-sm join-buttons");
    cell.appendChild(joinButton);
    row.appendChild(cell);
    // add the row to the end of the table body
    tblBody.appendChild(row);
    joinButton = document.createElement('button');
    joinButton.innerText = 'Join';

});
    availableGameTbl.appendChild(tblBody); // put the <tbody> in the <table>

    // add event listner to joinButtons
    Array.from(document.getElementsByClassName("join-buttons"))
    .forEach(function(element){
        element.addEventListener("click", function(){ // send message to server whan user click join button
            socket.send(JSON.stringify({'message' : 'opponent_connected', 'game_id' : element.id}));
            window.location.href = 'http://' + window.location.host + '/index/game/' + element.id + '/'; // redirect user to game room
        });
})
} else if (djangoData.message === 'new_game'){ // redirect user to waiting opponent web page
        window.location.href = 'http://' + window.location.host + '/index/game/waiting/' + djangoData.id + '/';
        }
}

setInterval(requestUpdates, 2000); // sending request each 2 sec

function requestUpdates(){ // send request for updates list of available games to server
    socket.send(JSON.stringify({'message' : 'update'}));
}

createGame.addEventListener("click", createGameRequest); // event listener for createGame button

function createGameRequest(){ // send create_game message with game name to server
    socket.send(JSON.stringify({'message' : 'create_game', 'game_name' : createGameInput.value}))
};

let socket = new WebSocket('ws://127.0.0.1:8000/ws/index/')
const availableGame = document.querySelector('#available-game')
// Make the list item
let li = document.createElement('li');
let joinButton = document.createElement('button');
joinButton.innerText = 'Join'

socket.onmessage = function(e){
    let djangoData = JSON.parse(e.data);
    availableGame.innerHTML = ''
    //availableGame.appendChild(ul);
    djangoData.forEach((item) => {
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
            socket.send(JSON.stringify({'message' : 'opponent connected', 'game_id' : element.id}))
            current_url = window.location.href
            window.location.href = current_url + 'game/' + element.id + '/';
        });
});
}

setInterval(requestUpdates, 2000)

function requestUpdates(){
    socket.send(JSON.stringify({'message' : 'update'}))
}


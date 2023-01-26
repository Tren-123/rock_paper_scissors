let socket = new WebSocket('wss://' + window.location.host + '/ws' + window.location.pathname) // open websocket connection with server
console.log('wss://' + window.location.host + '/ws' + window.location.pathname)
setInterval(requestUpdates, 2000) // sending request untill opponent field in game intance fill 

function requestUpdates(){ // send message for requesting update from server
    socket.send(JSON.stringify({'message' : 'update'}))
}

socket.onmessage = function(e){ // get messame from server. If opponent field in game intance fill redirect user to game room web page  
    let djangoData = JSON.parse(e.data);
    console.log(djangoData.message)
    if (djangoData.message === 'opponent_here'){
        window.location.href = window.location.protocol + '//' + window.location.host + '/index/game/' + djangoData.game_id + '/';
    };
    }
const wpns = document.querySelectorAll('#my_rock, #my_paper, #my_scissors') // buttons for choosing user weapon
const ywpn = document.querySelector('.result') // string with user weapon 
const owpn = document.querySelector('.opponent-weapon') // string with opponent weapon 
const wnr = document.querySelector('.winner') // string with winer results
const wpnDict = { // dictionary with myWeapon : [win if opp have this weapon, lose if opp have this weapon, draw if opp have this weapon]
    rock : ['scissors', 'paper', 'rock'],
    paper : ['rock', 'scissors', 'paper'],
    scissors : ['paper', 'rock', 'scissors']
} 
let resetButton // button to reset game after check results
let indexOpponentWeapon = getRandomIndex(wpns.length) // index of opp weapon in wpns array. Choosing randomly in getRandomIndex function

// listen of click event of weapon buttons
for (weapon of wpns) {
    weapon.addEventListener('click', function() {
      let yourWpn = this.innerText.toLowerCase()
      let oppWpn = wpns[indexOpponentWeapon].innerText.toLowerCase()
      ywpn.innerText = `Your weapon - ${this.innerText}`
      owpn.innerText = `Opponent weapon - ${wpns[indexOpponentWeapon].innerText}`
      checkWpns(wpnDict[yourWpn], oppWpn)
      setGameOver()
    });
  }

// get random index of weapon from weapons list 
function getRandomIndex(lengthOfArray) { 
    return Math.floor(Math.random() * lengthOfArray);
}
    
// compare user and opponent weapon and set text with winner results
function checkWpns(yourWpn, oppWpn) { 
    if (yourWpn[0] === oppWpn){
        wnr.innerText = 'You win!'
        wnr.style.backgroundColor = 'green';
    }
    else if (yourWpn[1] === oppWpn){
        wnr.innerText = 'You lose!'
        wnr.style.backgroundColor = 'red';
    }
    else if (yourWpn[2] === oppWpn){
        wnr.innerText = 'Draw'
        wnr.style.backgroundColor = 'grey'
    }

}

// freeze buttons of choosing weapon and create button of reset game
function setGameOver() {
    for (weapon of wpns){
        weapon.disabled = true
    }
    resetButton = document.createElement('button');
    resetButton.textContent = 'Start new game';
    document.body.append(resetButton);
    resetButton.addEventListener('click', resetGame);
  }

// delete text with user, opponent weapons and winner, unfreeze buttons whith choosing weapons, remove reset button, set new random index value
function resetGame() {
        const resetResults = [ywpn, owpn, wnr]
        for (const resetResult of resetResults) {
            resetResult.textContent = '';
        }

        resetButton.parentNode.removeChild(resetButton);

        for (weapon of wpns){
            weapon.disabled = false
        }
        indexOpponentWeapon = getRandomIndex(wpns.length)

    }







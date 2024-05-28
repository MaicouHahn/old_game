document.addEventListener('DOMContentLoaded', () => {
    
    const casas = document.querySelectorAll('.casa');
    const statusGame = document.getElementById('resultado');
    const btnIA = document.getElementById('buttonIA');
    const restartBtn = document.getElementById('button');
    const scoreboardDivs = document.querySelectorAll('.scoreboard div');

    let currentBoard = Array(9).fill('');

    const updateBoard = (board) => {
        currentBoard = board;
        casas.forEach((casa, index) => {
            casa.innerHTML = board[index];
        });
    };

    const updateScoreboard = (scoreboard) => {
        scoreboardDivs[0].innerHTML = scoreboard.wins;
        scoreboardDivs[1].innerHTML = scoreboard.losses;
        scoreboardDivs[2].innerHTML = scoreboard.draws;
    };

    const checkWinner = (response) => {
        if (response.winner) {
            statusGame.innerHTML = response.winner === 'Tie' ? "EMPATE!" : `'${response.winner}' WINNER`;
            restartBtn.style.display = 'inline-block';
        }
    };

    const makeMove = (index) => {
        fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ player_move: index }),
        })
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);
            updateScoreboard(data.scoreboard);
            checkWinner(data);
        });
    };

    const restartGame = () => {
        fetch('/restart', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);
            statusGame.innerHTML = 'JOGO DA VELHA';
            restartBtn.style.display = 'none';
        });
    };

    const toggleAI = () => {
        fetch('/toggle_ai', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            btnIA.innerHTML = data.ai_enabled ? "MAQUINA: ON" : "MAQUINA: OFF";
        });
    };

    casas.forEach((casa, index) => {
        casa.addEventListener('click', () => makeMove(index));
    });

    restartBtn.addEventListener('click', restartGame);
    btnIA.addEventListener('click', toggleAI);

    // Initialize the game state
    restartGame();
});

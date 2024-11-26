<template>
  <div>
    <canvas 
      id="snakeGame" 
      width="400" 
      height="400" 
      style="border: 1px solid black;"
    ></canvas>

    <div class="scoreboard">
      <p>Score: <span class="score">{{ score }}</span></p>
    </div>

    <div v-if="gameOver">
      <h3>Leaderboard</h3>
      <ul>
        <li v-for="(user, index) in leaderboard" :key="index">
          {{ user.username }}: <strong>{{ user.highest_score }}</strong>
        </li>
      </ul>
    </div>

    <div v-if="showCountdown" class="countdown">
      <p>Get Ready: {{ countdown }}</p>
    </div>

    <div v-if="gameOver">
      <button @click="startGame">Replay</button>
      <button @click="goToMenu">Go to Menu</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      score: 0,
      leaderboard: [],
      snake: [{ x: 5, y: 5 }],
      food: { x: 10, y: 10 },
      blackSquares: [],
      direction: 'RIGHT',
      gameInterval: null,
      gridSize: 20,
      gridCount: 20,
      foodsEaten: 0,
      gameOver: false,
      blackSquareSpawned: false,
      showCountdown: false,
      countdown: 2,
    };
  },

  methods: {
    startGame() {
      this.score = 0;
      this.snake = [{ x: 5, y: 5 }];
      this.food = { x: 10, y: 10 };
      this.blackSquares = [];
      this.direction = 'RIGHT';
      this.foodsEaten = 0;
      this.gameOver = false;
      this.blackSquareSpawned = false;
      this.showCountdown = true;
      this.countdown = 2;

      this.spawnInitialBlackSquares();

      const canvas = document.getElementById('snakeGame');
      const ctx = canvas.getContext('2d');

      const countdownInterval = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        } else {
          clearInterval(countdownInterval);
          this.showCountdown = false;
          this.gameInterval = setInterval(() => {
            this.updateGame(ctx);
          }, 100);
        }
      }, 1000);

      window.addEventListener('keydown', this.changeDirection);
    },

    updateGame(ctx) {
      this.moveSnake();

      if (this.checkCollision()) {
        this.gameOver = true;
        clearInterval(this.gameInterval);
        this.testPostMethod();
        return;
      }

      if (this.checkFoodCollision()) {
        this.score++;
        this.foodsEaten++;
        this.snake.push({});
        this.spawnFood();
      }

      if (this.foodsEaten % 2 === 0 && this.foodsEaten > 0 && !this.blackSquareSpawned) {
        this.spawnBlackSquare();
        this.blackSquareSpawned = true;
      }

      if (this.foodsEaten % 2 !== 0) {
        this.blackSquareSpawned = false;
      }

      if (this.checkBlackSquareCollision()) {
        this.gameOver = true;
        clearInterval(this.gameInterval);
        this.testPostMethod();
        return;
      }

      this.drawGame(ctx);
    },

    drawGame(ctx) {
      ctx.clearRect(0, 0, 400, 400);

      ctx.fillStyle = 'green';
      this.snake.forEach(segment => {
        ctx.fillRect(segment.x * this.gridSize, segment.y * this.gridSize, this.gridSize, this.gridSize);
      });

      ctx.fillStyle = 'red';
      ctx.fillRect(this.food.x * this.gridSize, this.food.y * this.gridSize, this.gridSize, this.gridSize);

      ctx.fillStyle = 'black';
      this.blackSquares.forEach(square => {
        ctx.fillRect(square.x * this.gridSize, square.y * this.gridSize, this.gridSize, this.gridSize);
      });
    },

    moveSnake() {
      const head = { ...this.snake[0] };

      if (this.direction === 'UP') head.y -= 1;
      else if (this.direction === 'DOWN') head.y += 1;
      else if (this.direction === 'LEFT') head.x -= 1;
      else if (this.direction === 'RIGHT') head.x += 1;

      this.snake.unshift(head);
      this.snake.pop();
    },

    changeDirection(event) {
      const key = event.key;

      if (key === 'ArrowUp' && this.direction !== 'DOWN') this.direction = 'UP';
      else if (key === 'ArrowDown' && this.direction !== 'UP') this.direction = 'DOWN';
      else if (key === 'ArrowLeft' && this.direction !== 'RIGHT') this.direction = 'LEFT';
      else if (key === 'ArrowRight' && this.direction !== 'LEFT') this.direction = 'RIGHT';
    },

    checkCollision() {
      const head = this.snake[0];

      const hitWall = head.x < 0 || head.x >= this.gridCount || head.y < 0 || head.y >= this.gridCount;
      const hitSelf = this.snake.slice(1).some(segment => segment.x === head.x && segment.y === head.y);

      return hitWall || hitSelf;
    },

    checkFoodCollision() {
      const head = this.snake[0];
      return head.x === this.food.x && head.y === this.food.y;
    },

    spawnFood() {
      let validPosition = false;
      let newFood;

      while (!validPosition) {
        newFood = {
          x: Math.floor(Math.random() * this.gridCount),
          y: Math.floor(Math.random() * this.gridCount),
        };

        const onBlackSquare = this.blackSquares.some(square => square.x === newFood.x && square.y === newFood.y);
        const onSnake = this.snake.some(segment => segment.x === newFood.x && segment.y === newFood.y);

        if (!onBlackSquare && !onSnake) {
          validPosition = true;
        }
      }

      this.food = newFood;
    },

    spawnBlackSquare() {
      const blackSquare = {
        x: Math.floor(Math.random() * this.gridCount),
        y: Math.floor(Math.random() * this.gridCount),
      };
      this.blackSquares.push(blackSquare);
    },

    spawnInitialBlackSquares() {
      for (let i = 0; i < 7; i++) {
        this.spawnBlackSquare();
      }
    },

    checkBlackSquareCollision() {
      const head = this.snake[0];
      return this.blackSquares.some(square => square.x === head.x && square.y === head.y);
    },

    async testPostMethod() {
      try {
        const token = this.getToken();
        if (!token) {
          console.error('No token found!');
          return;
        }

        const response = await fetch('http://127.0.0.1:8000/update-score/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({ score: this.score }),
        });

        if (response.ok) {
          console.log('Score updated successfully!');
          this.fetchLeaderboard();
        } else {
          console.error('Failed to update score.');
        }
      } catch (error) {
        console.error('Error updating score:', error);
      }
    },

    async fetchLeaderboard() {
      try {
        const response = await fetch('http://127.0.0.1:8000/leaderboard/');
        if (response.ok) {
          const data = await response.json();
          this.leaderboard = data.leaderboard;
        }
      } catch (error) {
        console.error('Error fetching leaderboard:', error);
      }
    },

    getCookie(name) {
      let cookieValue = null;
      if (document.cookie) {
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
          const trimmed = cookie.trim();
          if (trimmed.startsWith(name + '=')) {
            cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },

    getToken() {
      return localStorage.getItem('authToken');
    },

    goToMenu() {
      this.$router.push('/logedin'); 
    },
  },

  mounted() {
    this.fetchLeaderboard();
    this.startGame();
  },
};
</script>

<style scoped>
canvas {
  margin: 20px auto;
  display: block;
}

.scoreboard {
  text-align: center;
  font-size: 24px;
  margin: 10px 0;
}

.score {
  font-weight: bold;
  color: #ff5722;
}

.leaderboard {
  margin: 20px auto;
  text-align: center;
}

.countdown {
  text-align: center;
  font-size: 30px;
  color: #ff5722;
}

button {
  margin: 10px;
  padding: 10px;
  font-size: 16px;
}

button:hover {
  background-color: #f0f0f0;
}
</style>

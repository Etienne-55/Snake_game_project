<template>
  <div>
    <h2>Snake Game</h2>
    <p>Score: {{ score }}</p>
    <canvas id="gameCanvas" width="400" height="400" style="border:1px solid #000"></canvas>
    <button @click="replayGame" v-if="gameOver">Replay</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      score: 0,
      gameOver: false,
      game: null,
      snake: [],
      direction: null,
      food: {},
    };
  },
  mounted() {
    this.startGame();
  },
  methods: {
    startGame() {
      this.score = 0;
      this.gameOver = false;
      this.snake = [{ x: 180, y: 200 }];
      this.direction = null;
      this.food = {
        x: Math.floor(Math.random() * 19 + 1) * 20,
        y: Math.floor(Math.random() * 19 + 1) * 20,
      };

      const canvas = document.getElementById('gameCanvas');
      const ctx = canvas.getContext('2d');
      const box = 20;

      document.addEventListener('keydown', this.setDirection);

      const collision = (head, array) => {
        return array.some(segment => head.x === segment.x && head.y === segment.y);
      };

      const draw = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (let i = 0; i < this.snake.length; i++) {
          ctx.fillStyle = i === 0 ? 'green' : 'white';
          ctx.fillRect(this.snake[i].x, this.snake[i].y, box, box);
          ctx.strokeRect(this.snake[i].x, this.snake[i].y, box, box);
        }

        ctx.fillStyle = 'red';
        ctx.fillRect(this.food.x, this.food.y, box, box);

        let snakeX = this.snake[0].x;
        let snakeY = this.snake[0].y;

        if (this.direction === 'LEFT') snakeX -= box;
        if (this.direction === 'UP') snakeY -= box;
        if (this.direction === 'RIGHT') snakeX += box;
        if (this.direction === 'DOWN') snakeY += box;

        if (snakeX === this.food.x && snakeY === this.food.y) {
          this.score++;
          this.food = {
            x: Math.floor(Math.random() * 19 + 1) * box,
            y: Math.floor(Math.random() * 19 + 1) * box
          };
        } else {
          this.snake.pop();
        }

        let newHead = { x: snakeX, y: snakeY };

        if (
          snakeX < 0 ||
          snakeY < 0 ||
          snakeX >= canvas.width ||
          snakeY >= canvas.height ||
          collision(newHead, this.snake)
        ) {
          clearInterval(this.game);
          this.gameOver = true;
          document.removeEventListener('keydown', this.setDirection);
        } else {
          this.snake.unshift(newHead);
        }
      };

      if (this.game) clearInterval(this.game);
      this.game = setInterval(draw, 100);
    },
    setDirection(event) {
      if (event.keyCode === 37 && this.direction !== 'RIGHT') this.direction = 'LEFT';
      else if (event.keyCode === 38 && this.direction !== 'DOWN') this.direction = 'UP';
      else if (event.keyCode === 39 && this.direction !== 'LEFT') this.direction = 'RIGHT';
      else if (event.keyCode === 40 && this.direction !== 'UP') this.direction = 'DOWN';
    },
    replayGame() {
      this.startGame();
    },
  },
  beforeUnmount() {
    if (this.game) clearInterval(this.game);
    document.removeEventListener('keydown', this.setDirection);
  }
};
</script>
<template>
  <div class="game-container">
    <h1>{{ hello }}</h1>
    <br /><br />

    <router-link to="/coffee/new" class="start-game-button">Start Game</router-link>
    <br /><br />

    <h2>Leaderboard</h2>
    <table class="leaderboard">
      <thead>
        <tr>
          <th>Username</th>
          <th>Highest Score</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in leaderboard" :key="user.username">
          <td>{{ user.username }}</td>
          <td>{{ user.highest_score }}</td>
        </tr>
      </tbody>
    </table>
    <br />

    <button @click="goToMenu" class="return-button">Return to Login</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      hello: '',
      leaderboard: [],
    };
  },
  created() {
    this.fetchHello();
    this.fetchLeaderboard();
  },
  methods: {
    async fetchHello() {
      try {
        const response = await fetch('http://127.0.0.1:8000/hello/');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        this.hello = data.message;
      } catch (error) {
        console.error('Error fetching HelloWorld message:', error);
      }
    },

    async fetchLeaderboard() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/leaderboard/');
        this.leaderboard = response.data.leaderboard; 
      } catch (error) {
        console.error('Error fetching leaderboard:', error);
      }
    },

    async updateScore(score) {
      try {
        const userId = this.getUserId();
        const response = await axios.post(`http://127.0.0.1:8000/update_score/${userId}/${score}/`);
        if (response.data.status === 'success') {
          console.log('Score updated successfully');
          this.fetchLeaderboard();
        }
      } catch (error) {
        console.error('Error updating score:', error);
      }
    },

    gameOver(score) {
      this.updateScore(score); 
    },

    goToMenu() {
      this.$router.push('/'); 
    },
  },
};
</script>

<style scoped>
.game-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  text-align: center;
}

h1 {
  color: #333;
  margin-bottom: 20px;
}

h2 {
  color: #333;
  margin-bottom: 10px;
}

.leaderboard {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
  border-collapse: collapse;
}

.leaderboard th,
.leaderboard td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}

.leaderboard th {
  background-color: #007bff;
  color: white;
}

.leaderboard td {
  background-color: #f9f9f9;
}

.start-game-button {
  display: inline-block;
  padding: 10px 20px;
  color: white;
  background-color: #007bff;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  cursor: pointer;
}

.start-game-button:hover {
  background-color: #0056b3;
}

.return-button {
  padding: 10px 20px;
  color: #333;
  background-color: #f1f1f1;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.return-button:hover {
  background-color: #ddd;
}
</style>

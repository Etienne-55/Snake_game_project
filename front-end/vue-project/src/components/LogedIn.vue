<template>
  <div class="game-container">
    <h1>{{ hello }}</h1><br /><br />

    <router-link to="/coffee/new" class="start-game-button">Start game</router-link><br /><br />

    <button @click="goToMenu" class="return-button">Return to login</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      hello: '',     
      coffees: [],
    };
  },
  created() {
    this.fetchHello();
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
        this.errorMessage = 'Error loading HelloWorld message';
      }
    },
    
    goToMenu() {
      this.$router.push('/');
    },

    fetchCoffees() {
      axios.get('/api/coffee/')
        .then(response => { this.coffees = response.data; })
        .catch(error => { console.error(error); });
    },

    deleteCoffee(id) {
      axios.delete(`/api/coffee/${id}/`)
        .then(() => { this.fetchCoffees(); })
        .catch(error => { console.error(error); });
    },

    editCoffee(id) {
      this.$router.push(`/coffee/${id}/edit`);
    }
  },
  mounted() {
    this.fetchCoffees();
  }
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

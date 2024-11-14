<template>
    <div>
      <h1>{{ hello }}</h1><br><br>
    <router-link to="/coffee/new">Start game</router-link><br><br>

    <button @click="goToMenu">Return to login</button>

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
  
  </style>
  
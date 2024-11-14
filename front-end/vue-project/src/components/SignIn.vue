<template>
  <div class="signup-container">
    <h2>Sign Up</h2>
    <form @submit.prevent="signup" class="signup-form">
      <input v-model="email" type="email" placeholder="Email" required /><br />
      <input v-model="password" type="password" placeholder="Password" required /><br />
      <input v-model="confirmPassword" type="password" placeholder="Confirm Password" required /><br />
      <button type="submit">Sign Up</button>
    </form>

    <p v-if="message" class="message">{{ message }}</p>

    <button @click="goBack" class="back-button">Go back</button>
  </div>
</template>

<script>
import axios from 'axios';

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export default {
  data() {
    return {
      email: '',
      password: '',
      confirmPassword: '',
      message: ''
    };
  },
  methods: {
    goBack() {
      this.$router.push('/');
    },
    async signup() {
      const csrfToken = getCookie('csrftoken');
      try {
        const response = await axios.post('http://127.0.0.1:8000/signin/', {
          email: this.email,
          password: this.password,
          confirm_password: this.confirmPassword
        }, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          }
        });
        this.message = response.data;
      } catch (error) {
        console.error('Error', error);
        this.message = 'An error has occurred';
      }
    }
  }
};
</script>

<style scoped>
.signup-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  text-align: center;
}

h2 {
  color: #333;
  margin-bottom: 20px;
}

.signup-form input {
  width: 100%;
  max-width: 300px;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button[type="submit"] {
  width: 100%;
  max-width: 300px;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
}

button[type="submit"]:hover {
  background-color: #218838;
}

.message {
  color: #e74c3c;
  margin-top: 15px;
}

.back-button {
  margin-top: 20px;
  padding: 10px 20px;
  color: #333;
  background-color: #f1f1f1;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.back-button:hover {
  background-color: #ddd;
}
</style>

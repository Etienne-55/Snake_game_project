<template>
  <div class="login-container">
    <h1>{{ helloMessage }}</h1>

    <div class="login-box">
      <h2>Login</h2>
      <form @submit.prevent="login" class="login-form">
        <input v-model="email" type="email" placeholder="Email" required /><br />
        <input v-model="password" type="password" placeholder="Password" required /><br />
        <button type="submit">Login</button>
      </form>

      <p v-if="message" class="message">{{ message }}</p>

      <button @click="goToSignIn" class="signup-button">Sign up</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      helloMessage: '',
      email: '',
      password: '',
      message: ''
    };
  },
  created() {
    this.fetchHelloMessage();
  },
  methods: {
    async fetchHelloMessage() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/hello/');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        this.helloMessage = data.message;
      } catch (error) {
        console.error('Error fetching HelloWorld message:', error);
        this.message = 'Error loading HelloWorld message';
      }
    },

    goToSignIn() {
      this.$router.push('/sign-in');
    },

    async login() {
      try {
        const response = await fetch('http://127.0.0.1:8000/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        });

        if (response.ok) {
          const data = await response.json();

          localStorage.setItem('authToken', data.access_token); 
          localStorage.setItem('refreshToken', data.refresh_token);

          this.$router.push('/logedin'); 
        } else {
          const data = await response.json();
          this.message = `Login failed: ${data.message}`;
        }
      } catch (error) {
        console.error('Error:', error);
        this.message = 'An error has occurred';
      }
    },

    getCookie(name) {
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
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f0f2f5;
}

h1 {
  color: #333;
  margin-bottom: 20px;
}

.login-box {
  background-color: #ffffff;
  padding: 2em;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
  width: 300px;
}

h2 {
  color: #444;
  margin-bottom: 1em;
}

.login-form input {
  width: 100%;
  padding: 10px;
  margin: 8px 0;
  border-radius: 4px;
  border: 1px solid #ccc;
}

button[type="submit"] {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: #0056b3;
}

.message {
  color: #e74c3c;
  margin-top: 10px;
}

.signup-button {
  margin-top: 1em;
  background-color: #f1f1f1;
  color: #333;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.signup-button:hover {
  background-color: #ddd;
}
</style>

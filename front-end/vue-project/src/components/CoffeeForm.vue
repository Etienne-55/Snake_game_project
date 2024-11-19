<template>
  <div>
    <button @click="testPostMethod">Test POST Method</button>
    <p>{{ message }}</p>
    <div v-if="leaderboard.length > 0">
      <h3>Leaderboard</h3>
      <ul>
        <li v-for="(user, index) in leaderboard" :key="index">
          {{ user.username }}: {{ user.highest_score }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: '',
      leaderboard: [],
    };
  },

  methods: {
    async testPostMethod() {
      try {
        const token = this.getToken();
        if (!token) {
          this.message = 'No token found!';
          return;
        }

        const response = await fetch('http://127.0.0.1:8000/update-score/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken'), 
            'Authorization': `Bearer ${token}`, 
          },
          body: JSON.stringify({ click_count: 1 }), // Increment score by 1
        });

        if (response.ok) {
          this.message = 'Score updated successfully!';
          this.fetchLeaderboard(); // Refresh leaderboard after updating score
        } else if (response.status === 401) {
          console.log('Token expired, attempting to refresh...');
          const refreshResponse = await this.refreshToken();

          if (refreshResponse) {
            const newToken = this.getToken();
            const retryResponse = await fetch('http://127.0.0.1:8000/update-score/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken'), 
                'Authorization': `Bearer ${newToken}`,  
              },
              body: JSON.stringify({ click_count: 1 }), 
            });

            if (retryResponse.ok) {
              this.message = 'Score updated successfully with new token!';
              this.fetchLeaderboard(); // Refresh leaderboard
            } else {
              const errorData = await retryResponse.json();
              this.message = `Error: ${errorData.message || 'Unknown error'}`;
            }
          } else {
            this.message = 'Failed to refresh token!';
          }
        } else {
          const data = await response.json();
          this.message = `Error: ${data.message || 'Something went wrong'}`;
        }
      } catch (error) {
        console.error('Error:', error);
        this.message = 'An error has occurred';
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
    },

    getToken() {
      return localStorage.getItem('authToken');
    },

    getRefreshToken() {
      return localStorage.getItem('refreshToken');  
    },

    async refreshToken() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/token/refresh/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ refresh: this.getRefreshToken() }),  
        });

        if (response.ok) {
          const data = await response.json();
          localStorage.setItem('authToken', data.access);  
          localStorage.setItem('refreshToken', data.refresh);  
          return true;
        } else {
          console.error('Failed to refresh token');
          return false;
        }
      } catch (error) {
        console.error('Error refreshing token:', error);
        return false;
      }
    },
  },
  
  mounted() {
    this.fetchLeaderboard(); // Fetch leaderboard when component mounts
  },
};
</script>

<style scoped>
button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>

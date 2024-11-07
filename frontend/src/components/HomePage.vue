<template>
  <div>
    <h1>Welcome to the Snake Game!</h1>
    <button @click="startGame">Start Game</button>
  </div>
</template>

<script>
export default {
  methods: {
    startGame() {
      this.$router.push('/game'); // Navigate to the game page
    },
  },
};
</script>

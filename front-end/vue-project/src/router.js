import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/MainMenu.vue';
import SignIn from './components/SignIn.vue';
import LogedIn from './components/RankPage.vue';
import CoffeeForm from './components/GamePage.vue'

const routes = [
  { path: '/', component: HelloWorld },
  { path: '/sign-in', component: SignIn },
  { path: '/logedin', component: LogedIn},
  { path: '/coffee/new', component: CoffeeForm },
  { path: '/coffee/:id/edit', component: CoffeeForm },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

import Vue from 'vue'
import VueRouter from 'vue-router'
import Accueil from '../components/Accueil.vue'
import Reco from '../components/Recommendation.vue'
import AddSerie from '../components/AddSeries.vue'
Vue.use(VueRouter)

const routes = [


  {
    path:'/Recomendation',
    component: Reco,
    name: 'Reco'
    
  },
  {
    path:'/AddSeries',
    component :AddSerie,
    name:'AddSeries'
  },
  {
    path: '*',
    component: Accueil,
    name: 'Accueil'
    
  }
  
  
    
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

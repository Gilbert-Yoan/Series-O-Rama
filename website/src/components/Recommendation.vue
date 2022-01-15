<template>
  <div>
    <v-app-bar
      color="#3F51B5"
      dense
        dark
    ><!-- Bar color indigo-->
      <v-toolbar-title>LBProd</v-toolbar-title>

      <v-spacer></v-spacer>
      <v-col>
        <v-text-field
        :label="$t('Seach')"
        hide-details="auto"
        ></v-text-field>
    </v-col>
     <v-spacer></v-spacer>
    <v-btn
        elevation="2"
        plain
        @click="GoHome()"
        >{{$t('Home')}}</v-btn>   
    <v-divider
        vertical
    ></v-divider>
    <v-btn
        elevation="2"
        plain
        >{{$t('Recomendation')}}</v-btn>   
    <v-divider
        vertical
    ></v-divider>

        <v-btn
            elevation="2"
            plain
            >{{$t('Login')}}
        </v-btn>   
 
    <v-divider
        vertical
    ></v-divider>
     <v-btn 
     @click="changeLangueEN()"
      plain>
    <v-img
        max-width="40"
        src="../assets/AnglaisFalg.jpg"
    ></v-img>
    </v-btn>
    <v-divider
        vertical
    ></v-divider>
     <v-btn
     @click="changeLangueFR()"
      plain>
    <v-img
        max-width="40"
        src="../assets/FranceFlag.png"
    ></v-img>
    </v-btn>
     
    </v-app-bar>
       <v-card>
  <template>
      <v-card-title>{{$t('The most seen')}}</v-card-title>
  </template>
   </v-card>
   <br>
    <v-item-group>
    <v-container>
      <v-row >
        <v-col
          v-for="Serie in Series"
          :key="Serie.id"
          cols="auto"
          md="auto"
        >
          <v-item >
             <v-chip >
          
          {{Serie.name}}{{" "}} <v-rating
 
  length="1"
  readonly
  size="20"
  value="3"
></v-rating>{{Serie.rating}}
          
          </v-chip>
          </v-item>
        </v-col>
      </v-row>
    </v-container>
  </v-item-group>


  </div>
  
</template>

<script>
import LocaleLangue from "../i18n"
export default {
    data :() => ({
     
         LoginDialog:false,
         Series:[
             
             {
                 id:1,
                name: 'H',
                rating: 3.4,

             },
             {
                 id:2,
                name: 'Lost',
                rating: 4.6,

             },
             {
                 id:4,
                name: 'Walking Dead',
                rating: 4.9,

             },
             {
                 id:5,
                name: 'Stranger Things',
                rating: 5,

             }
         ]
      }),
    methods: {
        changeLangueEN(){
            LocaleLangue.locale='en'

        },
         changeLangueFR(){
            LocaleLangue.locale='fr'

        },
        Login(){
            this.LoginDialog = false
        },
        GoHome(){
            this.$router.push({
                name:"Accueil"
            })
        },
        GoReco(){
            this.$router.push({
                name:"Accueil"
            })
        }
    },
    
}
</script>

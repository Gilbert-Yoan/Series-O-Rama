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
        v-model="StringRecherche"
        :label="$t('Seach')"
        hide-details="auto"
        ></v-text-field>
        
    </v-col>
    <v-icon @click="CoupeChaineRecherche()">{{icon.mdiMagnify}}</v-icon>
     <v-spacer></v-spacer>
    <v-btn
        elevation="2"
        plain
        @click="GoHome"
        >{{$t('Home')}}</v-btn>   
    <v-divider
        vertical
    ></v-divider>
    <v-btn
        elevation="2"
        plain
        @click="GoReco"
        >{{$t('Recomendation')}}</v-btn>   
    <v-divider
        vertical
    ></v-divider>

        <v-btn v-if="IsConnect ==false"
            elevation="2"
            plain
            @click="Login()"
            >{{$t('Login')}}
        </v-btn>  
    <v-divider
        vertical
    ></v-divider>
     <v-icon v-if="IsConnect ==true" @click="AddSerie()">{{icon.mdiPlusBox}}</v-icon>
    
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
      <v-card-title>{{$t('Our Series')}}</v-card-title>
  </template>
   </v-card>
   <br>
   <v-item-group>
    <v-container>
      <v-row >
        <v-col
          v-for="Serie in Series"
          :key="Serie.id"
          cols="12"
          md="4"
        >
          <v-item >
             <v-card
                class="mx-auto elevation-20"
                 color="#F5F5F5"
                  
                style="max-width: 400px;"
             >
            <v-row justify="space-between">
            <v-col cols="8">
            <v-card-title>
           <div>
           
            <div>{{Serie.name}}</div>
           
          </div>
        </v-card-title>
      </v-col>
     
        </v-row>
        <v-divider dark></v-divider>
            <v-card-actions class="pa-4">
                {{$t('Rate this series')}}
                <v-spacer></v-spacer>
                <span color="#E0E0E0">
                ({{ Serie.rating }})
                </span>
                <v-rating
                v-model="Serie.rating"
                background-color="white"
                color="#FFD600"
                dense
                half-increments
                hover
                size="18"
                ></v-rating>
            </v-card-actions>
            </v-card>
          </v-item>
        </v-col>
      </v-row>
    </v-container>
  </v-item-group>
  
  </div>
</template>

<script>

import LocaleLangue from "../i18n" 
import { mdiMagnify,mdiPlusBox  } from '@mdi/js';
export default ({

  data :() => ({
      icon:{
        mdiMagnify,
        mdiPlusBox 
      },
        StringRecherche:"",
         IsConnect:false,
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
      })
  ,
          
    methods: {
        changeLangueEN(){
            LocaleLangue.locale='en'

        },
         changeLangueFR(){
            LocaleLangue.locale='fr'

        },
        Login(){
            this.IsConnect = true
        },
        GoHome(){
            this.$router.push({
                name:"Accueil"
            })
        },
        GoReco(){
            this.$router.push({
                name:"Reco"
            })
        },
        CoupeChaineRecherche(){
        var table = this.StringRecherche.split(" ")
        var StringFinal = ""
        StringFinal = StringFinal +"("
        for (const mot of table) {
          StringFinal = StringFinal +"'"+ mot +"',"
        }
        
        StringFinal = StringFinal.substring(StringFinal.length-1,0);
        StringFinal = StringFinal +")"
        console.log(StringFinal)
        },
        AddSerie(){
            this.$router.push({
              name:"AddSeries"
            })

        }

    },
    
})
</script>

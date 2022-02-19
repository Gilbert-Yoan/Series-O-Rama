<template>
  <div>
    <v-app-bar
      color="#3F51B5"
      dense
        dark
    ><!-- Bar color indigo-->
      <v-toolbar-title>LPProd</v-toolbar-title>

      <v-spacer></v-spacer>
      
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
    <br>
    <v-col
            cols="12"
            sm="6"
          >
            <v-text-field

              color="purple darken-2"
              :label="$t('Series Name')"
              required
            ></v-text-field>
          </v-col>
          <template>
              <v-col>
  <v-file-input
    v-model="files"
    how-size
    accept=".zip"
    :label="$t('Drop Files')"
    multiple
    prepend-icon="mdi-paperclip"
  >
    <template v-slot:selection="{ text }">
      <v-chip
        small
        label
        dark
        color="#3F51B5"
      >
        {{ text }}
      </v-chip>
    </template>
  </v-file-input>
  </v-col>
</template>
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
      }
          }),
    methods: {
        changeLangueEN(){
            LocaleLangue.locale='en'

        },
         changeLangueFR(){
            LocaleLangue.locale='fr'

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
        }

    },
    
    
})

</script>
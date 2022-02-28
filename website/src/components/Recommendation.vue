<template>
  <div>
    <v-app-bar
      color="#3F51B5"
      dense
        dark
    ><!-- Bar color indigo-->
      <v-toolbar-title>LPProd</v-toolbar-title>

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
          v-for="Serie in series"
          :key="Serie.noms"
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
           
            <div>{{Serie.noms}}</div>
           
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
    <v-dialog
      v-model="dialog"
      max-width="290"
    >
      <v-card>
        <v-card-title class="text-h5">
          
        </v-card-title>

        <v-card-text>
          <v-text-field
            label="Regular"
          ></v-text-field>
          <v-text-field
            v-model="email"
            :rules="[rules.required, rules.email]"
            label="E-mail"
          ></v-text-field>
          <v-text-field
            v-model="password"
            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[rules.required, rules.min]"
            :type="show1 ? 'text' : 'password'"
            name="input-10-1"
            label="Normal with hint text"
            hint="At least 8 characters"
            counter
            @click:append="show1 = !show1"
          ></v-text-field>
        
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            color="green darken-1"
            text
            @click="dialog = false"
          >
            Agree
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
  
</template>

<script>
import LocaleLangue from "../i18n"
import Api from "../Api";
export default {
    async created() {
    this.series = await Api.GetAllSeries()
    
  },
    data :() => ({
     
         LoginDialog:false,
         series:[],
         rules: {
          required: value => !!value || 'Required.',
           email: value => {
            const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            return pattern.test(value) || 'Invalid e-mail.'
          },
         }
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

<template>
  <div>
    <!-- Bar d'application -->
    <v-app-bar
      color="#3F51B5"
      dense
        dark
    ><!-- Bar color indigo-->
      <v-toolbar-title>Series-O-Rama</v-toolbar-title>

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
     <v-menu
        bottom
        min-width="200px"
        rounded
        offset-y
         v-if="IsConnect ==true"
      >
        <template v-slot:activator="{ on }">
          <v-btn
            icon
            x-large
            v-on="on"
          >
            <v-avatar
              color="#3F51B5"
              size="48"
              dark
            >
              <span class="whith--text text-h5">{{ user[0].initial }}</span>
            </v-avatar>
          </v-btn>
        </template>
        <v-card>
          <v-list-item-content class="justify-center">
            <div class="mx-auto text-center">
              <v-avatar
                color="#3F51B5"
              >
              
                <span class="white--text text-h5">{{ user[0].initial }}</span>
              </v-avatar>
              <h3>{{user[0].pseudo}}</h3>
              <p class="text-caption mt-1">
                {{ user[0].mail }}
              </p>
              <v-divider class="my-3"></v-divider>
              <v-btn
                depressed
                rounded
                text
              >
               {{$t('Edit Account')}}
              </v-btn>
              <v-divider class="my-3"></v-divider>
              <v-btn
                depressed
                v-if="user[0].isadmin==true"
                rounded
                text
                @click="AddSerie()"
              >
                {{$t('Add Series')}}
              </v-btn>
              <v-divider class="my-3"></v-divider>
              <v-btn
                depressed
                rounded
                text
                @click="Disconnect()"
              >
                {{$t('Disconnect')}}
              </v-btn>
            </div>
          </v-list-item-content>
        </v-card>
      </v-menu>
    
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
    <!-- Carte texte -->
   <v-card>
  <template>
      <v-card-title>{{$t('Our Series')}}</v-card-title>
  </template>
   </v-card>
   <br>
    <!--Listed des series-->
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
            <v-card-actions class="pa-4" >
                {{$t('Rate this series')}}
                <v-spacer></v-spacer>
                <span color="#E0E0E0">
                ({{ Serie.rating }})
                </span>
                <v-rating
                v-model="Serie.rating"
                :readonly="!IsConnect"
                background-color="#FFEA00"
                color="#FFD600"
                dense
                half-increments
                hover
                size="18"
                @input="addRating($event,Serie.noms)"
                >
                  
                </v-rating>
            </v-card-actions>
            </v-card>
          </v-item>
        </v-col>
      </v-row>
    </v-container>
  </v-item-group>
  <!-- pop Up create-->
  <v-dialog
      v-model="DialogCreateUser"
      max-width="290"
    >
      <v-card>
        <v-card-title class="text-h5">
          
        </v-card-title>

        <v-card-text>
          <v-text-field
          v-model="LoginCreate"
            :label="$t('Login:')"
            :rules="[rules.required]"
          ></v-text-field>
          <v-text-field
            v-model="email"
            :rules="[rules.required, rules.email]"
            label="E-mail"
          ></v-text-field>
          <v-text-field
            v-model="passwordCreate"
            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[rules.required]"
            :type="show1 ? 'text' : 'password'"
            
            :label="$t('Password')"
            
            counter
            @click:append="show1 = !show1"
          ></v-text-field>
        
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            color="green darken-1"
            text
            @click="CreateUser()"
          >
            {{$t('Create')}}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- pop Up Conection-->
    <v-dialog
      v-model="LoginDialog"
      max-width="290"
    >
      <v-card>
        <v-card-title class="text-h5">
          {{$t('Login')}}
        </v-card-title>

        <v-card-text>
          <v-text-field
            :label="$t('Login:')"
            v-model="loginConnect"
          ></v-text-field>
          <v-text-field
            v-model="password"
            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[rules.required]"
            :type="show1 ? 'text' : 'password'"
            
            :label="$t('Password')"
            
            counter
            @click:append="show1 = !show1"
          ></v-text-field>
        
        </v-card-text>

        <v-card-actions>
                <v-btn
            color="green darken-1"
            text
            justify="center"
          align="center"
            @click="ConfirmLogin()"
          >
            {{$t('Login')}}
          </v-btn>
          
        </v-card-actions>
        <v-card-actions>
          <v-col justify="center"
                align="center">
          <v-chip @click="DialogCreateUser = true"> {{$t('Create Account')}} </v-chip>
          </v-col>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>


<script>

import LocaleLangue from "../i18n" 
import { mdiMagnify,mdiPlusBox,mdiEye,mdiEyeOff    } from '@mdi/js';
import  Api from "../Api"
export default ({
  
  async created() {
    var user = sessionStorage.getItem("User")
  
    if (user !== null && user !== "[]"){
      this.user = JSON.parse(user)
      this.IsConnect = true
    }else{
      this.IsConnect = false
    }
    this.series = await Api.GetAllSeries()
    
  },
  data :() => ({
      icon:{
        mdiMagnify,
        mdiPlusBox,
        mdiEye ,
        mdiEyeOff  
      },
        series :[],
        loginConnect:"",
        password:"",
        user:[],
        email:"",
        LoginCreate:"",
        StringRecherche:"",
        passwordCreate:"",
         IsConnect:false,
         LoginDialog :false,
         DialogCreateUser:false,
         show1:false,
          rules: {
          required: value => !!value || 'Required.',
           email: value => {
            const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            return pattern.test(value) || 'Invalid e-mail.'
          },
         }
        
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
            this.LoginDialog = true
        },//Permet d'ouvrire le pop up de connection
        async ConfirmLogin(){
            this.LoginDialog = false
            if (this.loginConnect !=="" && this.password !=="") {
              this.user = await Api.UserConnect(this.loginConnect,this.password)
              let Initial = this.user[0].pseudo.split("")
              Initial = Initial[0]+ Initial[1]
              this.user[0].initial = Initial
              console.log(this.user);
              
              this.IsConnect =true
            }

        },//Permet de faire la requette de l'utilisateur a la BDD
         async CreateUser(){
          this.DialogCreateUser =false
          if (this.LoginCreate !== "" && this.passwordCreate !== "" && this.email !=="") {
            
            await Api.CreateAccount(this.LoginCreate,this.passwordCreate,this.email)
          }
          
        },//Permet de créé un user dans la bdd
        GoHome(){
            this.$router.push({
                name:"Accueil"
            })
        },
        GoReco(){
          var leUser = JSON.stringify(this.user)
          sessionStorage.setItem("User",leUser)
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
        this.Recherche(StringFinal)
        },//Decoupe la chaine taper par l'utilisateur par des espace mise en forme ('njn',...)
        async Recherche(String){
          this.series = await Api.REcherche(String)
          if (this.IsConnect === true){
            var table = this.StringRecherche.split(" ")
            for (const mot of table) {
             let Nbrecherche = await  Api.TestNbMotRechercher(this.user[0].idu)
              if (Nbrecherche[0].count < 5){
                let theMot =  await Api.TestMotexiste(mot)
                
                if (theMot.length >0){
                  await Api.InsertMot(this.user[0].idu,theMot[0].idm)
                }
              
              }else {
                let oldermot = await Api.OlderMot(this.user[0].idu)
                let theMot = await Api.TestMotexiste(mot)
                
                if (theMot.length > 0) {
                  await Api.UpdateMotRecher(this.user[0].idu, theMot[0].idm,oldermot[0].idm)
                }

              }
              
            }
          }
         
        },//Permet de faire la requette pour la recherche. Prend le un string sous forme ('khbkh',...)
        AddSerie(){
            this.$router.push({
              name:"AddSeries"
            })

        },//Permet d'aller sur la page pour rajouter une serie
        Disconnect(){
              this.IsConnect = false
          this.user = []
          sessionStorage.removeItem("User")
        },//Permet de deconnecter l'utilisateur
      async addRating(Note,Noms){

        let ids = await  Api.GetIDS(Noms)
        let DejaNote = await Api.TestDejanoter(this.user[0].idu,Noms)
        console.log(DejaNote)
        if (DejaNote.length !== 0){
          await Api.UpdateNote(this.user[0].idu,Note,ids[0].ids)
          
        }else{          
          await Api.InsertNote(this.user[0].idu,Note,ids[0].ids)
        }
        

      }
    },
    
})
</script>

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
    <v-col><v-autocomplete
  dense
  rounded
  solo
  :items="series"
  v-model="SeriesSelected"
></v-autocomplete></v-col>
<br>
    <v-col
            cols="12"
            sm="6"
            v-if="SeriesSelected =='Autre' "
          >
            <v-text-field
            v-model="AddNomSerie"
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
    webkitdirectory
    :label="$t('Drop Files')"
    multiple
    prepend-icon="mdi-paperclip"
    @change="read"
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

  <v-col v-if="Succesfull == true">
    <v-col>
    <v-icon x-large class="group pa-2 green">{{icon.mdiCheckBold}}</v-icon>{{$t('Successfully Uploaded')}}
    </v-col>
  </v-col>
  </div>
</template>

<script>
import LocaleLangue from "../i18n" 
import  Api from "../Api"
import { mdiMagnify,mdiPlusBox,mdiCheckBold   } from '@mdi/js';
export default ({

  data :() => ({
      icon:{
        mdiMagnify,
        mdiPlusBox,
        mdiCheckBold
      },
          series :[],
          Succesfull:false,
      files:[],
      AddNomSerie:"",
      SeriesSelected:""
          }),
          async created(){
            this.series = await Api.GetAllSeries()
            var LesSerie = this.series.slice() 
            this.series =[]
            for (const serie of LesSerie) {
              this.series.push(serie.noms)
            }
            this.series.push("Autre")
            console.log(this.series);

          },
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
        },
        async read(){
          
          this.Succesfull = false;
          for(const fichie of this.files) {
            var Nomfichier = fichie.name
            var data = await fichie.text()
            if (this.AddNomSerie !=="") {
              await Api.CopyFichier(Nomfichier,data,this.AddNomSerie)
              
            }else{
              await Api.CopyFichier(Nomfichier,data,this.SeriesSelected)
            }
            
           
          }this.Succesfull = true;
          this.files= [];
          this.AddNomSerie =""
        }

    },

})

</script>
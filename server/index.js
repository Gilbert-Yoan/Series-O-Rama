const express = require("express")
const app = express();
const cors = require("cors")


app.use(express.json());
app.use(cors());


const post = require("./routes/api/api")

app.use("/api",post)

var Port = 1313
if(process.env.NODE_ENV==="production"){
        app.use('/',express.static(__dirname+"/public/"));
        app.get(/.*/,(req,res)=>res.sendFile(__dirname+"/public/index.html"))
        
}

app.listen(Port,()=>console.log("Serveur up !! http/localhost:"+Port))
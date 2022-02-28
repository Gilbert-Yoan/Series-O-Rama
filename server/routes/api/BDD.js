const { log } = require("console");

const pg = require("pg").Pool;


var config = new pg({

host:"Localhost",
user:"postgres",
password:"passroot",
database:"DB",
port:5432
})

config.connect((err)=>{ 
    if (err) throw err
})
config.on('error',(err)=>{
    if (err) {
        throw err
    }
})

const AllSeries =(request,responce)=>{

config.query("SELECT AVG(note) as rating ,serie.noms FROM NOTER join serie on noter.ids = serie.ids group by serie.noms ;",
    (error,result)=>{

        if (error) {
            throw error
        }
        responce.status(200).json(result.rows);
    }
)
}
const UserConnect =(request,responce)=>{
   
    const login = request.body.Login
    const mdp = request.body.Password
    config.query("Select *  from utilisateur where pseudo ='" +login + "' and mdp ='"+mdp+"';",
        (error,result)=>{
    
            if (error) {
                throw error
            }
            console.log(result.rows);
            responce.status(200).json(result.rows);
        }
    )
    }

const CreateAccount =(request,responce)=>{
   
        const login = request.body.Login
        const mdp = request.body.Password
        const email = request.body.email
        config.query("INSERT INTO utilisateur(pseudo,mail,mdp,isAdmin) VALUES('"+login+"','" +email+"','"+mdp+"',false) ;",
            (error,result)=>{
        
                if (error) {
                    throw error
                }
                console.log(result.rows);
                responce.status(200).json(result.rows);
            }
        )
        }

module.exports ={

AllSeries,
UserConnect,
CreateAccount
}

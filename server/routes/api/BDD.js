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



module.exports ={

AllSeries

}

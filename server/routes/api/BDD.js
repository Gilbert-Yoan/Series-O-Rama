

const pg = require("pg").Pool;
const fs = require("fs");
const {spawn} = require("child_process")

var config = new pg({

host:"localhost",
user:"serieorama",
password:"passroot",
database:"serieorama",
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

config.query("SELECT AVG(note)::numeric(10,1) as rating ,serie.noms FROM NOTER join serie on noter.ids = serie.ids group by serie.noms ;",
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
                
                responce.status(200).json(result.rows);
            }
        )
        }
const REcherche =(request,responce)=>{
   
const string = request.body.String
 
    config.query("SELECT s.*, COUNT(s.ids), SUM(c.occurence),AVG(note)::numeric(10,1) as rating FROM SERIE s, CONTENIR c, MOT m ,noter n " +
        "WHERE s.ids = c.ids AND m.idm = c.idm and n.ids = s.ids AND m.mot IN "+string +" GROUP BY s.ids ORDER BY COUNT(s.ids) DESC,SUM(c.occurence) DESC; ",
                (error,result)=>{
            
                    if (error) {
                        throw error
                    }
                    
                    responce.status(200).json(result.rows);
                }
            )
            }
const GETRecoRAND =(request,responce)=>{

    config.query("SELECT AVG(note)::numeric(10,1) as rating ,serie.noms\n" +
        "FROM NOTER join serie on noter.ids = serie.ids group by serie.noms order by random() limit 20;",
        (error,result)=>{

            if (error) {
                throw error
            }
            responce.status(200).json(result.rows);
        }
    )
}
const TestNoter =(request,responce)=>{
    const Idu = request.body.Idu
    config.query(
        "Select * from noter where idu = "+Idu,
        (error,result)=> {

            if (error) {
                throw error
            }
            responce.status(200).json(result.rows);
        }
    )
}
const RecomendationViaLike =(request,responce)=>{
    const Idu = request.body.Idu
    const Ids = request.body.ids

    config.query(
        "WITH MOYENNES AS (SELECT idu, AVG(note) AS moy FROM NOTER GROUP BY idu),"+ 
        "NOTES_RETRANCHES AS (SELECT m.idu,n.ids, note-moy AS note FROM NOTER n, MOYENNES m WHERE m.idu IN (SELECT idu FROM NOTER WHERE ids IN (SELECT ids FROM NOTER WHERE idu="+Idu+")) AND m.idu = n.idu),"+ 
        "HAUT_SIMILARITES AS (" +
        "   SELECT SUM(n.note*n2.note)as somme,n.idu " +
        "    FROM NOTES_RETRANCHES n, NOTES_RETRANCHES n2 " +
        "    WHERE n.idu!=n2.idu AND n2.idu=3 AND n.ids=n2.ids " +
        "    GROUP BY n.idu)," +
        "BAS_SIMILARITES AS (" +
        "    SELECT SQRT(SUM(POWER(n.note,2))*SUM(POWER(n2.note,2))) as racine, n.idu " +
        "    FROM NOTES_RETRANCHES n, NOTES_RETRANCHES n2 " +
        "     WHERE n.idu!=n2.idu AND n2.idu=3 AND n.ids=n2.ids" +
        "    GROUP BY n.idu)," +
        "SIMILARITES AS (SELECT somme/racine as similarite, h.idu FROM HAUT_SIMILARITES h,BAS_SIMILARITES b WHERE h.idu=b.idu)," +
        "PARTIE_HAUTE AS (SELECT SUM(n.note*s.similarite) as haute FROM NOTES_RETRANCHES n, SIMILARITES s WHERE n.idu = s.idu AND n.ids = " + Ids+")," +
        "SOMME_SIMILARITES AS (SELECT SUM(ABS(similarite)) as sim FROM SIMILARITES)" +
        " SELECT (moy+(haute/sim))::numeric(10,1) as rating FROM MOYENNES m, PARTIE_HAUTE p, SOMME_SIMILARITES s WHERE m.idu ="+Idu+";",
        (error,result)=> {

            if (error) {
                throw error
            }
            responce.status(200).json(result.rows);
        }
    )
}

const SerieNonNoter =(request,responce)=>{
    const Idu = request.body.Idu
    config.query(
        "Select noms,serie.ids from serie where ids not in (Select ids from noter where idu = "+Idu + ")",
        (error,result)=> {

            if (error) {
                throw error
            }
            responce.status(200).json(result.rows);
        }
    )
}
const RechercheTest =(request,responce)=>{
    const Idu = request.body.Idu
    config.query(
        "Select * from chercher where idu="+Idu,
        (error,result)=> {

            if (error) {
                throw error
            }
            responce.status(200).json(result.rows);
        }
    )
}
const RecoViaRecherche =(request,responce)=>{
    const Idu = request.body.Idu
    console.log(Idu)
    config.query(
        "SELECT s.ids, s.nomS,  AVG(n.note)::numeric(10,1) as rating FROM serie s, contenir c, noter n " +
        "WHERE c.ids = n.ids AND c.ids = s.ids " +
        "AND c.idm IN (SELECT idm FROM CHERCHER WHERE idu="+Idu+")" +
        "GROUP BY s.ids, s.nomS;",
        (error,result)=> {

            if (error) {
                throw error
            }
            responce.status(200).json(result.rows);
        }
    )
}
const TestNbMotRechercher =(request,responce)=>{
    const Idu = request.body.Idu
    config.query(
        "Select COUNT(*) from chercher where idu= "+Idu 
        ,
        (error,result)=> {

            if (error) {
                throw error
            }
            responce.status(200).json(result.rows);
        }
    )
}
const OlderMot =(request,responce)=>{
    const Idu = request.body.Idu
    config.query(
        
        "Select Min(date_rech),idm,mot from chercher join mot using(idm) where idu= "+Idu+" group by idm , mot Limit 1 "
        ,
        (error,result)=> {

            if (error) {
                throw error
            }
            responce.status(200).json(result.rows);
        }
    )
}
const TestMotexiste =(request,responce)=>{
    const Mot = request.body.Mot
    config.query(

        "Select * from mot where LOWER(mot) = LOWER('"+Mot+"')"
        ,
        (error,result)=> {

            if (error) {
                throw error
            }
            responce.status(200).json(result.rows);
        }
    )
}
const UpdateMotRecher =(request,responce)=>{
    const idm = request.body.idm
    const idu = request.body.idu
    const idom = request.body.idom

    console.log(idm)
    console.log(idu)
    console.log(idom)

    config.query(

        "Update chercher set idm ="+idm+" ,date_rech = now() where idu = "+idu+" and idm ="+idom+" ;"
        ,
        (error,result)=> {

            if (error) {
                throw error
            }
            responce.status(200).json(result.rows);
        }
    )
}
const InsertMot =(request,responce)=>{
    const idm = request.body.idm
    const idu = request.body.idu
    
    config.query(

        "Insert into chercher VALUES("+idu+","+idm+",now()) "
        ,
        (error,result)=> {

            if (error) {
                throw error
            }
            responce.status(200).json(result.rows);
        }
    )
}
const TestDejanoter =(request,responce)=>{
    const idu = request.body.idu
    const Nom = request.body.Serie
    config.query(

        "Select * from noter join Serie using(ids) where noms = '"+Nom+"' and idu="+idu +" ;"
        ,
        (error,result)=> {

            if (error) {
                throw error
            }
            responce.status(200).json(result.rows);
        }
    )
}
const InsertNote =(request,responce)=>{
    const idu = request.body.idu

    const Note = request.body.Note
    const ids = request.body.ids

    config.query(

        "Insert into noter VALUES("+ids+","+idu+","+Note+") "
        ,
        (error,result)=> {

            if (error) {
                throw error
            }
            responce.status(200).json(result.rows);
        }
    )
}
const GetIds =(request,responce)=>{
    const Noms = request.body.Noms
    console.log(Noms)
    config.query(

        "Select ids from Serie where noms = '"+Noms +"' ;" 
        ,
        (error,result)=> {

            if (error) {
                throw error
            }
            responce.status(200).json(result.rows);
        }
    )
}
const  UPDAteNote=(request,responce)=>{
    const ids = request.body.ids
    const  idu= request.body.idu
    const note = request.body.note
    
    config.query(

        "Update noter set note = " +note+ " where idu =" +idu+ " and ids="+ids+";"
        ,
        (error,result)=> {

            if (error) {
                throw error
            }
            responce.status(200).json(result.rows);
        }
    )
}

const  CopyFichier=(request,responce)=>{

    var  Nomfichier = request.body.Nomfichier
    
    const  Data= request.body.Text
    const  NomSerie= request.body.NomSerie

    if (!fs.existsSync("../DELTA/"+NomSerie)){
        fs.mkdirSync("../DELTA/"+NomSerie, { recursive: true });
    }
    Nomfichier = "../DELTA/" + NomSerie + "/"+Nomfichier
    fs.writeFile(Nomfichier, Data, err2 => {
        if (err2) {
          console.log(err2);
          return;
        }
        responce.status(200).json(true);
    })

}

const  PythonRecherche=(request,responce)=>{
    const Chaine=request.body.Chaine
    console.log(Chaine)

   const process = spawn('python',['../app/search_queries/DEMO TFIDF.py',Chaine])
   var datatostring
   process.stdout.on('data',(data) =>{

        datatostring = data

   })
   process.stderr.on('data',(data)=>{

    console.log('err:' + data)

   })
   process.on('close',(code)=>{

    responce.send(datatostring)


   })
}
const  IsCherchermot=(request,responce)=>{
    const idm = request.body.idm
    const  idu= request.body.idu
    
    
    config.query(

        "Select * from chercher where idm= "+idm+" and idu=" +idu +";"
        ,
        (error,result)=> {

            if (error) {
                throw error
            }
            responce.status(200).json(result.rows);
        }
    )
}
module.exports ={

AllSeries,
UserConnect,
CreateAccount,
REcherche, 
GETRecoRAND,
TestNoter,
    RecomendationViaLike,
    SerieNonNoter,
    RechercheTest,
    RecoViaRecherche,
    TestNbMotRechercher,
    OlderMot,
    InsertMot,
    TestMotexiste,
    UpdateMotRecher,
    TestDejanoter,
    InsertNote,
    GetIds,
    UPDAteNote,
    CopyFichier,
    PythonRecherche,
    IsCherchermot
}

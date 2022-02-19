import axios from "axios";



class Api {

static GetAllSeries(){

    return new Promise((resolve,reject)=>{

        axios.post("api/AllSeries")
        .then((res)=>{

            const data = res.data;
            resolve(data)
        })
        .catch((err)=>{
            reject(err)
        
        
        });

    });

}




}//classe

export default Api;
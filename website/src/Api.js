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
static UserConnect(Login , Password){

    return new Promise((resolve,reject)=>{

        axios.post("api/UserConnect",{
            Login:Login,
            Password: Password

        })
        .then((res)=>{

            const data = res.data;
            resolve(data)
        })
        .catch((err)=>{
            reject(err)
        
        
        });

    });

}
static CreateAccount(Login , Password,email){

    return new Promise((resolve,reject)=>{

        axios.post("api/CreateAccount",{
            Login:Login,
            Password: Password,
            email: email

        })
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
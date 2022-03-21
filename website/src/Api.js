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
static REcherche(String){

    return new Promise((resolve,reject)=>{

        axios.post("api/REcherche",{
            String:String
            

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
static GetRecoRAND(){

        return new Promise((resolve,reject)=>{

            axios.post("api/GETRecoRAND")
                .then((res)=>{

                    const data = res.data;
                    resolve(data)
                })
                .catch((err)=>{
                    reject(err)


                });

        });

    }
static TestNoter(Idu){

        return new Promise((resolve,reject)=>{

            axios.post("api/TestNoter", {Idu:Idu})
                .then((res)=>{

                    const data = res.data;
                    resolve(data)
                })
                .catch((err)=>{
                    reject(err)


                });

        });

    }
static RecomendationViaLike(idu,ids){

        return new Promise((resolve,reject)=>{

            axios.post("api/RecomendationViaLike", {Idu:idu,ids:ids})
                .then((res)=>{

                    const data = res.data;
                    resolve(data)
                })
                .catch((err)=>{
                    reject(err)


                });

        });

    }
static SerieNonNoter(Idu){

        return new Promise((resolve,reject)=>{

            axios.post("api/SerieNonNoter", {Idu:Idu})
                .then((res)=>{

                    const data = res.data;
                    
                    resolve(data)
                })
                .catch((err)=>{
                    reject(err)


                });

        });

    }
    static RechercheTest (Idu){

        return new Promise((resolve,reject)=>{

            axios.post("api/RechercheTest", {Idu:Idu})
                .then((res)=>{

                    const data = res.data;

                    resolve(data)
                })
                .catch((err)=>{
                    reject(err)


                });

        });

    }
    static RecoViaRecherche (Idu){

        return new Promise((resolve,reject)=>{

            axios.post("api/RecoViaRecherche", {Idu:Idu})
                .then((res)=>{

                    const data = res.data;

                    resolve(data)
                })
                .catch((err)=>{
                    reject(err)


                });

        });

    }
    static TestNbMotRechercher (Idu){

        return new Promise((resolve,reject)=>{

            axios.post("api/TestNbMotRechercher", {Idu:Idu})
                .then((res)=>{

                    const data = res.data;

                    resolve(data)
                })
                .catch((err)=>{
                    reject(err)


                });

        });

    }
    static OlderMot (Idu){

        return new Promise((resolve,reject)=>{

            axios.post("api/OlderMot", {Idu:Idu})
                .then((res)=>{

                    const data = res.data;

                    resolve(data)
                })
                .catch((err)=>{
                    reject(err)


                });

        });

    }
    static TestMotexiste (Mot){

        return new Promise((resolve,reject)=>{

            axios.post("api/TestMotexiste", {Mot:Mot})
                .then((res)=>{

                    const data = res.data;

                    resolve(data)
                })
                .catch((err)=>{
                    reject(err)


                });

        });

    }
    static UpdateMotRecher (idu,idm,idom){

        return new Promise((resolve,reject)=>{

            axios.post("api/UpdateMotRecher", {idu:idu,idm:idm,idom:idom})
                .then((res)=>{

                    const data = res.data;

                    resolve(data)
                })
                .catch((err)=>{
                    reject(err)


                });

        });

    }
    static InsertMot (idu,idm){

        return new Promise((resolve,reject)=>{

            axios.post("api/InsertMot", {idu:idu,idm:idm})
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
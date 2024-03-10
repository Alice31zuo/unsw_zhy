import API from './api.js';
// A helper you may want to use when uploading new images to the server.
import { fileToDataUrl } from './helpers.js';

// This url may need to change depending on what port your backend is running
// on.
const api = new API('http://localhost:5000');

// Example usage of makeAPIRequest method.
api.makeAPIRequest('dummy/user')
    .then(r => console.log(r));

const timeTransfrom = (time) =>{
    var date = new Date(parseInt(time)); // 增加8小时
    console.log(date)
    return date.toJSON().substr(0, 19).replace('T', ' ');
}

// let LogSuccess = false

const basicFeed = () =>{
    // document.getElementById("registrationTable").style.display = "None" ;
    document.getElementById("afterLogIn").style.display = "block" ;
    const result = fetch('http://localhost:5000/user/feed',{
            method : "GET",
            headers : {
                'Accept' :'application/json' ,
                'Content-Type' :'application/json',
                // 'Authorization' : 'Token ' + document.getElementById("id").value
                'Authorization' : 'Token ' + document.getElementById("token").innerText,
            },
        }).then((data) => {
            if (data.status ===403){
                alert('Incorect Authorization information')
            }else if(data.status ===200){
                data.json().then(data =>{
                    const posts = data["posts"];
                    // console.log(posts)
                    document.getElementById("afterLogIn").style.display = "flex"
                    getFllowingUser(document.getElementById("signInUserName").value);
                    userProfile();
                    posts.map(post=>{
                    const postcontent = document.createElement('div');
                    postcontent.className = "post";
                    const buttonupArea = document.createElement('div');
                    buttonupArea.className = "PostbuttonUp"
                    const buttondownArea = document.createElement('div');
                    buttondownArea.className ="ostbuttonButtom"

                    const authorElement = document.createElement("input");

                    authorElement.type = "button";
                    authorElement.value = post.meta.author ;

                    authorElement.addEventListener("click", ()=>{pressUser(authorElement.value)}); //can function
                    buttonupArea.appendChild(authorElement)
                    
                    const postTime = document.createElement('div');
                    console.log(post.meta.published)
                    postTime.innerText = timeTransfrom(post.meta.published)
                    
                    buttonupArea.appendChild(postTime)
                    postcontent.appendChild(buttonupArea)

                    // postcontent.appendChild(buttonupArea)

                    // const idElement = document.createElement("div")
                    // idElement.innerText = post.id ;
                    // idElement.style.display = "none"
                    // postcontent.appendChild(idElement)

                    const descElement = document.createElement("div")

                    descElement.innerText = post.meta.description_text ;
                    postcontent.appendChild(descElement)

                    const imageElement = document.createElement("img");

                    imageElement.setAttribute("src",'data:image/jpeg;base64,${post.thumbnail}');
                    postcontent.appendChild(imageElement);

                    const likeElement = document.createElement("input")
                    likeElement.type = "button";
                    likeElement.value = "like" ;
                    likeElement.name = "like";
                    likeElement.addEventListener("click", ()=>{pressLike(post.id)}); 
                    buttondownArea.appendChild(likeElement)

                    const unlikeElement = document.createElement("input")
                    unlikeElement.type = "button";
                    unlikeElement.value = "unlike";
                    unlikeElement.name = "unlike";
                    unlikeElement.addEventListener("click", ()=>{pressUnLike(post.id)}); 
                    buttondownArea.appendChild(unlikeElement)

                    const likeNumElement = document.createElement("input")
                    likeNumElement.type = "button";

                    likeNumElement.value = post.meta.likes.length ;

                    likeNumElement.name = "likeNum";
                    likeNumElement.addEventListener("click", ()=>{pressshowLike(post.id,"","1")}); 
  
                    buttondownArea.appendChild(likeNumElement)

                    const CommentNumElement = document.createElement("input")
                    CommentNumElement.type = "button";
                    CommentNumElement.value = 'comments : ' + post.comments.length;
                    CommentNumElement.name = "commentNUM";
                    CommentNumElement.addEventListener("click",()=>{pressshowComment(post.id,"","1")})

                    // console.log(post.comments)
                    buttondownArea.appendChild(CommentNumElement)
                    postcontent.appendChild(buttondownArea)
                    document.getElementById("postArea").appendChild(postcontent)
                    ////////////////
                    
                })
            })
        }
    })
}



const  signInSubmit = () => {
    let UserName = document.getElementById("signInUserName").value ;
    let Password = document.getElementById("signInUserPassword").value ;
    let CPassword = document.getElementById("signInUserPasswordC").value ;
    if (Password === CPassword){
        const loginBody = {
            "username": UserName,
            "password": Password
        }
        const result = fetch('http://localhost:5000/auth/login',{
            method : "POST",
            headers : {
                'Accept' :'application/json',
                'Content-Type' :'application/json'
            },
            body:JSON.stringify(loginBody),
        }).then((data) => {
            if (data.status ===403){
                alert('Incorect Login information')
            }else if(data.status ===200){
                data.json().then(result => {
                    document.getElementById("signIn").style.display = "None";
                    document.getElementById("token").innerText = result.token;
                    console.log(result);
                    basicFeed() ;
                })
                console.log(data)
            }else{
                alert('please insert full infortmation') ;
            }
        }).catch((error) => {
            console.log("error" ,error) ;
        })
    }
    else{
        alert('please insert same password')
    }
}
document.getElementById("signInUserSubmit").addEventListener("click",()=> {signInSubmit()}) ;

const  registrate = () => {
    document.getElementById("signIn").style.display = "None" ;
    document.getElementById("registration").style.display = "block" ;
}

const registrateReturn = () =>{ 
    document.getElementById("signIn").style.display = "block" ;
    document.getElementById("registration").style.display = "None" ;
}

const registrateSubmit = () =>{
    let UserName =document.getElementById("registrationUserName").value ;
    let Password = document.getElementById("registrationUserPassword").value ;
    let CPassword = document.getElementById("registrationUserPasswordC").value ;
    let UserEmail = document.getElementById("registrationUserEmail").value ;
    let Name= document.getElementById("registrationName").value ;
    if (Password === CPassword){
        const registrateBody = {
            "username": UserName,
            "password": Password,
            "email" : UserEmail,
            "name" :Name
        }
        const result = fetch('http://localhost:5000/auth/signup',{
            method : "POST",
            headers : {
                'Accept' :'application/json' ,
                'Content-Type' :'application/json'
            },
            body:JSON.stringify(registrateBody),
        }).then((data) => {
            if (data.status ===409){
                alert('Username has already taken') ;
            }else if(data.status ===200){
                document.getElementById("registration").style.display = "None" ;
                document.getElementById("signIn").style.display = "block";         // sign in again or sign in directly?
            }else{
                alert('please insert full infortmation') ;
            }
        }).catch((error) => {
            console.log("error" ,error) ;
        })
    }
    else{
        alert('please insert same password') ;
    }

}

document.getElementById("registrationSubmit").addEventListener("click",()=> {registrate()}) ;
document.getElementById("registrationUserReturn").addEventListener("click",()=> {registrateReturn()}) ;
document.getElementById("registrationUserSubmit").addEventListener("click",()=> {registrateSubmit()}) ;
////////

const userProfile= () =>{
    const url = 'http://localhost:5000/user/?' + "username="+document.getElementById("signInUserName").value;
    const result = fetch(url,{
        method : "GET",
        headers : {
            'Accept' :'application/json' ,
            'Content-Type' :'application/json',
            'Authorization' : 'Token ' + document.getElementById("token").innerText,

        },
    }).then((data) => {
        if (data.status ===404){
            alert('User is not exist') ;
        }else if(data.status ===403){
            alert('please log in first') ;
        }else if(data.status ===400){
            alert('wrong request') ;
        }else if(data.status ===200){
            data.json().then(data =>{
                console.log(data)
                console.log("insidepressuser")
                // const Uprofilediv = document.createElement('div');
                const UprofileContent = document.getElementById("userInfoMain")

                const UidPart = document.getElementById("UidPart");
                const UauthorElementID = document.createElement("div");
                const UauthorElementIDlabel = document.createElement("label");
                UauthorElementIDlabel.innerText = "ID :"
                UauthorElementID.id ="authorElementID"
                UauthorElementIDlabel.for = "authorElementID"
                UauthorElementID.innerText = data.id;
                UidPart.appendChild(UauthorElementIDlabel);
                UidPart.appendChild(UauthorElementID);
                UprofileContent.append(UidPart)


                const UuserNamePart = document.getElementById("UuserNamePart");
                // UuserNamePart.className = "Uprofileblock"
                const UauthorElementNamelabel = document.createElement("label");
                const UauthorElementName = document.createElement("div");
                UauthorElementName.innerText = data.name;
                console.log(data.name);
                UauthorElementName.id = "authorElementName"
                UauthorElementNamelabel.for = "authorElementName"
                UauthorElementNamelabel.innerText = "Name :"
                UuserNamePart.appendChild(UauthorElementNamelabel) ;
                UuserNamePart.appendChild(UauthorElementName)                 
                UprofileContent.appendChild(UuserNamePart);
                
                const UuserEmailPart = document.getElementById("UuserEmailPart");
                // UuserEmailPart.className = "Uprofileblock"
                const UauthorElementEmail = document.createElement("div");
                const UauthorElementEmaillabel = document.createElement("label");
                UauthorElementEmail.id = "authorElementEmail"
                UauthorElementEmaillabel.for = "authorElementEmail"
                UauthorElementEmaillabel.innerText = "Email :"
                UauthorElementEmail.innerText = data.email;
                UuserEmailPart.appendChild(UauthorElementEmaillabel)
                UuserEmailPart.appendChild(UauthorElementEmail)
                UprofileContent.appendChild(UuserEmailPart);

                const UuserRnamePart = document.getElementById("UuserRnamePart");
                UuserRnamePart.className = "Uprofileblock"
                const UauthorElementRname = document.createElement("div");
                const UauthorElementRnamelabel = document.createElement("label");

                UauthorElementRname.innerText = data.username;
                console.log(UauthorElementRname.innerText);
                UauthorElementRname.id = "authorElementRname";
                UauthorElementRnamelabel.for = "authorElementRname";
                UauthorElementRnamelabel.innerText = "User Name :";
                UuserRnamePart.appendChild(UauthorElementRnamelabel);
                UuserRnamePart.appendChild(UauthorElementRname);

                UprofileContent.appendChild(UuserRnamePart);
                

                const UuserFnumPart = document.getElementById("UuserFnumPart");
                UuserFnumPart.className = "Uprofileblock"
                const UauthorElementFnumlabel = document.createElement("label");
                const UauthorElementFnum = document.createElement("div");

                UauthorElementFnum.innerText = data.followed_num;
                UauthorElementFnum.id = "authorElementFnum";
                UauthorElementFnumlabel.for = "authorElementFnum"
                UauthorElementFnumlabel.innerText = "follower number:"
                UuserFnumPart.appendChild(UauthorElementFnumlabel)
                UuserFnumPart.appendChild(UauthorElementFnum)
                UprofileContent.appendChild(UuserFnumPart);
                
                
                const Uauthorchange = document.createElement("input")
                Uauthorchange.type = "button";
                Uauthorchange.value = "change profile";

                Uauthorchange.addEventListener("click", ()=>{updatePofileInfo("","1")}); 
                UprofileContent.appendChild(Uauthorchange)

                const UauthorPost = document.createElement("input")
                UauthorPost.type = "button";
                UauthorPost.value = "own Page";
            
                UauthorPost.addEventListener("click", ()=>{pressUser(data.username)}); 
                UprofileContent.appendChild(UauthorPost)

                // const Uprofile = document.getElementById("userInfoMain");
                // Uprofile.appendChild(UprofileContent)
                })}
            
})}

//////////////
const getFllowingUser = (UserName)=>{
    const url = 'http://localhost:5000/user/?' + "username="+UserName;
    const result = fetch(url,{
        method : "GET",
        headers : {
            'Accept' :'application/json' ,
            'Content-Type' :'application/json',
            'Authorization' : 'Token ' + document.getElementById("token").innerText,

        },
    }).then((data) => {
        if (data.status ===404){
            alert('User is not exist') ;
        }else if(data.status ===403){
            alert('please log in first') ;
        }else if(data.status ===400){
            alert('wrong request') ;
        }else if(data.status ===200){
            data.json().then(data =>{
                // console.log("ueah")
                const followingUserPart = document.getElementById("followList")
                for(let i = 0 ; i <data.following.length ; i++){
                    console.log(data.following.length)
                    console.log(data.following)
                    const followingUser = document.createElement("input")
                    followingUser.type = "button";
                    // authorElementunFollow .value = "unfollow" ;
                    GetUserName(data.following[i],followingUser)
                    followingUser.addEventListener("click",() =>{pressUser(followingUser.value)})
                    followingUserPart.appendChild(followingUser)
                }            
                }).catch((error) => {console.log("error" ,error) ;}) ///for end
            }}).catch((error) => {console.log("error" ,error) ;})
}

///////////////main page get the user info 


/////////////////////////start to add the like and comment function 
const pressLike = (postId) =>{
    console.log(postId)
    // postId 
    const url ="http://localhost:5000/post/like?" + "id=" +postId
    const result = fetch(url,{
        method : "PUT",
        headers : {
            'Accept' :'application/json' ,
            'Content-Type' :'application/json',
            'Authorization' : 'Token ' + document.getElementById("token").innerText,
            // "id" :String(postId)
            // "id" :postId
        },
    }).then((data) => {
        if (data.status ===404){
            alert('post is not exist') ;
        }else if(data.status ===403){
            alert('please log in first') ;
        }else if(data.status ===400){
            alert('wrong request') ;
        }else{
            // alert('success') ;
        }
    }).catch((error) => {
        console.log("error" ,error) ;
    })
}

const pressUnLike = (postId) =>{
    const url ="http://localhost:5000/post/unlike?" + "id=" +postId
    const result = fetch(url,{
        method : "PUT",
        headers : {
            'Accept' :'application/json' ,
            'Content-Type' :'application/json',
            'Authorization' : 'Token ' + document.getElementById("token").innerText,

        },
    }).then((data) => {
        if (data.status ===404){
            alert('post is not exist') ;
        }else if(data.status ===403){
            alert('please log in first') ;
        }else if(data.status ===400){
            alert('wrong request') ;
        }else{
            // alert('success') ; updata
        }
    }).catch((error) => {
        console.log("error" ,error) ;
    })
}


///show likes
const pressshowLike = (PostId,element,num) =>{
    const url = 'http://localhost:5000/post/?id=' + PostId
    const result = fetch(url,{
            method : "GET",
            headers : {
                'Accept' :'application/json' ,
                'Content-Type' :'application/json',

                'Authorization' : 'Token ' + document.getElementById("token").innerText,
            }
        }).then((data) => {
            if (data.status ===404){
                alert('post is not exist') ;
            }else if(data.status ===403){
                alert('please log in first') ;
            }
            else if(data.status ===400){
                alert('wrong request') ;
            }
            else if(data.status ===200){
                document.getElementById("afterLogIn").style.display = "None"
                if (element !== ""){
                    element.style.display = "None"
                }
                data.json().then(data =>{        
                    let likeArray = data.meta.likes 
                    const postLikeUser = document.createElement('div'); //remmber to delete it         
                    for (let i = 0 ; i < likeArray.length ; i++){
                        const likeUserElement = document.createElement("input")
             
                        likeUserElement.type = "button";
                       
                        GetUserName(data.meta.likes[i],likeUserElement)
                      
                        postLikeUser.appendChild(likeUserElement);
                    }
                    const existlikeUserElement = document.createElement("input");
                    existlikeUserElement.type = "button";
                    existlikeUserElement.value = "return";   //use this to close the like 
                    existlikeUserElement.addEventListener("click",()=>{returncode(postLikeUser,element,num)});
                    postLikeUser.appendChild(existlikeUserElement);
                    const mianpage = document.getElementById("test")
                    mianpage.appendChild(postLikeUser)
                })
            }
        })
}
const returncode = (element,element1,judge) =>{
    if (judge === "1"){
        document.getElementById("test").removeChild(element);
        document.getElementById("afterLogIn").style.display = "flex";
    }
    else{
        console.log(element1)
        element1.style.display ="flex";
        document.getElementById("test").removeChild(element);
    }

}

const GetUserName= (UserId,element) =>{
    const url = 'http://localhost:5000/user/?id='+UserId 
    const result = fetch(url,{
        method : "GET",
        headers : {
            'Accept' :'application/json' ,
            'Content-Type' :'application/json',
            'Authorization' : 'Token ' + document.getElementById("token").innerText,

        },
    }).then((data) => {
        if (data.status ===404){
            alert('User is not exist') ;
        }else if(data.status ===403){
            alert('please log in first') ;
        }else if(data.status ===400){
            alert('wrong request') ;
        }else if(data.status ===200){
            data.json().then(data =>{
            element.value = data.username
        })}}).catch((error) => {console.log("error" ,error) ;})
}


////show comment
const pressshowComment = (PostId,element,num) =>{
    const url = 'http://localhost:5000/post/?id=' + PostId

    const result = fetch(url,{
            method : "GET",
            headers : {
                'Accept' :'application/json' ,
                'Content-Type' :'application/json',
                'Authorization' : 'Token ' + document.getElementById("token").innerText,
            }
        }).then((data) => {
            document.getElementById("afterLogIn").style.display = "None"
            if (element !== ""){
                element.style.display = "None"
            }
            if (data.status ===404){
                alert('post is not exist') ;
            }else if(data.status ===403){
                alert('please log in first') ;
            }
            else if(data.status ===400){
                alert('wrong request') ;
            }
            else if(data.status ===200){
                data.json().then(data =>{    
                    document.getElementById("afterLogIn").style.display = "None"
                    if (element !== ""){
                        element.style.display = "None"
                    }
                    let commentsArray = data.comments
                    const postcommentsUser = document.createElement('div'); //remmber to delete it  
        
                    const inputcommentsElement = document.createElement("input");
                    inputcommentsElement.type = "text";

                    inputcommentsElement.id = "inputcommentsElement"
                    postcommentsUser.appendChild(inputcommentsElement);

                    const commentsElementsubmit = document.createElement("input");
                    commentsElementsubmit.type = "button";
                    commentsElementsubmit.value = "submit";   /////this place add the return function ,remove the div
                    commentsElementsubmit.addEventListener("click",()=>{commentPost(PostId)})
                    postcommentsUser.appendChild(commentsElementsubmit);

                    for (let i = 0 ; i < commentsArray.length ; i++){
                        
                        const commentsUserElement =  document.createElement("input")
    
                        commentsUserElement.type = "button"
                        
                        
                        commentsUserElement.value = commentsArray[i].author;
                        commentsUserElement.addEventListener("click", ()=>{pressUser(commentsUserElement.value)});
                        
                        postcommentsUser.appendChild(commentsUserElement);

                        
                        const commentsUserElementdes = document.createElement("div")

                        commentsUserElementdes.innerText = commentsArray[i].comment;
                        postcommentsUser.appendChild(commentsUserElementdes);

                        const commentsUserElementTime = document.createElement("div")

                        commentsUserElementTime.innerText = commentsArray[i].published;
                        postcommentsUser.appendChild(commentsUserElementTime);

                    }
                    const existcommentsElement = document.createElement("input");
                    existcommentsElement.type = "button";
                    existcommentsElement.value = "return";   /////this place add the return function ,remove the div
                    existcommentsElement.addEventListener("click",()=>{returncode(postcommentsUser,element,num)});
                    postcommentsUser.appendChild(existcommentsElement);
                    const mianpage = document.getElementById("test")
                    mianpage.appendChild(postcommentsUser)
                })
            }
    })
}
//Feed Pagination??

const commentPost =(postId) =>{ 
    console.log(document.getElementById("inputcommentsElement").value)
    const url = 'http://localhost:5000/post/comment?id=' +postId
    const commentBody = {
        "comment": document.getElementById("inputcommentsElement").value,
    }
    const result = fetch(url ,{
        method : "PUT",
        headers : {
            'Accept' :'application/json' ,
            'Content-Type' :'application/json',
            'Authorization' : 'Token ' + document.getElementById("token").innerText,
        },
        body:JSON.stringify(commentBody),
    }).then((data) => {
        if(data.status ===403){
            alert('please log in first') ;
        }else if(data.status ===400){
            alert('wrong request') ;
        }else if(data.status ===404){
            alert('post not exist') ;
        }
    }).catch((error) => {
        console.log("error" ,error) ;
    })
}


///follow

const pressFollow = (userName) =>{
    const url = 'http://localhost:5000/user/follow' +"?username=" + userName
    const result = fetch(url,{
        method : "PUT",
        headers : {
            'Accept' :'application/json' ,
            'Content-Type' :'application/json',
            'Authorization' : 'Token ' + document.getElementById("token").innerText,
        },
    }).then((data) => {
        if (data.status ===404){
            alert('User is not exist') ;
        }else if(data.status ===403){
            alert('please log in first') ;
        }else if(data.status ===400){
            alert('wrong request') ;
        }
    }).catch((error) => {
        console.log("error" ,error) ;
    })
}

//unfollow
const pressUnFollow = (userName) =>{
    const url = 'http://localhost:5000/user/unfollow' +"?username=" + userName
    const result = fetch(url,{
        method : "PUT",
        headers : {
            'Accept' :'application/json' ,
            'Content-Type' :'application/json',
            'Authorization' : 'Token ' + document.getElementById("token").innerText,
        },
    }).then((data) => {
        if(data.status ===403){
            alert('please log in first') ;
        }else if(data.status ===400){
            alert('wrong request') ;
        }
    }).catch((error) => {
        console.log("error" ,error) ;
    })
}

//user profile
const pressUser= (pressUseName ) =>{
    const url = 'http://localhost:5000/user/?' + "username="+pressUseName
    const result = fetch(url,{
        method : "GET",
        headers : {
            'Accept' :'application/json' ,
            'Content-Type' :'application/json',
            'Authorization' : 'Token ' + document.getElementById("token").innerText,

        },
    }).then((data) => {
        if (data.status ===404){
            alert('User is not exist') ;
        }else if(data.status ===403){
            alert('please log in first') ;
        }else if(data.status ===400){
            alert('wrong request') ;
        }else if(data.status ===200){
            data.json().then(data =>{
                document.getElementById("afterLogIn").style.display = "None";
                console.log("insidepressuser")
                const profilediv = document.createElement('div');
                const profileContent = document.createElement('div');
                const idPart = document.createElement("div");
                const authorElementID = document.createElement("div");
                const authorElementIDlabel = document.createElement("label");
                authorElementIDlabel.innerText = "ID :"
                authorElementID.id ="authorElementID"
                authorElementIDlabel.for = "authorElementID"
                authorElementID.innerText = data.id;
                idPart.appendChild(authorElementIDlabel);
                idPart.appendChild(authorElementID);
                idPart.className = "Uprofileblock"
                profileContent.append(idPart)


                const userNamePart = document.createElement("div");
                const authorElementNamelabel = document.createElement("label");
                const authorElementName = document.createElement("div");
                authorElementName.innerText = data.username;
                authorElementName.id = "authorElementName"
                authorElementNamelabel.for = "authorElementName"
                authorElementNamelabel.innerText = "Name :"
                userNamePart.appendChild(authorElementNamelabel) ;
                userNamePart.appendChild(authorElementName)  
                userNamePart.className = "Uprofileblock"               
                profileContent.appendChild(userNamePart);
                
                const userEmailPart = document.createElement("div");
                const authorElementEmail = document.createElement("div");
                const authorElementEmaillabel = document.createElement("label");
                authorElementEmail.id = "authorElementEmail"
                authorElementEmaillabel.for = "authorElementEmail"
                authorElementEmaillabel.innerText = "Email :"
                authorElementEmail.innerText = data.email;
                userEmailPart.appendChild(authorElementEmaillabel)
                userEmailPart.appendChild(authorElementEmail)
                userEmailPart.className = "Uprofileblock"   
                profileContent.appendChild(userEmailPart);

                const userRnamePart = document.createElement("div");
                const authorElementRname = document.createElement("div");
                const authorElementRnamelabel = document.createElement("label");

                authorElementRname.innerText = data.name;
                authorElementRname.id = "authorElementRname";
                authorElementRnamelabel.for = "authorElementRname";
                authorElementRnamelabel.innerText = "User Name :";
                authorElementRnamelabel.className = "Uprofileblock" 
                userRnamePart.appendChild(authorElementRnamelabel);
                userRnamePart.appendChild(authorElementRname);

                profileContent.appendChild(userRnamePart);
                

                const userFnumPart = document.createElement("div");
                const authorElementFnumlabel = document.createElement("label");

                const authorElementFnum = document.createElement("div");

                authorElementFnum.innerText = data.followed_num;
                authorElementFnum.id = "authorElementFnum";
                authorElementFnumlabel.for = "authorElementFnum"
                authorElementFnumlabel.innerText = "Follow Number :"
                userFnumPart.appendChild(authorElementFnumlabel)
                userFnumPart.appendChild(authorElementFnum)
                userFnumPart.className = "Uprofileblock" 
                profileContent.appendChild(userFnumPart);
                

                const authorElementFollow = document.createElement("input")
                authorElementFollow .type = "button";
                authorElementFollow .value = "follow" ;

                authorElementFollow.addEventListener("click", ()=>{pressFollow(data.username)}); 
                profileContent.appendChild(authorElementFollow)
               

                const authorElementunFollow = document.createElement("input")
                authorElementunFollow .type = "button";
                authorElementunFollow .value = "unfollow" ;

                authorElementunFollow.addEventListener("click", ()=>{pressUnFollow(data.username)}); 
                profileContent.appendChild(authorElementunFollow)

  
///////////////////////change profile
                if (pressUseName == document.getElementById("signInUserName").value){
                    const authorchange = document.createElement("input")
                    authorchange.type = "button";
                    authorchange.value = "change profile" ;

                    authorchange.addEventListener("click", ()=>{updatePofileInfo(profilediv,"0")}); 
                    profileContent.appendChild(authorchange)
                
                    profilediv.appendChild(profileContent);
                    profileContent.removeChild(authorElementFollow)
                    profileContent.removeChild(authorElementunFollow)
                }
                const profiledivReturn = document.createElement("input")
                profiledivReturn.type = "button";
                
                profiledivReturn.value ="return" ;
                profiledivReturn.addEventListener("click", ()=>{returncode(profilediv,"","1")}); 
                
                profileContent.appendChild(profiledivReturn);
                profilediv.appendChild(profileContent);
                

                const mianpage = document.getElementById("test")
                
                const profilePostContent = document.createElement('div');
                

                for (let i = 0; i<data.posts.length;i++){
                    const url ="http://localhost:5000/post?" + "id=" + data.posts[i]
                    const result = fetch(url,{
                        method : "GET",
                        headers : {
                            'Accept' :'application/json' ,
                            'Content-Type' :'application/json',
                            
                            'Authorization' : 'Token ' + document.getElementById("token").innerText,
                            
                        }
                    }).then((data) => {
                        if (data.status ===200){
                            data.json().then(data =>{
                                const userpostcontent = document.createElement('div');
                                const userdescElement = document.createElement("div")
                                
                                userdescElement.innerText = data.meta.description_text ;
                                userpostcontent.appendChild(userdescElement)
            
                                const userimageElement = document.createElement("img");
                                
                                userimageElement.setAttribute("src",'data:image/jpeg;base64,${post.thumbnail}');
                                userpostcontent.appendChild(userimageElement);
            
                                const userlikeElement = document.createElement("input")
                                userlikeElement.type = "button";
                                userlikeElement.value = "like" ;
                                
                                userlikeElement.addEventListener("click", ()=>{pressLike(data.id)}); 
                                userpostcontent.appendChild(userlikeElement)
            
                                const userunlikeElement = document.createElement("input")
                                userunlikeElement.type = "button";
                                userunlikeElement.value = "unlike";
                                userunlikeElement.name = "unlike";
                                userunlikeElement.addEventListener("click", ()=>{pressUnLike(data.id)}); 
                                userpostcontent.appendChild(userunlikeElement)
            
                                const userlikeNumElement = document.createElement("input")
                                userlikeNumElement.type = "button";
                                
                                userlikeNumElement.value = data.meta.likes.length ;
            
                                userlikeNumElement.name = "likeNum";
                                userlikeNumElement.addEventListener("click", ()=>{pressshowLike(data.id,profilediv,"0")}); 
                               
                                userpostcontent.appendChild(userlikeNumElement)
            
                                const userCommentNumElement = document.createElement("input")
                                userCommentNumElement.type = "button";
                                userCommentNumElement.value = 'comments : ' +data.comments.length;
                                userCommentNumElement.name = "commentNUM";
                                userCommentNumElement.addEventListener("click",()=>{pressshowComment(data.id,profilediv,"0")})
        
                                userpostcontent.appendChild(userCommentNumElement)
                               
                                profilePostContent.appendChild(userpostcontent);

                                ////change and updata post
                                if (data.meta.author === document.getElementById("signInUserName").value){
                                    const changePost = document.createElement("input");
                                    changePost.type = "button";
                                    changePost.value = "deletePost" ;
                                    changePost.name = "deletePost";
                                    changePost.addEventListener("click", ()=>{deletePost(data.id)}); 
                                    profilePostContent.appendChild(changePost)

                                    const  updataPost= document.createElement("input");
                                    updataPost.type = "button";
                                    updataPost.value = "updataPost" ;
                                    updataPost.name = "updataPost";
                                    updataPost.addEventListener("click", ()=>{createChangePost(data.id)}); 
                                    profilePostContent.appendChild(updataPost)
                                }
                            })}
                        }).catch((error) => {console.log("error" ,error) ;})
                    } ///for end
                
                profilediv.appendChild(profilePostContent);
                
                profilediv.style.display = "flex";

                mianpage.appendChild(profilediv);
            })
    }}).catch((error) => {console.log("error" ,error) ;})
}


/////add post


const addPost =() =>{     ///400problem
    const file = document.getElementById("UserPostImgInput").files[0]
    fileToDataUrl(file).then(data=>{
        let src = data.substring(22,data.length)
        if(src[0]===","){src = src.substring(1,src.length)}
        console.log(src)
        const postBody = {
            "description_text": document.getElementById("UserPostInput").value,
            "src":  src
        }
        const result = fetch('http://localhost:5000/post/',{
        method : "POST",
        headers : {
            'Accept' :'application/json' ,
            'Content-Type' :'application/json',
            'Authorization' : 'Token ' + document.getElementById("token").innerText,
        },
        body:JSON.stringify(postBody),
        }).then((data) => {
            if(data.status ===403){
                alert('please log in first');
            }else if(data.status ===400){
                alert('wrong request');
            }else if(data.status ===200){
                alert("success");
            }
        }).catch((error) => {console.log("error" ,error);})
            
        })
}
const createChangePost= (postID)=>{

    const updataPostDiv = document.createElement("div")
    const updataPostElement = document.createElement("input")
    updataPostElement.type = "text";
    updataPostElement.id = "updataPostElement" ;

    updataPostDiv.appendChild(updataPostElement)

    const updataPostFileElement = document.createElement("input")
    updataPostFileElement.type = "file";
    updataPostFileElement.accept = "image/png, image/jpeg,image/jpg ";
    updataPostFileElement.id = "updataPostFileElement";

    updataPostDiv.appendChild(updataPostFileElement)
    const mianpage = document.getElementById("test")


    const updataPostFilesubElement = document.createElement("input")
    updataPostFilesubElement.type = "button";
    updataPostFilesubElement.value = "submit";

    updataPostFilesubElement.addEventListener("click", ()=>{updatePost(postID)}); 
    updataPostDiv.appendChild(updataPostFilesubElement)

    const updataPostDivReturn = document.createElement("input");
    updataPostDivReturn.type = "button";
    updataPostDivReturn.value = "return";   /////this place add the return function ,remove the div
    updataPostDivReturn.addEventListener("click",()=>{returncode(updataPostDiv,element,"0")});
    updataPostDiv.appendChild(updataPostDivReturn);

    mianpage.appendChild(updataPostDiv)
}

document.getElementById("UserPostSubmit").addEventListener("click",()=>{addPost()})

const updatePost =(postID) =>{
    const file = document.getElementById("updataPostFileElement").files[0]
    fileToDataUrl(file).then(data=>{
        let src = data.substring(22,data.length)
        // let src = data.substring(22,data.length)
        if(src[0]===","){src = src.substring(1,src.length)}
        const postBody = {
            "description_text": document.getElementById("updataPostElement").value, //so all the psot need a update button
            "src": src,
        }
        const url = 'http://localhost:5000/post/?id=' + postID
        const result = fetch(url,{
            method : "PUT",
            headers : {
                'Accept' :'application/json' ,
                'Content-Type' :'application/json',
                'Authorization' : 'Token ' + document.getElementById("token").innerText,
            },
            body:JSON.stringify(postBody),
        }).then((data) => {
            if(data.status ===403){
                alert('please log in first') ;
            }else if(data.status ===400){
                alert('wrong request') ;
            }else if(data.status ===404){
                alert('post not exist') ;
            }
            else if(data.status ===200){
                alert('success') ;
            }
        }).catch((error) => {console.log("error" ,error) ;})})
}

const deletePost = (postId) =>{
    const url = 'http://localhost:5000/post/?id=' + postId
    const result = fetch(url,{
        method : "DELETE",
        headers : {
            'Accept' :'application/json' ,
            'Content-Type' :'application/json',
            'Authorization' : 'Token ' + document.getElementById("token").innerText,
        }
    }).then((data) => {
        if(data.status ===403){
            alert('please log in first') ;
        }else if(data.status ===400){
            alert('wrong request') ;
        }else if(data.status ===404){
            alert('post not exist') ;
        }
        else if(data.status ===200){
            alert('yeah') ;
        }
    }).catch((error) => {
        console.log("error" ,error) ;
    })
}

const updatePofileInfo = (element,num) =>{
    // element.style.display = "None";
    document.getElementById("afterLogIn").style.display = "None"
    if (element !== ""){
        element.style.display = "None"
    }
    const updatePofileInfodiv = document.createElement('div'); //remmber to delete it    
    const updatePofileNameContainer = document.createElement('div');
    const updatePofileUserName = document.createElement("input");
    updatePofileUserName.type = "text";
    // postcommentsElement.value = "close";  
    updatePofileUserName.id = "inputcommentsElement";
    const updatePofileUserNameLabel = document.createElement("label");
    updatePofileUserNameLabel.innerText = "Name"
    updatePofileUserNameLabel.for = "inputcommentsElement"
    updatePofileNameContainer.appendChild(updatePofileUserNameLabel);
    updatePofileNameContainer.appendChild(updatePofileUserName);
    updatePofileNameContainer.className ="userInfoMainContainer"
    updatePofileInfodiv.appendChild(updatePofileNameContainer);
    // updatePofileInfodiv.appendChild(inputcommentsElement);
    const updatePofilePassword = document.createElement("input");
    updatePofilePassword.type = "password";
    // postcommentsElement.value = "close";  
    updatePofilePassword.id = "inputPasswordElement"
    
    ////
    const updatePofilePassContainer = document.createElement('div');
    const updatePofilePasswordLabel = document.createElement("label");
    updatePofilePasswordLabel.innerText = "Pssword"
    updatePofilePasswordLabel.for = "inputPasswordElement"
    updatePofilePassContainer.appendChild(updatePofilePasswordLabel);
    updatePofilePassContainer.appendChild(updatePofilePassword);
    updatePofilePassContainer.className ="userInfoMainContainer"
    updatePofileInfodiv.appendChild(updatePofilePassContainer);


    const updatePofileCPassContainer = document.createElement('div');
    const updatePofileCPassword = document.createElement("input");
    updatePofileCPassword.type = "password";
    // postcommentsElement.value = "close";  
    updatePofileCPassword.id = "inputCPasswordElement"
    
    ////
    const updatePofileCPasswordLabel = document.createElement("label");
    updatePofileCPasswordLabel.innerText = "Confirm Pssword"
    updatePofileCPasswordLabel.for = "inputCPasswordElement"
    updatePofileCPassContainer.appendChild(updatePofileCPasswordLabel);
    updatePofileCPassContainer.appendChild(updatePofileCPassword);
    updatePofileCPassContainer.className ="userInfoMainContainer";
    updatePofileInfodiv.appendChild(updatePofileCPassContainer);

//////////////////////
    const updatePofileEmailContainer = document.createElement('div');
    const updatePofileEmail = document.createElement("input");
    updatePofileEmail.type = "email";
    // postcommentsElement.value = "close";  
    updatePofileEmail.id = "inputEmailElement"
    
    ////
    const updatePofileEmailLabel = document.createElement("label");
    updatePofileEmailLabel.innerText = "Email"
    updatePofileEmailLabel.for = "inputEmailElement"
    updatePofileEmailContainer.appendChild(updatePofileEmailLabel);
    updatePofileEmailContainer.appendChild(updatePofileEmail);
    updatePofileEmailContainer.className ="userInfoMainContainer"
    updatePofileInfodiv.appendChild(updatePofileEmailContainer);
//////////////////////
    
    const updatePofilesubmit = document.createElement("input");
    updatePofilesubmit.type = "button";
    updatePofilesubmit.value = "submit";   
    updatePofilesubmit.addEventListener("click",()=>{updatePofile()})
    updatePofileInfodiv.appendChild(updatePofilesubmit);

    const updatePofileInfoReturn = document.createElement("input")
    updatePofileInfoReturn.type = "button";
    
    updatePofileInfoReturn.value ="return";
    updatePofileInfoReturn.addEventListener("click", ()=>{returncode(updatePofileInfodiv,element,num)}); 
    
    updatePofileInfodiv.appendChild(updatePofileInfoReturn);
    const mianpage = document.getElementById("test")
    mianpage.appendChild(updatePofileInfodiv)

}


////update the peofile
const updatePofile =() =>{ //so need a button to crealize the function and a popup to have a new page
    const confirmPass = document.getElementById("inputCPasswordElement").value;
    const changeinputPassword = document.getElementById("inputPasswordElement").value;
    if (confirmPass === changeinputPassword){
        const PofileBody = {
            "email": document.getElementById("inputEmailElement").value,
            "name": document.getElementById("inputcommentsElement").value,
            "password": changeinputPassword, //the password need confirm
        }
        const result = fetch('http://localhost:5000/user/',{
            method : "PUT",
            headers : {
                'Accept' :'application/json' ,
                'Content-Type' :'application/json',
                'Authorization' : 'Token ' + document.getElementById("token").innerText,
            },
            body:JSON.stringify(PofileBody),
        }).then((data) => {
            if(data.status ===403){
                alert('please log in first') ;
            }else if(data.status ===400){
                alert('wrong request') ;
            }else if(data.status ===404){
                alert('post not exist') ;
            }else if(data.status ===200){
                alert('success') ;
            }
        }).catch((error) => {
            console.log("error" ,error) ;
        })
    }
    else{
        alert("please input same password")
    }
}

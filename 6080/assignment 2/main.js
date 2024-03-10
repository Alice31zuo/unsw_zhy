import API from './api.js';
// A helper you may want to use when uploading new images to the server.
import { fileToDataUrl } from './helpers.js';

// This url may need to change depending on what port your backend is running
// on.
const api = new API('http://localhost:5000');

// Example usage of makeAPIRequest method.
api.makeAPIRequest('dummy/user')
    .then(r => console.log(r));


// let LogSuccess = false
const basicFeed = () =>{
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
                    posts.map(post=>{
                    const postcontent = document.createElement('div');
                    postcontent.className = "post";
                    const authorElement = document.createElement("input");
                    authorElement.type = "button";
                    authorElement.value = post.meta.author ;
                    // authorElement.name = "authorName";
                    // console.log(authorElement.value);
                    // console.log(post.id);
                    authorElement.addEventListener("click", ()=>{pressUser(authorElement.value)}); //can function
                    // const postauthor = document.createElement('div');
                    // postauthor.appendChild(authorElement)
                    postcontent.appendChild(authorElement)
                    // postcontent.appendChild(postauthor)
                    // postauthor.addEventListener("click", pressUser(authorElement.value));
                    // postauthor.addEventListener('click', (e) => {

                    //     pressUser(authorElement.value)
            
                    // })
                    // console.log(post.meta)
                    const idElement = document.createElement("div")
                    idElement.innerText = post.id ;
                    idElement.style.display = "none"
                    postcontent.appendChild(idElement)

                    const descElement = document.createElement("div")
                    // authorElement.type = "button";
                    descElement.innerText = post.meta.description_text ;
                    postcontent.appendChild(descElement)

                    const imageElement = document.createElement("img");
                    // authorElement.type = "button";
                    imageElement.setAttribute("src",'data:image/jpeg;base64,${post.thumbnail}');
                    postcontent.appendChild(imageElement);

                    const likeElement = document.createElement("input")
                    likeElement.type = "button";
                    likeElement.value = "like" ;
                    likeElement.name = "like";
                    likeElement.addEventListener("click", ()=>{pressLike(post.id)}); 
                    postcontent.appendChild(likeElement)

                    const unlikeElement = document.createElement("input")
                    unlikeElement.type = "button";
                    unlikeElement.value = "unlike";
                    unlikeElement.name = "unlike";
                    unlikeElement.addEventListener("click", ()=>{pressUnLike(post.id)}); 
                    postcontent.appendChild(unlikeElement)

                    const likeNumElement = document.createElement("input")
                    likeNumElement.type = "button";
                    // console.log(Array.isArray(post.meta.likes))
                    likeNumElement.value = post.meta.likes.length ;

                    likeNumElement.name = "likeNum";
                    likeNumElement.addEventListener("click", ()=>{pressshowLike(post.id)}); 
                    // likeNumElement.addEventListener("click, ()=>{pressshowLike()）
                    postcontent.appendChild(likeNumElement)

                    const CommentNumElement = document.createElement("input")
                    CommentNumElement.type = "button";
                    CommentNumElement.value = 'comments : ' + post.comments.length;
                    CommentNumElement.name = "commentNUM";
                    CommentNumElement.addEventListener("click",()=>{pressshowComment(post.id)})

                    // console.log(post.comments)
                    postcontent.appendChild(CommentNumElement)
                    document.getElementById("postArea").appendChild(postcontent)
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
                'Accept' :'application/json' ,
                'Content-Type' :'application/json'
            },
            body:JSON.stringify(loginBody),
        }).then((data) => {
            if (data.status ===403){
                alert('Incorect Login information')
            }else if(data.status ===200){
                data.json().then(result => {
                    document.getElementById("signIn").style.display = "None";
                    // LogSuccess = true
                    // document.getElementById("afterLogIn").style.display = "block" ;
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
// if (LogSuccess = true) {
//     document.getElementById("afterLogIn").style.display = "block"     
// }


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
            alert('success') ;
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
            // "id" : postId,//this need get the id first
        },
    }).then((data) => {
        if (data.status ===404){
            alert('post is not exist') ;
        }else if(data.status ===403){
            alert('please log in first') ;
        }else if(data.status ===400){
            alert('wrong request') ;
        }else{
            alert('success') ;
        }
    }).catch((error) => {
        console.log("error" ,error) ;
    })
}


///show likes
const pressshowLike = (PostId) =>{
    const url = 'http://localhost:5000/post/?id=' + PostId
    const result = fetch(url,{
            method : "GET",
            headers : {
                'Accept' :'application/json' ,
                'Content-Type' :'application/json',
                // 'Authorization' : 'Token ' + document.getElementById("id").value
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
                data.json().then(data =>{        
                    let likeArray = data.meta.likes 
                    const postLikeUser = document.createElement('div'); //remmber to delete it         
                    for (let i = 0 ; i < likeArray.length ; i++){
                        const likeUserElement = document.createElement("input")
                        // likeUserElement.className = "likeListButton"
                        likeUserElement.type = "button";
                        // likeUserElement.value = data.meta.likes[i];
                        GetUserName(data.meta.likes[i],likeUserElement)
                        //this should get the user name 
                        postLikeUser.appendChild(likeUserElement);
                    }
                    const existlikeUserElement = document.createElement("input");
                    existlikeUserElement.type = "button";
                    existlikeUserElement.value = "close";   //use this to close the like 
                    postLikeUser.appendChild(existlikeUserElement);
                    const mianpage = document.getElementById("test")
                    mianpage.appendChild(postLikeUser)
                })
            }
        })
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
                
            // return data.username;
        })}}).catch((error) => {console.log("error" ,error) ;})
}


////show comment
const pressshowComment = (PostId) =>{
    const url = 'http://localhost:5000/post/?id=' + PostId

    const result = fetch(url,{
            method : "GET",
            headers : {
                'Accept' :'application/json' ,
                'Content-Type' :'application/json',
                // 'Authorization' : 'Token ' + document.getElementById("id").value
                'Authorization' : 'Token ' + document.getElementById("token").innerText,
                // "id" : ,//this need get the id first
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
                data.json().then(data =>{        
                    let commentsArray = data.comments
                    const postcommentsUser = document.createElement('div'); //remmber to delete it  
        
                    const inputcommentsElement = document.createElement("input");
                    inputcommentsElement.type = "text";
                    // postcommentsElement.value = "close";  
                    inputcommentsElement.id = "inputcommentsElement"
                    postcommentsUser.appendChild(inputcommentsElement);

                    const commentsElementsubmit = document.createElement("input");
                    commentsElementsubmit.type = "button";
                    commentsElementsubmit.value = "submit";   /////this place add the return function ,remove the div
                    commentsElementsubmit.addEventListener("click",()=>{commentPost(PostId)})
                    postcommentsUser.appendChild(commentsElementsubmit);

                    for (let i = 0 ; i < commentsArray.length ; i++){
                        
                        const commentsUserElement =  document.createElement("input")
                        // commentsUserElement.className = "commentsListButton"
                        // commentsUserElement.typ = "";
                        commentsUserElement.type = "button"
                        
                        
                        commentsUserElement.value = commentsArray[i].author;
                        commentsUserElement.addEventListener("click", ()=>{pressUser(commentsUserElement.value)});
                        
                        postcommentsUser.appendChild(commentsUserElement);
                        // console.log("!!!!")
                        
                        const commentsUserElementdes = document.createElement("div")
                        // commentsUserElementdes.className = "commentsListButton"
                        // commentsUserElement.typ = "";
                        commentsUserElementdes.innerText = commentsArray[i].comment;
                        postcommentsUser.appendChild(commentsUserElementdes);

                        const commentsUserElementTime = document.createElement("div")
                        // commentsUserElementdes.className = "commentsListButton"
                        // commentsUserElement.typ = "";
                        commentsUserElementTime.innerText = commentsArray[i].published;
                        postcommentsUser.appendChild(commentsUserElementTime);

                        ////change and delete post
                        


                    }
                    const existcommentsElement = document.createElement("input");
                    existcommentsElement.type = "button";
                    existcommentsElement.value = "close";   /////this place add the return function ,remove the div
                    postcommentsUser.appendChild(existcommentsElement);
                    const mianpage = document.getElementById("test")
                    mianpage.appendChild(postcommentsUser)
                })
            }
    })
}
//Feed Pagination??

const commentPost =(postId) =>{ //so need a comment input in the comment show area
    console.log(document.getElementById("inputcommentsElement").value)
    const url = 'http://localhost:5000/post/comment?id=' +postId
    const commentBody = {
        "comment": document.getElementById("inputcommentsElement").value, //so all the psot need a update button
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
            // "username" : ,//this would be the botton value
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
            // "username" : pressUseName,//this would be the botton value
            // "id": userId,
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
                console.log("insidepressuser")
                const profilediv = document.createElement('div');
                const profileContent = document.createElement('div');
                // postcontent.className = "profileContent";
                const authorElementID = document.createElement("div");
                authorElementID.innerText = data.id;
                // authorElementID.name = "authorName";
                profileContent.appendChild(authorElementID);
                // console.log(post.meta)
                const authorElementName = document.createElement("div");
                authorElementName.innerText = data.username;
                // authorElementID.name = "authorName";
                profileContent.appendChild(authorElementName);
                //
                const authorElementEmail = document.createElement("div");
                authorElementEmail.innerText = data.email;
                // authorElementID.name = "authorName";
                profileContent.appendChild(authorElementEmail);
                //
                const authorElementRname = document.createElement("div");
                authorElementRname.innerText = data.name;
                // authorElementID.name = "authorName";
                profileContent.appendChild(authorElementRname);
                //
                const authorElementFnum = document.createElement("div");
                authorElementFnum.innerText = data.followed_num;
                // authorElementID.name = "authorName";
                profileContent.appendChild(authorElementFnum);
                //
                // profilediv.appendChild(profileContent);

                const authorElementFollow = document.createElement("input")
                authorElementFollow .type = "button";
                authorElementFollow .value = "follow" ;

                authorElementFollow.addEventListener("click", ()=>{pressFollow(data.username)}); 
                profileContent.appendChild(authorElementFollow)
                // profilediv.appendChild(profileContent);
                // profilediv.appendChild(profileContent);

                const authorElementunFollow = document.createElement("input")
                authorElementunFollow .type = "button";
                authorElementunFollow .value = "unfollow" ;

                authorElementunFollow.addEventListener("click", ()=>{pressUnFollow(data.username)}); 
                profileContent.appendChild(authorElementunFollow)
                // profilediv.appendChild(profileContent);
                profilediv.appendChild(profileContent);
///////////////////////change profile
                
                const authorchange = document.createElement("input")
                authorchange.type = "button";
                authorchange.value = "change profile" ;

                authorchange.addEventListener("click", ()=>{updatePofileInfo()}); 
                profileContent.appendChild(authorchange)
                // profilediv.appendChild(profileContent);
                profilediv.appendChild(profileContent);



                const mianpage = document.getElementById("test")
                // mianpage.appendChild(profilediv)
                ///then get the post
                const profilePostContent = document.createElement('div');
                //use the same part in the feed

                for (let i = 0; i<data.posts.length;i++){
                    const url ="http://localhost:5000/post?" + "id=" + data.posts[i]
                    const result = fetch(url,{
                        method : "GET",
                        headers : {
                            'Accept' :'application/json' ,
                            'Content-Type' :'application/json',
                            // 'Authorization' : 'Token ' + document.getElementById("id").value
                            'Authorization' : 'Token ' + document.getElementById("token").innerText,
                            // "id" : userId,//this need get the id first
                        }
                    }).then((data) => {
                        if (data.status ===200){
                            data.json().then(data =>{
                                const userpostcontent = document.createElement('div');
                                // postcontent.className = "post";
                                // const userElement = document.createElement("input");
                                // userElement.type = "button";
                                // userElement.value = data.meta.author ;

                                // userpostcontent.appendChild(userElement)

            
                                const userdescElement = document.createElement("div")
                                // authorElement.type = "button";
                                userdescElement.innerText = data.meta.description_text ;
                                userpostcontent.appendChild(userdescElement)
            
                                const userimageElement = document.createElement("img");
                                // authorElement.type = "button";
                                userimageElement.setAttribute("src",'data:image/jpeg;base64,${post.thumbnail}');
                                userpostcontent.appendChild(userimageElement);
            
                                const userlikeElement = document.createElement("input")
                                userlikeElement.type = "button";
                                userlikeElement.value = "like" ;
                                // likeElement.name = "like";
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
                                // console.log(Array.isArray(post.meta.likes))
                                userlikeNumElement.value = data.meta.likes.length ;
            
                                userlikeNumElement.name = "likeNum";
                                userlikeNumElement.addEventListener("click", ()=>{pressshowLike(data.id)}); 
                                // likeNumElement.addEventListener("click, ()=>{pressshowLike()）
                                userpostcontent.appendChild(userlikeNumElement)
            
                                const userCommentNumElement = document.createElement("input")
                                userCommentNumElement.type = "button";
                                userCommentNumElement.value = 'comments : ' +data.comments.length;
                                userCommentNumElement.name = "commentNUM";
                                userCommentNumElement.addEventListener("click",()=>{pressshowComment(data.id)})
            
                                // console.log(post.comments)
                                userpostcontent.appendChild(userCommentNumElement)
                                // document.getElementById("postArea").appendChild(postcontent)


                                // const userprofilePContent = document.createElement('div');
                                // userprofilePContent.className = "post";
                                // const userauthorElement = document.createElement("input");
                                // authorElement.type = "button";
                                // authorElement.value = data.meta.author ;
                                // // authorElement.name = "authorName";
                                // profilePContent.appendChild(authorElement);
                                // // console.log(post.meta)
                                // const idElement = document.createElement("div");
                                // idElement.innerText = data.id ;
                                // idElement.style.display = "none";
                                // profilePContent.appendChild(idElement);

                                // const descElement = document.createElement("div");
                                // // authorElement.type = "button";
                                // descElement.innerText = data.meta.description_text ;
                                // profilePContent.appendChild(descElement);

                                // const imageElement = document.createElement("img");
                                // // authorElement.type = "button";
                                // imageElement.setAttribute("src",'data:image/jpeg;base64,${data.thumbnail}');
                                // pprofilePContent.appendChild(imageElement);

                                // const likeElement = document.createElement("input");
                                // likeElement.type = "button" ;
                                // likeElement.value = "like" ;
                                // likeElement.name = "like" ;
                                // profilePContent.appendChild(likeElement);

                                // const likeNumElement = document.createElement("input");
                                // likeNumElement.type = "button";
                                // if (data.likes[0] ){    //this need fix so as feed part
                                //     likeNumElement.value = post.meta.likes[0] ;
                                // }
                                // else{
                                //     likeNumElement.value =0 ;
                                // }
                                // likeNumElement.name = "likeNum";
                                // profilePContent.appendChild(likeNumElement);

                                // const CommentNumElement = document.createElement("input")
                                // CommentNumElement.type = "button";
                                // CommentNumElement.value = 'comments : ' + post.comments.length;
                                // CommentNumElement.name = "commentNUM";
                                // // console.log(post.comments)
                                // profilePContent.appendChild(CommentNumElement);
                                // document.getElementById("postArea").appendChild(postcontent)
                                profilePostContent.appendChild(userpostcontent);

                                ////change and updata post
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

                            })}
                        }).catch((error) => {console.log("error" ,error) ;})
                    } ///for end
                profilediv.appendChild(profilePostContent);
                mianpage.appendChild(profilediv);
            })
    }}).catch((error) => {console.log("error" ,error) ;})
}


/////add post


const addPost =() =>{     ///400problem
    const file = document.getElementById("UserPostImgInput").files[0]
    // console.log(document.getElementById("UserPostimgInput").value)

    fileToDataUrl(file).then(data=>{
        let src = data.substring(22,data.length)
        if(src[0]===","){src = src.substring(1,src.length)}
        console.log(src)
        const postBody = {
            "description_text": document.getElementById("UserPostInput").value,
            "src":  src
            // "src":""
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
            // console.log(src)
        })
    // console.log(fileToDataUrl(file))
    // console.log(src)
    // const postBody = {
    //     "description_text": document.getElementById("UserPostInput").value,
    //     "src":  'data:image/png;base64,' + src
    //     // "src":""
    // }
    // console.log(document.getElementById("UserPostimgInput").value)
    // console.log(postBody)
    // const result = fetch('http://localhost:5000/post/',{
    //     method : "POST",
    //     headers : {
    //         'Accept' :'application/json' ,
    //         'Content-Type' :'application/json',
    //         'Authorization' : 'Token ' + document.getElementById("token").innerText,
    //     },
    //     body:JSON.stringify(postBody),
       
    // }).then((data) => {
    //     if(data.status ===403){
    //         alert('please log in first');
    //     }else if(data.status ===400){
    //         alert('wrong request');
    //     }else if(data.status ===200){
    //         alert("success");
    //     }
    // }).catch((error) => {
    //     console.log("error" ,error);
    // })
}
const createChangePost= (postID)=>{
    const updataPostDiv = document.createElement("div")
    const updataPostElement = document.createElement("input")
    updataPostElement.type = "text";
    updataPostElement.id = "updataPostElement" ;
    // likeElement.name = "like";
    // userlikeElement.addEventListener("click", ()=>{pressLike(data.id)}); 
    updataPostDiv.appendChild(updataPostElement)

    const updataPostFileElement = document.createElement("input")
    updataPostFileElement.type = "file";
    updataPostFileElement.accept = "image/png, image/jpeg,image/jpg ";
    updataPostFileElement.id = "updataPostFileElement";
    // updataPostFileElement.name = "unlike";
    updataPostDiv.appendChild(updataPostFileElement)
    const mianpage = document.getElementById("test")


    // mianpage.appendChild(updataPostDiv)

    const updataPostFilesubElement = document.createElement("input")
    updataPostFilesubElement.type = "button";
    updataPostFilesubElement.value = "submit";
    // updataPostFileElement.name = "unlike";
    updataPostFilesubElement.addEventListener("click", ()=>{updatePost(postID)}); 
    updataPostDiv.appendChild(updataPostFilesubElement)
    // const mianpage = document.getElementById("test")
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

const updatePofileInfo = () =>{
    const updatePofileInfodiv = document.createElement('div'); //remmber to delete it      
    const updatePofileUserName = document.createElement("input");
    updatePofileUserName.type = "text";
    // postcommentsElement.value = "close";  
    updatePofileUserName.id = "inputcommentsElement"
    updatePofileInfodiv.appendChild(updatePofileUserName);
    const updatePofileUserNameLabel = document.createElement("label");
    updatePofileUserNameLabel.innerText = "Name"
    updatePofileUserNameLabel.for = "inputcommentsElement"
    updatePofileInfodiv.appendChild(updatePofileUserNameLabel);
    // updatePofileInfodiv.appendChild(inputcommentsElement);
    const updatePofilePassword = document.createElement("input");
    updatePofilePassword.type = "password";
    // postcommentsElement.value = "close";  
    updatePofilePassword.id = "inputPasswordElement"
    updatePofileInfodiv.appendChild(updatePofilePassword);
    ////
    const updatePofilePasswordLabel = document.createElement("label");
    updatePofilePasswordLabel.innerText = "Pssword"
    updatePofilePasswordLabel.for = "inputPasswordElement"
    updatePofileInfodiv.appendChild(updatePofilePasswordLabel);

    const updatePofileCPassword = document.createElement("input");
    updatePofileCPassword.type = "password";
    // postcommentsElement.value = "close";  
    updatePofileCPassword.id = "inputCPasswordElement"
    updatePofileInfodiv.appendChild(updatePofileCPassword);
    ////
    const updatePofileCPasswordLabel = document.createElement("label");
    updatePofileCPasswordLabel.innerText = "Confirm Pssword"
    updatePofileCPasswordLabel.for = "inputCPasswordElement"
    updatePofileInfodiv.appendChild(updatePofileCPasswordLabel);
//////////////////////
    const updatePofileEmail = document.createElement("input");
    updatePofileEmail.type = "email";
    // postcommentsElement.value = "close";  
    updatePofileEmail.id = "inputEmailElement"
    updatePofileInfodiv.appendChild(updatePofileEmail);
    ////
    const updatePofileEmailLabel = document.createElement("label");
    updatePofileEmailLabel.innerText = "Email"
    updatePofileEmailLabel.for = "inputEmailElement"
    updatePofileInfodiv.appendChild(updatePofileEmailLabel);
//////////////////////
    const updatePofilesubmit = document.createElement("input");
    updatePofilesubmit.type = "button";
    updatePofilesubmit.value = "submit";   /////this place add the return function ,remove the div
    updatePofilesubmit.addEventListener("click",()=>{updatePofile()})
    updatePofileInfodiv.appendChild(updatePofilesubmit);
    const mianpage = document.getElementById("test")
    mianpage.appendChild(updatePofileInfodiv)

}


////update the peofile
const updatePofile =() =>{ //so need a button to crealize the function and a popup to have a new page
    const PofileBody = {
        "email": document.getElementById("inputEmailElement").value,
        "name": document.getElementById("inputcommentsElement").value,
        "password": document.getElementById("inputPasswordElement").value, //the password need confirm
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

let userInfo = {}
if (window.localStorage.getItem('AUTH-TOKEN')){
    $('#signOut').removeClass('d-none')
    $('#login-modal-button').addClass('d-none')
}
var submitButton = document.getElementById('submit-button');
// var loginButton = document.getElementById('login-button');

// 主函数
submitButton.addEventListener('click', () => {
    if(!window.localStorage.getItem('AUTH-TOKEN')){
        $('#notLogin').collapse('show')
        return
    }
    var houseData = {}
    houseData.Suburb = document.getElementById('suburb').value;
    houseData.Rooms = document.getElementById('bedrooms').value;
    houseData.Type = document.getElementById('type').value;
    houseData.Distance = document.getElementById('distance').value;
    houseData.Car = document.getElementById('cars').value;
    houseData.Building_Area = document.getElementById('area').value;
    houseData.Year = document.getElementById('buildingAge').value;
    console.log(houseData)
    getPrice(houseData)
    // getRanSuburbs(houseData)
})

function getPrice(data) {
    var url = 'http://127.0.0.1:5000/house/data';
    fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, cors, *same-origin
        body: JSON.stringify(data), // data can be `string` or {object}!
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            "AUTH-TOKEN": window.localStorage.getItem("AUTH-TOKEN")
            // "Content-Type": "application/x-www-form-urlencoded",
        }
    })
    .then(res => res.json())
    .then(response => {
          console.log(response)
            var housePrice = document.getElementById('result')
            if(response.price){
                housePrice.innerText = `$ ${response.price} K`
                document.getElementById('access_num').innerText=response.access

                if(!$('#invalidResult').hasClass('d-none')) $('#invalidResult').addClass('d-none')
                $('#result').removeClass('d-none')
            }
            else {
                if(!$('#result').hasClass('d-none')) $('#result').addClass('d-none')
                document.getElementById('getPriceError').innerText=response.message
                $('#invalidResult').removeClass('d-none')
                $('#getPriceError').text(response.message)
            }
        console.log('Success:', JSON.stringify(response))
    })
    .catch(error => console.error('Error:', error))
}

// login
$('#loginSubmit').click(()=>{
    let url = 'http://127.0.0.1:5000/auth/login'
    let data = {
        username: $('#usernameInput').val(),
        password: $('#passwordInput').val()
    }
    fetch(url,{
        method:'POST',
        body:JSON.stringify(data),
        headers:{
            "Content-Type":"application/json"
        }
    })
    .then(res=>{
        if(res.status === 400 || res.status === 403) {
            $('#invalidLogin').removeClass('d-none')
            throw 0
        }
        return res.json()
    })
    .then(resp=>{
        console.log(resp.token)
        document.getElementById('name').innerText=resp.username
        document.getElementById('access_num').innerText=resp.access
        window.localStorage.setItem("AUTH-TOKEN",resp.token)
        $('#notLogin').collapse('hide')
        $('#login_modal').modal('hide')
        $('#signOut').removeClass('d-none')
        $('#login-modal-button').addClass('d-none')
    })
    .catch(err=>{
        console.log(err)
    })
})


// 登陆框关闭后数据清零
$('#login_modal').on('hidden.bs.modal', ()=>{
    $('#invalidLogin').addClass('d-none')
    $('#usernameInput').prop('value','')
    $('#passwordInput').prop('value','')
})

// 登出按钮
$('#signOut').click(()=>{
    userInfo = {}
    window.localStorage.clear()
    $('#signOut').addClass('d-none')
    $('#login-modal-button').removeClass('d-none')
})

$(function () {
    $('[data-toggle="popover"]').popover()
})

// $('#clipboardPopover').popover('show')
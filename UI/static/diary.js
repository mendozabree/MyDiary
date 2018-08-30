function pickDate(){
    document.getElementById('my_date').setAttribute("type", "date");
}
function registerUser() {
    let firstName = document.getElementById('firstName').value;
    let lastName = document.getElementById('lastName').value;
    let username = document.getElementById('userName').value;
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;
    let confirmPassword = document.getElementById('confirm_password').value;
    fetch('https://r-mydiary.herokuapp.com/api/v1/auth/signup', {
    // fetch('http://127.0.0.1:5000/api/v1/auth/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json; charset=UTF-8'
        },
        body: JSON.stringify({
            username: username, first_name: firstName, last_name: lastName,
            email: email, password: password, confirm_password:confirmPassword
        })
    })
        .then((response) => response.json())
        .then(function (data) {
            if (data['message']['status'] === 'Success'){
                let accessToken = data['message']['access_token'];
                localStorage.setItem('token', accessToken)
                let refresh = data['message']['refresh_token']
                localStorage.setItem('refreshToken', refresh)
                location.href='./home.html'
            }else{
                console.log(data['message']['message']);
                let errorMessages = document.getElementById('output');
                errorMessages.innerText = data['message']['message'];
                errorMessages.setAttribute("class", "error")
            }
        })
}
function login(){
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    fetch('https://r-mydiary.herokuapp.com/api/v1/auth/login', {
    // fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json; charset=UTF-8'
        },
        body: JSON.stringify({username:username, password:password})
    })
        .then((response) => response.json())
        .then (function (result) {
            let output = result['message']['status'];
            if (output === 'Success'){
                let accessToken = result['message']['access_token'];
                localStorage.setItem('token', accessToken)
                let refresh = data['message']['refresh_token']
                localStorage.setItem('refreshToken', refresh)
                location.href='./home.html'
            }else {
                let error = document.getElementById('status')
                error.innerHTML = result['message']['message'];
                error.setAttribute('class', 'error')
            }
        })
}
function login_status(){
    let token = localStorage.getItem('token')
    if (token){
        console.log('I have the token')
        location.href='home.html'
    }
    else {
        console.log('I should login')
    }
}
function logout() {
    let token = localStorage.getItem('token')
    fetch('https://r-mydiary.herokuapp.com/api/v1/logout',{
        method: 'GET',
        headers: {Authorization : `Bearer ${token}`}
    })
        .then((response) => response.json())
        .then(function (data) {
            if (data['message']['status'] === 'Success'){
                location.href='sign_in.html'
                localStorage.removeItem('token')
                console.log(data)
            }else {
                alert(data['message']['message'])
                console.log(data)
            }
        })
}
function refreshToken() {
    localStorage.removeItem('token')
    let refresh = localStorage.getItem('refreshToken')
    fetch('http://127.0.0.1:5000/api/v1/refresh',{
        method: 'POST',
        headers: {Authorization : `Bearer ${refresh}`}
    })
        .then((response) => response.json())
        .then(function (data) {
            localStorage.setItem('token', data['message']['access_token'])
            console.log(data['message']['access_token'])
        })
    return localStorage.getItem('token')
}
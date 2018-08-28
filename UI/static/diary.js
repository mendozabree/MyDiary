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
    fetch('https://r-mydiary.herokuapp.com//api/v1/auth/signup', {
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
            let output = data['message']['message'];
            if (output === 'User successfully registered.'){
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
                let token = result['message']['token'];
                document.cookie = token + ";expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"
                document.cookie = token + ";path=/";
                location.href='./home.html'
            }else {
                let error = document.getElementById('status')
                error.innerHTML = result['message']['message'];
                error.setAttribute('class', 'error')
            }
        })
}
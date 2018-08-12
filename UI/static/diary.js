function pickDate(){
    document.getElementById('my_date').setAttribute("type", "date");
}
function registerUser() {
    let firstname = document.getElementById('firstName').value;
    let lastname = document.getElementById('lastName').value;
    let username = document.getElementById('userName').value;
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;

    fetch('http://127.0.0.1:5000/api/v1/auth/signup', {
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*' ,
            'Content-Type': 'application/json; charset=UTF-8'
        },
        body: JSON.stringify({
            username: username, first_name: firstname, last_name: lastname,
            email: email, password: password
        })
    })
        .then((response) => response.json())
        .then(function (data) {
            let output = data['message']['message']
            if (output === 'User successfully registered.'){
                location.href='./home.html'
            }else{
                document.getElementById('output').innerHTML = data['message']['message'];
                console.log('Request succeeded with JSON response', data)
            }
        })
}
function login(){
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers:{
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json; charset=UTF-8'
        },
        body: JSON.stringify({username:username, password:password})
    })
        .then((response) => response.json())
        .then (function (result) {
            let output = result['message']['status'];
            if (output === 'Success'){
                let token = result['message']['token'];
                console.log(token)
                document.cookie = token + ";expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"
                document.cookie = token + ";path=/";
                // document.cookie = "name=" + token + ";expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"

                location.href='./home.html'

            }else {
                document.getElementById('status').innerHTML = result['message']['message'];
                console.log('Request succeeded with JSON response', result)
            }
        })
}
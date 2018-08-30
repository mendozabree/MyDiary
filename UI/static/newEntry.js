function userEntry() {
    let title = document.getElementById('my_title').value;
    let content = document.getElementById('my_content').innerText;
    let token = localStorage.getItem('token');
    // fetch('https://r-mydiary.herokuapp.com/api/v1/entries', {
    fetch('http://127.0.0.1:5000/api/v1/entries', {
        method: 'POST',
        headers: {Authorization : `Bearer ${token}`,
        'Content-Type':'application/json'},
        body: JSON.stringify({title:title, content:content})
    })
        .then((response) => response.json())
        .then(function (data) {
            if (data['msg'] === 'Token has expired'){
			    refreshToken()
            }
			if (data['message']['status'] === 'Success') {
                console.log(data['message']['message'])
                location.href='home.html'
			}
			else {
			    document.getElementById('error').innerText = data['message']['message']
            }
        })
}
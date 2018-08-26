function userEntry() {
    let title = document.getElementById('my_title').value;
    let content = document.getElementById('my_content').value;
    fetch('http://127.0.0.1:5000/api/v1/entries', {
        method: 'POST',
        headers: {Authorization : `Bearer ${document.cookie}`,
        'Content-Type':'application/json'},
        body: JSON.stringify({title:title, content:content})
    })
        .then((response) => response.json())
        .then(function (data) {
			if (data['message']['status'] === 'Success') {
                console.log(data['message']['message'])
                location.href='home.html'

			}
			if (data['message']['status'] === 'Fail'){
				document.getElementById('error').innerText = data['message']['message']
                // console.log(data)
			}else{
			    location.href='unauthorized.html'
            }
        })
}
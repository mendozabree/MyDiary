function viewSpecific(){
    // location.href='/MyDiary/UI/my_entry.html'
    let entryId = localStorage.getItem("viewEntryId")
    fetch('http://127.0.0.1:5000/api/v1/entries/' + entryId, {
        method: 'GET',
        headers: {Authorization : `Bearer ${document.cookie}`}
    })
        .then((response) => response.json())
        .then(function (data) {
			if (data['message']['status'] === 'Success') {
                // document.getElementById('date').value = data['message']['entry'][2]
                document.getElementById('title').innerText = data['message']['entry']['title']
                document.getElementById('content').innerText = data['message']['entry']['content']
                console.log(data)
			}else{
				alert(data['message']['message'])
			}
        })
    localStorage.removeItem('viewEntryId')
    console.log(localStorage.getItem('viewEntryId'))
    console.log(localStorage.getItem('editEntryId'))

}
function modifyEntry(){
    let entryId = localStorage.getItem("editEntryId")
    let myId = parseInt(entryId)
    let url = 'http://127.0.0.1:5000/api/v1/entries/' + myId
    fetch(url, {
        method: 'GET',
        headers: {Authorization : `Bearer ${document.cookie}`}
    })
        .then((response) => response.json())
        .then(function (data) {
			if (data['message']['status'] === 'Success') {
                // document.getElementById('date').value = data['message']['entry'][2]
                document.getElementById('my_title').value = data['message']['entry']['title']
                document.getElementById('my_content').innerText = data['message']['entry']['content']
                console.log('gotten data')
			}
        })
    console.log(localStorage.getItem('viewEntryId'))
    console.log(localStorage.getItem('editEntryId'))
}
function editUserEntry() {
    let entryId = localStorage.getItem("editEntryId")
    let title = document.getElementById('my_title').value
    let content = document.getElementById('my_content').value
    let myId = parseInt(entryId)
    let url = 'http://127.0.0.1:5000/api/v1/entries/' + myId
    fetch( url, {
        method: 'PUT',
        headers: {Authorization : `Bearer ${document.cookie}`,
        'Content-Type':'application/json'},
        body: JSON.stringify({title:title, content:content})
    })
        .then((response) => response.json())
        .then(function (data) {
            if (data['message']['status'] === 'Success'){
                // location.href='home.html'
                console.log(data)
            }else {
                console.log(data)
            }
        })
    localStorage.removeItem('editEntryId')
}
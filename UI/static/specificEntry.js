function viewSpecific(){
    // location.href='/MyDiary/UI/my_entry.html'
    let entryId = localStorage.getItem("viewEntryId")
    fetch('https://r-mydiary.herokuapp.com/api/v1/entries/' + entryId, {
        method: 'GET',
        headers: {Authorization : `Bearer ${document.cookie}`}
    })
        .then((response) => response.json())
        .then(function (data) {
			if (data['message']['status'] === 'Success') {
			    let newDate = new Date(data['message']['entry']['date'])
                let dateOnly = newDate.toDateString()
                document.getElementById('date').innerText = dateOnly
                document.getElementById('title').innerText = data['message']['entry']['title']
                document.getElementById('content').innerText = data['message']['entry']['content']
			}else{
				alert(data['message']['message'])
			}
        })
    localStorage.removeItem('viewEntryId')
    console.log(localStorage.getItem('viewEntryId'))
    console.log(localStorage.getItem('editEntryId'))

}
function checkHeader(){
    fetch('https://r-mydiary.herokuapp.com/home',{
        method:'GET',
        headers: {Authorization : `Bearer ${document.cookie}`}
    })
        .then((response) => response.json())
        .then((data) => {
            if (data['message'] === 'Welcome user'){
                console.log(data)
                console.log(localStorage.getItem('editClicked'))
                console.log(localStorage.getItem('editEntryId'))
                modifyEntry()
            }if (data['msg'] === "Token has expired") {
                location.href='unauthorized.html'
                console.log(data)
            }if (data['msg'] === "Missing Authorization Header"){
                location.href='login_required.html'
            }
        })
}
function modifyEntry(){
    if (localStorage.getItem("editClicked") === "true"){
        let entryDate = document.getElementById('my_date');
        entryDate.setAttribute('disabled', 'disabled');
        let update = document.getElementById('updateBtn')
        update.style.display = 'block';
        let entryId = localStorage.getItem("editEntryId")
        let myId = parseInt(entryId)
        let url = 'https://r-mydiary.herokuapp.com/api/v1/entries/' + myId
        fetch(url, {
            method: 'GET',
            headers: {Authorization : `Bearer ${document.cookie}`}
        })
            .then((response) => response.json())
            .then(function (data) {
                if (data['message']['status'] === 'Success') {
                    let newDate = new Date(data['message']['entry']['date'])
                    let dateOnly = newDate.toDateString()
                    document.getElementById('my_date').innerText = dateOnly
                    document.getElementById('my_title').value = data['message']['entry']['title']
                    document.getElementById('my_content').innerText = data['message']['entry']['content']
                    // console.log(dateOnly)
                }if (data['message']['status'] === 'Fail'){
                    alert('You can no longer edit this entry!')
                    console.log(data)
                    location.href='home.html'
                }
            });
        localStorage.removeItem("editClicked")
    }else{
        let save = document.getElementById('saveBtn');
        save.style.display = 'block';
        let myDate = new Date();
        let myDay = myDate.toDateString()
        let myString = myDay.toString()
        document.getElementById('my_date').innerText = myString
        console.log(myDay)
    }
}
function editUserEntry() {
    let entryId = localStorage.getItem("editEntryId")
    let title = document.getElementById('my_title').value
    let content = document.getElementById('my_content').innerText
    let myId = parseInt(entryId)
    let url = 'https://r-mydiary.herokuapp.com/api/v1/entries/' + myId
    fetch( url, {
        method: 'PUT',
        headers: {Authorization : `Bearer ${document.cookie}`,
        'Content-Type':'application/json'},
        body: JSON.stringify({title:title, content:content})
    })
        .then((response) => response.json())
        .then(function (data) {
            if (data['message']['status'] === 'Success'){
                location.href='home.html'
            }else {
                // alert(data)
                console.log(data)
            }
        })
    localStorage.removeItem('editEntryId')
}
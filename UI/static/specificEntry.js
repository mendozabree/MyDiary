function viewSpecific(){
    checkExpired()
    let entryId = localStorage.getItem("viewEntryId");
    let token = localStorage.getItem('token');
    document.getElementById('username').innerText = localStorage.getItem('user')

    fetch('https://r-mydiary.herokuapp.com/api/v1/entries/' + entryId, {
    // fetch('http://127.0.0.1:5000/api/v1/entries/' + entryId, {
        method: 'GET',
        headers: {Authorization : `Bearer ${token}`}
    })
        .then((response) => response.json())
        .then(function (data) {
            if (data['msg'] === 'Token has expired'){
			        refreshToken()
            }
			if (data['message']['status'] === 'Success') {
			    let newDate = new Date(data['message']['entry']['date']);
                document.getElementById('date').innerText = newDate.toDateString();
                document.getElementById('title').innerText =
                    data['message']['entry']['title'];
                document.getElementById('content').innerText =
                    data['message']['entry']['content'];
			}
        });
    localStorage.removeItem('viewEntryId')
}
// checks if token is expired and calls function to populate fields
function checkHeader(){
    let token = localStorage.getItem('token');

    fetch('https://r-mydiary.herokuapp.com/home',{
    // fetch('http://127.0.0.1:5000/home',{
        method:'GET',
        headers: {Authorization : `Bearer ${token}`}
    })
        .then((response) => response.json())
        .then((data) => {
            if (data['msg'] === 'Token has expired'){
			        refreshToken()
			    }
            if (data['message'] === 'Welcome user'){
                modifyEntry()
            }
            if (data['msg'] === "Missing Authorization Header"){
                location.href='login_required.html'
            }
            if (data['msg'] === "Not enough segments"){
                location.href='login_required.html'
            }
        })
}
// Get the entry info and populate the fields before the user edits.
function modifyEntry(){
    checkExpired()
    let error = document.getElementById('error');
    error.style.display = 'none';
    document.getElementById('username').innerText = localStorage.getItem('user')
    if (localStorage.getItem("editClicked") === "true"){
        let update = document.getElementById('updateBtn');
        update.style.display = 'block';
        let entryDate = document.getElementById('my_date');
        entryDate.setAttribute('disabled', 'disabled');

        let token = localStorage.getItem('token');
        let entryId = localStorage.getItem("editEntryId");
        let myId = parseInt(entryId);
        let url = 'https://r-mydiary.herokuapp.com/api/v1/entries/' + myId;
        // let url = 'http://127.0.0.1:5000/api/v1/entries/' + myId;

        fetch(url, {
            method: 'GET',
            headers: {Authorization : `Bearer ${token}`}
        })
            .then((response) => response.json())
            .then(function (data) {
                if (data['msg'] === 'Token has expired'){
			        refreshToken()
			    }
                if (data['message']['status'] === 'Success') {
                    let newDate = new Date(data['message']['entry']['date']);
                    document.getElementById('my_date').innerText =
                        newDate.toDateString();
                    document.getElementById('my_title').value =
                        data['message']['entry']['title'];
                    document.getElementById('my_content').innerText =
                        data['message']['entry']['content']
                }
            });
        localStorage.removeItem("editClicked")
    }else{ //Make Save button visible for someone making a new entry
        let save = document.getElementById('saveBtn');
        save.style.display = 'block';
        let myDate = new Date();
        let myDay = myDate.toDateString();
        document.getElementById('my_date').innerText = myDay.toString();
    }
}
function editUserEntry() {
    let entryId = localStorage.getItem("editEntryId");
    let title = document.getElementById('my_title').value;
    let content = document.getElementById('my_content').innerText;
    let token = localStorage.getItem('token');
    let myId = parseInt(entryId);
    let url = 'https://r-mydiary.herokuapp.com/api/v1/entries/' + myId;
    // let url = 'http://127.0.0.1:5000/api/v1/entries/' + myId;

    fetch( url, {
        method: 'PUT',
        headers: {Authorization : `Bearer ${token}`,
        'Content-Type':'application/json'},
        body: JSON.stringify({title:title, content:content})
    })
        .then((response) => response.json())
        .then(function (data) {
            if (data['msg'] === 'Token has expired'){
                refreshToken()
            }
            if (data['message']['status'] === 'Success'){
                location.href='home.html'
            }
        });
    localStorage.removeItem('editEntryId')
}
window.onload = function () {
    let imgUpload = document.getElementById('imgUpload')
    let uploadBtn = document.getElementById('uploadBtn')
    
    uploadBtn.onclick = function () {
        imgUpload.click();
    };
    function previewImage(uploader){
        if(uploader.files && uploader.files[0]){
            let userPicture = document.getElementById('userPicture');
            userPicture.setAttribute('src', window.URL.createObjectURL(uploader.files[0]));
        }
    }
    imgUpload.onchange = function () {
        previewImage(this)
    }
};
function changeUsername() {
    let username = document.getElementById('username').value;
    if (username || username !== "") {
        fetch('https://r-mydiary.herokuapp.com/api/v1/auth/change_username',{
            method: 'PUT',
            headers: {Authorization : `Bearer ${document.cookie}`,
            'Content-Type':'application/json'},
            body: JSON.stringify({username:username})
        })
            .then((response) => response.json())
            .then((data) => {
                if (data['message']['status'] === 'Success'){
                    let msg = document.getElementById('uname')
                    msg.style.display = 'block'
                    document.getElementById('uname').innerText = data['message']['message']
                    document.getElementById('username').value = ''
                } else {
                    let error = document.getElementById('errorMsg')
                    error.style.display = 'block'
                    document.getElementById('errorMsg').innerText = data['message']['message']
                }
            })
    }let error = document.getElementById('uname')
    error.style.display = 'none'

}
function changePassword() {
    let currentPassword = document.getElementById('currentPassword').value;
    let newPassword = document.getElementById('newPassword').value;
    let confirmPassword = document.getElementById('confirmPassword').value;
    if (newPassword || newPassword !== "") {
        fetch('https://r-mydiary.herokuapp.com/api/v1/auth/change_password',{
            method: 'PUT',
            headers: {Authorization : `Bearer ${document.cookie}`,
            'Content-Type':'application/json'},
            body: JSON.stringify({current_password:currentPassword,
                new_password: newPassword, confirm_password:confirmPassword})
        })
            .then((response) => response.json())
            .then((data) => {
                if (data['message']['status'] === 'Success'){
                    let msg = document.getElementById('pswd')
                    msg.style.display = 'block'
                    document.getElementById('pswd').innerText = data['message']['message']
                    document.getElementById('currentPassword').value = ''
                    document.getElementById('newPassword').value = ''
                    document.getElementById('confirmPassword').value = ''
                } else {
                    let error = document.getElementById('errorMsg')
                    error.style.display = 'block'
                    document.getElementById('errorMsg').innerText = data['message']['message']
                }
            })
    }let error = document.getElementById('errorMsg')
    error.style.display = 'none'
    let msg = document.getElementById('pswd')
    msg.style.display = 'none'
}
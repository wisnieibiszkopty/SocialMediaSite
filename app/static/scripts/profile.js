$(document).ready(function(){
    $('#change-about-submit').click(changeAbout);
    $('#change-avatar-submit').click(changeAvatar);
    $('#change-bg-submit').click(changeBackground);
    $('#create-comment').click(addComment);
})

function changeAbout(){
    let user_id = $('#user-id').text();
    let text = $('#about').val();
    console.log(text);
    data = {};
    data.user_id = user_id;
    data.text = text;
    console.log(data);
    fetch('edit-about',{
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if(result.status === "0"){
            location.reload();
        } else{
            console.log("Nie udało się zmienić opisu.");
        }
    })
    .catch(error => {

    })
}

function changePicture(type, file){
    const user_id = $('#user-id').text();
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', user_id);
    formData.append('type', type);

    fetch('edit-picture', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        if(result.status === "0"){
            location.reload();
        } else{
            console.log("Wystąpił problem z dodaniem zdjęcia do bazy danych");
        }
    })
    .catch(error => {
        console.error("Błąd: ", error);
    });
}

function changeAvatar(){
    const fileInput = document.querySelector('input[type="file"]');
    const file = fileInput.files[0];
    changePicture(1, file);
    console.log(fileInput + " " + fileInput.length)
    console.log(file);
}

function changeBackground(){
    const fileInput = document.querySelectorAll('input[type="file"]')[1];
    const file = fileInput.files[0];
    changePicture(2, file);
    console.log(fileInput + " " + fileInput.length)
    console.log(file);
}

function addComment(){
    let text = $("#add-comment").val();
    const user_tag = $('#user-id').text();
    let data = {};
    data.text = text;
    data.user_tag = user_tag;

    if(text.length < 3) console.log("Komentarz musi mieć przynajmniej 3 znaki.");
    else{
        fetch('add-comment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json',},
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {

        })
        .then(error => {
            console.error("Błąd: ", error);
        })
    }
}
import { fetchAPI } from "./script.js";

$(document).ready(function(){
    $('#change-about-submit').click(function(){
        let user_id = $('#user-id').text();
        let text = $('#about').val();
        console.log(text);
        let data = {};
        data.user_id = user_id;
        data.text = text;
        fetchAPI('edit-about', JSON.stringify(data), changeAbout);
    });

    $('#change-avatar-submit').click(changeAvatar);
    $('#change-bg-submit').click(changeBackground);

    $('#create-comment').click(function(){
        let text = $("#add-comment").val();
        const user_tag = $('#user-id').text();
        let data = {};
        data.text = text;
        data.user_tag = user_tag;

        if(text.length < 3) console.log("Komentarz musi mieć przynajmniej 3 znaki.");
        else fetchAPI('add-comment', JSON.stringify(data), addComment);
    });

    $('.delete-comment').click(function(){
        let parent = $(this).parent().parent();
        let id = parent.attr('id');
        fetchAPI('delete-comment', JSON.stringify(id), deleteComment);
    });

    //$('#comments-tab').click();
    $('#posts-tab').click(function(){
        const user_tag = $('#user-id').text();
        console.log(user_tag);
        let data = {};
        data.usertag = user_tag;
        fetchAPI('get-posts', JSON.stringify(data), getPosts);
    });
    //$('#answears-tab').click(getAnswears);
    //$('#friends-tab').click(getFriends);
})

function changeAbout(result){
    if(result.status === "0"){
        location.reload();
        $('#about').val('');
    }
    else console.log("Nie udało się zmienić opisu.");
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

function addComment(result){
    if(result.status === "0") {
        location.reload();
        $("#add-comment").val('');
    }
}

function deleteComment(result){
    console.log(result.id);
    if(result.status === "0"){
        $('#' + result.id).remove();
    } else console.log("Nie udało się usunąć komentarza");
}

function getPosts(result){
    console.log(result.data);
    let div;
    let a;
    for(let i=0; i<result.data.length;i++){
        div = document.createElement('div');
        div.classList.add('user-post');
        a = document.createElement('a');
        a.setAttribute('href', '/post/' + result.data[i][2] + '/' + result.data[i][1]);
        a.innerText += result.data[i][0];
        div.appendChild(a);
        $('#posts-details').append(div);
    }
}

function getAnswears(result){
    console.log("get answears");
}

function getFriends(result){
    console.log("get friends");
}
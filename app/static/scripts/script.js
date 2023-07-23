import { checkRegistration, checkLogin } from "./validation.js";

export function fetchAPI(url, data, func){
    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: data
    })
    .then(response => response.json())
    .then(result => {
        func(result);
    })
    .catch(error => {
        console.error("Błąd: ", error);
    })
}

window.addEventListener('beforeunload',function(){
    let css_variables = {};
    css_variables.main = $('main').css('background-color');
    css_variables.second = $('#sidebar').css('background-color');
    css_variables.text = $('main').css('color');
    css_variables.icon = $('#mode').attr('class');
    let css_json = JSON.stringify(css_variables);
    localStorage.setItem('css_styles', css_json);
})

document.addEventListener('DOMContentLoaded', function(){
    let root = document.querySelector(':root');
    if(localStorage.getItem('css_styles')){
        let css_variables = JSON.parse(localStorage.getItem('css_styles'));
        root.style.setProperty('--main', css_variables.main);
        root.style.setProperty('--second', css_variables.second);
        root.style.setProperty('--text', css_variables.text);
        $('#mode').removeClass();
        $('#mode').addClass(css_variables.icon);
    } 
})

$(document).ready(function(){
    $('#mode').click(changeMode);

    $('#show-list').click(openNav);
    $('#cls-btn').click(closeNav);

    $('.dropbtn').click(function(){
        let dropdown = $('#dropdown');
        let avatar = $('#profile-avatar');
        dropdown.toggleClass('show');
        if(dropdown.hasClass('show')){
            avatar.removeClass('bi-caret-down-fill');
            avatar.addClass('bi-caret-up-fill')
        } else{
            avatar.removeClass('bi-caret-up-fill');
            avatar.addClass('bi-caret-down-fill')
        }
    });

    $("#registration-submit").click(function(){
        let validation = checkRegistration();
        if(validation){
            let data = {};
            data.username = $("#username").val();
            data.user_id = $("#user_id").val();
            data.email = $("#email").val();
            data.pass = $("#pass1").val();
            sendRegistrationForm(data);
        }
    })

    $("#login-submit").click(loginSubmit);

    $("#logout").click(function(){
        fetch('/logout')
            .then(function(response) {
                location.reload()
            })
            .catch(function(error) {
                console.error(error);
            });
    })

    $("#add-post-submit").click(addPost);
})

function loginSubmit(){
    let validation = checkLogin();
    if(validation){
        let data = {}
        data.email = $("#login-email").val();
        data.pass = $("#pass").val();
        sendLoginForm(data);
    }
}

function changeMode(){
    let root = document.querySelector(':root');

    if($('#mode').hasClass('bi-sun')){
        $('#mode').removeClass('bi-sun');
        $('#mode').addClass('bi-moon');
        root.style.setProperty('--main', '#ffffff');
        root.style.setProperty('--second', '#e7e9eb')
        root.style.setProperty('--text','#000000');
    } 
    else{
        $('#mode').removeClass('bi-moon');
        $('#mode').addClass('bi-sun');
        root.style.setProperty('--main', '#1f1f1f');
        root.style.setProperty('--second','#181818');
        root.style.setProperty('--text','#ffffff');
    }
}

function openNav(){
    document.getElementById("sidebar").style.width = "20%";
}

function closeNav(){
    document.getElementById("sidebar").style.width = "0";
}

document.getElementById("loginModal").addEventListener("keydown", (e) => {
    if(e.key === "Enter"){ loginSubmit(); }
})

function sendLoginForm(data){
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        if(result.status === "0"){
            location.reload();
        } else{
            let loginDiv = "<div id='lg-msg' class='alert alert-danger" +
            " alert-dismissible fade show' role='alert'></div>";
            let button = "<button type='button' class='btn-close' " +
            " data-bs-dismiss='alert' aria-label='Close'></button>";
            let message = "Użytkownik o takim adresie e-mail i haśle nie istnieje!"
            $('#login-message').html(loginDiv);
            $('#lg-msg').html(message + button);
        }
    })
    .catch(error => {
        console.error('Błąd: ',error);
    })
}

function sendRegistrationForm(data){
    fetch('/registration', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
      if(result.status === "0"){
        const fileInput = document.querySelector('input[type="file"]');
        const file = fileInput.files[0];
        uploadAvatar(file, data.user_id);
      } else{
        console.log("Nie udało się dodać użytkownika.");
        let div = "<div id='rg-msg' class='alert alert-danger" +
        " alert-dismissible fade show' role='alert'></div>";
        let button = "<button type='button' class='btn-close' " +
        " data-bs-dismiss='alert' aria-label='Close'></button>";
        let message = "Użytkownik o takim adresie e-mail lub identyfikatorze już istnieje!"
        $('#register-message').html(div);
        $('#rg-msg').html(message + button);
      }
    })
    .catch(error => {
      // Obsługa błędów
      console.error('Błąd:', error);
    });
}

function uploadAvatar(file, user_id){
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', user_id);

    fetch('/upload_avatar', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        if(result.status === "0"){
            console.log(result.redirect);
            window.location.href = result.redirect;
        } else{
            console.log("Wystąpił problem z dodaniem zdjęcia do bazy danych");
        }
    })
    .catch(error => {
        console.error("Błąd: ", error);
    });
}

function addPost(){
    let post = {};
    post.title = $('#post-title').val();
    post.content = $('#post-content').val();

    let fileInput = document.getElementById("post-img");
    let file = fileInput.files;
    post.hasFile = file.length > 0;
    console.log(post.hasFile);
    console.log(fileInput.files[0]);

    let video_link = $('#add-video').val();
    post.video_link = convertYoutubeUrl(video_link);

    // nie ma zdjęcia, sprawdź dlaczego
    fetch('/post/create-post', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', },
        body: JSON.stringify(post)
    })
        .then(response => response.json())
        .then(result => {
            console.log(result.status);
            if(result.status === "0"){
                const formData = new FormData();
                console.log(result.post_id);
                formData.append('post_id', result.post_id);
                formData.append('file', fileInput.files[0]);
                if(post.hasFile){
                    fetch('/post/add-image',{
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json())
                    .then(result => {
                        console.log(result.status);
                        if(result.status === "0") window.location.href = result.redirect;                        
                    })
                    .catch(error => { console.error("Błąd: ", error); });
                } 
            } else if(result.status === "1") window.location.href = result.redirect;  
        })
        .catch(error => { console.error("Błąd: ", error); });
}

function convertYoutubeUrl(url){
    return url.slice(32, 43);
}
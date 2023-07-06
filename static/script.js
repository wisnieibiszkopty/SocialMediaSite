import { checkRegistration, checkLogin } from "./validation.js";

window.addEventListener('beforeunload',function(){
    let css_variables = {};
    css_variables.main = $('main').css('background-color');
    css_variables.second = $('#sidebar').css('background-color');
    css_variables.text = $('main').css('color');
    css_variables.icon = $('#mode').attr('class');
    css_json = JSON.stringify(css_variables);
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

    $("#registration-submit").click(function(){
        let validation = checkRegistration();
        if(validation){
            let data = {};
            data.username = $("#username").val();
            data.user_id = $("#user_id").val();
            data.email = $("#email").val();
            data.pass = $("#pass1").val();
            sendRegistrationForm(data);

            const fileInput = document.querySelector('input[type="file"]');
            const file = fileInput.files[0];
            uploadAvatar(file);
        }
    })

    $("#login-submit").click(function(){
        let validation = checkLogin();
        if(validation){
            let data = {}
            data.email = $("#login-email").val();
            data.pass = $("#pass").val();
            sendLoginForm(data);
        }
    })
})

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
    document.getElementById("sidebar").style.width = "15%";
}

function closeNav(){
    document.getElementById("sidebar").style.width = "0";
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
      // Otrzymane dane z serwera
      console.log(result);
    })
    .catch(error => {
      // Obsługa błędów
      console.error('Błąd:', error);
    });
}

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
            console.log("DZIAŁA!!!!");
            //location.reload();
        }
    })
    .catch(error => {
        console.error('Błąd: ',error);
    })
}

function uploadAvatar(file){
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload_avatar', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(result => {
        console.log(result);
    })
    .catch(error => {
        console.error("Błąd: ", error);
    });
}
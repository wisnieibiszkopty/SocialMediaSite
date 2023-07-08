let div = "<div id='rg-msg' class='alert alert-danger alert-dismissible fade show' role='alert'></div>";
let loginDiv = "<div id='lg-msg' class='alert alert-danger alert-dismissible fade show' role='alert'></div>";
let button = "<button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button>";

// do ogólnej poprawy, ale działa

function checkInput(id,regex,message) {
    let input = document.getElementById(id);
    if(!regex.test(input.value)){
        $('#register-message').html(div);
        $('#rg-msg').html(message + button);
        return false;
    }
    return true;
}

function checkLoginInput(id,regex,message){
    let input = document.getElementById(id);
    if(!regex.test(input.value)){
        $('#login-message').html(loginDiv);
        $('#lg-msg').html(message + button);
        return false;
    }
    return true;
}

function checkName(){
    let id = 'username';
    let message = 'Musisz podać poprawną nazwę Użytkownika!';
    let regex = new RegExp("^[a-zA-Z0-9]{3,}$");
    return checkInput(id, regex, message);
}

function checkId(){
    let id = 'user_id';
    let message = 'Musisz podać poprawny identyfikator Użytkownika!';
    let regex = new RegExp("^[a-zA-Z0-9]{3,}$");
    return checkInput(id, regex, message);
}

function checkEmail(){
    let id = 'email';
    let message = "To nie wygląda jak adres e-mail!";
    let regex = new RegExp("^[a-zA-Z0-9_]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]+$");
    return checkInput(id, regex, message);
}

function checkLoginEmail(){
    let id = 'login-email';
    let message = "To nie wygląda jak adres e-mail!";
    let regex = new RegExp("^[a-zA-Z0-9_]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]+$");
    return checkLoginInput(id, regex, message);

}

function checkPassword(){
    let id = 'pass1';
    let message = 'Musisz podać poprawne hasło!';
    let regex = new RegExp("^[a-zA-Z0-9]{3,}$");
    return checkInput(id, regex, message);
}

function checkLoginPassword(){
    let id = 'pass';
    let message = 'Musisz podać poprawne hasło!';
    let regex = new RegExp("^[a-zA-Z0-9]{3,}$");
    return checkLoginInput(id, regex, message);
}

function checkIfPasswordAreSame(){
    let pass1 = $('#pass1').val();
    let pass2 = $('#pass2').val();
    if(pass1 === pass2) return true;
    else{
        $('#register-message').html(div);
        let message = "Hasła nie są identyczne!";
        $('#rg-msg').html(message + button);
        return false;
    } 
}

function checkImage(){
    const fileInput = document.getElementById('img');
    const selectedFiles = fileInput.files;

    if(selectedFiles.length > 0) return true;
    else{
        $('#register-message').html(div);
        let message = "Zdjęcie profilowe nie zostało przesłane lub jest nieprawidłowe!";
        $('#rg-msg').html(message + button);
        return false;
    }
}

export function checkLogin(){
    let validation;
    validation = checkLoginEmail();
    if(!validation) return false;
    validation = checkLoginPassword();
    return validation;

}

export function checkRegistration(){
    let validation;
    validation = checkName();
    if(!validation) return false;
    validation = checkId();
    if(!validation) return false;
    validation = checkEmail();
    if(!validation) return false;
    validation = checkPassword();
    if(!validation) return false;
    validation = checkIfPasswordAreSame();
    if(!validation) return false;
    validation = checkImage();
    return validation;
}
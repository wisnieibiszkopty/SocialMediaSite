import { fetchAPI } from "./script.js";

document.addEventListener('DOMContentLoaded', function(){
    let img = $('#post-image');
    let src = img.attr('src');
    if(src === "/static/"){
        let parent = img.parent();
        parent.remove();
    }

    let yt_player = $('#yt-player');
    if(yt_player.html() === "") yt_player.remove();
})

$(document).ready(function(){
    $('#answear-btn').click(function(){
        console.log('działa');
        let data = {};
        let text = $('#answear-text').val();
        if(text.length > 2) data.text = text;
        const currentUrl = window.location.href;
        let post_id = currentUrl.lastIndexOf('/');
        let post = currentUrl.slice(post_id+1, currentUrl.length);
        fetchAPI(post + '/add-comment', JSON.stringify(data), addAnswear);
    });

    $('#post-image img').click(imageFullscreen);
})

function addAnswear(result){
    if(result.status === "0"){
        $('#answear-text').val('');
        location.reload();
    } else console.log("Nie udało się dodać odpowiedzi.");
}

function imageFullscreen(){
    let div = document.createElement('div');
    let img_src = $('#post-image img').attr('src');
    let img = document.createElement('img');
    img.setAttribute('src',img_src);
    img.setAttribute('alt',img_src);
    img.setAttribute('id', 'fullscreen-img');
    div.appendChild(img);
    div.classList.add('highlight');
    div.setAttribute('id', 'fullscreen');
    document.body.appendChild(div);
}

window.onclick = function (event){
    let img = document.getElementById('fullscreen-img');

    if(event.target.contains(img)){
        $('#fullscreen').remove();
    }
}

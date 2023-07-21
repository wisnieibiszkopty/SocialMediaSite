document.addEventListener('DOMContentLoaded', function(){
    let img = $('#post-image');
    let src = img.attr('src');
    if(src === "/static/"){
        let parent = img.parent();
        console.log(parent);
        parent.remove();
    }

    let yt_player = $('#yt-player');
    if(yt_player.html() === "") yt_player.remove();
})

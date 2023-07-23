let page = 1;
let loadPage = true;

// 5 ostatnich pytań się póki co nie wczytuje bo jest powtrzymywane, ale
// serwer nie dostaje też próśb o nowe posty

const throttleFunction=(func, delay)=>{
    let prev = 0;
    return (...args) => {
        let now = new Date().getTime();
        if(now - prev> delay){
            prev = now;
            return func(...args);
        }
    }
}

function loadPages(){
    if(!loadPage) $(window).removeEventListener('scroll', throttleFunction);
    if($(window).scrollTop() + $(window).height() > $(document).height() - 200){
        getPosts();
    }
}

$(window).scroll(throttleFunction(loadPages, 100));

function getPosts(){
    fetch('index/' + page)
        .then(response => response.json())
        .then(data => {
            let post = {};
            console.log("Ilość wczytanych elementów: " + data.length);
            for(let i=0; i<data.length; i++){
                post.user_id = data[i][0];
                post.username = data[i][1];
                post.usertag = data[i][2];
                post.avatar = data[i][3];
                post.post_id = data[i][4];
                post.title = data[i][5];
                post.date = data[i][6];

                console.log(post);

                let post_div = document.createElement('div');
                let user_div = document.createElement('div');
                let avatar = document.createElement('a');
                let img = document.createElement('img');
                img.setAttribute('src','/static/images/avatars/' + post.avatar);
                avatar.setAttribute('href', '/profile/' + post.usertag);
                avatar.appendChild(img);

                let user_information = document.createElement('div');
                let username = document.createElement('p');
                username.innerText += post.username;
                let date = document.createElement('p');
                date.innerText += post.date;
                user_information.appendChild(username);
                user_information.appendChild(date);

                user_div.appendChild(avatar);
                user_div.appendChild(user_information);

                let title_div = document.createElement('div');
                let title = document.createElement('a');
                title.innerText += post.title;
                title.setAttribute('href', '/post/' + post.user_id + '/' + post.post_id);
                title_div.appendChild(title);

                post_div.setAttribute('class', 'post')
                post_div.appendChild(user_div);
                post_div.appendChild(title_div);
                $('#posts').append(post_div);

                loadPage = post.post_id > 5;
                console.log("Load page: " + loadPage);
            }
            
        })
        .catch(error => {
            console.error('Błąd:', error);
        });

    page ++;
}

getPosts();
from flask import Blueprint, request, jsonify, session, current_app, url_for, render_template
from app.DatabaseConnector import UseDatabase, ConnectionError, CredentialsError, SQLError
import app.utils as utl

bp = Blueprint('post', __name__, url_prefix='/post')


@bp.route('/<user_id>/<post_id>')
def view_post(user_id, post_id):
    try:
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            sql = """SELECT COUNT(*) FROM post WHERE post_id = %s AND user_id = %s"""
            cursor.execute(sql, (post_id, user_id))
            count = cursor.fetchall()
            if count[0][0] != 0:
                sql = """SELECT user.username, user.usertag, user.avatar, post.date, post.title, post.content, post.has_file,
                post.video_link FROM post INNER JOIN user ON user.user_id=post.user_id WHERE post_id = %s"""
                cursor.execute(sql, (post_id, ))
                data = cursor.fetchall()
                data = data[0]
                username = data[0]
                usertag = data[1]
                avatar = "images/avatars/" + data[2]
                date = data[3]
                post_title = data[4]
                content = data[5]
                has_file = data[6]
                video_link = data[7]
                print(has_file)
                if has_file != 0:
                    image = "images/posts/" + post_id + "_" + data[2]
                    print(image)
                else:
                    image = ""

                if video_link != "":
                    video_link = utl.create_youtube_player(video_link)

                return render_template('post.html', title=post_title,
                                       username=username,
                                       usertag=usertag,
                                       avatar=avatar,
                                       date=date,
                                       post_title=post_title,
                                       content=content,
                                       image=image,
                                       video=video_link)
    except SQLError as err:
        print(err)


@bp.route('/create-post', methods=['POST'])
def create_post():
    data = request.json
    print(data)
    title = data['title']
    content = data['content']
    has_file = data['hasFile']
    video_link = data['video_link']
    user_id = session['user_id']
    date = utl.get_date_with_hours()

    try:
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            sql = """INSERT INTO post (user_id, title, content, has_file, video_link, date) 
            VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (user_id, title, content, has_file, video_link, date))
            sql = """SELECT count(*) FROM post"""
            cursor.execute(sql)
            count = cursor.fetchall()
    except SQLError as err:
        print(err)
        return jsonify({"status": "2"})

    if not has_file:
        return jsonify({"status": "1",
                        "redirect": url_for('post.view_post', user_id=user_id, post_id=count[0][0])})

    return jsonify({"status": "0",
                    "post_id": count[0][0]})


@bp.route('/add-image', methods=['POST'])
def add_image():
    if 'file' not in request.files:
        print("nie ma zdjęcia")
        return jsonify({"status": "1"})

    file = request.files['file']
    usertag = session['user_tag']
    user_id = session['user_id']
    post_id = request.form.get('post_id')
    filename = str(post_id) + "_" + utl.hash_image_name(usertag)
    file.save('app/static/images/posts/' + filename)
    result = {"status": "0",
              "redirect": url_for('post.view_post', user_id=user_id, post_id=post_id)}
    return result


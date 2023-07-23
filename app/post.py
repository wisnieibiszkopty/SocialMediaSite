from flask import Blueprint, request, jsonify, session, current_app, url_for, render_template
from app.DatabaseConnector import UseDatabase, ConnectionError, CredentialsError, SQLError
import app.utils as utl
from app.utils import Answear

bp = Blueprint('post', __name__, url_prefix='/post')


@bp.route('/<user_id>/<post_id>')
def view_post(user_id, post_id):
    try:
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            sql = """SELECT COUNT(*) FROM post WHERE post_id = %s AND user_id = %s"""
            cursor.execute(sql, (post_id, user_id))
            count = cursor.fetchall()
            if count[0][0] != 0:
                sql = """SELECT user.username, user.usertag, user.avatar, post.date,
                post.title, post.content, post.has_file,
                post.video_link, COUNT(post_upvotes.post_id), COUNT(post_downvotes.post_id),
                COUNT(post_heart.post_id), COUNT(post_answears.post_id) 
                FROM post LEFT JOIN post_upvotes ON post_upvotes.post_id=post.post_id
                LEFT JOIN post_downvotes ON post_downvotes.post_id=post.post_id
                LEFT JOIN post_heart ON post_heart.post_id=post.post_id
                LEFT JOIN post_answears ON post_answears.post_id=post.post_id
                INNER JOIN user ON user.user_id=post.user_id WHERE post.post_id = %s
                GROUP BY user.username, user.usertag, user.avatar,
                post.date, post.title, post.content, post.has_file, post.video_link"""
                cursor.execute(sql, (post_id, ))
                data = cursor.fetchall()
                data = data[0]
                print(data)
                username = data[0]
                usertag = data[1]
                avatar = "images/avatars/" + data[2]
                date = data[3]
                post_title = data[4]
                content = data[5]
                has_file = data[6]
                video_link = data[7]
                upvotes = data[8]
                downvotes = data[9]
                hearts = data[10]
                comments = data[11]

                print("upvotes: " + str(upvotes) + " downvotes: " + str(downvotes) + " hearts: " + str(hearts) + " comments: " + str(comments))
                if has_file != 0:
                    image = "images/posts/" + post_id + "_" + data[2]
                else:
                    image = ""

                if video_link != "":
                    video_link = utl.create_youtube_player(video_link)

                sql = """SELECT post_answears.text, post_answears.user_id,
                user.username, user.usertag, user.avatar FROM post_answears
                INNER JOIN user ON user.user_id = post_answears.user_id
                WHERE post_id = %s"""

                cursor.execute(sql, (post_id,))
                answears_list = cursor.fetchall()
                answears = []
                for answear in answears_list:
                    answears.append(Answear(answear[0], answear[1], answear[2], answear[3], answear[4]))

                return render_template('post.html', title=post_title,
                                       username=username,
                                       usertag=usertag,
                                       avatar=avatar,
                                       date=date,
                                       post_title=post_title,
                                       content=content,
                                       image=image,
                                       video=video_link,
                                       upvotes=upvotes,
                                       downvotes=downvotes,
                                       hearts=hearts,
                                       comments=comments,
                                       answears=answears)
    except SQLError as err:
        print(err)
        return jsonify({"status": "1"})


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


@bp.route('/<user_id>/<post_id>/add-comment', methods=['POST'])
def add_comment(user_id, post_id):
    data = request.json
    text = data['text']
    user = session['user_id']

    try:
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            sql = """INSERT INTO post_answears (post_id, user_id, text) VALUES (%s, %s, %s)"""
            cursor.execute(sql, (post_id, user, text))
        return jsonify({"status": "0"})
    except SQLError as err:
        print(err)

    return jsonify({"status": "1"})

from flask import Blueprint, render_template, request, session, jsonify, url_for, redirect, current_app
from app.DatabaseConnector import UseDatabase, ConnectionError, CredentialsError, SQLError
import app.utils as utl
from app.utils import Post

bp = Blueprint('base', __name__)


@bp.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@bp.route('/')
@bp.route('/home')
def home_page():
    try:
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            sql = """SELECT user.user_id, user.username, user.usertag, user.avatar, post.post_id, post.title, post.date FROM post
            INNER JOIN user ON post.user_id=user.user_id ORDER BY post.date DESC LIMIT 10"""
            cursor.execute(sql)
            posts_data = cursor.fetchall()
            posts = []
            for post in posts_data:
                posts.append(Post(post[0], post[1], post[2], post[3], post[4], post[5], post[6]))

    except SQLError as err:
        print(err)

    return render_template("index.html", posts=posts)


@bp.route('/groups/<group_id>')
def group_page(group_id):
    return 'Znajdujesz się na stronie grupy ' + group_id


@bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data['email']
    password = data['pass']
    print("email: " + email + " pass: " + password)
    hash_password = utl.hash_password(password)

    with UseDatabase(current_app.config['dbconfig']) as cursor:
        sql = """SELECT usertag, avatar, user_id FROM user WHERE email = %s AND password = %s """
        cursor.execute(sql, (email, hash_password))
        user_data = cursor.fetchall()
        if user_data:
            session['user_tag'] = user_data[0][0]
            session['avatar_path'] = "images/avatars/" + user_data[0][1]
            session['user_id'] = user_data[0][2]
            result = {"status": "0"}
        else:
            result = {"status": "1"}

    return jsonify(result)


@bp.route('/registration', methods=['POST'])
def register_user():
    data = request.get_json()
    usertag = data['user_id']
    username = data['username']
    email = data['email']
    password = data['pass']
    hash_password = utl.hash_password(password)
    filename = utl.hash_image_name(usertag)

    try:
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            sql = """SELECT COUNT(*) FROM user WHERE usertag = %s OR email = %s"""
            cursor.execute(sql, (usertag, email))
            count = cursor.fetchall()
            if count[0][0] == 0:
                sql = """INSERT INTO profile (background, about_me, join_date) values (%s, %s, %s)"""
                cursor.execute(sql, (filename, "", utl.get_date()))
                sql = """SELECT COUNT(*) FROM profile"""
                cursor.execute(sql)
                profile_id = cursor.fetchall()[0][0]
                print(profile_id)

                sql = """INSERT INTO user (usertag, username, email, password, avatar, profile_id)
                VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (usertag, username, email, hash_password, filename, profile_id))
                session['user_id'] = usertag
                print("Dodano użytkownika do bazy danych")
                result = {"status": "0"}
            else:
                print("Nie udało się dodać użytkownika")
                result = {"status": "1"}
    except SQLError as err:
        print(err)
        result = {"status": "1"}
    return jsonify(result)


@bp.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'file' not in request.files:
        result = {"status": "1"}
        return jsonify(result)

    file = request.files['file']
    user_id = request.form.get('user_id')
    print("USER: " + user_id)
    filename = utl.hash_image_name(user_id)
    print("FILENAME: " + filename)
    file.save('app/static/images/avatars/' + filename)
    background = utl.createProfileBackground(file)
    background.save('app/static/images/backgrounds/' + filename)
    result = {"status": "0",
              "redirect": url_for('profile.user_profile', user_id=user_id)}

    return jsonify(result)


@bp.route('/logout')
def logout():
    session.clear()
    return "ok"

from flask import Flask, render_template, request, session, jsonify, url_for, redirect
from src.DatabaseConnector import UseDatabase, ConnectionError, CredentialsError, SQLError
from secrets import token_hex
import src.utils as utl

app = Flask(__name__, template_folder='html')

app.secret_key = token_hex()

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'website_admin',
                          'password': 'website',
                          'database': 'social_media'}


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.route('/')
@app.route('/home')
def home_page():
    if 'username' in session:
        username = session['username']
    else:
        username = ""
    return render_template("index.html", username=username)


@app.route('/profile/<user_id>')
def user_profile(user_id):
    with UseDatabase(app.config['dbconfig']) as cursor:
        sql = """SELECT usertag, username, join_date, avatar FROM user WHERE usertag = %s"""
        cursor.execute(sql, (user_id,))
        data = cursor.fetchall()
        if data:
            user_id = data[0][0]
            username = data[0][1]
            join_date = data[0][2]
            avatar = data[0][3]
            filename = "/images/avatars/" + avatar
            background = "/images/backgrounds/" + avatar

            return render_template("profile.html", title="Profil " + username,
                                   username=username,
                                   user_id=user_id,
                                   date=join_date,
                                   friends=0,
                                   about_me="placeholder",
                                   filename=filename,
                                   background=background)
        else:
            return redirect("404.html", 404)


@app.route('/groups/<group_id>')
def group_page(group_id):
    return 'Znajdujesz się na stronie grupy ' + group_id


@app.route('/post/<post_id>')
def show_post(post_id):
    return 'Post ' + post_id


@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data['email']
    password = data['pass']
    print("email: " + email + " pass: " + password)
    hash_password = utl.hash_password(password)

    with UseDatabase(app.config['dbconfig']) as cursor:
        sql = """SELECT usertag FROM user WHERE email = %s AND password = %s """
        cursor.execute(sql, (email, hash_password))
        user_data = cursor.fetchall()
        if user_data:
            session['user_id'] = user_data[0][0]
            result = {"status": "0"}
        else:
            result = {"status": "1"}

    return jsonify(result)


@app.route('/registration', methods=['POST'])
def register_user():
    data = request.get_json()
    usertag = data['user_id']
    username = data['username']
    email = data['email']
    password = data['pass']
    hash_password = utl.hash_password(password)
    filename = utl.hash_image_name(usertag)

    with UseDatabase(app.config['dbconfig']) as cursor:
        sql = """SELECT COUNT(*) FROM user WHERE usertag = %s OR email = %s"""
        cursor.execute(sql, (usertag, email))
        count = cursor.fetchall()
        if count[0][0] == 0:
            sql = """INSERT INTO profile (background, about_me) values (%s, %s)"""
            cursor.execute(sql, (filename, ""))
            sql = """SELECT COUNT(*) FROM profile"""
            cursor.execute(sql)
            profile_id = cursor.fetchall()[0][0]

            sql = """INSERT INTO user (usertag, username, email, password, avatar, profile_id)
            VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (usertag, username, email, hash_password, filename, profile_id))
            session['user_id'] = usertag
            print("Dodano użytkownika do bazy danych")

            result = {"status": "0"}
        else:
            print("Nie udało się dodać użytkownika")
            result = {"status": "1"}

    return jsonify(result)


@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'file' not in request.files:
        result = {"status": "1"}
        return jsonify(result)

    file = request.files['file']
    user_id = request.form.get('user_id')
    filename = utl.hash_image_name(user_id)
    file.save('static/images/avatars/' + filename)
    background = utl.createProfileBackground(file)
    background.save('static/images/backgrounds/' + filename)
    result = {"status": "0",
              "redirect": url_for('user_profile', user_id=user_id)}

    return jsonify(result)


@app.route('/logout')
def logout():
    session.clear()
    return "ok"


if __name__ == '__main__':
    app.run(debug=True)

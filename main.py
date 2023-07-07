from flask import Flask, render_template, request, session, jsonify, url_for
from src.DatabaseConnector import UseDatabase, ConnectionError, CredentialsError, SQLError
from secrets import token_hex
import src.utils as utl

app = Flask(__name__, template_folder='html')

app.secret_key = token_hex()

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'website_admin',
                          'password': 'website',
                          'database': 'social_media'}


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
        sql = """SELECT username, email FROM user WHERE user_id = %s"""
        cursor.execute(sql, (user_id,))
        data = cursor.fetchall()
        username = data[0][0]
        email = data[0][1]
        filename = "/images/avatars/" + utl.hash_image_name(user_id)

    return render_template("profile.html", title="Profil " + username,
                           filename=filename,
                           username=username,
                           user_id=user_id,
                           email=email)


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
        sql = """SELECT user_id, username, email, password FROM user WHERE email = %s AND password = %s """
        cursor.execute(sql, (email, password))
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
    user_id = data['user_id']
    username = data['username']
    email = data['email']
    password = data['pass']

    with UseDatabase(app.config['dbconfig']) as cursor:
        sql = """SELECT COUNT(*) FROM user WHERE user_id = %s OR email = %s"""
        cursor.execute(sql, (user_id, email))
        count = cursor.fetchall()
        if count[0][0] == 0:

            sql = """INSERT INTO user (user_id, username, email, password)
            VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (user_id, username, email, password))
            session['user_id'] = user_id
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
    result = {"status": "0",
              "redirect": url_for('user_profile', user_id=user_id)}

    return jsonify(result)


@app.route('/logout')
def logout():
    session.clear()
    return "ok"


if __name__ == '__main__':
    app.run(debug=True)

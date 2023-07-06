from flask import Flask, render_template, request, session, jsonify
from secrets import token_hex


app = Flask(__name__, template_folder='html')

app.secret_key = token_hex()


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
    u_id = user_id
    username = user_id
    about_me = "Lubie koty"
    return render_template("profile.html", title="Profil " + username,
                           username=username,
                           user_id=u_id,
                           about_me=about_me)


@app.route('/groups/<group_id>')
def group_page(group_id):
    return 'Znajdujesz się na stronie grupy ' + group_id


@app.route('/post/<post_id>')
def show_post(post_id):
    return 'Post ' + post_id


@app.route('/registration', methods=['POST'])
def register_user():
    data = request.get_json()
    print(data)
    result = {"status": "0"}
    return jsonify(result)


@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    # generowanie funkcji skrótu
    # sprawdzanie w bazie danych czy użytkownik istnieje
    # jeśli nie istnieje zwracamy że nie
    # jeśli tak pobieramy z bazy nazwe użytkownika

    # username = "kamil"
    # session['username'] = username
    result = {"status": "0"}
    return jsonify(result)


@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'file' not in request.files:
        return 'Brak pliku w żądaniu', 400

    file = request.files['file']

    file.save('images/avatars/' + file.filename)

    return 'Plik został przesłany i zapisany pomyślnie!'


if __name__ == '__main__':
    app.run(debug=True)

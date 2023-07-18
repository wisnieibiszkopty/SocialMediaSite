from flask import Blueprint, render_template, current_app, redirect, request, jsonify, session
from app.DatabaseConnector import UseDatabase, ConnectionError, CredentialsError, SQLError
import app.utils as utl

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/<user_id>')
def user_profile(user_id):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        sql = """SELECT user.username, user.join_date, user.avatar, profile.about_me FROM user 
        inner join profile on profile.profile_id=user.profile_id WHERE usertag = %s"""
        cursor.execute(sql, (user_id,))
        data = cursor.fetchall()
        if data:
            username = data[0][0]
            join_date = data[0][1]
            avatar = data[0][2]
            about_me = data[0][3]
            filename = "/images/avatars/" + avatar
            background = "/images/backgrounds/" + avatar

            return render_template("profile.html", title="Profil " + username,
                                   username=username,
                                   user_tag=user_id,
                                   date=join_date,
                                   friends=0,
                                   about_me=about_me,
                                   filename=filename,
                                   background=background)
        else:
            return redirect("404.html", 404)


@bp.route('/edit-about', methods=['POST'])
def edit_about():
    data = request.json
    user_id = data['user_id']
    text = data['text']

    try:
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            sql = """update profile inner join user on user.profile_id = profile.profile_id
                     set profile.about_me = %s where user.usertag = %s; """
            cursor.execute(sql, (text, user_id))
        return jsonify({"status": "0"})
    except SQLError:
        return jsonify({"status": "1"})


@bp.route('/edit-picture', methods=['POST'])
def edit_picture():
    if 'file' not in request.files:
        result = {"status": "1"}
        print(result)
        return jsonify(result)

    image_type = request.form.get('type')
    file = request.files['file']
    user_id = request.form.get('user_id')
    filename = utl.hash_image_name(user_id)

    if image_type == '1':
        file.save('app/static/images/avatars/' + filename)
    elif image_type == '2':
        file.save('app/static/images/backgrounds/' + filename)

    result = {"status": "0"}
    print(result)
    return jsonify(result)


@bp.route('/add-comment', methods=['POST'])
def add_comment():
    data = request.json
    comment = data['text']
    user_tag = data['user_tag']
    user_id = session['user_id']

    try:
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            sql = """select user_id from user where usertag = %s"""
            cursor.execute(sql, (user_tag, ))
            profile_id = cursor.fetchall()
            sql = """insert into profile_comment (user_id, comment, profile_id) values %s %s %s"""
            cursor.execute(sql, (user_id, comment, profile_id))

    except SQLError:
        return jsonify({"status": "1"})

    return jsonify({"status": "0"})

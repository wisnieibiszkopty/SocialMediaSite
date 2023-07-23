from flask import Blueprint, current_app, jsonify
from app.DatabaseConnector import UseDatabase, SQLError
from app.utils import Post

bp = Blueprint('index', __name__, url_prefix='/index')


@bp.route('/<page>', methods=['GET'])
def get_page(page):
    limit = 5
    print("page: " + page)
    try:
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            sql = """SELECT user.user_id, user.username, user.usertag, user.avatar, post.post_id, post.title, post.date FROM post
            INNER JOIN user ON post.user_id=user.user_id ORDER BY post.date DESC LIMIT %s OFFSET %s"""
            cursor.execute(sql, (limit, limit*int(page)))
            posts_data = cursor.fetchall()

            return jsonify(posts_data)
    except SQLError as err:
        print(err)

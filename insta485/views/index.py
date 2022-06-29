"""
Insta485 index (main) view.
URLs include:
/
"""
import flask
import insta485
from flask import request, redirect, url_for, session
import os
import arrow


@insta485.app.route('/')
def show_index():
    """Display / route."""
 
    # Connect to database
    connection = insta485.model.get_db()
    # Query database
    logname = "awdeorio"
    cur = connection.execute(
        "SELECT username, fullname "
        "FROM users "
        "WHERE username != ?",
        (logname, )
    )
    users = cur.fetchall()
    print(users)
    # Add database info to context
    context = {"users": users}
    return flask.render_template("index.html", **context)
  

@insta485.app.route('/main/', methods=['POST'])
def login():
    """Display / route."""
    
    
    
    context = {}
    target = request.args.get("target", "/")
    return flask.render_template("personal_web.html", **context)














@insta485.app.route('/comments/', methods=['GET'])
def comments():
    """Display / route."""
    connection = insta485.model.get_db()

    logname = "awdeorio"
    # postid, filename, owner, created
    posts = connection.execute(
        " SELECT "
        " posts.postid, posts.filename, posts.owner, posts.created"
        " FROM following"
        " JOIN posts"
        " ON following.username2 = posts.owner"
        " WHERE following.username1 == ?"
        " UNION "
        " SELECT * FROM posts WHERE owner == ? ORDER BY postid DESC;",
        (logname, logname,)
    ).fetchall()

    # print(posts)

    # [{'postid': 6, 'filename': 'd24ba948be094dd8970eaf90df205a7e.jpeg', 'owner': 'testuser', 'created': '2021-09-26 01:20:17'}, 
    # {'postid': 5, 'filename': 'ef2b4da6d27149d6907b8454f4c61e53.jpeg', 'owner': 'awdeorio', 'created': '2021-09-26 01:17:51'}, 
    # {'postid': 3, 'filename': '9887e06812ef434d291e4936417d125cd594b38a.jpg', 'owner': 'awdeorio', 'created': '2021-09-26 01:17:35'}, 
    # {'postid': 1, 'filename': '122a7d27ca1d7420a1072f695d9290fad4501a41.jpg', 'owner': 'awdeorio', 'created': '2021-09-26 01:17:35'}]

    # print(posts[0]["postid"])
    # 6
    # print(posts[3]["filename"])
    # 122a7d27ca1d7420a1072f695d9290fad4501a41.jpg

    for post in posts:
        post_id = post["postid"]
        # have to check if this post has a like or not?
        # likes
        cur_like_count = connection.execute(
            "SELECT COUNT (postid) FROM("
            " SELECT DISTINCT postid, likeid FROM"
            " (SELECT following.username1, following.username2,"
            " posts.postid, posts.owner,"
            " likes.likeid, likes.owner"
            " FROM following"
            " JOIN posts ON following.username2 = posts.owner"
            " JOIN likes ON posts.postid = likes.postid)"
            " WHERE username1 == ?"
            " UNION "
            " SELECT postid, likeid FROM (SELECT posts.postid, "
            "posts.owner, likes.likeid"
            " FROM posts"
            " JOIN likes ON likes.postid = posts.postid)"
            " WHERE owner == ? ORDER BY postid DESC)"
            " WHERE postid == ?;",
            (logname, logname, post_id,)
        ).fetchall()
        # print(cur_like_count)
        # [{'COUNT (postid)': 2}]
        # [{'COUNT (postid)': 2}]
        # [{'COUNT (postid)': 1}]
        # [{'COUNT (postid)': 3}]

        print(post["filename"])
        # 已经分解为每个post了，不需要再[0]
        # d24ba948be094dd8970eaf90df205a7e.jpeg
        # ef2b4da6d27149d6907b8454f4c61e53.jpeg
        # 9887e06812ef434d291e4936417d125cd594b38a.jpg 依次


        cur_like_count = cur_like_count[0]["COUNT (postid)"]

        print(cur_like_count)
        # 2
        # 2
        # 1
        # 3
        post["likes"] = cur_like_count
        

        comment_text = connection.execute(
            "SELECT text, comments.owner FROM comments"
            " JOIN posts ON posts.postid = comments.postid"
            " WHERE comments.postid == ?;",
            (post_id,)
        ).fetchall()
        post["comments"] = comment_text

        profile_pic = connection.execute(
            "SELECT users.filename, posts.postid FROM users"
            " JOIN posts ON posts.owner == users.username "
            "WHERE posts.postid == ?;",
            (post_id,)
        ).fetchall()[0]["filename"]

        post["profile_pic"] = profile_pic

        post["created"] = arrow.get(post["created"],
                                    'YYYY-MM-DD HH:mm:ss').humanize()
        # =now.shift(minutes=-15)
        # print(profile_pic)

        like_status = connection.execute(
            "SELECT COUNT (owner) FROM"
            " (SELECT posts.postid, likes.likeid, likes.owner"
            " FROM posts"
            " JOIN likes"
            " ON posts.postid = likes.postid WHERE posts.postid == ?)"
            " WHERE owner == ?;", (post_id, logname, )
        ).fetchall()[0]["COUNT (owner)"]
        post["like_status"] = like_status

    # Add database info to context
    context = {"posts": posts, "logname": logname}
    print(context)
    return flask.render_template("comments.html", **context)















@insta485.app.route('/uploads/<path:filename>')
def download_file(filename):
    """Download file."""
    # if 'username' not in session:
    #     flask.abort(403)
    # if not os.path.exists(os.path.join("var/uploads", filename)):
    #     flask.abort(404)
    return flask.send_from_directory(insta485.app.config['UPLOAD_FOLDER'],
                                     filename, as_attachment=True)
    
@insta485.app.route('/pictures/<path:filename>')
def download_file1(filename):
    """Download file."""
    # if 'username' not in session:
    #     flask.abort(403)
    # if not os.path.exists(os.path.join("var/uploads", filename)):
    #     flask.abort(404)
    return flask.send_from_directory(insta485.app.config['RES_FOLDER'],
                                     filename, as_attachment=True)

@insta485.app.route('/Resume/<path:filename>')
def download_file2(filename):
    """Download file."""
    # if 'username' not in session:
    #     flask.abort(403)
    # if not os.path.exists(os.path.join("var/uploads", filename)):
    #     flask.abort(404)
    return flask.send_from_directory(insta485.app.config['RESUME_FOLDER'],
                                     filename, as_attachment=True)
######################################
############ Imports #################
######################################

from datetime import datetime
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy


######################################
############# Config #################
######################################


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import Post


######################################
########### Functions ################
######################################


def get_post(post_id):
    post = db.session.query(Post).filter_by(post_id=post_id).one()
    if post is None:
        abort(404)
    return post


######################################
############# Routes #################
######################################


@app.route('/')
def index():
    posts = db.session.query(Post).all()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    posts = db.session.query(Post).filter(Post.post_id!=post_id)
    active_post = get_post(post_id)
    print(active_post.content)
    return render_template('post.html', posts=posts, active_post=active_post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if 'excerpt' in request.form:
            content_type = 'excerpt'
        elif 'note' in request.form:
            content_type = 'note'

        if not title:
            flash('Title is required!')
        else:
            new_post = Post(
                title=title,
                content=content,
                content_type=content_type
            )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('index'))
            
    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        

        if not title:
            flash('Title is required!')
        else:
            updated_post = Post(
                post.post_id,
                post.created,
                title,
                content,
                post.content_type
            )
            db.session.query(Post).filter_by(post_id=post.post_id).update(updated_post)
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    db.session.query(Post).filter_by(post_id=post.post_id).delete()
    db.session.commit()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))
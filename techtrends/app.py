import sqlite3, logging, sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

connection_count = 0

##############
## DB CALLS ##
##############

# Get database connection
def get_db_connection():
    global connection_count 
    
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection_count += 1
    return connection

# Get post based on ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    connection.close()
    return post

# Get all posts
def get_posts():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return posts

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

##############
### ROUTES ###
##############

# Main route
@app.route('/')
def index():
    posts = get_posts()

    return render_template('index.html', posts=posts)

# Health endpoint
@app.route('/healthz')
def status():
  response = app.response_class(
          response=json.dumps({"result":"OK - healthy"}),
          status=200,
          mimetype='application/json'
  )

  app.logger.debug('Healthz request successful!')
  return response

# Metrics endpoint
@app.route('/metrics')
def metrics():
  response = app.response_class(
          response=json.dumps({"db_connection_count": connection_count,"post_count": len(get_posts())}),
          status=200,
          mimetype='application/json'
  )

  app.logger.debug('Metrics request successful!')
  return response

# About endpoint
@app.route('/about')
def about():
    app.logger.debug('About page retrieved!')
    return render_template('about.html')

# Article endpoint based on ID
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.debug('Article with id {id} does not exist!'.format(id=post_id))
      return render_template('404.html'), 404
    else:
      app.logger.debug('Article {title} retrieved!'.format(title=post['title']))
      return render_template('post.html', post=post)

# Create endpoint
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            connection.commit()
            connection.close()

            app.logger.debug('Article {title} created!'.format(title=title))
            return redirect(url_for('index'))

    return render_template('create.html')

# Start application
if __name__ == "__main__":
   logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)
   app.run(host='0.0.0.0', port='3111')
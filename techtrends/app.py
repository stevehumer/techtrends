import sqlite3, logging, sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

connection_count = 0

# Function to get a database connection.
def get_db_connection():
    increment_connection_count()
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

def increment_connection_count():
    global connection_count 
    connection_count += 1

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    connection.close()
    return post

# Function to get all posts
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

# Define the main route of the web application 
@app.route('/')
def index():
    posts = get_posts()

    return render_template('index.html', posts=posts)

# Define the health endpoint
@app.route('/healthz')
def status():
  response = app.response_class(
          response=json.dumps({"result":"OK - healthy"}),
          status=200,
          mimetype='application/json'
  )

  app.logger.debug('Healthz request successful!')
  return response

# Define the metrics endpoint
@app.route('/metrics')
def metrics():
  posts = get_posts()

  response = app.response_class(
          response=json.dumps({"db_connection_count": connection_count,"post_count": len(posts)}),
          status=200,
          mimetype='application/json'
  )

  ## log line
  app.logger.debug('Metrics request successful!')
  return response

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.debug('Article does not exist, returning 404 page')
      return render_template('404.html'), 404
    else:
      app.logger.debug(post['created'] + ', Article ' + post['title'] + ' retrieved!')
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.debug('About page retrieved!')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            app.logger.debug('Article ' + title + ' created!')
            return redirect(url_for('index'))

    return render_template('create.html')

# Start the application on port 3111 and set up logging to stdout
if __name__ == "__main__":
   logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)
   app.run(host='0.0.0.0', port='3111')

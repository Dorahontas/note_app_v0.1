import flask

# create an instance of the Flask application
app = flask.Flask(__name__)


# load the content of a text file to a variable and returning it
def load_file(file_name):
  content = ''

  f = open(file_name, 'r') # open the file
  content = f.read() # read the content
  f.close() # close the file

  return content # return the content


# the Flask function that serves '/'
@app.route('/')
def index():
  index_html = load_file('index.html') # load the file index.html

  # replace '## INDEX_HTML ##' with a paragraph 'The content comes here!!!'
  index_html = index_html.replace('## INDEX_HTML ##', '<p>The content comes here!!!</p>')

  return index_html # serve the html to '/'


if __name__ == '__main__':
  app.run(debug=True) # run the application in debug mode


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


# write a note to the notes line - simply add a new line to the file
def add_note_to_file(note):
  f = open('notes_database.txt', 'a') # open the file in append mode
  f.write(note) # write the note to the file
  f.write('\n') # add a new line after the note is written to the database file
  f.close() # close the file


# the Flask function that serves '/'
@app.route('/')
def index():
  # add_notes is the default page so serve it at '/'
  return add_note() # serve /


# the Flask function that serves '/add_note'
@app.route('/add_note')
def add_note():
  note_text = flask.request.args.get('note') # process the html get request
  if note_text: # if there is a request for adding a new note
    add_note_to_file(note_text) # append a new line to the notes database file

  index_html = load_file('index.html') # load the file index.html

  add_note_html = load_file('templates/add_note.html') # load the file templates/add_note.html

  # replace '## INDEX_HTML ##' with the content of templates/add_note_html
  index_html = index_html.replace('## INDEX_HTML ##', add_note_html)

  return index_html # serve /add_note


# the Flask function that serves '/all_notes'
@app.route('/all_notes')
def all_notes():
  all_notes_html = load_file('templates/all_notes.html') # load the file templates/all_notes.html
  all_notes_html = all_notes_html.replace('## ALL_NOTES_HTML ##', '<p>All the notes come here.</p>')

  index_html = load_file('index.html') # load the file index.html

  # replace '## INDEX_HTML ##' with the content of templates/add_note_html
  index_html = index_html.replace('## INDEX_HTML ##', all_notes_html)

  return index_html # serve /all_notes


# the Flask function that serves '/search_notes'
@app.route('/search_notes')
def search_notes():
  search_notes_html = load_file('templates/search_notes.html') # load the file templates/search_notes.html
  search_notes_html = search_notes_html.replace('## FOUND_NOTES_HTML ##', '<p>No notes found.</p>')

  index_html = load_file('index.html') # load the file index.html

  # replace '## INDEX_HTML ##' with the content of templates/add_note_html
  index_html = index_html.replace('## INDEX_HTML ##', search_notes_html)

  return index_html # serve /search_notes


if __name__ == '__main__':
  app.run(debug=True) # run the application in debug mode


import flask
import datetime

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
def add_text_to_file(file_name, text):
  f = open(file_name, 'a') # open the file in append mode
  f.write(text) # write the text to the file
  f.write('\n') # add a new line after the text is written to the file
  f.close() # close the file

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
    note_text = note_text + '##' + str(datetime.datetime.now())[0:16]
    add_text_to_file('notes_database.txt', note_text) # append a new line to the notes database file

  index_html = load_file('index.html') # load the file index.html

  add_note_html = load_file('templates/add_note.html') # load the file templates/add_note.html
  if note_text:
    add_note_html = add_note_html.replace('## NOTE_ADDED_STATUS ##', 'Note added successfully')
  else:
    add_note_html = add_note_html.replace('## NOTE_ADDED_STATUS ##', '')

  # replace '## INDEX_HTML ##' with the content of templates/add_note_html
  index_html = index_html.replace('## INDEX_HTML ##', add_note_html)

  return index_html # serve /add_note


# the Flask function that serves '/all_notes'
@app.route('/all_notes')
def all_notes():
  note_html = load_file('templates/note.html') # load the file templates/note.html
  notes = load_file('notes_database.txt') # load all the notes from the notes_database.txt file
  notes = notes.split('\n') # split the notes into a list of individual notes (the separator is '\n')
  notes.reverse()

  notes_html = '' # create an empty string where all the notes formatted in html will be added
  for note in notes: # iterate through all the notes loaded from the datebase file
    if note != '': # process the note only if it's not empty
      note = note.split('##')
      aux = note_html.replace('## NOTE_TEXT ##', note[0]) # format the text of the note in html and add it to the result notes_html
      aux = aux.replace('## DATE ##', note[1])
      notes_html = notes_html + aux + '<br>' # format the text of the note in html and add it to the result notes_html

  all_notes_html = load_file('templates/all_notes.html') # load the file templates/all_notes.html
  all_notes_html = all_notes_html.replace('## ALL_NOTES_HTML ##', notes_html) # insert the notes in html format to the template all_notes page

  index_html = load_file('index.html') # load the file index.html

  # replace '## INDEX_HTML ##' with the content of templates/add_note_html
  index_html = index_html.replace('## INDEX_HTML ##', all_notes_html) # insert the all_notes (the all the notes in it) to the index page

  return index_html # serve /all_notes


# the Flask function that serves '/search_notes'
@app.route('/search_notes')
def search_notes():
  search_text = flask.request.args.get('search') # process the html get request

  note_html = load_file('templates/note.html') # load the file templates/note.html
  notes = load_file('notes_database.txt') # load all the notes from the notes_database.txt file
  notes = notes.split('\n') # split the notes into a list of individual notes (the separator is '\n')

  search_notes_html = load_file('templates/search_notes.html') # load the file templates/search_notes.html

  notes_found_html = '' # create an empty string where all the found notes formatted in html will be stored
  if search_text: # proceed only if the search_text is not empty (there is a search request from the user)
    for note in notes: # iterate through all the notes
      note = note.split('##')
      if search_text.lower() in note[0].lower(): # if the searched text is in the note (case insensitive search)
        aux = note_html.replace('## NOTE_TEXT ##', note[0])
        aux = aux.replace('## DATE ##', note[1])
        notes_found_html = notes_found_html + aux + '<br>'

    if notes_found_html == '': # in case no notes are found
      search_notes_html = search_notes_html.replace('## NOTES_FOUND_STATUS ##', 'No notes found!') # display a message to the user
    else:
      search_notes_html = search_notes_html.replace('## NOTES_FOUND_STATUS ##', '') # set the NOTES_FOUND_STATUS to empty string, because there are results

  else: # no search request from the user
    search_notes_html = search_notes_html.replace('## NOTES_FOUND_STATUS ##', '') # set the NOTES_FOUND_STATUS to empty string

  search_notes_html = search_notes_html.replace('## NOTES_FOUND_HTML ##', notes_found_html)

  index_html = load_file('index.html') # load the file index.html

  # replace '## INDEX_HTML ##' with the content of templates/add_note_html
  index_html = index_html.replace('## INDEX_HTML ##', search_notes_html)

  return index_html # serve /search_notes


# the Flask function that serves '/comments'
@app.route('/comments')
def comments():
  comment_text = flask.request.args.get('comment') # process the html get request
  comment_type = flask.request.args.get('comment_type') # process the html get request

  if comment_text and comment_type:
    comment_with_type = comment_type + '##' + comment_text + '##' + str(datetime.datetime.now())[:-10]
    add_text_to_file('comments_database.txt', comment_with_type)

  comment_positive_html = load_file('templates/comment_positive.html') # load the file templates/comment_positive.html
  comment_negative_html = load_file('templates/comment_negative.html') # load the file templates/comment_negative.html

  comments = load_file('comments_database.txt') # load all the comments from the comments_database.txt file
  comments = comments.split('\n') # split the comments into a list of individual comments (the separator is '\n')
  comments.reverse()

  comments_html = '' # create an empty string where all the comments formatted in html will be added
  for comment in comments: # iterate through all the notes loaded from the datebase file
    if comment != '':
      comment = comment.split('##') # split the type (positive or negative) and the text
      if comment[0] == 'positive':
        aux = comment_positive_html.replace('## COMMENT_TEXT ##', comment[1])
        aux = aux.replace('## DATE ##', comment[2])
        comments_html = comments_html + aux + '<br>'
      if comment[0] == 'negative':
        aux = comment_negative_html.replace('## COMMENT_TEXT ##', comment[1])
        aux = aux.replace('## DATE ##', comment[2])
        comments_html = comments_html + aux + '<br>'

  all_comments_html = load_file('templates/comments.html') # load the file templates/all_notes.html
  all_comments_html = all_comments_html.replace('## COMMENTS_HTML ##', comments_html) # insert the comments in html format to the template comments page

  index_html = load_file('index.html') # load the file index.html

  # replace '## INDEX_HTML ##' with the content of templates/add_note_html
  index_html = index_html.replace('## INDEX_HTML ##', all_comments_html) # insert the all_notes (the all the notes in it) to the index page

  return index_html # serve /all_notes


if __name__ == '__main__':
  app.run(debug=True) # run the application in debug mode


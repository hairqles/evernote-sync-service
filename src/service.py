from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
from flask import Flask
from flask import request
from cache import Cache
import os

key = os.environ.get('EVERNOTE_CONSUMER_KEY', None)
if not key:
    raise ValueError('You must have "EVERNOTE_CONSUMER_KEY" variable')

secret = os.environ.get('EVERNOTE_CONSUMER_SECRET', None)
if not secret:
    raise ValueError('You must have "EVERNOTE_CONSUMER_SECRET" variable')

cache = Cache()
app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'Hello, World!'

@app.route('/get_authorize_url')
def get_authorize_url():
    callback = request.args.get('callback')
    user_id = request.args.get('user_id')
    client = EvernoteClient(
        consumer_key=key,
        consumer_secret=secret,
        sandbox=True
    )
    
    request_token = client.get_request_token(callback)
    cache.set(user_id, request)
    url = client.get_authorize_url(request_token)
    return url

@app.route('/get_auth_token')
def get_auth_token():
    oauth_verifier = request.args.get('oauth_verifier')
    user_id = request.args.get('user_id')
    request_token = cache.get(user_id)
    app.logger.debug('get_auth_token - user_id: {0} request_token: {1}'.format(user_id, request_token))

    client = EvernoteClient(
        consumer_key=key,
        consumer_secret=secret,
        sandbox=True
    )

    auth_token = client.get_access_token(
        request_token['oauth_token'],
        request_token['oauth_token_secret'],
        oauth_verifier
    )

    return auth_token

@app.route('/notebooks')
def get_notebooks():
    user_id = request.args.get('access_token')
    if not user_id:
        return

    client = EvernoteClient(token=access_token)
    note_store = client.get_note_store()
    notebooks = note_store.listNotebooks()
    return notebooks

@app_route('/notes')
def get_notes():
    access_token = request.args.get('access_token')
    if not user_id:
        return 
    
    notebook = request.args.get('notebook')
    if not user_id:
        return 

    client = EvernoteClient(token=access_token)
    note_store = client.get_note_store()

    NoteFilter filter = new NoteFilter();
    filter.setOrder(NoteSortOrder.UPDATED.getValue());
    filter.setNotebookGuid(notebook);
    notes = note_store.findNotesMetadata(access_token, filter)
    return notes
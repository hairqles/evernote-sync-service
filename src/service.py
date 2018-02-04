from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter
import evernote.edam.type.ttypes as Types
from flask import Flask
from flask import request
from flask import jsonify
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

@app.route('/authorize')
def get_authorize_url():
    callback = request.args.get('callback')
    if not callback:
        return jsonify(error="missing callback")

    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify(error="missing user_id")

    client = EvernoteClient(
        consumer_key=key,
        consumer_secret=secret,
        sandbox=True
    )
    
    request_token = client.get_request_token(callback)
    cache.set(user_id, request_token)
    app.logger.debug('authorize - user_id: {0} request_token: {1}'.format(user_id, request_token))
    url = client.get_authorize_url(request_token)
    return jsonify(authorize_url=url)

@app.route('/authenticate')
def get_auth_token():
    oauth_verifier = request.args.get('oauth_verifier')
    if not oauth_verifier:
        return jsonify(error="missing oauth_verifier")

    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify(error="missing user_id")

    request_token = cache.get(user_id)
    app.logger.debug('authenticate - user_id: {0} request_token: {1}'.format(user_id, request_token))

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
    return jsonify(auth_token=auth_token)

@app.route('/notebooks')
def get_notebooks():
    auth_token = request.args.get('auth_token')
    if not auth_token:
        return

    client = EvernoteClient(token=auth_token)
    note_store = client.get_note_store()
    notebooks = note_store.listNotebooks()
    return notebooks

@app.route('/notes')
def get_notes():
    auth_token = request.args.get('auth_token')
    if not auth_token:
        return 
    
    notebook = request.args.get('notebook')
    if not notebook:
        return 

    client = EvernoteClient(token=auth_token)
    note_store = client.get_note_store()

    filter = NoteFilter(order=NoteSortOrder.UPDATED, notebookGuid=notebook)
    notes = note_store.findNotesMetadata(auth_token, filter)
    return notes
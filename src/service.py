from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter
from evernote.edam.notestore.ttypes import NotesMetadataResultSpec
import evernote.edam.type.ttypes as Types
from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from cache import Cache
from parser import ENMLToHTML
import os
import json

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
    
    token = client.get_request_token(callback)
    cache.set(user_id, token)
    app.logger.debug('authorize - user_id: {0} token: {1}'.format(user_id, token))
    app.logger.debug('authorize - cache: {0}'.format(cache.data))
    url = client.get_authorize_url(token)
    return jsonify(authorize_url=url)

@app.route('/authenticate')
def get_auth_token():
    oauth_verifier = request.args.get('oauth_verifier')
    if not oauth_verifier:
        return jsonify(error="missing oauth_verifier")

    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify(error="missing user_id")
    
    app.logger.debug('authenticate - cache: {0}'.format(cache.data))
    token = cache.get(user_id)
    app.logger.debug('authenticate - user_id: {0} token: {1}'.format(user_id, token))
    cache.delete(user_id)

    client = EvernoteClient(
        consumer_key=key,
        consumer_secret=secret,
        sandbox=True
    )

    auth_token = client.get_access_token(
        token['oauth_token'],
        token['oauth_token_secret'],
        oauth_verifier
    )
    return jsonify(auth_token=auth_token)

@app.route('/notebooks')
def get_notebooks():
    auth_token = request.args.get('auth_token')
    if not auth_token:
        return jsonify(error="missing auth_token")
    
    client = EvernoteClient(token=auth_token)
    note_store = client.get_note_store()
    notebooks = note_store.listNotebooks()
    app.logger.debug('notebooks - {0}'.format(notebooks))
    
    resp = []
    for n in notebooks:
        resp.append({'guid': n.guid, 'name':n.name})
    app.logger.debug('resp - {0}'.format(resp))
    
    return jsonify(notebooks=resp)

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
    
    offset = 0
    max_notes = 1000
    filter = NoteFilter(order=Types.NoteSortOrder.UPDATED, notebookGuid=notebook)
    result_spec = NotesMetadataResultSpec(includeTitle=True)
    metadata = note_store.findNotesMetadata(auth_token, filter, offset, max_notes, result_spec)
    
    notes = []
    for n in metadata.notes:
        content = note_store.getNoteContent(auth_token, n.guid)
        notes.append({'guid': n.guid, 'content': unicode(ENMLToHTML(content)), 'title': n.title})

    return jsonify(notes=notes)
from project_main import app, db
from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify, Response
from sqlalchemy.sql import func
from models import User
import urllib
import logging
import json

### get a list of all available rest api ###
@app.route('/', methods=['GET'])
def list_api():
    output = []
    html = "<!DOCTYPE html><html><head><title>Page Title</title></head><body><p>%s</p></body></html>"
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("<b>%s</b><br>%s<br>%s<br>"%(rule.endpoint, methods, url))
        output.append(line)

    return html%"</p><p>".join(sorted(output))

### test db ###
@app.route('/testdb')
def testdb():
    if db.session.query("1").from_statement("SELECT 1").all():
        return 'DB is working.'
    else:
        return 'DB is broken.'

### create an user ###
@app.route('/user', methods=['POST'])
def create_user():
    try:
        logging.info("receive a create_user request")
        input_data = request.get_json()
        name = str(input_data.get('name'))
        zipcode = int(input_data.get('zipcode'))
        user = User(name, zipcode)
        db.session.add(user)
        db.session.commit()
        return Response("user %s is created"%user.id, status=200)
    except Exception, e:
        logging.error(e)
        return Response(status=500)

### delete an user ###
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        logging.info("receive a delete_user request")
        user = User.query.get(id)
        if not user:
            return Response(status=404)
        user.delete()  # TODO: return error when id is not in the table
        db.session.commit()
        return Response("delete an user: %s"%id, status=200)
    except Exception, e:
        logging.error(e)
        return Response(status=500)
    
### get an user from id ###
@app.route('/user/<id>', methods=['GET'])
def retrive_user(id):
    try:
        logging.info("receive a retrive_user request")
        user = User.query.get(id)
        if not user:
            return Response(status=404)
        return Response(json.dumps(user.dictionary), mimetype='application/json', status=200)
    except Exception, e:
        logging.error(e)
        return "Error in getting user"

### get all users ###
@app.route('/user', methods=['GET'])
def retrive_all_users():
    try:
        logging.info("receive a retrive_all_users request")
        users = User.query.all()
        json_result = json.dumps([user.dictionary for user in users])
        return Response(json_result, mimetype='application/json', status=200)
    except Exception, e:
        logging.error(e)
        return "Error in getting user"

### update an user ###
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    try:
        logging.info("receive a update_user request")
        input_data = request.get_json()
        updated_data = {}
        if 'name' in input_data:
            updated_data['name'] = input_data['name']
        if 'zipcode' in input_data:
            updated_data['zipcode'] = input_data['zipcode']
        user = User.query.filter_by(id=id).update(updated_data)
        db.session.commit()
        return Response("update user %s"%id, status=200)
    except Exception, e:
        logging.error(e)
        return "Error in updating user"

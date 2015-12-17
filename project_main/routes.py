from project_main import app
from flask import Flask, render_template, request, flash, session, redirect, url_for
from sqlalchemy.sql import func
from models import db, Ad, Impression, Click
import urllib
import logging
from collections import OrderedDict

IMPRESSION_WEIGHT = 1
CLICK_WEIGHT = 2

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

### create an ad ###
@app.route('/ad', methods=['POST'])
def create_ad():
    try:
        logging.info("receive a create_ad request")
        category_id = request.form["category_id"]
        content = request.form["content"]
        ad = Ad(category_id, content)
        db.session.add(ad)
        db.session.commit()
        return "creata a new ad!\ncategory_id:%s\ncontent:%s\n"%(category_id,content)
    except Exception, e:
        logging.error(e)
        return "Error in creating ad"

### delete an ad ###
@app.route('/ad/<id>', methods=['DELETE'])
def delete_ad(id):
    try:
        logging.info("receive a delete_ad request")
        Ad.query.filter_by(id=id).delete()  # TODO: return error when id is not in the table
        db.session.commit()
        return "delete an ad: %s"%id
    except Exception, e:
        logging.error(e)
        return "Error in deleting ad"
    
### get an ad from id ###
@app.route('/ad/<id>', methods=['GET'])
def retrive_ad(id):
    try:
        logging.info("receive a retrive_ad request")
        ad = Ad.query.get(id)
        return "Get an ad:\nid:%s\ncategory_id:%s\ncontent:%s\n"%(id,ad.category_id,ad.content)
    except Exception, e:
        logging.error(e)
        return "Error in getting ad"

### run algorithm and get an ad ###
@app.route('/ad', methods=['GET'])
def retrive_ad_smart():
    try:
        score_table = {}
        res1 = Impression.query.add_columns(func.count(Impression.aid),Impression.aid).group_by(Impression.aid).all()
        res2 = Click.query.add_columns(func.count(Click.aid),Click.aid).group_by(Click.aid).all()
        for impression,score,aid in res1:
            score_table.setdefault(aid,0)
            score_table[aid]+=score*IMPRESSION_WEIGHT
        for impression,score,aid in res2:
            score_table.setdefault(aid,0)
            score_table[aid]+=score*CLICK_WEIGHT
        highest_aid,highest_score = max(score_table.items(),key=lambda x:x[1])
        highest_ad = Ad.query.get(highest_aid)
        # return "Get an ad:\nid:%s\ncategory_id:%s\ncontent:%s\nscore:%s"%(highest_ad.id,highest_ad.category_id,highest_ad.content,highest_score)
        return str(highest_aid)
    except Exception, e:
        logging.error(e)
        return "Error in retrive_ad_smart"

### register an impression ###
@app.route('/impression', methods=['POST'])
def register_impression():
    try:
        logging.info("receive a register_impression request")
        aid = request.form["aid"]
        timestamp = request.form["timestamp"]
        impression = Impression(aid, timestamp)
        db.session.add(impression)
        db.session.commit()
        return "register an impression!\naid:%s\ntimestamp:%s\n"%(aid,timestamp)
    except Exception, e:
        logging.error(e)
        return "Error in registering impression"

### register an click ###
@app.route('/click', methods=['POST'])
def register_click():
    try:
        logging.info("receive a register_click request")
        aid = request.form["aid"]
        timestamp = request.form["timestamp"]
        click = Click(aid, timestamp)
        db.session.add(click)
        db.session.commit()
        return "register an click!\naid:%s\ntimestamp:%s\n"%(aid,timestamp)
    except Exception, e:
        logging.error(e)
        return "Error in registering click"

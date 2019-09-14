import json
from flask import Blueprint, jsonify, abort, request, make_response
from playhouse.shortcuts import model_to_dict, dict_to_model
from models import News

app_url = Blueprint('', __name__)


@app_url.route('/', methods = ['GET'])
def get_news():
    news_models = News.select().get()
    json_data = json.dumps(model_to_dict(news_models))
    return jsonify(json_data)

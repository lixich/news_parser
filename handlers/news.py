import json
from flask import Blueprint, jsonify, request, make_response
from playhouse.shortcuts import model_to_dict, dict_to_model
from models import NewsModel
from .error import generate_error

app_url = Blueprint('', __name__)


@app_url.route('/', methods = ['GET'])
def get_news():
    order = request.args.get('order') if 'order' in request.args else None
    desc = request.args.get('desc') if 'desc' in request.args else False
    limit = request.args.get('limit') if 'limit' in request.args else None
    offset = request.args.get('offset') if 'offset' in request.args else None
    if order not in NewsModel.get_fields():
        return generate_error(400, 'Field "order" is incorrect')
    if desc not in (False, True):
        return generate_error(400, 'Field "desc" is incorrect')
    news_models = NewsModel.select().get()
    json_data = json.dumps(model_to_dict(news_models))
    return jsonify(json_data)

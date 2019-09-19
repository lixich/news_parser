from flask import Blueprint, jsonify, request
from models import db, NewsModel
from .error import generate_error
from scheduler import parse_news

app_url = Blueprint('', __name__)
LIMIT_COUNT = 500
DEFAULT_LIMIT_COUNT = 5


@app_url.route('/', methods=['GET'])
def get_news():
    order = str(request.args.get('order')) if 'order' in request.args else 'id'
    desc = str(request.args.get('desc')).lower() if 'desc' in request.args else 'false'
    limit = str(request.args.get('limit')) if 'limit' in request.args else str(DEFAULT_LIMIT_COUNT)
    offset = str(request.args.get('offset')) if 'offset' in request.args else None

    if order not in NewsModel.get_fields():
        return generate_error(400, 'Field "order" is incorrect')
    order_field = getattr(NewsModel, order)
    if desc not in ('false', 'true'):
        return generate_error(400, 'Field "desc" is incorrect')
    if desc == 'true':
        order_field = order_field.desc()
    if limit and not limit.isnumeric():
        return generate_error(400, 'Field "limit" is incorrect')
    if limit:
        limit = int(limit)
        if limit > LIMIT_COUNT:
            return generate_error(400, '"limit" is too long')
    if offset and not offset.isnumeric():
        return generate_error(400, 'Field "offset" is incorrect')
    if offset:
        offset = int(offset)
    query = NewsModel.select().order_by(order_field)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)

    news_dicts = list(query.dicts())

    return jsonify(news_dicts)


@app_url.route('/update', methods=['GET'])
def update_news():
    news_dicts = parse_news()
    with db.atomic():
        NewsModel.insert_many(news_dicts).execute()
    return jsonify(news_dicts)

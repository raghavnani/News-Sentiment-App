import json
from flask import request, Response
from app.models.alchemy_encoder import AlchemyEncoder
from flask import Blueprint
from app.services.news_service import NewsService

new_service = NewsService()
news_api = Blueprint('news_api', __name__)

@news_api.route('/api/getNewsFromApi', methods=['GET'])
def get_news_from_api():

    results = new_service.do_scrape_news_filter()
    result = json.dumps(results, cls=AlchemyEncoder)

    return Response(response=result, status=200, content_type="application/json")


@news_api.route('/api/getNewsWithCondition', methods=['GET'])
def get_all_news_with_condition():

    print('========================================================')

    condition = request.args.get('condition')

    page = int(request.args.get('page'))

    first = page * 20
    last = first + 20

    results = new_service.get_news_with_condition(condition)
    result = json.dumps(results[first:last], cls=AlchemyEncoder)

    return Response(response=result, status=200, content_type="application/json")


@news_api.route('/api/getNewsByNewsFilterId', methods=['GET'])
def get_news_by_news_filter_id():

    news_filter_id = request.args.get('news_filter_id')

    results = new_service.get_news_by_news_filter_id(news_filter_id)
    result = json.dumps(results, cls=AlchemyEncoder)

    return Response(response=result, status=200, content_type="application/json")
#
# @news_api.route('/api/getLatestNews', methods=['GET'])
# def get_latest_news():
#
#     print('=============================================================================')
#     results = new_service.get_latest_news()
#     result = json.dumps(results[first:last], cls=AlchemyEncoder)
#
#     return Response(response=result, status=200, content_type="application/json")
#
#




# @news_api.route('/getSavedNewsForUser', methods=['GET'])
# def get_saved_news_for_user():
#
#     user_id = request.args.get('user_id')
#
#     results = new_service.get_save_news_for_user(user_id)
#     result = json.dumps(results, cls=AlchemyEncoder)
#
#     return Response(response=result, status=200, content_type="application/json")
#

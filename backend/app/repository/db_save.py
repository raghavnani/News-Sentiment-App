#
# from app.models.models import User, News
#
# import datetime
# from app import db
#
# def save_news(article):
#
#     news = News(news_filter_id=article['news_filter_id'], source=article['source'], title=article['title'],
#                 content=article['content'], description=article['description'], url=article['url'],
#                 image_url=article['imageUrl'], published_at=str(datetime.datetime.now()).split('.')[0])
#
#     db.session.add(news)
#     db.session.commit()
#
#
# def update_news_sentiment(article):
#     result = News.query.filter_by(news_filter_id=article['news_filter_id'])
#
#     result.sentiment = article['sentiment']
#     result.text = article['text']
#     result.logits = article['logits']
#
#     db.session.commit()
#
#
# def update_user_name():
#
#     result = User.query.filter_by(username='blu_admin_u').first()
#
#     print(result)
#
#     result.username = 'Raghav'
#     db.session.commit()
#
#     return result.username
#

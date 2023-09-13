# import flask
# from model.preprocessing_text.preprocessing import Preprocessing
# from flask import Response
# from model.models.torch_preprocessing import TorchDataPreprocessing
# from model.models.bert_preprocessing import BertPreProcessing
# import numpy as np
# from transformers import BertForSequenceClassification
# from transformers import BertTokenizer
# from api_crawler.newsfilter_api import get_urls
# from scrapy.crawler import CrawlerRunner
# from crawler.spiders.crawler import NewsFilter
# from twisted.internet import reactor
# from multiprocessing import Process, Queue, Manager
# from torch.nn.functional import softmax
# from scrapy.signalmanager import dispatcher
# import json
# from flask_cors import CORS
# import pandas as pd
# import time
# import atexit
# from apscheduler.schedulers.background import BackgroundScheduler
# import os
# import datetime
# import pytz
# from news import News
# from flask import request
# from scrapy import signals
#
#
# from app import app
#
# cors = CORS(app)
#
# spiders = ["NewsFilter"]
#
#
# class PreprocessInput:
#
#     def __init__(self):
#         try:
#             self.preprocessor = Preprocessing()
#             self.pytorch_convertor = TorchDataPreprocessing()
#             self.bert_preprocessor = BertPreProcessing(max_length=128)
#
#             self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
#
#             path = os.path.join(app.root_path, 'model/model_weights/sentiment_model')
#
#             self.sentiment_model = BertForSequenceClassification.from_pretrained(path, cache_dir=None, num_labels=3)
#
#             self.sentiment_model.cpu()
#             self.sentiment_model.eval()
#
#         except Exception as e:
#             print(e)
#
#
# @app.route('/', methods=['GET'])
# def home():
#     return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
#
#
# @app.route('/sentiment', methods=['GET'])
# def sentiment_predictor():
#     articles = do_scrape_news_fliter()
#     return_articles = []
#
#     for i in articles:
#         try:
#             article = i
#
#             header = article['title']
#             text = article['text']
#
#             if text == '':
#                 text = article['description']
#
#             count = len(header.split())
#             detailed_text = header + '. ' + text + ' $word_count_split$ ' + str(count)
#             sumarized_text = preprocess.preprocessor.summarize_input(detailed_text, word_limit=120)
#             clean_text = preprocess.preprocessor.normalize(sumarized_text, lowercase=False, lemmatize=True,
#                                                            only_alpha=True)
#             ids1, masks1, segments1 = preprocess.bert_preprocessor.get_bert_tokens_masks_segments(clean_text,
#                                                                                                   preprocess.tokenizer)
#             ids = preprocess.pytorch_convertor.convert_arrays_to_tensors(ids1)
#             masks = preprocess.pytorch_convertor.convert_arrays_to_tensors(masks1)
#             segments = preprocess.pytorch_convertor.convert_arrays_to_tensors(segments1)
#
#             logits = preprocess.sentiment_model(input_ids=ids,
#                                                 token_type_ids=segments,
#                                                 attention_mask=masks)[0]
#
#             logits = softmax(logits, dim=1)
#
#             logits = logits.detach().numpy()
#
#             pred = np.argmax(logits, axis=1)
#
#             saved = 0
#
#             if pred == 0:
#                 sentiment = 'Positive'
#                 if logits[0][0].round(2) > 0.80:
#                     saved = 1
#             elif pred == 1:
#                 sentiment = 'Negative'
#                 if logits[0][1].round(2) > 0.80:
#                     saved = 1
#             else:
#                 sentiment = 'Neutral'
#
#             print(sentiment, ','.join(map(str, logits[0])), header)
#
#             article['logits'] = ','.join(map(str, logits[0]))
#             article['sentiment'] = sentiment
#
#             article['saved'] = saved
#
#             db_run.update_sentiment_for_inserted_news(conn, article)
#
#             return_articles.append(article)
#
#         except Exception as e:
#             print(e)
#
#     result = json.dumps(return_articles)
#
#     return Response(response=result, status=200, content_type="application/json")
#
#
#
# @app.route('/predictSentimentFromText', methods=['POST'])
# def give_sentiment():
#
#     return_articles = []
#
#     try:
#         header = request.json['title']
#         text = request.json['text']
#
#         article = {'header': header, 'title': text}
#
#         count = len(header.split())
#         detailed_text = header + '. ' + text + ' $word_count_split$ ' + str(count)
#         sumarized_text = preprocess.preprocessor.summarize_input(detailed_text, word_limit=120)
#         clean_text = preprocess.preprocessor.normalize(sumarized_text, lowercase=False, lemmatize=True,
#                                                        only_alpha=True)
#         ids1, masks1, segments1 = preprocess.bert_preprocessor.get_bert_tokens_masks_segments(clean_text,
#                                                                                               preprocess.tokenizer)
#         ids = preprocess.pytorch_convertor.convert_arrays_to_tensors(ids1)
#         masks = preprocess.pytorch_convertor.convert_arrays_to_tensors(masks1)
#         segments = preprocess.pytorch_convertor.convert_arrays_to_tensors(segments1)
#
#         logits = preprocess.sentiment_model(input_ids=ids,
#                                             token_type_ids=segments,
#                                             attention_mask=masks)[0]
#
#         logits = softmax(logits, dim=1)
#
#         logits = logits.detach().numpy()
#
#         pred = np.argmax(logits, axis=1)
#
#         if pred == 0:
#             sentiment = 'Positive'
#         elif pred == 1:
#             sentiment = 'Negative'
#         else:
#             sentiment = 'Neutral'
#
#         print(sentiment, ','.join(map(str, logits[0])), header)
#
#         article['logits'] = ','.join(map(str, logits[0]))
#         article['sentiment'] = sentiment
#
#         return_articles.append(article)
#
#     except Exception as e:
#         print(e)
#
#     result = json.dumps(return_articles)
#
#     return Response(response=result, status=200, content_type="application/json")
#
#
#
# # @app.route('/scrape', methods=['GET'])
# def do_scrape_news_fliter():
#     print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
#
#     articles = get_urls()
#     return_articles = []
#
#     for article in articles:
#
#         key = db_run.save_news_with_out_sentiment(conn, article)
#
#
#
#         print('=================================================================================', key)
#
#         if key:
#             manager = Manager()
#             return_dict = manager.dict()
#             return_dict['article'] = article
#             q = Queue()
#             p = Process(target=f, args=(q, return_dict))
#             p.start()
#             queue = q.get()
#             p.join()
#
#             if queue is not None:
#                 raise queue
#
#             return_articles.append(return_dict['extra_articles'])
#
#     results = return_articles
#
#     return results
#
#
# def f(q, return_dict):
#     try:
#         results = []
#         article = return_dict['article']
#
#         def crawler_results(signal, sender, item, response, spider):
#             results.append(item)
#
#         dispatcher.connect(crawler_results, signal=signals.item_passed)
#
#         runner = CrawlerRunner()
#         deferred = runner.crawl(NewsFilter, url=article['url'])
#         deferred.addBoth(lambda _: reactor.stop())
#         reactor.run()
#         q.put(None)
#         article['text'] = results[0]['text']
#
#         return_dict['extra_articles'] = article
#         # publishedAt = return_articles[0]['publishedAt']
#
#     except Exception as e:
#         q.put(e)
#
#     return return_dict
#
#
# @app.route('/getNewsWithCondition/', methods=['GET'])
# def get_all_news_with_condition():
#     condition = request.args.get('condition')
#     result = db_run.get_sentimet_news_query(conn, condition)
#     news_list = []
#
#     for i in result:
#         news = News(_id=i[0], news_filter_id=i[1], source=i[2], title=i[3], content=i[4],
#                     description=i[5], url=i[6], image_url=i[7], published_at=i[8], text=i[9],
#                     logits=i[10], sentiment=i[11], saved=i[12])
#
#         news_list.append(news.__dict__)
#
#     text = json.dumps(news_list)
#
#     return Response(response=text, status=200, content_type="application/json")
#
#
# @app.route('/getSavedNews/', methods=['GET'])
# def get_saved_news():
#
#     result = db_run.get_saved_news_query(conn)
#     news_list = []
#
#     for i in result:
#         news = News(_id=i[0], news_filter_id=i[1], source=i[2], title=i[3], content=i[4],
#                     description=i[5], url=i[6], image_url=i[7], published_at=i[8], text=i[9],
#                     logits=i[10], sentiment=i[11], saved=i[12])
#
#         news_list.append(news.__dict__)
#
#     text = json.dumps(news_list)
#
#     return Response(response=text, status=200, content_type="application/json")
#
#
# @app.route('/updateSavedArticle', methods=['PUT'])
# def update_saved_article():
#     key = request.json['id']
#     saved = request.json['saved']
#
#     print(key, saved)
#     result = db_run.update_saved_news(conn, key, saved)
#
#     text = json.dumps({'saved': result})
#
#     return Response(response=text, status=200, content_type="application/json")
#
#
# def print_date_time():
#     print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
#
#
# if __name__ == '__main__':
#     with app.app_context():
#         preprocess = PreprocessInput()
#         db_path = os.path.join(app.root_path, 'DB/test/news.db')
#         conn = db_run.create_connection(db_path)
#         # db_run.create_table(conn, 'news')
#         # db_run.create_table(conn, 'negative')
#         # db_run.create_table(conn, 'neutral')
#         scheduler = BackgroundScheduler()
#         scheduler.add_job(func=sentiment_predictor, trigger="interval", seconds=60)
#         scheduler.start()
#         app.run(host='0.0.0.0', debug=True, port=5001, use_reloader=False)
#         # Shut down the scheduler when exiting the app
#         # atexit.register(lambda: scheduler.shutdown())
#         atexit.register(lambda: db_run.finalize_connection(conn))

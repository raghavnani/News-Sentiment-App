from app import app
from app.nlp.preprocessing.preprocessing_text import Preprocessing
from app.nlp.preprocessing.torch_preprocessing import TorchDataPreprocessing
from app.nlp.preprocessing.bert_preprocessing import BertPreProcessing
from transformers import BertForSequenceClassification
from transformers import BertTokenizer
import os
from torch.nn.functional import softmax
import numpy as np

from app.crawler.spiders.crawler import NewsFilter
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from twisted.internet import reactor
from scrapy import signals


def singleton(cls):
    instance = [None]

    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return wrapper


class PreprocessInput:

    def __init__(self):
        try:
            self.preprocessor = Preprocessing()
            self.pytorch_convertor = TorchDataPreprocessing()
            self.bert_preprocessor = BertPreProcessing(max_length=128)

            self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

            path = os.path.join(app.root_path, 'nlp/model_weights/sentiment_model')

            self.sentiment_model = BertForSequenceClassification.from_pretrained(path, cache_dir=None, num_labels=3)

            self.sentiment_model.cpu()
            self.sentiment_model.eval()

        except Exception as e:
            print(e)


    def run_crawler_in_loop(self, queue, return_dict):
        try:
            results = []
            article = return_dict['article']

            def crawler_results(signal, sender, item, response, spider):
                results.append(item)

            dispatcher.connect(crawler_results, signal=signals.item_passed)

            runner = CrawlerRunner()
            deferred = runner.crawl(NewsFilter, url=article['url'])
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            queue.put(None)
            article['text'] = results[0]['text']

            updated_article = self.predict_sentiment(article)

            return_dict['updated_article'] = updated_article

        except Exception as e:
            queue.put(e)

        return return_dict


    def predict_sentiment(self, input_article):

        article = input_article

        header = article['title']
        text = article['text']

        if text == '':
            text = article['description']

        count = len(header.split())
        detailed_text = header + '. ' + text + ' $word_count_split$ ' + str(count)
        sumarized_text = self.preprocessor.summarize_input(detailed_text, word_limit=120)
        clean_text = self.preprocessor.normalize(sumarized_text, lowercase=False, lemmatize=True,
                                                       only_alpha=True)
        ids1, masks1, segments1 = self.bert_preprocessor.get_bert_tokens_masks_segments(clean_text,
                                                                                              self.tokenizer)
        ids = self.pytorch_convertor.convert_arrays_to_tensors(ids1)
        masks = self.pytorch_convertor.convert_arrays_to_tensors(masks1)
        segments = self.pytorch_convertor.convert_arrays_to_tensors(segments1)

        logits = self.sentiment_model(input_ids=ids,
                                            token_type_ids=segments,
                                            attention_mask=masks)[0]

        logits = softmax(logits, dim=1)

        logits = logits.detach().numpy()

        pred = np.argmax(logits, axis=1)

        if pred == 0:
            sentiment = 'Positive'
        elif pred == 1:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'

        print(sentiment, ','.join(map(str, logits[0])), header)

        article['logits'] = ','.join(map(str, logits[0]))
        article['sentiment'] = sentiment

        return article

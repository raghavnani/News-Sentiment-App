import urllib.request
import json


def get_urls(published_at=None):
    # API endpoint
    API = ""

    queryString = 'source.id:(-"sec-api") AND title:(-"INVESTOR ALERT") AND title:(-"Bragar") AND title:(-"Rosen") AND title:(-"Stockholder Investigation") AND title:(-"Shareholder Alert") AND title:(-"Class Action") AND title:(-HAGENS)'

    if published_at:
        query = queryString + ' AND {}'.format(published_at)
        size = 50
    else:
        query = queryString
        size = 5

    print(query)

    payload = {
        "type": "filterArticles",
        "queryString": query,
        "size": size,
        # 'order': 'asc'
        # 'sort': {'order': 'asc'}
        # 'publishedAt': published_at,
    }

    # Format your payload to JSON bytes
    jsondata = json.dumps(payload)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes

    # Instantiate the request
    req = urllib.request.Request(API)

    # Set the correct HTTP header: Content-Type = application/json
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    # Set the correct length of your request
    req.add_header('Content-Length', len(jsondataasbytes))

    # Send the request to the API
    response = urllib.request.urlopen(req, jsondataasbytes)

    # Read the response
    res_body = response.read()
    # Transform the response into JSON
    articles = json.loads(res_body.decode("utf-8"))

    new_articles = []

    for i in articles['articles']:
        article = {'news_filter_id': i['id'],
                    'source': i['source']['name'],
                   # 'categories' : i['categories'],
                   # 'symbols': i['symbols'],
                   'title': i['title'],
                   'content': i['content'],
                   'description': i['description'],
                   'url': i['url'],
                   'imageUrl': i['imageUrl'],
                   'publishedAt': i['publishedAt'],
                   # 'industries': i['industries'],
                   # 'sectors': i['sectors']
                   }

        # article = {'source' : articles['articles'][0]['source']['name'],
        #            # 'categories' : articles['articles'][0]['categories'],
        #            # 'symbols': articles['articles'][0]['symbols'],
        #            'title': articles['articles'][0]['title'],
        #            'content': articles['articles'][0]['content'],
        #            'description': articles['articles'][0]['description'],
        #            'url': articles['articles'][0]['url'],
        #            'imageUrl' : articles['articles'][0]['imageUrl'],
        #            'publishedAt' : articles['articles'][0]['publishedAt'],
        #            # 'industries': articles['articles'][0]['industries'],
        #            # 'sectors': articles['articles'][0]['sectors']
        #            }
        new_articles.append(article)

    # print(len(new_articles))
    # for i in articles['articles']:
    #     print(i['publishedAt'], i['title'])

    return new_articles


# import datetime
# import pytz

# now = str(datetime.datetime.now().replace(tzinfo=datetime.timezone.utc))

# print(now)

# time = now.split()[0] + 'T' + now.split()[1].split('.')[0]

# print("publishedAt:[2020-05-29T20:00:00+00:00 TO {}]".format(time))
#
# print(get_urls())
#
# (get_urls("publishedAt:[2020-05-29T20:00:00+00:00 TO {}]".format(time)))

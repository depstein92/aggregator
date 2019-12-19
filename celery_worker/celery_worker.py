from celery import Celery

import requests
import os
import json

URL_LIST = [ #move to constants file
   'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/4632/summary',
   'https://api-football-v1.p.rapidapi.com/v2/predictions/157462',
   'https://api-basketball.p.rapidapi.com/standings',
   'https://sportsop-soccer-sports-open-data-v1.p.rapidapi.com/v1/leagues',
   'https://movie-database-imdb-alternative.p.rapidapi.com/',
   'https://wft-geo-db.p.rapidapi.com/v1/locale/locales',
   'https://adsbexchange-com1.p.rapidapi.com/sqk/%7Bsqk%7D/'
]

URL_LIST_TITLE = [ #move to constants file
   'Recipes for you to enjoy',
   'Football facts',
   'Basketball facts',
   'Soccer facts',
   'Suggested movie',
   'Random city facts',
   'Flight info around the world'
]

HEADERS = [ #move to constants file
    'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com',
    'api-football-v1.p.rapidapi.com',
    'api-basketball.p.rapidapi.com',
    'sportsop-soccer-sports-open-data-v1.p.rapidapi.com',
    'movie-database-imdb-alternative.p.rapidapi.com',
    'wft-geo-db.p.rapidapi.com',
    'adsbexchange-com1.p.rapidapi.com'
]

worker = Celery('celery_worker',
             broker='amqp://dan:dan@localhost:5672/dan_host',
             backend='',
             ignore_result=False)


@worker.task
def execute_celery_tasks():
    data = []
    for i, url in enumerate(URL_LIST):
        headers = {
          'x-rapidapi-host': HEADERS[i],
          'x-rapidapi-key': "d06d900824mshf97a044c62f3e56p143b65jsnb65dee23984e"
        }
        response = requests.get(url, headers=headers)
        data.append({
        'title': URL_LIST_TITLE[i],
        'data': json.loads(response.text)
        })
    return data

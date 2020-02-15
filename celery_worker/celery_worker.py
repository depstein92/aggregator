from celery import Celery

import requests
import os
import json
import threading

def filter_relevant_users(data=None):
  if data is None:
    return []


  relevant_data = json.loads(data)["results"]
  user_data = []

  for user in relevant_data:
    user_info = {
      "name" : user["name"],
      "age" : user["dob"]["age"],
      "picture": user["picture"]["thumbnail"],
      "gender" : user["gender"],
      "location": user["location"]["city"]
    }
    user_data.append(user_info)

  return user_data


# to start workers: celery -A celery_worker worker --loglevel=debug

URL_LIST = [ #move to constants file
    'https://randomuser.me/api/?results=500',
    'https://randomuser.me/api/?results=500',
    'https://randomuser.me/api/?results=500',
    'https://randomuser.me/api/?results=500',
    'https://randomuser.me/api/?results=500',
    'https://randomuser.me/api/?results=500',
    'https://randomuser.me/api/?results=500'
]

worker = Celery('celery_worker',
             broker='amqp://dan:dan@localhost:5672/dan_host',
             backend='amqp',
             ignore_result=False,
             CELERY_IGNORE_RESULT=False)

'''
NOTES:
    percentage_complete is incremented by
    14, because 1/7 of 100 is about 14... blah blah blah
'''

@worker.task(bind=True, ignore_result = False)
def execute_celery_tasks(self):
    data = []
    percent = 0
    self.update_state(state='STARTING',
                      meta={'percent': percent,
                            'status': 'Loading...',
                            'data': data})

    for url in URL_LIST:
        res = requests.get(url)
        user_data = filter_relevant_users(res.text)
        percent += 14
        print('percent Complete:', percent)
        self.update_state(state='PROGRESS',
                          meta={'percent': percent,
                                'status': 'Loading...',
                                'data': data})

    self.update_state(state='FINISHED',
                      meta={'percent': percent,
                      'status': 'Loading...',
                      'data': data})

    return { 'percentage': data }

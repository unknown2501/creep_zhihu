import requests
from bs4 import BeautifulSoup
import json

import models

HEADERS_ANTICREEP = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}


def get_followings(user_id):
    furl = "https://www.zhihu.com/people/{user_id}/following?page={page}"
    page = 1
    following = []
    while True:
        # print(f"CREEPING PAGE{page}")
        response = requests.get(
            furl.format(user_id=user_id, page=page),
            headers=HEADERS_ANTICREEP
        )
        if response.status_code != 200:
            raise Exception("REJECTED!")
        page += 1

        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find(id='js-initialData')
        data = json.loads(data.text)

        following_page = data['initialState']['entities']['users'].keys()
        following_page = list(following_page)

        following_page = [id for id in following_page if (id != user_id)]

        if following_page:
            following += following_page
            continue
        break

    return following


def get_new_pins(user_id, latest_update=0):

    furl = "https://www.zhihu.com/people/{user_id}/pins"
    response = requests.get(
        furl.format(user_id=user_id)
    )

    print(response.status_code)

    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find(id='js-initialData')
    data = json.loads(data.text)

    pins = data['initialState']['entities']['pins']
    return pins


def update_pins(user_id):
    pins_db = models.Pins.filter(
        models.Pins.user_id == user_id).order_by(models.Pins.time_update)
    pins_db = list(pins_db)

    if not pins_db:
        latest_update = 0
    else:
        latest_update = pins_db[-1].time_update

    pins_new = get_new_pins(user_id, latest_update)

    for key in pins_new.keys():
        if pins_new[key]['updated'] > latest_update:
            models.Pins.create(
                content=pins_new[key]['content'][0]['content'],
                user_id=user_id,
                time_update=pins_new[key]['updated'],
                pin_id=key
            )


user_id = 's.invalid'
get_new_pins(user_id)

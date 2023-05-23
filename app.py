from fastapi import FastAPI
from creep import *
from models import *

app = FastAPI()


@app.get("/")
def root():
    return {'hello': 'creep_zhihu'}


@app.get("/pins/")
def get_pins(user_id: str):

    update_pins(user_id)

    pins = models.Pins.filter(models.Pins.user_id == user_id).order_by(
        models.Pins.time_update)
    pins = pins.dicts()
    pins = pins[:20]

    return {'pins': pins}


@app.get("/timeline/")
def get_tl(user_id: str):

    followings = get_followings(user_id)

    pins = []
    for followee_id in followings:
        pins += models.Pins.filter(models.Pins.user_id == user_id).order_by(
            models.Pins.time_update).dicts()
    pins = sorted(pins, key=lambda x: x['time_update'])
    pins = pins[:20]
    return {'pins': pins}

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app,port=8005)
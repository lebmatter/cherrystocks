from huey import RedisHuey, crontab
from niftyredis import get_or_update

huey = RedisHuey()


@huey.periodic_task(crontab(minute='5', hour='0'))
def periodic_crawler():
    '''
    Huey task scheduler is simpler to use.
    Other options I checked were:
    1) threading.Timer() in a loop
    2) Celelry with Redis backed.

    To run the scheduler in a different thread,
    huey_consumer.py tasks.huey -k process -w 4
    '''

    # Update gainers and losers
    get_or_update(True)
    get_or_update(False)

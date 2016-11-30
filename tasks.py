from huey import RedisHuey, crontab
from niftyredis import get_or_update

huey = RedisHuey('niftyupdater', host='localhost:6379/0')

@huey.periodic_task(crontab(minute='5', hour='0'))
def periodic_crawler():
    get_or_update()
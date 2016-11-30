import redis
from niftyparser import get_niftyfifty
import datetime
import time

r = redis.Redis(host='localhost', port=6379, db=0)

def get_or_update():
    '''
    Funtion checks for avialable keys in keyspace.
    1) If key not found:
        get data from NSE website.
        Save the values with timestamp as key and ttl 5 minutes.
    2) If key is found:
        get data from cache with timestamp Key
    '''
    keys = r.keys()
    if not keys:
        # empty keys means cache has cleared.
        data = get_niftyfifty()
        tstamp = datetime.datetime.strptime(data['time'], "%b %d, %Y %H:%M:%S")
        tstamp = int(time.mktime(tstamp.timetuple()))
        # Save timestamp for reference
        r.set('tstamp', tstamp)
        r.expire('tstamp', 300)
        for entry in data['data']:
            entry_key = '{}:{}'.format(tstamp, entry['symbol'])
            r.hmset(
                entry_key, {
                    'symbol': entry_key,
                    'openPrice': entry['openPrice'],
                    'highPrice': entry['highPrice'],
                    'lowPrice': entry['lowPrice'],
                    'ltp': entry['ltp'],
                    'previousPrice': entry['previousPrice'],
                    'netPrice': entry['netPrice'],
                    'tradedQuantity': entry['tradedQuantity'],
                    'turnoverInLakhs': entry['turnoverInLakhs']})

            r.expire(entry_key, 300)
        print "Data from Crawling."
        return data['data']
    elif 'tstamp' in keys:
        entry_keys = keys.remove('tstamp')
        data = []
        for entry_key in entry_keys:
            data.append(r.hgetall(entry_key))
        print "Data from Redis Cache"
        return data


if __name__ == '__main__':
    data = get_niftyfifty()
    print data

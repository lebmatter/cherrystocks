import redis
from niftyparser import get_niftyfifty
import datetime
import time

r = redis.Redis(host='localhost', port=6379, db=0)

def get_or_update(gainers=True):
    '''
    Funtion checks for avialable keys in keyspace.
    1) If key not found:
        get data from NSE website.
        Save the values with timestamp as key and ttl 5 minutes.
    2) If key is found:
        get data from cache with timestamp Key
    '''
    tstamp_key = 'gtstamp' if gainers else 'ltstamp'
    if not r.exists(tstamp_key):
        # empty keys means cache has cleared.
        data = get_niftyfifty(gainers)
        tstamp = datetime.datetime.strptime(data['time'], "%b %d, %Y %H:%M:%S")
        tstamp = int(time.mktime(tstamp.timetuple()))
        # Save timestamp for reference
        r.set(tstamp_key, tstamp)
        r.expire(tstamp_key, 300)
        for entry in data['data']:
            entry_key = '{}:{}:{}'.format(tstamp_key, tstamp, entry['symbol'])
            r.hmset(
                entry_key, {
                    'symbol': entry['symbol'],
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
    else:
        last_tstamp = r.get(tstamp_key)
        entry_keys = r.keys('{}:{}*'.format(tstamp_key, last_tstamp))
        print 'Current keys in cahce are: ', entry_keys
        data = []
        for entry_key in entry_keys:
            data.append(r.hgetall(entry_key))
        print "Data from Redis Cache"
        return data


if __name__ == '__main__':
    data = get_niftyfifty()
    print data

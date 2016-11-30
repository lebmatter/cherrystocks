import requests
import json


def get_niftyfifty(gainers=True):
    '''
    I wanted to use BeutifulSoup at first. But it won't parse dynamic data.
    Then next option was Selenium with PhantomJS, whch I was familiar with. But it will be an overhead.
    So decided to find the ajax call and use it to get 'Nifty 50' data.

    By default it will get gainers list.
    '''

    if gainers:
        url = 'https://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json'
    else:
        url = 'https://www.nseindia.com/live_market/dynaContent/live_analysis/losers/niftyLosers1.json'
    req = requests.get(url)

    data = json.loads(req.text)
    return data


if __name__ == '__main__':
    data = get_niftyfifty()
    print data

import cherrypy
import os
from niftyredis import get_or_update


class CherryStocks(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')

@cherrypy.expose
class CherryStocksWebService(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        data = get_or_update()
        return data


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/niftyfifty': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8080,
                       })
    webapp = CherryStocks()
    webapp.niftyfifty = CherryStocksWebService()
    cherrypy.quickstart(webapp, '/', conf)

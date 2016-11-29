import cherrypy
import os


class CherryStocks(object):
    @cherrypy.expose
    def index(self):
        return "Hello!"


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.quickstart(CherryStocks(), '/', conf)
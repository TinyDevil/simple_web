from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple


class App(object):
    def __init__(self):
        self.url_map = Map()

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return Response(getattr(self, endpoint)(request, **values))
        except Exception as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def route(self, rule, **options):
        def wrapper(f):
            endpoint = 'on_' + f.__name__
            route_rule = Rule(rule, endpoint=endpoint, **options)
            self.url_map.add(route_rule)
            setattr(self, endpoint, f)
        return wrapper

    def run(self):
        run_simple('127.0.0.1', 5000, self)

app = App()

@app.route('/nima/<username>', methods=['POST', 'GET'])
def bbk(request, username):
    return username

if __name__ == '__main__':

    app.run()


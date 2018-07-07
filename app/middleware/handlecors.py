
ALLOWED_ORIGINS = ['http://localhost:8000','http://localhost:3000'] # Or load this from a config file

class CorsMiddleware(object):

    def process_request(self, request, response):
        origin = request.get_header('Origin')
        if origin in ALLOWED_ORIGINS:
            response.set_header('Access-Control-Allow-Origin', origin)
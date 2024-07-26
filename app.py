import logging
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        logger.info(f"Request: {request.method} {request.path}")
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"Body: {request.get_data(as_text=True)}")
        logger.info('-' * 40)

        def custom_start_response(status, headers, exc_info=None):
            logger.info(f"Response status: {status}")
            logger.info(f"Response headers: {headers}")
            logger.info('-' * 40)
            logger.info('-' * 40)
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)

def application(environ, start_response):
    response = Response('Request Logged.', mimetype='text/plain')
    return response(environ, start_response)

app = LoggingMiddleware(application)

if __name__ == '__main__':
    run_simple('0.0.0.0', 4000, app)

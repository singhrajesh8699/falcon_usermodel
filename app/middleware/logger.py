import falcon
from app import log

LOG = log.get_logger()

class ResponseLogger(object):
    def process_response(self, req, resp, resource):
        LOG.info('{0} {1} {2}'.format(req.method, req.relative_uri, resp.status[:3]))

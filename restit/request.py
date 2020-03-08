class Request:
    def __init__(self, query_parameters: dict, wsgi_environment: dict = None):
        self.query_parameters = query_parameters
        self.wsgi_environment = wsgi_environment

# RestIt

[![Documentation Status](https://readthedocs.org/projects/restit/badge/?version=latest)](https://restit.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/Rollmops/restit/badge.svg?branch=master)](https://coveralls.io/github/Rollmops/restit?branch=master)
![Python package](https://github.com/Rollmops/restit/workflows/Python%20package/badge.svg)

Python HTTP REST library including OOP-readiness and Open-API generation

## Features

* [WSGI](#https://www.python.org/dev/peps/pep-3333/) conform
* Validation (using [marshmallow](#https://marshmallow.readthedocs.io/en/stable/)):
    * query parameter validation
    * path parameter validation
    * request body validation
    * response body validation
* [OpenApi](#https://swagger.io/docs/specification/about/) documentation generation
* *OOP* ready (no module-based global instances necessary)
* Easy to test
* very few dependencies

## Quick example

````python
from restit.request import Request
from restit.request_mapping import request_mapping
from restit.resource import Resource
from restit.response import Response
from restit.restit_app import RestitApp


@request_mapping("/")
class IndexResource(Resource):
    def get(self, request: Request) -> Response:
        return Response("Hello from index.")


app = RestitApp(resources=[IndexResource()])


if __name__ == "__main__":
    app.start_development_server()
````

You can also use a production-ready server like [Gunicorn](#https://gunicorn.org/) 
(given the name of the above module is *restit_app_test.py*):

````bash
gunicorn -w 4 restit_app_test:app
````



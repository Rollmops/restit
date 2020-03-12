import unittest

import requests

from restit import Resource, Response, Request, request_mapping, RestitApp
from restit.internal.open_api.open_api_spec import OpenApiSpec
from restit.internal.open_api_resource import OpenApiResource


@request_mapping("/path")
class FirstResource(Resource):
    def get(self, request: Request) -> Response:
        """This is a summary.

        And here we go with a description
        """
        return Response("Hallo")


@request_mapping("/path/:id<int>/wuff/:id2")
class SecondResource(Resource):
    def get(self, request: Request) -> Response:
        return Response("Hallo")


class OpenApiSpecTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.open_api_spec = OpenApiSpec(
            title="First OpenApi Test",
            description="Super description",
            version="1.2.3"
        )

        self.open_api_spec.register_resource(FirstResource())
        self.open_api_spec.register_resource(SecondResource())

    def test_something(self):
        open_api_dict = self.open_api_spec.generate()
        expected_open_api_dict = {
            'info': {
                'description': 'Super description',
                'title': 'First OpenApi Test',
                'version': '1.2.3'
            },
            'openapi': '3.0.0',
            'paths': {
                '/path': {
                    'options': {
                        'parameters': [],
                        'responses': {}
                    }
                },
                '/path/{id}/wuff/{id2}': {
                    'options': {
                        'parameters': [
                            {
                                'description': None,
                                'in': 'path',
                                'name': 'id',
                                'required': True,
                                'schema': {
                                    'format': None,
                                    'type': 'integer'
                                }
                            },
                            {
                                'description': None,
                                'in': 'path',
                                'name': 'id2',
                                'required': True,
                                'schema': {
                                    'format': None,
                                    'type': 'string'
                                }
                            }
                        ],
                        'responses': {}
                    }
                }
            }
        }
        self.assertEqual(expected_open_api_dict, open_api_dict)

    def test_serve_open_api(self):
        open_api_resource = OpenApiResource(self.open_api_spec)
        restit_app = RestitApp(resources=[open_api_resource], debug=True, raise_exceptions=True)

        with restit_app.start_development_server_in_context(port=0) as port:
            response = requests.get(f"http://127.0.0.1:{port}/api")
            self.assertEqual(200, response.status_code)
            self.assertIn("text/html", response.headers["Content-Type"])
            self.assertIn("<title>Swagger UI</title>", response.text)

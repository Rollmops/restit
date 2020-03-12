import unittest

import requests

from restit import Resource, Response, Request, request_mapping, RestitApp, OpenApiDocumentation


@request_mapping("/path")
class FirstResource(Resource):
    def get(self, request: Request, **path_params) -> Response:
        """This is a summary.

        And here we go with a description
        """
        return Response("Hallo")


@request_mapping("/path/:id<int>/wuff/:id2")
class SecondResource(Resource):
    def get(self, request: Request, **path_params) -> Response:
        return Response("Hallo")


class OpenApiSpecTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.open_api_documentation = OpenApiDocumentation(
            title="First OpenApi Test",
            description="Super description",
            version="1.2.3"
        )

        self.open_api_documentation.register_resource(FirstResource())
        self.open_api_documentation.register_resource(SecondResource())

    def test_something(self):
        open_api_dict = self.open_api_documentation.generate_spec()
        expected_open_api_dict = {
            'info': {
                'description': 'Super description',
                'title': 'First OpenApi Test',
                'version': '1.2.3'
            },
            'openapi': '3.0.0',
            'paths': {
                '/path': {
                    'get': {
                        'description': 'And here we go with a description',
                        'parameters': [],
                        'responses': {},
                        'summary': 'This is a summary.'
                    }
                },
                '/path/{id}/wuff/{id2}': {
                    'get': {
                        'description': None,
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
                        'responses': {},
                        'summary': None
                    }
                }
            }
        }
        self.assertEqual(expected_open_api_dict, open_api_dict)

    def test_serve_open_api(self):
        restit_app = RestitApp(
            resources=[
                FirstResource(),
                SecondResource()
            ], debug=True, raise_exceptions=True
        )

        restit_app.set_open_api_documentation(
            OpenApiDocumentation(title="First documentation", description="", version="1.2.3")
        )

        with restit_app.start_development_server_in_context(port=0) as port:
            response = requests.get(f"http://127.0.0.1:{port}/api")
            self.assertEqual(200, response.status_code)
            self.assertIn("text/html", response.headers["Content-Type"])
            self.assertIn("<title>Swagger UI</title>", response.text)

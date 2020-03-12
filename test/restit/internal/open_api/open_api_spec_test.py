import unittest

from restit import Resource, Response, Request, request_mapping
from restit.internal.open_api.open_api_spec import OpenApiSpec


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
    def test_something(self):
        open_api_spec = OpenApiSpec(
            title="First OpenApi Test",
            description="Super description",
            version="1.2.3"
        )

        open_api_spec.register_resource(FirstResource())
        open_api_spec.register_resource(SecondResource())

        open_api_dict = open_api_spec.generate()

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

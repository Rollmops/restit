import unittest

import requests
from marshmallow import Schema, fields

from restit import Resource, Response, Request, request_mapping, RestitApp, query_parameter, \
    request_body
from restit.open_api import OpenApiDocumentation
from restit.open_api.contact_object import ContactObject
from restit.open_api.info_object import InfoObject
from restit.open_api.license_object import LicenseObject
from restit.response_status_decorator import response_status

EXPECTED_OPEN_API_DICT = {
    'openapi': '3.0.0',
    'info': {
        'title': 'First OpenApi Test',
        'version': '1.2.3',
        'description': 'Super description',
        'termsOfService': 'http://example.com/terms/',
        'contact': {
            'name': 'API Support',
            'url': 'http://www.example.com/support',
            'email': 'support@example.com'
        },
        'license': {
            'name': 'Apache 2.0',
            'url': 'https://www.apache.org/licenses/LICENSE-2.0.html'
        }
    },
    'paths': {
        '/path': {
            'get': {
                'responses': {},
                'parameters': [{
                    'name': 'param1',
                    'in': 'query',
                    'description': 'A query parameter',
                    'required': False,
                    'schema': {
                        'type': 'integer',
                        'description': 'An integer field.',
                        'default': 10
                    }
                }],
                'summary': 'This is a summary.',
                'description': 'And here we go with a description'
            },
            'post': {
                'responses': {
                    'default': {
                        'description': 'Hmm...some default',
                        'content': {
                            'text/plain': {
                                'schema': {
                                    'type': 'integer',
                                    'description': 'An integer field.',
                                    'default': 10
                                }
                            }
                        }
                    },
                    200: {
                        'description': 'Everything worked fine',
                        'content': {
                            'text/plain': {
                                'schema': {
                                    'type': 'integer',
                                    'description': 'An integer field.',
                                    'default': 10
                                }
                            }
                        }
                    }
                },
                'parameters': [],
                'summary': None,
                'description': None,
                'requestBody': {
                    'description': 'A request body',
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {
                                'required': ['field1'],
                                'type': 'object',
                                'description': 'A bird with a flight speed exceeding that of an unladen swallow.\n    ',
                                'properties': {
                                    'field2': {
                                        'type': 'integer',
                                        'description': 'An integer field.',
                                        'default': 10
                                    },
                                    'field1': {
                                        'type': 'string',
                                        'description': 'A string field.'
                                    }
                                }
                            }
                        },
                        'image/png': {
                            'schema': {
                                'type': 'string',
                                'description': 'A string field.'
                            }
                        }
                    }
                }
            },
            'options': {
                'responses': {},
                'parameters': [],
                'summary': 'Identifying allowed request methods.',
                'description': 'The HTTP OPTIONS method is used to describe the communication options for the target resource.'
            }
        },
        '/path/{id}/wuff/{id2}': {
            'get': {
                'responses': {},
                'parameters': [{
                    'name': 'id',
                    'in': 'path',
                    'required': True,
                    'description': '',
                    'schema': {
                        'type': 'integer',
                        'description': 'An integer field.',
                        'default': 10
                    }
                }, {
                    'name': 'id2',
                    'in': 'path',
                    'required': True,
                    'description': '',
                    'schema': {
                        'type': 'string',
                        'description': 'A string field.'
                    }
                }],
                'summary': None,
                'description': None
            },
            'options': {
                'responses': {},
                'parameters': [{
                    'name': 'id',
                    'in': 'path',
                    'required': True,
                    'description': '',
                    'schema': {
                        'type': 'integer',
                        'description': 'An integer field.',
                        'default': 10
                    }
                }, {
                    'name': 'id2',
                    'in': 'path',
                    'required': True,
                    'description': '',
                    'schema': {
                        'type': 'string',
                        'description': 'A string field.'
                    }
                }],
                'summary': 'Identifying allowed request methods.',
                'description': 'The HTTP OPTIONS method is used to describe the communication options for the target resource.'
            }
        }
    },
    'components': {
        'schemas': {}
    }
}


class MyRequestBodySchema(Schema):
    """A bird with a flight speed exceeding that of an unladen swallow.
    """

    __reusable_open_api_component__ = True

    field1 = fields.String(required=True)
    field1.__doc__ = "Description for field1"
    field2 = fields.Integer()


@request_mapping("/path")
class FirstResource(Resource):
    @query_parameter("param1", description="A query parameter", field_type=fields.Integer(default=10))
    def get(self, request: Request, **path_params) -> Response:
        """This is a summary.

        And here we go with a description
        """
        return Response("Hallo")

    @request_body(
        {
            "application/json": MyRequestBodySchema(),
            "image/png": fields.String(required=True)
        }, description="A request body", required=True
    )
    @response_status(200, {"text/plain": fields.Integer()}, "Everything worked fine")
    @response_status(None, {"text/plain": fields.Integer()}, "Hmm...some default")
    def post(self, request: Request, **path_params) -> Response:
        return Response("123", 201)


@request_mapping("/path/:id<int>/wuff/:id2")
class SecondResource(Resource):
    def get(self, request: Request, **path_params) -> Response:
        return Response("Hallo")


class OpenApiSpecTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.open_api_documentation = OpenApiDocumentation(
            info=InfoObject(
                title="First OpenApi Test", description="Super description", version="1.2.3",
                contact=ContactObject("API Support", "http://www.example.com/support", "support@example.com"),
                license=LicenseObject("Apache 2.0", "https://www.apache.org/licenses/LICENSE-2.0.html"),
                terms_of_service="http://example.com/terms/"
            )
        )

        self.open_api_documentation.register_resource(FirstResource())
        self.open_api_documentation.register_resource(SecondResource())

    def test_generate_spec(self):
        self.maxDiff = None
        open_api_dict = self.open_api_documentation.generate_spec()

        self.assertEqual(EXPECTED_OPEN_API_DICT, open_api_dict)

    def test_serve_open_api(self):
        restit_app = RestitApp(
            resources=[
                FirstResource(),
                SecondResource()
            ], debug=True, raise_exceptions=True
        )

        restit_app.set_open_api_documentation(self.open_api_documentation)

        # restit_app.start_development_server()

        with restit_app.start_development_server_in_context(port=0) as port:
            response = requests.get(f"http://127.0.0.1:{port}/api/")
            self.assertEqual(200, response.status_code)
            self.assertIn("text/html", response.headers["Content-Type"])
            self.assertIn("<title>Swagger UI</title>", response.text)

            response = requests.get(f"http://127.0.0.1:{port}/api/swagger.json")
            self.assertEqual(200, response.status_code)

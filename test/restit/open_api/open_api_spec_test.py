import unittest

import requests
from marshmallow import Schema, fields
from marshmallow.validate import Regexp, Range

from restit import Resource, Response, Request, RestItApp
from restit.decorator import path, query_parameter, request_body, response
from restit.open_api import OpenApiDocumentation, reusable_schema
from restit.open_api.contact_object import ContactObject
from restit.open_api.info_object import InfoObject
from restit.open_api.license_object import LicenseObject


@reusable_schema
class MyRequestBodySchema(Schema):
    """A bird with a flight speed exceeding that of an unladen swallow.
    """
    field1 = fields.String(required=True, validate=[Regexp(r"\w+")])
    field1.__doc__ = "Description for field1"
    field2 = fields.Integer(validate=[Range(min=1, max=100)])


@path("/path")
class FirstResource(Resource):
    """First resource summary

    Super description.
    """

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
    @response(200, {"text/plain": fields.Integer()}, "Everything worked fine")
    @response(None, {"text/plain": fields.Integer()}, "Hmm...some default")
    def post(self, request: Request, **path_params) -> Response:
        return Response("123", 201)


@path("/path/:id<int>/wuff/:id2")
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

        self.assertEqual({
            'schemas': {
                'MyRequestBodySchema': {
                    'required': ['field1'],
                    'type': 'object',
                    'description': 'A bird with a flight speed exceeding that of an unladen swallow.\n    ',
                    'properties': {
                        'field2': {
                            'type': 'integer',
                            'description': 'An integer field.',
                            'minimum': 1,
                            'maximum': 100,
                            'exclusiveMinimum': False,
                            'exclusiveMaximum': False
                        },
                        'field1': {
                            'description': 'Description '
                                           'for '
                                           'field1',
                            'pattern': '\\w+',
                            'type': 'string'
                        }
                    }
                }
            }
        }, open_api_dict["components"])

        self.assertEqual({
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
        }, open_api_dict["info"])
        self.assertEqual("3.0.0", open_api_dict["openapi"])

        paths_path = open_api_dict["paths"]["/path"]
        self.assertEqual("First resource summary", paths_path["summary"])
        self.assertEqual("Super description.", paths_path["description"])

        self.assertEqual({
            'responses': {},
            'parameters': [{
                'name': 'param1',
                'in': 'query',
                'description': 'A query parameter',
                'required': False,
                'schema': {
                    'default': 10,
                    'type': 'integer',
                    'description': 'An integer field.',
                }
            }],
            'summary': 'This is a summary.',
            'description': 'And here we go with a description'
        }, paths_path["get"])

        self.assertEqual({
            'responses': {
                'default': {
                    'description': 'Hmm...some default',
                    'content': {
                        'text/plain': {
                            'schema': {
                                'type': 'integer',
                                'description': 'An integer field.'
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
                                'description': 'An integer field.'
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
                            '$ref': '#/components/schemas/MyRequestBodySchema'
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
        }, paths_path["post"])

        path_with_params = open_api_dict["paths"]["/path/{id}/wuff/{id2}"]

        self.assertIn({
            'name': 'id',
            'in': 'path',
            'required': True,
            'description': '',
            'schema': {
                'type': 'integer',
                'description': 'An integer field.'
            }
        }, path_with_params["get"]["parameters"])

        self.assertIn({
            'name': 'id2',
            'in': 'path',
            'required': True,
            'description': '',
            'schema': {
                'type': 'string',
                'description': 'A string field.'
            }
        }, path_with_params["get"]["parameters"])

    def test_serve_open_api(self):
        restit_app = RestItApp(
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

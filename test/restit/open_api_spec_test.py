import unittest

import requests
from marshmallow import Schema, fields

from restit import Resource, Response, Request, request_mapping, RestitApp, OpenApiDocumentation, query_parameter, \
    request_body


class MyRequestBodySchema(Schema):
    """Schema title"""
    field1 = fields.String()
    field2 = fields.Integer()


@request_mapping("/path")
class FirstResource(Resource):
    @query_parameter("param1", description="A query parameter", type=int, required=False, default=10)
    def get(self, request: Request, **path_params) -> Response:
        """This is a summary.

        And here we go with a description
        """
        return Response("Hallo")

    @request_body(
        {
            "application/json": MyRequestBodySchema(),
            "image/png": bytes
        }, description="A request body"
    )
    def post(self, request: Request, **path_params) -> Response:
        return Response("123", 201)


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

    def test_generate_spec(self):
        self.maxDiff = None
        open_api_dict = self.open_api_documentation.generate_spec()
        expected_open_api_dict = {'openapi': '3.0.0',
                                  'info': {'title': 'First OpenApi Test', 'description': 'Super description',
                                           'version': '1.2.3'}, 'paths': {'/path': {'get': {'responses': {},
                                                                                            'parameters': [
                                                                                                {'name': 'param1',
                                                                                                 'in': 'query',
                                                                                                 'description': 'A query parameter',
                                                                                                 'required': False,
                                                                                                 'schema': {
                                                                                                     'type': 'integer',
                                                                                                     'default': 10}}],
                                                                                            'summary': 'This is a summary.',
                                                                                            'description': 'And here we go with a description'},
                                                                                    'post': {'responses': {},
                                                                                             'parameters': [],
                                                                                             'summary': None,
                                                                                             'description': None},
                                                                                    'options': {'responses': {},
                                                                                                'parameters': [],
                                                                                                'summary': 'Identifying allowed request methods.',
                                                                                                'description': 'The HTTP OPTIONS method is used to describe the communication options for the target resource.'}},
                                                                          '/path/{id}/wuff/{id2}': {
                                                                              'get': {'responses': {}, 'parameters': [
                                                                                  {'name': 'id', 'in': 'path',
                                                                                   'required': True,
                                                                                   'description': None,
                                                                                   'schema': {'type': 'integer',
                                                                                              'default': 10}},
                                                                                  {'name': 'id2', 'in': 'path',
                                                                                   'required': True,
                                                                                   'description': None,
                                                                                   'schema': {'type': 'string'}}],
                                                                                      'summary': None,
                                                                                      'description': None},
                                                                              'options': {'responses': {},
                                                                                          'parameters': [{'name': 'id',
                                                                                                          'in': 'path',
                                                                                                          'required': True,
                                                                                                          'description': None,
                                                                                                          'schema': {
                                                                                                              'type': 'integer',
                                                                                                              'default': 10}},
                                                                                                         {'name': 'id2',
                                                                                                          'in': 'path',
                                                                                                          'required': True,
                                                                                                          'description': None,
                                                                                                          'schema': {
                                                                                                              'type': 'string'}}],
                                                                                          'summary': 'Identifying allowed request methods.',
                                                                                          'description': 'The HTTP OPTIONS method is used to describe the communication options for the target resource.'}}},
                                  'components': {'schemas': {}}}
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

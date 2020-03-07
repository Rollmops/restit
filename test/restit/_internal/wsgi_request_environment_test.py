import unittest

# noinspection PyProtectedMember
from restit._internal.wsgi_request_environment import RequestType, WsgiRequestEnvironment


class WsgiEnvironmentTestCase(unittest.TestCase):
    def test_create_from_wsgi_environment_dict(self):
        wsgi_request_enviroment = WsgiRequestEnvironment.create_from_wsgi_environment_dict(
            {
                "REQUEST_METHOD": "GET",
                "PATH_INFO": "/"
            }
        )

        self.assertEqual(RequestType.GET, wsgi_request_enviroment.request_method)
        self.assertEqual("/", wsgi_request_enviroment.path)

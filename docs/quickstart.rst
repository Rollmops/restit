Quickstart
==========

A Minimal Application
---------------------

To get started with RestIt we can use the following code snippet:

.. code-block:: python

    from restit import Request, Resource, Response, RestItApp
    from restit.decorator import path


    @path("/")
    class IndexResource(Resource):
        def get(self, request: Request) -> Response:
            return Response("Hello from index.")


    app = RestItApp(resources=[IndexResource()])


    if __name__ == "__main__":
        # start a development server on http://127.0.0.1:5000
        app.start_development_server()

One of the key aspects of *REST* and the *RestIt* library are *Resources*. Since a resource is identified with an
*URI*, in our Python code we assign it using the :func:`~restit.request_mapping_decorator.request_mapping` decorator.



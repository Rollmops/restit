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
*URI*, in our Python code we assign it using the :func:`~restit.decorator.path` decorator.


Adding a Swagger/OpenApi Documentation
--------------------------------------

To get your HTTP app serving a *OpenApi* documentation you have to create an instance of
:class:`~restit.open_api.OpenApiDocumentation` and pass it to your :class:`~restit.RestItApp` constructor.

.. code-block:: python

    open_api_documentation = OpenApiDocumentation(
        info=InfoObject(title="My HTTP API", version="1.0.0"), path="/api"
    )

    app = RestItApp(
        resources=[IndexResource()], open_api_documentation=open_api_documentation
    )

Once you start your development server and navigate to ``http://127.0.0.1:5000/api/`` you will see a minimal *OpenApi*
documentation.

.. note::

    Since we did not yet provide any information about our API we do not see too much in the *OpenApi* documentation yet.



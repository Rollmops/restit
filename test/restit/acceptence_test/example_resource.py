from marshmallow import Schema, fields
from marshmallow.fields import Boolean

from restit import Resource, Response, Request
from restit.decorator import path, response, query_parameter
from restit.exception import BadRequest
from test.restit.acceptence_test.todo_repo import TodoRepo


class TodosSchema(Schema):
    """A collection of todo names"""

    collection = fields.List(fields.String())
    sort = fields.Boolean()


@path("/")
class TodosResource(Resource):
    def __init__(self, repo: TodoRepo):
        super().__init__()
        self.repo = repo

    @response(
        200, description="Get a list of all todo ids",
        content_types={"application/json": TodosSchema()}
    )
    @query_parameter(
        "sort", description="Flag if the todo list should be sorted", field_type=Boolean(default=True)
    )
    def get(self, request: Request) -> Response:
        """Get a list of all todo ids"""

        raise BadRequest("Huhu")
        todo_ids = self.repo.get_todo_ids()

        return Response({"collection": todo_ids, "sort": request.query_parameters["sort"]})

from marshmallow import Schema, fields

from restit import Resource, request_mapping, Response, Request, query_parameter
from restit.response_status_decorator import response_status
from test.restit.acceptence_test.todo_repo import TodoRepo


class TodosSchema(Schema):
    """A collection of todo names"""

    collection = fields.List(fields.String())


@request_mapping("/")
class TodosResource(Resource):
    def __init__(self, repo: TodoRepo):
        super().__init__()
        self.repo = repo

    @response_status(
        200, description="Get a list of all todo ids",
        content_types={"application/json": TodosSchema()}
    )
    @query_parameter(
        "sort", description="Flag if the todo list should be sorted", field_type=bool, default=False, required=False
    )
    def get(self, request: Request, **path_params) -> Response:
        """Get a list of all todo ids"""

        todo_ids = self.repo.get_todo_ids()

        return Response({"collection": todo_ids})
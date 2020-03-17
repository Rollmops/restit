from datetime import datetime

_TODOS = {
    1: ("Get beer", datetime(2020, 4, 1, 20, 0), "At least 10 boxes"),
    2: ("Get wine", datetime(2020, 4, 2, 20, 0), "At least 100 bottles"),
}


class TodoRepo:
    @staticmethod
    def get_todo_ids():
        return list(_TODOS.keys())

    @staticmethod
    def find_by_id(_id: str):
        return _TODOS[_id]

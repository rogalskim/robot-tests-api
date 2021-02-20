class Endpoints:
    info = "info"
    tasks = "tasks"
    robots = "robots"


class Query:
    def __init__(self, key: str, value: str = None) -> None:
        self._key = key
        self._value = value
        self._text = f"{key}={value}"

    def __repr__(self) -> str:
        return self.text()

    def key(self) -> str:
        return self._key

    def value(self) -> str:
        return self._value

    def text(self) -> str:
        return self._text


class Queries:
    @staticmethod
    def modification_time() -> Query:
        return Query("q", "mod_time")

    @staticmethod
    def single_task(task_id: str) -> Query:
        return Query("id", task_id)

    @staticmethod
    def all_tasks() -> Query:
        return Query("q", "all")

    @staticmethod
    def recent_tasks() -> Query:
        return Query("q", "recent")


class RequestUrl:
    def __init__(self, root: str, endpoint: str, query: Query = None):
        self._root = root
        self._endpoint = endpoint
        self._query = query
        self._text = f"{root}/{endpoint}" if query is None else f"{root}/{endpoint}?{query}"

    def __repr__(self) -> str:
        return self.text()

    def root(self) -> str:
        return self._root

    def endpoint(self) -> str:
        return self._endpoint

    def query(self) -> Query:
        return self._query

    def text(self) -> str:
        return self._text


class RequestUrls:
    @staticmethod
    def get_modification_time(server_address: str) -> RequestUrl:
        return RequestUrl(server_address, Endpoints.info, Queries.modification_time())

    @staticmethod
    def get_robots(server_address: str) -> RequestUrl:
        return RequestUrl(server_address, Endpoints.robots, None)

    @staticmethod
    def get_single_task(server_address: str, task_id: int) -> RequestUrl:
        return RequestUrl(server_address, Endpoints.tasks, Queries.single_task(str(task_id)))

    @staticmethod
    def get_all_tasks(server_address: str) -> RequestUrl:
        return RequestUrl(server_address, Endpoints.tasks, Queries.all_tasks())

    @staticmethod
    def create_task(server_address: str) -> RequestUrl:
        return RequestUrl(server_address, Endpoints.tasks, None)

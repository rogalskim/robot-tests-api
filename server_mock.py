import time
from typing import Any

import requests
import requests_mock

from task import Task


class MockConstants:
    fail_key = "mock_fail"
    true = "True"
    false = "False"


class ServerMock:
    def __init__(self, server_address: str) -> None:
        self._adapter = requests_mock.Adapter()
        self._next_task_id = 1701
        self._tasks = {}
        self._robots = ["Molly", "Bosco", "Doretta", "Karl"]

        self._adapter.register_uri(method="GET",
                                   url=f"{server_address}/info",
                                   text=self._get_modification_timestamp)

        self._adapter.register_uri(method="POST",
                                   url=f"{server_address}/tasks",
                                   text=self._create_task)

    @staticmethod
    def _should_response_fail(request: requests.Request) -> bool:
        if MockConstants.fail_key not in request.headers.keys():
            return False
        return request.headers[MockConstants.fail_key] == MockConstants.true

    def _get_modification_timestamp(self, request: requests.Request, context: Any) -> str:
        """
        Mock callback for Server modification time requests.

        :returns: modification timestamp as str
        """
        if self._should_response_fail(request):
            context.status_code = requests.codes.server_error
            context.reason = "Internal server error."
        else:
            context.status_code = requests.codes.ok

        current_time = str(int(time.time()))
        return current_time

    def _create_task(self, request: requests.Request, context: Any) -> str:
        """
        Mock callback for Task creation requests.

        :returns: Task id as string
        """
        requested_task_details = request.json()

        if self._should_response_fail(request):
            context.status_code = requests.codes.server_error
            context.reason = "Internal server error."
            return context.reason
        elif requested_task_details["robot_name"] not in self._robots:
            context.status_code = requests.codes.bad_request
            context.reason = "Invalid robot name requested."
            return context.reason
        else:
            context.status_code = requests.codes.ok

        new_task = Task(task_id=self._next_task_id,
                        creation_time=int(time.time()),
                        robot_id=self._robots.index(requested_task_details["robot_name"]),
                        branch=requested_task_details["branch"],
                        runs=requested_task_details["runs"])
        self._tasks[self._next_task_id] = new_task
        self._next_task_id += 1

        return str(new_task.task_id)

    def get_mock_adapter(self) -> requests_mock.Adapter:
        return self._adapter
